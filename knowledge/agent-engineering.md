---
title: AI Agent Engineering 통합 지식베이스
source: Google Drive / KDT AI HUMAN 강의·실습 자료
source_root: https://drive.google.com/drive/folders/1dgs2PekmLTTZVVEzawHbetbiXHLvFJ9n
generated: 2026-09-11
language: ko
scope: LLM 제어·출력계약, Agent 런타임, Tool 설계, MCP, n8n, FastAPI, SQLite, Observability, Docker, GCP, RAG 실습 자료
---

# AI Agent Engineering 통합 지식베이스

이 문서는 Google Drive 폴더에 있는 강의 PDF, Jupyter Notebook, README, 실습 워크플로를 하나의 지식 문서로 재구성한 것이다. 강의 순서를 그대로 옮기기보다 서로 반복되는 개념을 합쳐 **설계 → 실행 → 검증 → 복구 → 관측 → 배포**의 흐름으로 정리했다.

> [!NOTE]
> 이 문서는 폴더 내부 자료를 기준으로 만든 학습용 지식베이스다. 클라우드 요금, 특정 서비스 UI, 모델 이름·성능, 제품 정책처럼 시간이 지나며 바뀔 수 있는 정보는 실제 사용 시 최신 공식 문서를 다시 확인하는 것이 좋다.

---

## 0. 전체 그림: AI Agent를 무엇으로 봐야 하는가

가장 압축된 관점은 다음과 같다.

```text
LLM
  + Instructions
  + Context / Memory
  + Tools
  + Output Contract
  + Validation
  + Runtime / Harness
  + Loop
  + Observability
  = 운영 가능한 Agent
```

단순 LLM 호출과 운영 가능한 Agent의 차이는 **모델 자체보다 모델 주변의 실행 계약과 제어 구조**에서 생긴다.

LLM은 본질적으로 다음 세 가지 한계를 가진다.

1. **Frozen Knowledge**: 학습 이후의 최신 사실을 스스로 알 수 없다. → Search, RAG, Tool이 필요하다.
2. **Finite Context Window**: 한 번에 볼 수 있는 정보와 대화 기억에는 한계가 있다. → Memory와 Context Engineering이 필요하다.
3. **No Side Effect**: 텍스트만 생성해서는 파일 저장, API 호출, DB 갱신 같은 실제 행동을 할 수 없다. → Tool, MCP, Computer Use 같은 실행 계층이 필요하다.

Agent를 구성하는 최소 요소는 다음 네 가지로 볼 수 있다.

```text
Agent = Model + Instructions + Tools + Context
```

하지만 프로덕션에서는 이것만으로 부족하다. 출력이 틀릴 수 있고, 도구가 실패할 수 있고, 잘못된 행동이 실제 부작용을 만들 수 있기 때문이다. 그래서 자료 전체에서 반복되는 핵심 흐름은 다음과 같다.

```text
Contract
  ↓
Generate / Decide
  ↓
Validate
  ↓
Execute
  ↓
Observe
  ↓
Repair / Retry / Escalate
  ↓
Persist & Monitor
```

### Agentic Engineering의 확장 단계

자료의 Agentic Engineering 강의는 발전 단계를 다음처럼 설명한다.

```text
Prompt Engineering
    ↓
Context Engineering
    ↓
Harness Engineering
    ↓
Loop Engineering
    ↓
Graph Engineering
```

- **Prompt Engineering**: 한 번의 호출을 어떻게 잘 만들 것인가.
- **Context Engineering**: 어떤 정보와 도구를 모델에게 보여줄 것인가.
- **Harness Engineering**: 모델이 안전하게 일할 실행 환경을 어떻게 제공할 것인가.
- **Loop Engineering**: 목표가 달성될 때까지 어떻게 반복·검증·복구할 것인가.
- **Graph Engineering**: 여러 Agent/Loop와 사람을 어떤 구조로 연결할 것인가.

중요한 점은 뒤 단계가 앞 단계를 없애는 것이 아니라 **포함하면서 확장한다**는 것이다.

---

# 1. Workflow와 Agent

## 1.1 핵심 판단 기준

Workflow와 Agent를 가르는 가장 유용한 질문은 이것이다.

> **다음 행동이 입력을 보기 전에 이미 정해져 있는가?**

정해져 있다면 Workflow에 가깝고, 입력·중간 결과에 따라 모델이 다음 행동을 고르게 해야 한다면 Agent가 필요하다.

```text
Workflow
A → B → C → D
순서와 분기가 설계 시점에 대부분 고정

Agent
Goal
 ↓
Observe → Decide → Tool → Observe → Decide ...
런타임에 다음 행동을 선택
```

### Workflow가 적합한 경우

- 단계가 안정적으로 고정되어 있다.
- 규칙 기반 분기가 충분하다.
- 결과 재현성이 중요하다.
- 잘못된 자유도가 오히려 위험하다.
- 비용과 지연을 예측 가능하게 유지해야 한다.

### Agent가 적합한 경우

- 사용자의 요구가 다양해서 필요한 도구가 매번 달라진다.
- 중간 결과를 보고 다음 행동을 결정해야 한다.
- 미리 모든 분기를 하드코딩하기 어렵다.
- 탐색, 계획, 조사처럼 열린 문제를 다룬다.

**자율성은 기능이 아니라 비용과 위험을 동반하는 설계 선택**이다. Agent를 만들 수 있다고 해서 모든 과정을 Agent로 만드는 것은 좋은 설계가 아니다.

---

## 1.2 네 가지 실행 패턴

자료에서는 실행 구조를 크게 네 패턴으로 정리한다.

### Sequential

```text
Input → Step A → Step B → Step C → Output
```

앞 단계의 결과가 다음 단계의 입력이 되는 조립라인이다.

적합한 예:

- 문서 읽기 → 요약 → 분류 → 저장
- STT → 정제 → LLM → TTS
- 수집 → 변환 → DB 적재

### Parallel

```text
             ┌→ Task A ─┐
Input ───────┼→ Task B ─┼→ Merge
             └→ Task C ─┘
```

서로 독립적인 작업을 동시에 처리한다. 병렬화 가능한 작업은 latency를 줄일 수 있지만, 합치는 단계의 계약이 필요하다.

### Loop

```text
Draft → Review → Pass?
          ↑       │
          └─ Fix ─┘
```

기준을 만족할 때까지 수정·검증을 반복한다. 무한 반복을 막기 위해 **종료 조건과 최대 시도 횟수**가 반드시 있어야 한다.

### LLM-based / Agentic

모델이 입력과 상황을 보고 다음 행동 또는 도구를 고른다.

```text
Observe → Reason → Act → Observe ...
```

패턴 선택과 안전성은 별개의 축이다. Sequential이라고 안전한 것도 아니고, Agent라고 반드시 위험한 것도 아니다. **부작용의 크기, 가역성, 권한**을 따로 설계해야 한다.

---

# 2. Agent Loop: Think / Act / Observe / Verify

운영 가능한 Agent는 단발성 프롬프트보다 피드백 루프에 가깝다.

```text
Goal
 ↓
Observe
 ↓
Reason / Think
 ↓
Act
 ↓
Verify
 ↓
Goal reached? ── No ──→ Observe
       │
      Yes
       ↓
   Terminate
```

핵심은 **행동 자체가 아니라 행동의 결과를 다시 관찰한다는 것**이다.

좋은 Loop에는 다음이 필요하다.

- 명확한 목표 상태
- 관찰 가능한 중간 상태
- 실행 가능한 Action
- 성공/실패를 판정하는 Verify 단계
- 실패 시 수정 전략
- 최대 반복 횟수
- 사람에게 넘길 Escalation 조건
- 종료 조건

### Reflexion의 위치

모델에게 실패를 설명하고 자기수정을 유도하는 Reflexion은 유용할 수 있지만, 자료 전체의 설계 철학은 **사후 반성보다 사전 계약을 우선**한다.

```text
나쁜 구조
모호한 Tool / Output
→ 실패
→ 모델에게 다시 생각하라고 함
→ 또 실패 가능

좋은 구조
명확한 Tool Contract
+ Output Contract
+ Validation
→ 실패 공간 자체를 축소
→ 필요한 경우에만 Repair
```

---

# 3. 출력 계약(Output Contract)

## 3.1 왜 계약이 필요한가

LLM이 생성한 텍스트를 사람이 읽는 데에는 유연성이 장점이지만, 프로그램이 처리할 때에는 같은 유연성이 장애물이 된다.

예를 들어 감정 필드 하나가 다음처럼 흔들릴 수 있다.

```text
positive
긍정
긍정적
매우 긍정적
POSITIVE
좋음
```

후처리 코드가 이를 모두 수용하기 시작하면 매핑과 정규식이 계속 늘어난다. 따라서 **출력 다양성을 후처리에서 고치는 대신 생성 시점에 계약으로 줄이는 것**이 핵심이다.

## 3.2 출력 계약의 6원칙

강의에서 정리한 여섯 원칙은 다음과 같다.

1. **고정 키**: 필드 이름을 정확히 고정한다.
2. **타입 명시**: string, integer, boolean, array 등을 명확히 한다.
3. **범위/허용값 제약**: enum이나 최소·최대 범위를 둔다.
4. **기본값 정의**: 알 수 없거나 해당하지 않을 때의 값을 정한다.
5. **예시 포함**: 정상 출력 한두 개로 해석 공간을 줄인다.
6. **순수 JSON 강제**: 설명문·Markdown fence 없이 데이터만 반환하게 한다.

예시:

```json
{
  "schema_version": "1.0",
  "sentiment": "positive | neutral | negative",
  "sentiment_score": 0.0,
  "issue": "none | delivery_delay | product_defect | other",
  "delay_days": 0
}
```

이 자료의 실습에서는 느슨한 계약과 6원칙 계약을 같은 조건에서 비교했을 때, 필드 위반이 크게 감소했다. 중요한 교훈은 특정 숫자 자체보다 다음 문장이다.

> **프롬프트에서 계약을 명시하는 비용이 후처리 예외를 끝없이 유지하는 비용보다 싸다.**

## 3.3 계약이 해결하지 못하는 것

스키마가 맞는다고 의미까지 맞는 것은 아니다.

```json
{
  "issue": "delivery_delay",
  "delay_days": 0
}
```

타입과 enum은 모두 맞지만 논리적으로 모순일 수 있다.

따라서 검증은 최소 두 층으로 생각한다.

```text
1. Structural Validation
   JSON인가?
   필수 필드가 있는가?
   타입/enum/range가 맞는가?

2. Semantic / Business Validation
   필드끼리 논리적으로 일치하는가?
   실제 업무 규칙을 만족하는가?
```

---

# 4. Validation Pipeline: 실패를 전제로 설계하기

## 4.1 검증기는 모델보다 먼저 검증한다

모델 출력을 검증하기 전에 **검증 함수 자체를 유닛 테스트**해야 한다.

권장 순서:

```text
Known Good Fixture
Known NO_JSON Fixture
Known JSON_DECODE Fixture
Known SCHEMA_VIOLATION Fixture
          ↓
Validator Unit Test
          ↓
Real Model Output
```

검증기가 틀리면 모델 성능 평가도 틀린다.

## 4.2 실패 유형을 분류하라

자료에서는 최소 다음 세 범주를 사용한다.

```text
NO_JSON
JSON_DECODE
SCHEMA_VIOLATION
```

조금 더 큰 단계로 묶으면:

```text
Parsing Failure
  ├─ NO_JSON
  └─ JSON_DECODE

Validation Failure
  └─ SCHEMA_VIOLATION
```

중요한 이유는 **실패 종류가 다음 행동을 결정하기 때문**이다.

좋은 반환 형식 예:

```json
{
  "success": false,
  "stage": "validation",
  "error_type": "SCHEMA_VIOLATION",
  "error_message": "sentiment_score must be between -1 and 1",
  "retryable": true,
  "data": null
}
```

사용자에게는 내부 구현 세부를 그대로 노출하지 않고, 내부 trace에는 상세 `error_type`을 남기는 식으로 분리할 수 있다.

---

# 5. Retry와 Repair

## 5.1 무조건 재호출하지 않는다

재시도 정책의 핵심은 다음이다.

```text
STRICT → REPAIR → FAIL
```

### Stage 1: STRICT

처음부터 명확한 계약으로 생성한다.

### Stage 2: REPAIR

단순히 똑같은 요청을 다시 보내는 것이 아니다. 다음 증거를 제공한다.

- 원래 입력
- 직전의 잘못된 출력
- 검증기가 판정한 오류 종류
- 위반한 규칙

그리고 모델의 역할을 **생성기(generator)**에서 **수정기(repairer)**로 바꾼다.

```text
원본 입력 + 실패 출력 + 에러 근거
                    ↓
                 REPAIR
```

### Stage 3: FAIL

예산을 소진한 뒤에는 명시적으로 종료한다.

```json
{
  "success": false,
  "next_action": "human_review",
  "attempts": [ ... ]
}
```

FAIL은 사고가 아니라 **정상적인 종료 상태**다.

## 5.2 오류마다 처방이 다르다

대표적인 정책:

| 오류 | 일반적인 처리 |
|---|---|
| 형식/스키마 오류 | 근거를 포함한 REPAIR |
| 429 | backoff + jitter 후 제한적 재시도 |
| 일시적 5xx | backoff 후 제한적 재시도 |
| timeout | 재시도 가능 여부를 코드 정책으로 판정 |
| 401/403 | 재시도보다 인증/권한 문제 해결 |
| 사실성 불확실 | 검색·근거 확인 또는 사람 검토 |
| 고위험 쓰기 작업 | 자동 재시도보다 승인/중단 |

재시도 여부를 모델에게 다시 묻기보다, 가능한 한 **상태값과 결정적 코드 규칙**으로 처리한다.

## 5.3 Retry Budget

재시도는 공짜가 아니다.

```text
Retry Benefit
= rescued failures

Retry Cost
= extra tokens
+ extra latency
+ extra API calls
+ duplicate side-effect risk
```

따라서 성공률 하나만 보면 안 된다. 최소 다음 지표를 같이 본다.

- first-try success rate
- final success rate
- rescue rate
- average attempts
- p95 latency
- cost per successful task
- human-review rate
- duplicate side-effect risk

---

# 6. SLA와 Release Gate

프로토타입에서는 “잘 되더라”가 기준이 될 수 있지만, 서비스 출시 여부는 **명시적 게이트**로 바꾸는 것이 좋다.

예시:

```text
ReleaseGate
  ├─ final_success_rate >= target
  ├─ p95_latency <= budget
  ├─ cost_per_task <= budget
  ├─ first_try_rate >= guardrail
  └─ required_evidence_present == true
```

## 6.1 한 번에 하나만 바꾸기

개선 실험은 `ExperimentCard`처럼 조건을 고정한다.

```yaml
change: retry_policy_v2
quality_metric: final_success_rate
guardrail: p95_latency
baseline_model: same
input_dataset: same
output_contract: same
```

여러 조건을 동시에 바꾸면 개선 원인을 특정할 수 없다.

## 6.2 수식은 계획, Trace가 정본

독립 실패를 가정한 이론 계산은 계획용으로 쓸 수 있지만 실제 실패는 같은 입력, 같은 프롬프트 구조, 같은 외부 시스템 때문에 상관되어 있을 수 있다.

따라서:

```text
수학 모델 → 예상
실제 trace → 확정
차이 → 원인 분석 대상
```

## 6.3 SLA는 서비스 맥락에 따라 다르다

같은 지연시간도 배치 시스템에서는 충분히 빠르고, 실시간 대화에서는 느릴 수 있다. 따라서 `GO`는 항상 다음처럼 읽어야 한다.

> **어느 서비스 요구조건에 대한 GO인가?**

---

# 7. Tool 설계

Agent가 도구를 잘못 고르는 문제는 종종 모델 성능보다 **도구 계약의 품질** 문제다.

## 7.1 도구 설계 4원칙

1. **단일 책임(Single Responsibility)**
2. **명시적 인자(Explicit Arguments)**
3. **구조화된 반환(Structured Return)**
4. **설명적 Docstring(Descriptive Docstring)**

좋은 도구는 모델이 추측해야 할 빈칸을 줄인다.

### 나쁜 예

```python
def check_policy(topic):
    """정책을 확인한다."""
    return "가능"
```

문제:

- 어떤 `topic`이 허용되는가?
- 언제 써야 하는가?
- 언제 쓰면 안 되는가?
- 실패는 어떻게 표현되는가?
- 반환 문자열을 프로그램이 어떻게 분기하는가?

### 더 나은 예

```python
def check_refund_policy(reason: str) -> dict:
    """
    환불 가능 여부를 조회한다.

    Use when:
      - 사용자가 환불 정책 또는 특정 환불 사유의 적용 여부를 묻는 경우

    Do NOT use when:
      - 실제 환불을 실행해야 하는 경우

    Allowed reason:
      - change_of_mind
      - product_defect

    Returns:
      {
        "status": "covered | not_covered | error",
        "reason": str,
        "needs_approval": bool,
        "error_message": str | None
      }
    """
```

---

## 7.2 Tool Description의 5요소

도구 설명에는 다음 다섯 요소가 있으면 좋다.

```text
What        무엇을 하는가
When        언제 쓰는가 / 언제 쓰지 않는가
How         어떤 인자를 어떻게 넣는가
Output      무엇을 반환하는가
Constraints 제약, 부작용, 승인 조건은 무엇인가
```

특히 `DO NOT use when ...`은 중요하다. Agent에게 가능한 행동뿐 아니라 **금지 경계**도 알려준다.

하지만 설명은 어디까지나 가이드다.

```text
Description = 모델에게 알려주는 규칙
Gate / Permission = 실제로 강제하는 규칙
```

“승인 후 실행하라”고 프롬프트에 쓰는 것만으로는 충분하지 않다.

```python
if result["needs_approval"]:
    return {"status": "waiting_for_approval"}
```

처럼 **상태와 코드 경로**가 실제 동작을 막아야 한다.

---

## 7.3 오류 반환도 Tool Contract다

문자열 오류보다 구조화된 오류가 좋다.

```json
{
  "status": "timeout",
  "error_message": "upstream did not respond in 3s",
  "retryable": true,
  "data": null
}
```

왜냐하면 호출자가 다음 행동을 결정할 수 있기 때문이다.

```python
if result["retryable"]:
    retry()
else:
    stop_or_escalate()
```

“모른다”, “범위 밖이다”, “일시적 실패다”를 표현할 상태가 없으면 모델은 가장 가까운 값을 억지로 끼워 맞출 수 있다.

---

# 8. 부작용과 가역성: 도구를 만들어도 되는가

도구 설계에서 가장 먼저 물어야 할 질문은 다음이다.

> **이 도구가 잘못 호출되면 되돌릴 수 있는가?**

자료의 개념을 실무형으로 정리하면:

| 위험 수준 | 예 | 기본 전략 |
|---|---|---|
| 낮음 | read/search/list | 자동 실행 가능 |
| 중간 | 비용 드는 검색, 대량 조회 | limit, timeout, budget |
| 중간~높음 | 문서/메일 초안 생성 | draft 후 사람 확인 |
| 높음 | 실제 발송, 삭제, 결제, 권한 변경 | 명시적 승인·강한 gate |
| 매우 높음 | 임의 코드/명령 실행 | sandbox + 최소권한 + 제한 또는 금지 |

### Draft-first 패턴

되돌리기 어려운 행동은 가능한 한 두 단계로 나눈다.

```text
Generate Draft
   ↓
Human Review / Policy Gate
   ↓
Commit / Send / Delete / Pay
```

이는 n8n 영업 예제에서도 “메일 발송”이 아니라 **Gmail Draft 생성**으로 설계한 이유와 연결된다.

### 멱등성만으로 충분하지 않은 이유

`request_id` 기반 멱등성을 넣어도 Agent가 재시도할 때 매번 다른 ID를 만들면 중복 실행이 생길 수 있다. 따라서 부작용 제어는 멱등성 하나가 아니라 다음의 조합이 좋다.

```text
Idempotency
+ Stable operation key
+ Approval gate
+ Retry policy
+ Audit log
```

---

# 9. Harness Engineering

Harness는 모델을 더 똑똑하게 만드는 계층이 아니라 **모델이 실제로 일할 환경을 제공하는 계층**이다.

핵심 책임:

- Tool Dispatch
- Context Management
- Permission Gating
- State Persistence
- Error Recovery

자료에서는 Harness를 다음 6층으로 설명한다.

```text
L6 Plugins       배포·공유
L5 Agent Teams   여러 Agent의 협업 구조
L4 Subagents     Context 격리·위임
L3 Hooks         결정적 강제 규칙
L2 Skills        반복 절차와 방법
L1 Policy        프로젝트 기본 규칙
```

### 중요한 원칙

- 정책과 절차와 강제를 한곳에 몰아넣지 않는다.
- 판단은 LLM이 할 수 있지만, 보안·검증처럼 결정적이어야 하는 것은 코드/Hook이 맡는다.
- 처음부터 복잡한 Harness를 만들지 않는다.
- 실제 실패가 발생한 지점에 필요한 층을 추가한다.

```text
Fail → Identify cause → Add smallest guardrail → Measure again
```

---

# 10. Main Agent와 Subagent

Subagent는 단순히 “Agent를 여러 개 쓰는 것”보다 **Context와 책임을 분리하는 장치**로 이해하는 편이 좋다.

장점:

- Main context 보존
- 전문화된 역할
- 별도 도구 권한
- 병렬 수행
- 저렴한 모델로 작업 라우팅 가능

주의점:

- context가 분리되므로 필요한 정보가 전달되지 않으면 성능이 떨어진다.
- 지나치게 고정된 위임 구조는 모델의 유연성을 오히려 제한할 수 있다.
- Subagent에게 필요한 정책·절차가 자동으로 모두 전달된다고 가정하면 안 된다.

따라서 “많이 쪼갤수록 좋다”보다 다음 기준이 낫다.

> **Context 오염을 줄이거나 책임/권한을 명확히 분리할 실익이 있는가?**

---

# 11. MCP(Model Context Protocol)

## 11.1 MCP가 푸는 문제

도구를 Agent 코드 안에 직접 정의하면 그 Agent에 강하게 결합된다.

```text
Agent A ── custom integration ── Service X
Agent B ── another integration ── Service X
Agent C ── another integration ── Service X
```

MCP의 핵심 아이디어는 기능을 **별도 서버로 표준화**하고, Client가 런타임에 발견하도록 만드는 것이다.

```text
Host / Agent
    ↓
MCP Client
    ↓ protocol
MCP Server
    ↓
External System
```

### 세 역할

- **Host**: 사용자 요청과 LLM 실행을 관리하는 애플리케이션.
- **Client**: MCP 연결, 메시지 라우팅, 서버 capability 발견을 담당.
- **Server**: 실제 Tool/Resource/Prompt를 제공.

Client는 서버 구현 코드를 직접 import하지 않아도 프로토콜을 통해 도구 목록과 설명을 발견할 수 있다.

---

## 11.2 MCP의 세 Primitive

### Tool

행동을 수행하는 실행 함수.

```text
search_documents
create_event
query_database
```

### Resource

읽기 전용으로 제공되는 컨텍스트/데이터.

```text
file://docs/policy.md
schema://database/orders
```

### Prompt

재사용 가능한 지시 템플릿.

```text
summarize_meeting
review_pull_request
plan_trip
```

핵심 구분:

```text
Tool     = Action
Resource = Context / Data
Prompt   = Reusable Instruction
```

---

## 11.3 Transport

### stdio

로컬 MCP 서버를 자식 프로세스로 띄우고 표준입출력으로 통신한다.

가장 중요한 규칙:

> **stdio MCP 서버의 stdout은 프로토콜 전용이다.**

따라서 디버그용 `print()`를 stdout에 쓰면 프로토콜 메시지를 깨뜨릴 수 있다. 로그는 stderr 또는 logging으로 분리한다.

### Streamable HTTP

원격 서버를 네트워크로 연결할 때 사용한다. 원격에서는 인증, 권한, TLS, 네트워크 노출이 중요한 설계 요소가 된다.

---

## 11.4 MCP와 Tool 설계 원칙은 연결된다

MCP가 도구를 표준화해도 **나쁜 도구가 좋은 도구가 되는 것은 아니다**.

서버가 공개하는 Tool Schema와 Description에는 앞서 정리한 원칙을 그대로 적용한다.

```text
Single Responsibility
Explicit Arguments
Structured Return
Clear Description
What / When / How / Output / Constraints
```

MCP는 연결 문제를 해결하고, Tool Contract는 의미 문제를 해결한다.

---

## 11.5 MCP 보안 기본선

자료에서 반복되는 보안 원칙을 운영 기준으로 정리하면:

- API 키를 코드에 하드코딩하지 않는다.
- `.env`, secret manager 등으로 분리한다.
- 서버를 필요 이상으로 공용 네트워크에 노출하지 않는다.
- 사용자/Agent별 최소 권한을 적용한다.
- 읽기와 쓰기 capability를 분리한다.
- 고위험 도구에는 승인 gate를 둔다.
- 프롬프트 가드레일만 보안 경계로 믿지 않는다.
- 모든 중요한 실행은 감사 가능한 로그를 남긴다.

---

# 12. n8n: 시각적 Workflow Engineering

n8n 자료의 목적은 노드 이름을 외우는 것이 아니라 **시각적 워크플로 사고법**을 익히는 것이다.

## 12.1 네 가지 사고법

```text
1. Trigger로 시작한다
2. Node로 작업을 쪼갠다
3. Data Flow를 추적한다
4. AI Node를 필요한 곳에 끼운다
```

### 1) Trigger

“무엇이 일어나면 시작하는가?”

예:

- Schedule
- Webhook
- Gmail Trigger
- GitHub event
- RSS update

### 2) Node

작업을 작은 함수처럼 분해한다.

```text
Fetch → Transform → LLM → Validate → Store → Notify
```

### 3) Data Flow

n8n에서 중요한 것은 노드 그림보다 **노드 사이를 흐르는 JSON**이다.

문제가 생기면 “어느 노드가 빨간가?”보다 먼저:

```text
이 노드에 실제로 어떤 JSON이 들어왔는가?
어떤 필드가 다음 노드로 전달되었는가?
배열의 item 단위가 무엇인가?
```

를 확인한다.

### 4) AI Node

AI는 워크플로 전체가 아니라 비결정적 판단이 필요한 부분에 삽입한다.

```text
Deterministic Nodes
→ LLM
→ Structured Output
→ Deterministic Validation / If
```

---

## 12.2 AI Workflow의 표준 5단계

n8n 자료에서 반복되는 구조:

```text
Trigger
  ↓
Data Collection
  ↓
AI Analysis / Generation
  ↓
Post-processing / Validation
  ↓
Delivery / Action
```

예를 들면:

```text
GitHub Webhook
→ PR diff 수집
→ LLM 코드 리뷰(JSON 계약)
→ If(score threshold)
→ 자동 처리 또는 사람 리뷰
```

중요한 철학은 **AI가 최종 권한을 항상 가져야 하는 것은 아니라는 것**이다.

---

## 12.3 Drive에 포함된 n8n 실습 워크플로

실습 폴더에는 다음 유형의 예제가 있다.

```text
1_basic_chatbot.json
2_ai_agent_tools.json
3_webhook_chatbot_backend.json
4_rss_summary_sheets.json
5_rag_indexing.json
6_ollama_local_llm.json
7_multi_agent_debate.json
8. RAG_Chatbot.json
```

이를 학습 순서로 보면:

```text
Basic Chat
→ Tool 사용
→ Webhook/API 연결
→ 외부 데이터 자동화
→ RAG Indexing
→ Local LLM
→ Multi-Agent
→ RAG Chatbot
```

즉 n8n은 단순 자동화 도구라기보다, **Trigger + Data + AI + Action을 시각적으로 조립하는 Agent Runtime의 한 형태**로 볼 수 있다.

---

# 13. RAG와 Memory

## 13.1 RAG가 필요한 이유

LLM은 최신 정보와 사내/개인 문서를 기본적으로 알지 못한다.

```text
User Query
   ↓
Retrieve relevant chunks
   ↓
Context Injection
   ↓
LLM Answer
```

RAG는 모델 weight를 바꾸는 것이 아니라 **질문 시점에 필요한 외부 정보를 Context에 넣는 방식**이다.

Foundation Model 적응 방법을 큰 축으로 보면:

- Full Fine-Tuning
- PEFT / LoRA
- In-context Learning / Prompting
- RAG

실무에서는 먼저 Prompt/RAG로 해결 가능한지 확인하고, 모델 자체를 바꿔야 할 명확한 이유가 있을 때 Fine-Tuning을 검토하는 접근이 비용 효율적이다.

## 13.2 Memory의 역할

Memory는 “모델이 똑똑한가”와 다른 문제다.

```text
Foundation Model = 어떤 뇌를 쓰는가
Memory           = 무엇을 기억하게 하는가
Tool             = 무엇을 할 수 있게 하는가
```

Agent Memory를 설계할 때는 적어도 다음 질문이 필요하다.

- 어떤 정보를 저장할 것인가?
- 언제 검색할 것인가?
- 얼마나 오래 보존할 것인가?
- 사용자가 수정/삭제할 수 있는가?
- 현재 Context와 장기 Memory가 충돌하면 무엇을 우선할 것인가?
- 개인/보안 데이터를 어떤 권한으로 읽는가?

---

# 14. FastAPI: Agent를 API 서비스로 감싸기

FastAPI는 Agent 로직을 웹 서비스로 제공할 때 자연스럽게 연결되는 계층이다.

## 14.1 핵심 구성

```text
FastAPI = Starlette 기반 웹 계층 + Pydantic 기반 검증
```

타입 힌트가 동시에 다음 역할을 한다.

```text
Input Parsing
+ Validation
+ API Schema
+ Auto Documentation
```

예:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TaskCreate(BaseModel):
    title: str
    priority: str

@app.post("/tasks", status_code=201)
def create_task(payload: TaskCreate):
    return {"id": 1, **payload.model_dump()}
```

잘못된 요청은 함수 실행 전에 Pydantic 검증에서 차단할 수 있다.

---

## 14.2 REST 기본

```text
GET     조회
POST    생성
PUT     전체 교체
PATCH   일부 수정
DELETE  삭제
```

좋은 URL 설계:

```text
POST   /tasks
GET    /tasks/1
PATCH  /tasks/1
DELETE /tasks/1
```

동작 이름을 URL에 넣기보다 **명사형 Resource + HTTP Method**로 표현한다.

GET은 기본적으로 side effect가 없어야 한다.

---

## 14.3 입력 통로 세 가지

```text
Path Parameter   무엇을 지목하는가
Query Parameter  어떻게 조회할 것인가
Request Body     구조화된 데이터를 전달
```

예:

```http
PATCH /tasks/1?notify=true
Content-Type: application/json

{"title":"장보기"}
```

---

## 14.4 상태 코드의 책임 분리

대표적으로:

```text
2xx 성공
4xx 요청/권한 문제
5xx 서버/의존 시스템 문제
```

FastAPI Agent API에서는 특히 다음을 구분하면 좋다.

```text
422  형식/타입 검증 실패
400  우리가 정의한 비즈니스 규칙 위반
401  인증되지 않음
403  인증됐지만 권한 없음
404  자원 없음
502  upstream 서비스 문제
500  예상하지 못한 내부 오류
```

이 분류는 앞의 Agent 오류 계약과 그대로 연결된다.

---

# 15. SQLite: Agent 실행 원장 만들기

## 15.1 SQLite가 잘 맞는 이유

SQLite는 서버 프로세스가 따로 없는 **파일 하나짜리 데이터베이스**다.

장점:

- 설정이 거의 없다.
- Python 표준 라이브러리로 바로 쓸 수 있다.
- 복사만으로 백업하기 쉽다.
- 로컬 Agent, 실험, 배치 로그, 단일 사용자 앱에 좋다.
- SQL로 결과를 다시 집계할 수 있다.

한계:

- 매우 높은 동시 쓰기
- 여러 서버에서 동시에 쓰는 대규모 서비스

이런 상황에서는 PostgreSQL 같은 서버형 DB가 더 적합하다.

---

## 15.2 Python 기본 패턴

```python
import sqlite3

conn = sqlite3.connect("agent_runs.db")

with conn:
    conn.execute(
        "INSERT INTO runs(run_id, status) VALUES (?, ?)",
        (run_id, status),
    )
```

문자열 조립 대신 `?` parameter binding을 사용해 값을 SQL 코드와 분리한다.

```text
Bad
f"SELECT * FROM users WHERE name='{name}'"

Good
conn.execute("SELECT * FROM users WHERE name=?", (name,))
```

---

## 15.3 Agent 운영용 스키마 사고법

실습은 기술 결과와 사람 검토 대상을 분리한다.

예시:

```text
runs
  run_id
  model
  contract_version
  started_at
  finished_at

results
  run_id
  item_id
  status
  error_type
  attempts
  latency_ms
  output_json

review_queue
  run_id
  item_id
  reason
  review_status
```

핵심은 **기술 실패와 업무상 승인 필요를 같은 상태로 뭉개지 않는 것**이다.

```text
validation_success = true
human_approval_required = true
```

둘은 동시에 존재할 수 있다.

---

## 15.4 UPDATE/DELETE 안전 습관

```sql
SELECT id, title FROM todos WHERE title = '장보기';

-- 영향 범위를 확인한 뒤
UPDATE todos SET done = 1 WHERE title = '장보기';
```

**쓰기 전에 같은 WHERE로 SELECT를 먼저 실행**하는 습관은 작은 SQLite 실습에서도 프로덕션 DB 안전성으로 그대로 이어진다.

---

# 16. Observability: 로그에서 운영으로

## 16.1 Print 로그의 한계

한 번의 실험은 `print()`로 볼 수 있지만, 여러 run을 비교하기 시작하면 다음이 필요해진다.

- trace
- span
- generation
- latency
- token/cost
- error taxonomy
- score
- run/version metadata
- 검색과 필터

자료의 흐름은 다음과 같다.

```text
Model Run
  ↓
SQLite Ledger
  ↓
Langfuse 같은 Observability Tool
```

## 16.2 원본 DB와 관측 도구를 함께 쓰는 이유

자료의 결론은 둘 중 하나를 고르는 것이 아니다.

```text
Own DB
  장점: 데이터 소유, 자유로운 SQL, 보관 정책 제어

Observability Tool
  장점: trace 구조, UI, 점수, 비교, 알림
```

실무형 구조:

```text
Source of Truth     = Own DB / Event Store
Operational View    = Observability Platform
```

## 16.3 “보냈다”와 “저장됐다”를 구분

비동기 관측 SDK에서는 `flush()` 호출만으로 서버에 반영됐다고 단정하면 안 된다. 전송 후 다시 읽어서 확인하는 read-back 검증이 중요하다.

```text
Emit → Flush → Read Back → Confirm
```

이 사고는 메시지 큐, 로그 파이프라인, 외부 API 적재에도 그대로 적용된다.

---

# 17. Docker: Agent의 실행 계약

Docker 자료에서 가장 중요한 정의는 다음과 같다.

> **Docker는 Agent 실행 환경을 계약으로 고정하는 도구다.**

세 가지 핵심 가치:

```text
Reproducibility
Isolation
Composability
```

## 17.1 Reproducibility

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

환경을 문서로 설명하는 대신 Dockerfile로 실행 가능하게 고정한다.

`latest`보다 버전 태그 또는 digest를 사용하는 것이 재현성에 유리하다.

---

## 17.2 Isolation

컨테이너는 VM과 달리 호스트 커널을 공유하지만 namespace와 cgroup으로 프로세스와 자원을 격리한다.

주요 제한:

```text
--cpus
--memory
--pids-limit
network namespace
mount namespace
user namespace
```

Agent가 생성한 코드를 실행해야 할 때는 일반 애플리케이션보다 더 강한 제한이 필요하다.

예시 사고법:

```text
network disabled unless required
read-only filesystem where possible
non-root user
CPU limit
memory limit
PID limit
timeout
temporary writable directory
no host secrets mounted
```

Docker는 강력한 경계지만 완전한 보안 샌드박스와 동일한 것은 아니다. 고위험 멀티테넌트 환경에서는 더 강한 격리 계층도 검토해야 한다.

---

## 17.3 Image와 Container

```text
Image      = 불변 설계도
Container  = Image + writable runtime layer
Volume     = Container가 사라져도 남아야 하는 데이터
```

영속 데이터는 컨테이너의 writable layer에 의존하지 않는다.

---

## 17.4 Storage 세 종류

```text
tmpfs         임시 데이터 / sandbox
bind mount    개발 중 호스트 코드 공유
named volume  DB 등 영속 데이터
```

---

## 17.5 Dockerfile 기본 원칙

자료를 실무 체크리스트로 정리하면:

1. 의존성 파일을 먼저 COPY해 캐시를 활용한다.
2. 가능한 작은 base image를 사용한다.
3. 불필요한 빌드 산출물과 package cache를 제거한다.
4. `.dockerignore`를 둔다.
5. runtime은 non-root user로 실행한다.
6. `EXPOSE`는 문서일 뿐 실제 포트 공개와 다름을 이해한다.
7. 필요하면 multi-stage build를 사용한다.

---

## 17.6 Docker Compose

여러 서비스를 한 장의 YAML로 묶는다.

```yaml
services:
  api:
    build: .
    ports:
      - "127.0.0.1:8000:8000"
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16
```

핵심 명령:

```bash
docker compose up -d --build
docker compose ps
docker compose logs -f
docker compose exec api sh
docker compose down
```

`down -v`는 볼륨까지 삭제할 수 있으므로 데이터가 필요한 환경에서는 주의한다.

---

# 18. GCP 배포의 기본 그림

Drive의 GCP 자료는 Docker 다음 단계로 클라우드 배포를 연결한다.

강의의 핵심 서비스는 다음 둘이다.

```text
Cloud Run = 컨테이너 실행
Cloud SQL = 관리형 관계형 DB
```

큰 흐름:

```text
Local App
  ↓ Docker build
Container Image
  ↓ Registry / Deployment
Cloud Run
  ↓
Public or controlled HTTPS endpoint
  ↓
Cloud SQL / External APIs
```

운영 배포에서는 로컬과 달리 다음을 별도로 관리해야 한다.

- 프로젝트/환경 구분
- 인증과 IAM
- Secret 관리
- 네트워크 노출 범위
- DB connection
- 로그/모니터링
- 비용 한도
- 배포 버전과 rollback

`gcloud` CLI는 이러한 클라우드 자원을 터미널에서 제어하는 도구다.

---

# 19. 통합 아키텍처: 자료 전체를 하나로 연결하기

이 폴더의 내용을 하나의 실제 서비스 구조로 합치면 다음과 같다.

```text
┌─────────────────────────────────────────────┐
│                User / Client                │
└──────────────────────┬──────────────────────┘
                       │
                 HTTP / Webhook
                       │
┌──────────────────────▼──────────────────────┐
│                  FastAPI                    │
│ Request schema / auth / status code         │
└──────────────────────┬──────────────────────┘
                       │
              Workflow or Agent?
                       │
        ┌──────────────┴──────────────┐
        │                             │
┌───────▼────────┐             ┌──────▼───────┐
│ Deterministic  │             │ Agent Loop   │
│ Workflow       │             │ Decide/Act   │
└───────┬────────┘             └──────┬───────┘
        │                             │
        └──────────────┬──────────────┘
                       │
                Tool Contract
                       │
          ┌────────────┴────────────┐
          │                         │
   Local Functions              MCP Client
                                    │
                              MCP Server(s)
                                    │
                      DB / Search / Gmail / etc.
                       │
                 Tool Result
                       │
               Structured Status
                       │
                Output Contract
                       │
                  Validation
                       │
            ┌──────────┴──────────┐
            │                     │
          Pass                   Fail
            │                     │
            │             Repair / Backoff
            │                     │
            │              Retry Budget End?
            │                     │
            │              Human Review
            │                     │
            └──────────┬──────────┘
                       │
                  SQLite / DB
                       │
                 Observability
                       │
              Metrics / Release Gate
                       │
                  Docker Image
                       │
                 Cloud Deployment
```

이 구조에서 각 기술의 역할은 겹치지 않는다.

| 기술/개념 | 주 역할 |
|---|---|
| Output Contract | 모델 출력의 형식 경계 |
| Validator | 계약 위반과 실패 분류 |
| Retry/Repair | 복구 정책 |
| Workflow | 고정된 실행 순서 |
| Agent | 런타임 판단 |
| Tool Contract | 외부 행동의 의미 경계 |
| MCP | Tool/Resource/Prompt 연결 표준 |
| n8n | 시각적 오케스트레이션 |
| FastAPI | HTTP 서비스 경계 |
| SQLite | 로컬/배치 실행 원장 |
| Langfuse류 | Trace·Score·운영 관측 |
| Docker | 재현 가능한 실행 환경·격리 |
| GCP | 원격 운영 인프라 |

---

# 20. 실패 분류표: 어디서 깨졌는가

Agent 시스템을 디버깅할 때는 “LLM이 이상하다”로 끝내지 말고 실패 위치를 분리한다.

```text
[Input]
  ├─ invalid request
  ↓
[Planning]
  ├─ wrong workflow/agent choice
  ├─ wrong tool selection
  ↓
[Tool Call]
  ├─ bad arguments
  ├─ permission denied
  ├─ timeout / 429 / 5xx
  ↓
[Generation]
  ├─ no JSON
  ├─ malformed JSON
  ↓
[Validation]
  ├─ schema violation
  ├─ business rule violation
  ↓
[Action]
  ├─ duplicate side effect
  ├─ irreversible action
  ↓
[Persistence]
  ├─ commit failure
  ├─ missing run metadata
  ↓
[Observability]
  ├─ event emitted but not ingested
  ├─ trace correlation missing
```

“어디서 실패했는지”가 분명해야 담당자와 처방도 분리할 수 있다.

---

# 21. 운영 가능한 Agent를 만드는 체크리스트

## 21.1 설계 전

- [ ] 다음 행동이 고정되어 있는가? → Workflow 우선 검토
- [ ] 정말 런타임 판단이 필요한가? → Agent 필요성 확인
- [ ] 외부 데이터가 필요한가? → Search/RAG/Tool
- [ ] 장기 기억이 필요한가? → Memory 정책
- [ ] 실제 부작용이 있는가? → 위험도/가역성 분류

## 21.2 Output

- [ ] 고정 키
- [ ] 타입
- [ ] enum/range
- [ ] default/null 정책
- [ ] 예시
- [ ] 순수 JSON/structured output
- [ ] 필드 간 business rule 검증

## 21.3 Tool

- [ ] Single responsibility
- [ ] Explicit arguments
- [ ] Structured return
- [ ] What/When/How/Output/Constraints
- [ ] 실패 상태와 retryable 필드
- [ ] timeout
- [ ] side effect 명시
- [ ] approval gate
- [ ] idempotency/중복 방지

## 21.4 Retry

- [ ] 실패 종류를 먼저 분류
- [ ] format failure는 evidence-based repair
- [ ] 429/5xx는 backoff+jitter
- [ ] auth failure는 재시도하지 않음
- [ ] max attempts 존재
- [ ] 실패 후 human_review/stop 상태 존재
- [ ] 추가 latency/cost 측정

## 21.5 Runtime / MCP

- [ ] 최소 권한
- [ ] secret 하드코딩 없음
- [ ] read/write capability 분리
- [ ] MCP stdio stdout 오염 없음
- [ ] remote transport 인증
- [ ] tool description 명확
- [ ] audit trail 존재

## 21.6 Persistence / Observability

- [ ] run_id
- [ ] model/version
- [ ] prompt/contract version
- [ ] input/output reference
- [ ] attempts
- [ ] error taxonomy
- [ ] latency
- [ ] cost/token
- [ ] human review status
- [ ] trace read-back 확인

## 21.7 Deployment

- [ ] Dockerfile 고정
- [ ] `.dockerignore`
- [ ] non-root
- [ ] resource limits
- [ ] 필요한 포트만 노출
- [ ] secrets image에 포함하지 않음
- [ ] persistent data는 volume/DB
- [ ] health check
- [ ] rollback 가능한 이미지 버전
- [ ] cloud IAM/network/cost 확인

---

# 22. RAG 실습용 AI 정책 문서 요약

`Practice_N8N/data`에는 RAG/검색 실습용으로 미국과 대한민국의 AI 정책 문서가 포함되어 있다. 이 절은 정치적 평가가 아니라 **문서 자체의 구조를 검색용 도메인 지식으로 요약**한다.

## 22.1 미국: America's AI Action Plan (2025-07)

문서는 크게 세 축으로 구성되어 있다.

```text
Pillar I   Accelerate AI Innovation
Pillar II  Build American AI Infrastructure
Pillar III Lead in International AI Diplomacy and Security
```

주요 주제:

- AI 혁신과 민간 도입 촉진
- 오픈소스·오픈웨이트 AI 지원
- 과학·정부·국방 영역 AI 활용
- 데이터센터, 전력망, 반도체 등 인프라 확충
- 사이버보안과 AI incident response
- 동맹국과의 AI 기술 협력 및 수출
- 첨단 반도체·컴퓨트 관련 안보와 통제
- frontier model 평가와 국가안보 위험 관리

RAG 실습 관점에서는 “정책 축 → 하위 정책 행동” 구조가 뚜렷해서 **heading 기반 chunking, 정책별 retrieval, 국가 간 주제 비교** 실습에 적합하다.

## 22.2 대한민국: 대한민국 인공지능 행동계획 (2026-02-25)

문서는 **3대 정책축, 12대 전략분야**로 구성된다.

### 정책축 1: AI 혁신 생태계 조성

1. AI고속도로 구축
2. 차세대 AI 기술 선점
3. AI 핵심인재 확보
4. 독자 범용 AI 모델 확보
5. AI 규제혁신

### 정책축 2: 범국가 AI 기반 대전환

6. 산업 AI 대전환
7. 공공 AI 대전환
8. 지역 AI 대전환
9. AI 기반 문화강국
10. AI 기반 국방강국

### 정책축 3: 글로벌 AI 기본사회 기여

11. AI 기본사회 실현
12. 글로벌 AI 이니셔티브 강화

문서 초반은 컴퓨팅·데이터·반도체·전력·보안을 AI 인프라의 핵심 요소로 보고, 이후 산업·공공·지역·문화·국방 전환과 글로벌 협력으로 확장한다.

RAG 실습 관점에서는 다음 질문을 만들기 좋다.

```text
- 특정 전략분야의 세부 행동계획은 무엇인가?
- 인프라 관련 항목만 모아 요약하라.
- 산업/공공/지역 AX의 차이를 비교하라.
- 미국 문서의 Infrastructure 축과 한국의 AI고속도로 축을 문서 근거만으로 비교하라.
```

---

# 23. 학습 로드맵

이 폴더 자료를 다시 공부한다면 다음 순서가 개념 연결이 좋다.

```text
[LLM 기본]
Sampling / Model choice / Local LLM
        ↓
[출력 안정화]
Output Contract
→ Validation
→ Retry / Repair
→ SLA / Cost
        ↓
[Agent]
Workflow vs Agent
→ Think-Act-Observe
→ Reflexion
→ Tool Design
→ Workflow Patterns
        ↓
[연결]
MCP Architecture
→ MCP Server / Client
→ Resource / Prompt
→ Multi-Agent / A2A
        ↓
[실전 시스템]
FastAPI
+ n8n
+ RAG
+ SQLite
+ Observability
        ↓
[운영]
Docker
→ Cloud Deployment
```

### 가장 중요한 연결 관계

```text
Structured Output   ↔ FastAPI/Pydantic schema
Tool Contract       ↔ MCP Tool Schema
Retry Policy        ↔ n8n Error Branch / Agent Loop
SQLite Ledger       ↔ Observability Trace
Docker Isolation    ↔ Agent Tool Safety
RAG                 ↔ MCP Resource / Search Tool
Human Review        ↔ High-risk Action Gate
```

이 연결을 이해하면 각각의 기술을 따로 외울 필요가 줄어든다.

---

# 24. 한 페이지 요약

```text
1. 모든 문제를 Agent로 풀지 않는다.
   다음 단계가 미리 정해지면 Workflow가 더 낫다.

2. LLM 출력을 믿지 말고 계약한다.
   Fixed keys + types + enum/range + defaults + examples + pure JSON.

3. 검증은 결과 뒤에 붙이는 장식이 아니다.
   Parsing → Schema → Business rule을 구분한다.

4. 실패는 종류가 있어야 한다.
   NO_JSON / JSON_DECODE / SCHEMA_VIOLATION / timeout / auth ...

5. 재시도는 '다시 해'가 아니다.
   실패 증거를 주고 Repair하며, budget을 다 쓰면 명시적으로 끝낸다.

6. Tool 설명은 API 계약이다.
   What / When / How / Output / Constraints.

7. 설명은 보안 경계가 아니다.
   권한, 승인, timeout, resource limit는 코드가 강제한다.

8. MCP는 도구를 재사용 가능한 서버 경계로 분리한다.
   Host ↔ Client ↔ Server, Tool / Resource / Prompt.

9. Agent의 실행은 기록해야 개선할 수 있다.
   SQLite/DB에 원본을 남기고 Observability에서 trace와 score를 본다.

10. Docker는 Agent의 실행 계약이다.
    Reproducibility + Isolation + Composability.

11. 출시 여부는 느낌이 아니라 Release Gate로 결정한다.
    성공률 + p95 latency + cost + first-try + human review.

12. 고위험 행동은 Draft → Gate → Commit으로 나눈다.
```

---

# 25. Drive 자료 인덱스

## A. `1. LLM 제어와 출력계약`

핵심 범위:

- 다음 토큰 확률 분포
- temperature / top-p / top-k
- seed와 재현성 한계
- 로컬 SLM
- 토큰 경제학
- closed vs open model 비교
- 모델 선택과 라우팅
- 출력 계약 설계
- 검증 파이프라인
- 3단계 재시도
- 100건 실측
- 실패 분류
- SLA와 비용
- Self-Consistency
- SQLite 실행 원장
- Langfuse 관측
- 근거 기반 리서치 Agent
- Few-shot / CoT / ReAct 특강

대표 파일:

```text
README.md
12강_출력_계약_설계_원칙(AI_Pair).ipynb
13강_검증_파이프라인(AI_Pair).ipynb
14강_3단계_재시도_전략(AI_Pair).ipynb
17강_SLA와_비용(AI_Pair).ipynb
19강_배치_파이프라인_SQLite(AI_Pair).ipynb
20강_대시보드와_모니터링(AI_Pair).ipynb
Agent의 뇌_LLM과 Memory.pdf
Agentic Engineering 개념.pdf
MCP 개념.pdf
```

## B. `2. Agent런타임과 MCP`

정규 강의 흐름:

```text
01~05  Agent runtime / Think-Act-Observe / log / Reflexion
06~09  Tool design / description / errors / orchestration
10~14  Sequential / Parallel / Loop / pattern selection
15~20  MCP problem / architecture / server / client / capstone / resource·prompt
21~23  Web search / Local LLM / Multi-agent Supervisor
```

특강:

```text
LLM API 기초 1: Text / Structured Output / Tool Call
Streaming
Multimodal
Embedding / Web Search
Prompt Caching / Cost Optimization
A2A Agent Communication
```

## C. `Practice_N8N`

```text
n8n tutorial.pdf
n8n-practice-workflow/
  1_basic_chatbot.json
  2_ai_agent_tools.json
  3_webhook_chatbot_backend.json
  4_rss_summary_sheets.json
  5_rag_indexing.json
  6_ollama_local_llm.json
  7_multi_agent_debate.json
  8. RAG_Chatbot.json

data/
  Americas-AI-Action-Plan.pdf
  대한민국 인공지능행동계획(2026~2028).pdf
```

## D. `Practice_Docker`

```text
Docker for AI Engineer.pdf
Docker tutorial and deployment.pdf
[실습1] Docker 활용.pdf
[실습2] Docker 기본 명령어.pdf
[실습3] Docker Compose.pdf
Google Cloud Platform deck.pdf
chatbot-gcp.zip
```

## E. `Practice_Sqlite3`

```text
SQLite 튜토리얼.pdf
sqlite3-tutorial.zip
Data/
```

## F. `Practice_FastAPI`

```text
FastAPI deck for KDT.pdf
```

---

# 26. 최종 설계 원칙

이 자료들을 하나로 묶었을 때 가장 중요한 원칙은 다음 문장으로 정리할 수 있다.

> **LLM의 불확실성을 없애려고 하지 말고, 불확실성이 있어도 시스템이 안전하게 동작하도록 경계를 설계한다.**

그 경계는 한 가지 기술이 아니라 여러 층으로 만들어진다.

```text
Prompt / Context
    ↓
Output Contract
    ↓
Validation
    ↓
Tool Contract
    ↓
Permission / Gate
    ↓
Retry / Escalation
    ↓
Persistence
    ↓
Observability
    ↓
Sandbox / Deployment
```

좋은 Agent 시스템은 모델이 한 번에 완벽한 답을 내는 시스템이 아니라,

- 무엇을 할 수 있는지 명확하고,
- 잘못된 출력을 판별할 수 있고,
- 실패를 종류별로 처리하며,
- 위험한 행동은 강제로 제한하고,
- 실행 근거를 남기고,
- 실제 지표로 개선 여부를 판단할 수 있는 시스템이다.
