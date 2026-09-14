# Factory Agent Hub — Project2 Implementation Runbook

> 이 문서는 **구현 순서와 실행 Gate의 source of truth**다.  
> 제품의 문제 정의·범위·아키텍처·경험 근거는 [`PROJECT_PLAN.md`](./PROJECT_PLAN.md), 요구사항 충족 여부는 [`REQUIREMENTS_CHECKLIST.md`](./REQUIREMENTS_CHECKLIST.md), 하드웨어 상세는 [`hardware/`](./hardware/)를 따른다.
>
> Project2의 구현 마감은 **2026-10-08 24:00**이다. 이 문서는 기존의 하드웨어 중심 `Day 1~14` 계획을 Project2 전체 전달물 기준으로 다시 정리한다.

## 1. 완료 정의

10월 8일 코드 동결 시 아래가 함께 존재해야 한다.

### 서비스

- Vercel에 실제 사용자 UI가 배포되어 있다.
- Cloud Run의 FastAPI가 외부에서 동작한다.
- `GET /health`, `POST /api/agent`, `/docs`가 동작한다.
- `/mcp`가 FastMCP Streamable HTTP endpoint로 동작한다.
- `/api/agent`와 `/mcp`의 역할이 분리되어 있다.
- `docker compose up` 한 줄로 로컬 핵심 서비스를 재현할 수 있다.
- `.env.example`이 있고 secret이 저장소에 커밋되지 않는다.

### LLM 제어

- Setup / Operator 출력은 Pydantic contract로 검증한다.
- validation 실패 시 제한된 repair retry와 명시적인 종료 조건이 있다.
- 장비 정보가 없으면 추측하지 않고 `NEEDS_INFO` 또는 `REJECTED`로 종료한다.
- 실제 write timeout은 자동 재전송하지 않고 `RESULT_UNKNOWN`으로 종료한다.
- 동일 조건에서 최소 2개 모델의 품질·비용·p50/p95·계약 준수율을 비교한다.
- output contract 준수율은 최종적으로 **100회 이상 실행**에서 측정한다.

### Skill / MCP / Edge

- `skills/factory-device-integration/SKILL.md`가 실제 Agent 판단에 사용된다.
- MCP는 Registry 조회와 검증된 capability 실행만 제공한다.
- LLM이 raw shell, 임의 Python, raw Serial 문자열을 직접 실행하지 않는다.
- Raspberry Pi Edge Gateway가 Registry / policy / deterministic execution / Serial routing / audit을 담당한다.
- 실제 장비 write에는 validation과 approval gate가 있다.

### Langfuse / Evaluation

- 모든 LLM call이 trace된다.
- trace에 input/output/model/tokens/latency/cost와 `user_id`/`session_id`가 남는다.
- Prompt Management에서 prompt version을 관리하고 trace와 연결한다.
- Langfuse Dataset에 **30건 이상**의 평가 케이스가 있다.
- 정상·경계·실패 유도 케이스가 모두 포함된다.
- 최소 2개의 분리된 평가 축을 사용한다.
- 같은 Dataset을 변경 전/후 최소 두 번 측정한다.
- 한 번에 한 요소만 바꾸고 regression case를 기록한다.
- `EVAL_REPORT.md`에 변경점, 전후 점수, regression, KEEP/DISCARD 판단을 남긴다.

### Physical validation

- Conveyor와 Robot Arm이 Agent 없이 각각 단독 제어된다.
- 두 장비는 서로 다른 고정 text Serial protocol을 사용한다.
- 동일한 generic Serial Adapter / DeviceSpec 구조로 두 장비를 표현한다.
- freeze 이후 두 번째 장비 온보딩을 위해 platform code/schema/system prompt/firmware를 수정하지 않는다.
- local stop은 Agent/MCP와 무관하게 Arduino에서 우선 처리한다.

---

## 2. 작업 축과 역할

3명 기준으로는 아래 세 축을 병렬로 진행한다. 4명이면 Evaluation / Evidence를 독립 축으로 분리한다.

| 축 | 주요 책임 | 반드시 남길 증거 |
|---|---|---|
| Hardware / Edge | Arduino firmware, physical smoke, Pi, Serial Adapter, Registry, executor | hardware smoke, protocol, audit log, failure log |
| Agent / Contract | Setup/Operator, Pydantic, Skill, validation/retry, model compare | schema, prompt version, contract run 결과 |
| Service / MCP | FastAPI, FastMCP, Docker, Cloud Run, Vercel, auth/CORS | deployed URL, `/health`, `/docs`, `/mcp` smoke |
| Evaluation / Evidence (4인 시) | Dataset, rubric, Langfuse, before/after eval, screenshots/video | 30+ Dataset, EVAL_REPORT, screenshots, demo video |

역할이 나뉘더라도 contract와 freeze 대상은 팀 전체가 함께 검토한다.

---

## 3. 09/14–09/17 — 사전기획 정리

현재 주제는 Factory Agent Hub 하나를 기준으로 정리한다. 형식만 맞추기 위한 B/C 후보 작성은 현재 보류한다.

### 완료된 것

- [x] Embedded/IoT Device Integration 3개월 직접 경험 Gate 확인
- [x] 공개 GitHub commit 근거 확보
- [x] Project2 요구사항 원문 저장
- [x] `PROJECT_PLAN.md`로 기획 source of truth 통합
- [x] Project2 요구사항 체크리스트 작성
- [x] Skill 초안 작성
- [x] 대표 eval 후보 10건 정리
- [x] 하드웨어 spec / BOM / packing list 정리

### 남은 것

- [ ] 최근 실제 Device Integration 반복 사례와 현재 대안 2~3건 보강
- [ ] customer journey / 단계별 pain point 정리
- [ ] 평가 10건의 expected result / 판정 근거 구체화
- [ ] 하드웨어 주문·수령 일정 확정

**Gate:** 문제 정의가 “Factory 운영 경험”이 아니라 **직접 경험한 Device Integration 반복 업무**에 계속 연결되어 있어야 한다.

---

## 4. 09/18–09/23 — Contract Freeze

이 구간의 목표는 코드를 많이 만드는 것이 아니라 **구현 전에 바뀌면 큰 비용이 드는 계약을 먼저 동결하는 것**이다.

### 4.1 Service contract

FastAPI 공개 계약:

```text
GET  /health
POST /api/agent
/mcp            # Streamable HTTP MCP
/docs
```

`POST /api/agent` 기본 입력:

```text
AgentRequest
  session_id
  mode: setup | operate
  message
  context
```

공통 응답:

```text
AgentResponse
  status
  message
  data
  errors[]
  trace_id
```

Setup structured output:

```text
DeviceSpecDraftResponse
  status: READY | NEEDS_INFO | REJECTED
  device_spec: DeviceSpec | null
  missing_fields[]
  warnings[]
  user_message
```

Operator structured output:

```text
PlanResponse
  status: READY | NEEDS_APPROVAL | REJECTED
  plan.steps[]
    capability_id
    arguments
    expected_state
  warnings[]
  user_message
```

### 4.2 Device / execution contract

최소 DeviceSpec / Capability 필드:

```text
device
  id
  version
  adapter
  connection

capability
  id
  name
  description
  command_template
  parameters
  read_write
  risk
  success_condition
  state_verification
  verification_state
```

상태 전이:

```text
DRAFT
→ VALIDATED
→ REVIEWED
→ TEST_APPROVED
→ VERIFIED
→ ACTIVE
```

미검증 capability는 Operator discovery/invoke에서 제외한다.

### 4.3 MCP contract

초기 tool은 다음 범위에서 고정한다.

```text
list_devices()
get_device(device_id)
list_capabilities(device_id)
get_device_status(device_id)
validate_device_spec(spec)
invoke_capability(device_id, capability_id, arguments, approval_token)
```

새 장비별 MCP Tool을 생성하지 않는다.

### 4.4 Failure contract

| 실패 | 처리 |
|---|---|
| LLM schema violation | 실패 내용을 넣어 repair retry 최대 1회 후 structured failure |
| 필수 장비 정보 누락 | 추측 금지, `NEEDS_INFO` |
| unsupported protocol/capability | `REJECTED` |
| invalid type/range | executor 전 단계에서 차단 |
| approval 없음/불일치 | 장비 전송 없이 차단 |
| read timeout | 제한된 retry budget 사용 가능 |
| write timeout / 응답 유실 | 자동 재전송 금지, `RESULT_UNKNOWN` |
| Edge disconnect | downstream step 중단 |
| local stop | Arduino가 즉시 우선 처리, 재가동은 상태 확인 + 새 승인 |

### 4.5 Eval contract

9월 23일까지 Langfuse Dataset으로 옮길 **30건 이상**을 확정한다.

권장 분포:

| 유형 | 수 |
|---|---:|
| 정상 Setup | 8 |
| 필수 정보 누락 / 모호함 | 5 |
| 타입·범위 오류 | 4 |
| injection / 위험 자유 문자열 | 3 |
| 미지원 protocol / capability | 3 |
| unverified / approval 오류 | 3 |
| 정상 Operator Plan | 2 |
| timeout / disconnect / result unknown | 2 |

각 케이스에 최소 다음을 적는다.

```text
input
expected status / expected contract
판정 기준
이 케이스를 넣은 이유
category
```

평가 축은 하나의 종합 점수로 합치지 말고 최소 두 개로 분리한다. 예:

- `contract_correctness`
- `safety_and_boundary`
- 필요 시 `task_quality`

### 4.6 09/23 Gate

- [ ] API contract freeze
- [ ] Pydantic output contract freeze
- [ ] failure/retry policy freeze
- [ ] Skill v1 freeze
- [ ] MCP tool contract freeze
- [ ] observability field freeze
- [ ] 30+ Dataset + rubric 준비
- [ ] Cloud Run ↔ Pi 인증 방식 결정
- [ ] Conveyor / Robot protocol 초안 준비

---

## 5. 09/28–09/29 — Skeleton + Hardware Bring-up

소프트웨어 skeleton과 실물 bring-up을 **병렬**로 진행한다.

### Service / Agent skeleton

- [ ] FastAPI app 생성
- [ ] `GET /health`
- [ ] `/docs` 확인
- [ ] `POST /api/agent` request/response Pydantic 적용
- [ ] LLM service layer 한 곳으로 호출 집중
- [ ] Langfuse trace 기본 연결
- [ ] Dockerfile / compose 작성
- [ ] `docker compose up` smoke
- [ ] Vercel UI skeleton: Setup / Operate / error state
- [ ] FastMCP `/mcp` skeleton

### Hardware bring-up

Conveyor:

- kit 조립
- motor 정격/전원 확인
- DRV8833 연결
- 30초 이상 연속 구동
- IR sensor 반복 감지
- local stop 입력 확인
- Serial request/response 구현

Robot Arm:

- kit 조립 / servo model 기록
- external 5V 5A servo power
- common GND
- joint safe range / HOME 확인
- 저하중 pick/place
- local stop 입력 확인
- Serial request/response 구현

세부 전원·부품·local stop 조건은 [`hardware/HARDWARE_SPEC.md`](./hardware/HARDWARE_SPEC.md)를 따른다.

### Hardware Gate

- [ ] 두 장비 모두 Agent 없이 독립 제어 가능
- [ ] 두 Serial protocol이 서로 다르고 문서화됨
- [ ] local stop이 Pi/MCP 없이 동작
- [ ] physical state를 명령 성공과 별도로 확인 가능

Hardware Gate가 늦어지면 UI나 API 작업을 멈추지 않는다. 반대로 mock 성공을 physical Gate 통과로 세지 않는다.

---

## 6. 09/30 — 중간 체크포인트

이날은 기능 추가보다 **현재 증거를 정리하는 날**로 둔다.

보여줄 것:

- 문제 정의 / 직접 경험 근거
- 30건 eval 설계와 rubric
- 전체 architecture
- FastAPI / Docker / Langfuse skeleton
- 두 장비 hardware smoke 또는 현재 blocker
- 명시적으로 잘라낸 범위

이 시점에서 hardware가 불안정하면 Robot의 노출 joint 수, Conveyor speed 단계, 부가 sensor를 줄인다. Project2 필수 서비스 항목을 줄이지 않는다.

---

## 7. 09/30–10/02 — Core Integration

### 7.1 Setup Agent

- 자연어 → `DeviceSpecDraftResponse`
- Langfuse Prompt v1 사용
- Pydantic validation
- repair retry 최대 1회
- missing/ambiguous info → `NEEDS_INFO`
- unsupported / injection → `REJECTED`
- Human Review state
- 제한된 Device Test
- verified capability만 ACTIVE

### 7.2 Operator Agent

- Registry / MCP discovery만 사용
- 등록되지 않은 기능 추측 금지
- raw Serial 생성 금지
- machine-readable PlanSpec 생성
- write step approval 확인
- state verification과 audit 기록

### 7.3 Edge Core

- stable Arduino mapping
- generic text Serial Adapter
- Registry
- deterministic validator / executor
- operation key
- audit log
- timeout/disconnect/result-unknown

### 7.4 MCP

- FastMCP Streamable HTTP
- tool 목록 고정
- read/write capability 구분
- write invoke에서 approval token 검증
- MCP access control 적용

### 7.5 Deployment

- Cloud Run에 FastAPI 배포
- Vercel에 UI 배포
- browser direct call이면 CORS/auth/secret exposure 문서화
- Cloud Run ↔ Pi edge authenticated route smoke
- 외부에서 `/health` 확인
- 실제 UI → `/api/agent` 정상/실패 흐름 확인

### 7.6 Model comparison

같은 입력/조건에서 최소 2개 모델을 비교한다.

기록:

```text
quality / eval axis scores
contract compliance
failure rate
cost per request
p50 latency
p95 latency
```

최종 모델 선택 근거를 남긴다.

### 10/02 Gate

- [ ] Vercel UI 동작
- [ ] Cloud Run `/health`, `/api/agent`, `/docs` 동작
- [ ] `/mcp` 연결 및 tool smoke
- [ ] Docker 재현
- [ ] Langfuse trace에 필수 metadata 기록
- [ ] 두 모델 비교 결과 존재
- [ ] Setup happy path 1개 + failure path 1개 E2E
- [ ] Edge actual device invoke 최소 1개 성공

---

## 8. 10/06 — Baseline Measurement

이날부터는 새 기능보다 **측정과 실패 분석**이 우선이다.

### Dataset baseline

같은 30+ Dataset을 Prompt v1 / 선택 모델로 실행한다.

측정:

- 평가 축별 score
- output contract pass rate
- unsafe/unsupported rejection
- plan validity / tool-call correctness
- p50 / p95
- tokens
- avg cost/request

### 100+ contract run

대표 입력군을 포함하여 100회 이상 structured output 실행을 모은다.

기록:

```text
total runs
valid contract count
validation failures
repair retry success
final failure count
contract compliance rate
```

### Failure analysis

실패를 예시 문장으로만 정리하지 않고 Langfuse trace ID와 연결한다.

예:

- missing field를 임의 보완
- 위험 write가 READY로 분류
- unsupported protocol을 spec으로 생성
- tool argument type 오류
- 불필요한 retry
- 비용/latency 이상치

---

## 9. 10/07 — One Change → Remeasure

baseline 실패에서 **가장 영향이 큰 한 요소**를 선택한다.

가능한 변경:

- Prompt v1 → v2
- 예시 수정
- structured output instruction 수정
- 모델 교체
- validator rule 수정

한 번에 여러 요소를 동시에 바꾸지 않는다.

같은 Dataset을 다시 실행하고 다음을 비교한다.

```text
axis score before / after
contract compliance before / after
p95 before / after
cost/request before / after
regressed cases
```

변경 결과는 `KEEP` 또는 `DISCARD`로 명시한다. 실패한 개선 시도도 기록한다.

---

## 10. 10/08 — Release Gate / Code Freeze

### Service Gate

- [ ] Vercel production URL
- [ ] Cloud Run production URL
- [ ] `GET /health`
- [ ] `POST /api/agent`
- [ ] `/docs`
- [ ] `/mcp`
- [ ] Docker / compose 10분 내 재현
- [ ] `.env.example`
- [ ] secret 미커밋

### LLM / Eval Gate

- [ ] Prompt version trace 연결
- [ ] Dataset 30+
- [ ] baseline + remeasurement
- [ ] 2+ 평가 축
- [ ] 2개 모델 비교
- [ ] 100+ contract run
- [ ] `EVAL_REPORT.md`

### Evidence Gate

- [ ] Langfuse dashboard screenshot 3장 이상
- [ ] detailed trace screenshot 1장
- [ ] MCP connection / tool / invocation evidence
- [ ] 정상 사용자 흐름 demo
- [ ] 실패 사용자 흐름 demo
- [ ] physical device execution evidence
- [ ] README 재현 절차
- [ ] README 상단 one-line problem/solution + metrics table + `docker compose up`

### Freeze

10월 8일 24:00 이후 평가 대상 코드 변경을 하지 않는다.

10월 9~11일은 발표 자료와 데모 영상 정리만 한다.

---

## 11. Physical no-code onboarding 검증

Project2 필수 조건과 별개로 이 프로젝트의 핵심 기술 가설을 검증하는 데모다.

```text
Before
Registry = Conveyor only

Freeze
- Setup / Operator code
- system prompt / examples
- DeviceSpec schema
- MCP tools
- Serial Adapter
- validator / executor
- Conveyor firmware / protocol
- Robot firmware / protocol

User gives Robot Arm information
→ Setup Agent draft
→ validation
→ human review
→ limited device test
→ ACTIVE Registry

After
Registry = Conveyor + Robot Arm

Same Operator
Same MCP
Same Serial Adapter
→ discover both devices
→ approved finite PlanSpec
→ physical execution
→ state verification / audit
```

평가 중 새 장비를 맞추기 위해 freeze 대상을 수정하면 no-code onboarding 실패로 기록한다.

---

## 12. 필수 실패 회귀

최소 다음 케이스는 자동 또는 재현 가능한 테스트로 남긴다.

- schema invalid output
- missing required device information
- invalid integer / enum / range
- command injection / newline injection
- unsupported protocol
- unknown capability
- unverified capability invoke
- approval 없는 write
- approval 후 arguments 변경
- spec version 변경 후 old approval 사용
- Edge disconnect
- read timeout
- write timeout / lost response → `RESULT_UNKNOWN`
- local stop active
- local stop wire disconnect

실제 장비가 필요한 실패와 LLM/contract만으로 재현 가능한 실패를 구분한다.

---

## 13. 범위 축소 순서

일정이 밀릴 때 **Project2 필수 조건부터 지우면 안 된다.**

먼저 제거:

1. LCD / NeoPixel 등 장식 UI
2. RFID
3. potentiometer / manual jog 등 부가 local UI
4. Robot에서 노출하는 joint/capability 수
5. Conveyor speed 단계
6. 복잡한 multi-device 자동화
7. UI animation / 시각적 polish
8. 부가 dashboard / 관리 기능

끝까지 유지:

```text
Vercel actual UI
Cloud Run FastAPI
GET /health + POST /api/agent + /docs
FastMCP /mcp
Docker / docker compose up
Pydantic output contract + retry/failure behavior
Skill
Langfuse tracing + Prompt Management + Dataset/re-eval
30+ eval cases
2-model comparison
100+ contract runs
actual failure path
.env.example / no secrets
```

프로젝트 고유 검증에서 가능한 한 유지:

```text
2 physical devices
2 frozen Serial protocols
1 generic Serial Adapter
DeviceSpec / Capability contract
human review / limited test / Registry
approval + deterministic execution
no-code onboarding evidence
```

한 장비의 기구 문제가 장기화되면 mock으로 성공 처리하지 말고 **더 단순한 실제 Serial 장비로 대체**한다.

---

## 14. 지금부터의 즉시 작업

현재 시점(2026-09-14)의 다음 순서는 다음과 같다.

1. 최근 Device Integration 반복 사례 / 현재 대안 근거 보강
2. customer journey와 pain point 정리
3. 대표 eval 10건의 expected result / rubric 구체화
4. 30건 Dataset 초안으로 확장
5. API / Pydantic / MCP / observability contract 작성
6. 하드웨어 주문·수령 준비
7. 구현 시작 전 repo skeleton과 역할 분담 확정

지금은 아직 기능 코드를 많이 만드는 단계가 아니다. **09/23까지 계약과 평가 기준을 먼저 고정하고, 09/28부터 서비스/하드웨어를 병렬 구현한다.**