# Project2 요구사항 체크리스트

> 기준 문서
>
> - `requirements/project2-webpage.md`
> - `requirements/project2-guide-v3.pdf` — 2차 팀 프로젝트 가이드 v3, 2026-09-11
>
> 점검 시점: **2026-09-14**
>
> 이 문서는 현재 저장소가 Project2 요구사항을 얼마나 충족하고 있는지 판단하는 **실행 체크리스트**다. 요구사항 원문은 `requirements/`의 두 파일을 source of truth로 사용한다. 기존 기획 문서가 있다고 해서 구현/측정 요구사항을 충족한 것으로 판정하지 않는다.

## 상태 정의

- `PASS` — 현재 저장소에 요구사항을 충족하는 산출물 또는 증거가 존재함
- `PARTIAL` — 설계/문서는 있으나 구현 또는 측정 증거가 아직 부족함
- `TODO` — 아직 산출물이 없음
- `BLOCKED` — 외부 결정이나 사람의 실제 경험 증거가 먼저 필요함
- `LATER` — 마감 전 필요하지만 현재 단계에서는 아직 수행 시점이 아님
- `DEFERRED` — 요구사항 자체는 남아 있지만 현재 프로젝트 정리 단계에서 의도적으로 보류함

---

# 1. 가장 먼저 닫아야 하는 주제 Gate

| 요구사항 | 상태 | 현재 근거 | 남은 일 |
|---|---|---|---|
| 팀원 중 해당 버티컬 도메인을 **3개월 이상 직접 경험**한 사람이 있어야 함 | `PASS` | `dudgns128/webos-gardening`에서 김재훈(`nanocode00`)의 2024-06-02~09-24 직접 HW-SW 통합 기록 확인. I²C sensor/actuator contract, 실제 데이터 변환, service 연동, timing/API 수정 commit을 `PROJECT_PLAN.md`에 링크함 | 최종 발표/README에서 동일 근거를 짧게 제시 |
| 실제 사용자의 반복 업무를 해결하는 주제일 것 | `PARTIAL` | 직접 경험한 새 센서·액추에이터·장비의 HW-SW 통합 반복 업무로 문제 범위를 좁힘 | 스마트 화분 경험의 구체 사례와 현재 대안을 2~3개 사례로 보강 |
| 사전기획에서 개인별 문제 후보 **3개** 준비 | `DEFERRED` | Factory Agent Hub 단일 주제를 기준으로 기획을 정리하기로 함. 형식만 채우기 위한 B/C는 만들지 않음 | 교육과정에서 3개 후보 제출을 실제 검수할 경우에만 별도로 보완 |
| 후보별 사용자 상황·현재 대안·범위 정리 | `PASS` for selected topic | `PROJECT_PLAN.md`에 선택 주제의 사용자, JTBD, 현재 대안/가설, 범위와 제외 범위를 통합 | B/C 후보는 현재 작성하지 않음 |
| 9/17까지 평가셋 후보 **10건** 준비 | `PASS` | `PROJECT_PLAN.md`에 선택 주제 대표 평가 케이스 10건과 30건 분포가 존재 | 9/23까지 실제 Dataset 30건으로 구체화 |
| 디자인 씽킹 기반 문제 정의 | `PARTIAL` | ICP/JTBD, 치명적 가정, 대안 비교가 존재 | 사용자 경험 근거를 반영한 최종 문제 정의 문장 확정 |
| 고객 여정 맵 / 단계별 pain point | `TODO` | 명시적 customer journey map 없음 | 최종 주제 확정 후 작성 |
| 유사 제품/현재 대안 분석 | `PARTIAL` | 기존 script/SDK/manual spec/workflow/PLC 후보 비교가 있음 | 실제 사용 대안과 경쟁 제품을 확인해 확정 |

**판정:** Candidate A의 **3개월 직접 경험 Gate는 PASS**로 본다. 공개 GitHub 기록만으로도 2024-06-02~09-24의 Embedded/IoT HW-SW 통합 작업이 확인된다. 과거 경험은 I²C 기반이며, 이번 MVP의 Serial Adapter는 검증용 구현 선택으로 구분한다. Factory Automation 실무 경험을 근거로 주장하지 않는다.

---

# 2. 핵심 기능 조건 6개 — 미충족 시 해당 평가축 점수 없음

## 필수 1 — 동작 가능한 배포 URL

| 세부 요구 | 상태 | 현재 |
|---|---|---|
| 외부에서 실제 동작하는 서비스 URL | `TODO` | 구현 코드/배포 없음 |
| 로컬 전용이 아닐 것 | `TODO` | 아직 서비스 없음 |

## 필수 2 — FastAPI + Docker

| 세부 요구 | 상태 | 현재 |
|---|---|---|
| FastAPI 백엔드 | `TODO` | 코드 없음 |
| Dockerfile | `TODO` | 없음 |
| `docker compose up` 한 줄로 전체 서비스 실행 | `TODO` | compose 없음 |
| clone 후 `.env.example` 복사 + 키 입력 + compose 실행 | `PARTIAL` | `.env.example`은 존재, 실행 스택 없음 |
| 채점자가 **10분 안에 로컬 재현** 가능 | `TODO` | 미구현 |

## 필수 3 — LLM API + 출력 계약

| 세부 요구 | 상태 | 현재 |
|---|---|---|
| LLM API가 핵심 로직에 사용됨 | `PARTIAL` | Setup/Operator Agent 설계만 존재 |
| Pydantic 응답 스키마 | `PARTIAL` | `PROJECT_PLAN.md`에 계약 초안만 존재, 코드 없음 |
| 검증 로직 | `PARTIAL` | DeviceSpec/validator 설계는 있으나 코드 없음 |
| 재시도 전략 | `PARTIAL` | Skill에 structured output repair 최대 1회 규칙 존재, 코드 없음 |
| 최종 실패/폴백/사용자 안내 | `PARTIAL` | 실패 원칙은 문서화, 실제 API 동작 없음 |

## 필수 4 — Langfuse 3축 운영

| 세부 요구 | 상태 | 현재 |
|---|---|---|
| Observability / tracing | `TODO` | 설계만 있음 |
| Prompt Management | `TODO` | 설계만 있음 |
| Evaluation / Dataset | `TODO` | 30건 Dataset 미작성 |
| 변경 후 **같은 평가셋 재측정** | `TODO` | 측정 전 |
| 한 번만 평가하지 않을 것 | `TODO` | 측정 전 |

## 필수 5 — Domain LLM + Skill + MCP Server

| 세부 요구 | 상태 | 현재 |
|---|---|---|
| 도메인 판단 기준을 담은 Skill | `PASS` draft | `skills/factory-device-integration/SKILL.md`로 요구 경로에 배치 |
| Skill에 용어·규칙·예외 처리 | `PASS` draft | DeviceSpec, capability, approval, timeout, result unknown 등 작성 |
| MCP Server 구현 | `TODO` | tool 설계만 존재 |
| FastMCP 기반 구현 | `TODO` | 코드 없음 |
| 실제 도메인 데이터/행동을 tool로 제공 | `TODO` | Raspberry Pi/Registry/Device 실행 설계만 존재 |

## 필수 6 — 소개 페이지 + 저장소 정리

| 세부 요구 | 상태 | 현재 |
|---|---|---|
| 서비스 소개 페이지 별도 구성 | `TODO` | 없음 |
| `.env.example` | `PASS` | 존재 |
| 민감값 커밋 금지 | `PARTIAL` | 현재 노출된 secret은 없으나 구현 후 지속 확인 필요 |
| 팀 저장소 정리 | `PARTIAL` | 문서 구조는 있으나 현재 파일 중복이 많음. 요구사항 충족 후 통합 예정 |

---

# 3. 공통 배포 구조 / Endpoint

목표 제출 구조:

```text
User
  -> Vercel / Next.js UI
  -> Cloud Run / FastAPI
       -> GET  /health
       -> POST /api/agent
       -> /mcp  (Streamable HTTP)
       -> Langfuse / LLM / domain APIs
       -> Raspberry Pi Edge Gateway (이 프로젝트의 추가 physical execution plane)
```

| 요구사항 | 상태 | 비고 |
|---|---|---|
| Vercel 서비스 UI | `TODO` | 아직 frontend 없음 |
| Cloud Run FastAPI | `TODO` | backend 없음 |
| `GET /health` | `TODO` | 없음 |
| `POST /api/agent` | `TODO` | 없음 |
| `/mcp` Streamable HTTP endpoint | `TODO` | 없음 |
| `/api/agent`와 `/mcp` 역할 분리 | `PARTIAL` | 문서 설계에는 반영됨 |
| MCP 접근 제어 방식 문서화 | `TODO` | token/allowed client 등 실제 방식 미정 |
| 브라우저→Cloud Run 직접 호출 시 CORS 설명 | `TODO` | 실제 배포 구조 확정 후 README 기록 |
| 인증 방식 설명 | `TODO` | 미정 |
| 브라우저에 secret을 노출하지 않을 것 | `TODO` | 구현 시 검증 필요 |

**Factory Agent Hub 추가 조건:** Cloud Run에서 USB Serial을 직접 사용할 수 없으므로 실제 장비 동작은 Raspberry Pi Edge Gateway로 분리한다. Cloud Run↔Pi 경계도 인증된 API로 만들고 raw shell/raw serial endpoint는 열지 않는다.

---

# 4. LLM 제어력 — 평가축 ②

## 4.1 출력 계약

| 요구사항 | 상태 | 현재 |
|---|---|---|
| Pydantic 모델 코드 | `TODO` | 문서 초안만 있음 |
| 검증 실패 처리 코드 | `TODO` | 없음 |
| 재시도 횟수/프롬프트/포기 조건 | `PARTIAL` | 정책 문서는 있음 |
| **100건 이상 실행한 계약 준수율** | `TODO` | 실측 없음 |
| 실패 경로 trace 가능 | `TODO` | Langfuse 미구현 |

### Factory Agent Hub에서 측정할 계약 후보

- `DeviceSpecDraftResponse`
- `PlanResponse`
- API-level `AgentResponse`

계약 준수율은 최종 30건 eval과 별도로 **100건 이상 structured output 실측**을 남긴다.

## 4.2 모델 선택

| 요구사항 | 상태 |
|---|---|
| 최소 **2개 이상 모델**을 같은 입력으로 비교 | `TODO` |
| 같은 프롬프트 / 같은 평가셋 / 같은 판정 기준 | `TODO` |
| 품질 비교 | `TODO` |
| 요청당 비용 비교 | `TODO` |
| p50 / p95 지연 비교 | `TODO` |
| 계약 준수율 / 실패율 비교 | `TODO` |
| 최종 모델 선택 이유 기록 | `TODO` |

## 4.3 프롬프트 관리

| 요구사항 | 상태 |
|---|---|
| 프롬프트를 코드 여러 곳에 흩뿌리지 않음 | `TODO` |
| Langfuse Prompt로 관리 | `TODO` |
| prompt version 유지 | `TODO` |
| 무엇을 왜 바꿨는지 기록 | `TODO` |

---

# 5. 서비스 준비도 — 평가축 ③

## 5.1 재현 가능성

최종 README에서 아래 흐름이 실제 동작해야 한다.

```bash
git clone <team-repo>
cp .env.example .env
# 필요한 키만 입력
docker compose up
```

상태: `TODO`

## 5.2 API 설계

| 요구사항 | 상태 |
|---|---|
| FastAPI `/docs` 활성 | `TODO` |
| request 모델 Pydantic | `TODO` |
| response 모델 Pydantic | `TODO` |
| health endpoint | `TODO` |
| 구조화 로그: request ID | `TODO` |
| 구조화 로그: model | `TODO` |
| 구조화 로그: tokens | `TODO` |
| 구조화 로그: latency | `TODO` |

## 5.3 사용성

| 요구사항 | 상태 |
|---|---|
| 사용자가 처리 중임을 알 수 있음 | `TODO` |
| 실패 시 다음 행동 안내 | `TODO` |
| 무엇을 입력해야 하는지 화면에서 안내 | `TODO` |
| 정상 경로뿐 아니라 실패 흐름도 UI에서 확인 가능 | `TODO` |

## 5.4 3차 확장을 위한 구조

LLM 호출을 controller/UI에 흩뿌리지 않고 하나의 service layer로 모은다. 이는 점수용 필수 항목은 아니지만 PDF에서 강하게 권장한다.

상태: `TODO`

---

# 6. Langfuse / Evals — 평가축 ④

## 6.1 Observability

모든 LLM 호출에 다음이 trace로 남아야 한다.

| 항목 | 상태 |
|---|---|
| input | `TODO` |
| output | `TODO` |
| model | `TODO` |
| tokens | `TODO` |
| latency | `TODO` |
| cost | `TODO` |
| retry 발생 여부/횟수 | `TODO` |
| `user_id` | `TODO` |
| `session_id` | `TODO` |
| tool/MCP calls | `TODO` |
| prompt version | `TODO` |

제출용 **Langfuse 대시보드 스크린샷 3장 이상**, 그중 **trace 상세 1장**이 필요하다.

상태: `TODO`

## 6.2 Prompt Management

| 요구사항 | 상태 |
|---|---|
| Langfuse Prompt 등록 | `TODO` |
| version 기록 | `TODO` |
| 배포 없이 변경/rollback 시연 | `TODO` |
| trace에서 사용 prompt version 확인 | `TODO` |

## 6.3 Dataset / Evaluation

| 요구사항 | 상태 | 목표 |
|---|---|---|
| Langfuse Dataset **30건 이상** | `TODO` | 9/23까지 초안 확정 |
| 정상 케이스 포함 | `PARTIAL` | 후보만 있음 |
| 경계 케이스 포함 | `PARTIAL` | 후보만 있음 |
| 실패 유도 케이스 포함 | `PARTIAL` | 후보만 있음 |
| 각 건마다 정답 또는 판정 기준 | `TODO` | 작성 필요 |
| 각 판정의 이유 | `TODO` | 작성 필요 |
| 로컬 파일만이 아니라 Langfuse Dataset에 등록 | `TODO` | 구현 후 등록 |
| 도메인 평가축 **2개 이상** 분리 | `TODO` | 예: contract/unsafe/tool/plan 등 |

현재 Candidate A의 초기 10건은 좋은 출발점이지만 필수 30건을 충족하지 않는다.

## 6.4 LLM-as-judge 사용 시

| 요구사항 | 상태 |
|---|---|
| 생성 모델과 judge 모델을 다르게 둠 | `TODO / 선택` |
| judge 호출 trace로 들어갈 수 있음 | `TODO / 선택` |
| judge 판정과 사람 판단의 차이를 검증 | `TODO / 권장` |

LLM-as-judge는 판정 방식 중 하나이며 반드시 써야 하는 것은 아니지만, PDF 평가축은 이를 적극적으로 다룬다.

## 6.5 재측정

| 요구사항 | 상태 |
|---|---|
| baseline 측정 | `TODO` |
| 한 번에 한 요소만 변경 | `TODO` |
| 같은 Dataset으로 두 번째 측정 | `TODO` |
| 회귀한 문항 확인 | `TODO` |
| KEEP / DISCARD 결정 | `TODO` |
| 효과 없었던 시도도 기록 | `TODO` |

## 6.6 비용과 품질 동시 판단

최종 리포트/발표에 아래 표가 필요하다.

```text
model | eval scores by axis | cost/request | p95 latency | selected?
```

그리고 선택 이유를 한 문장으로 설명한다.

상태: `TODO`

## 6.7 필수 운영 지표

| 지표 | 개선 전 | 개선 후 |
|---|---:|---:|
| 평가셋 점수 — 축별 | TODO | TODO |
| 계약 준수율 | TODO | TODO |
| p50 지연 | TODO | TODO |
| p95 지연 | TODO | TODO |
| 요청당 평균 비용 | TODO | TODO |

`EVAL_REPORT.md`에서 이 전후 비교와 실패 분석을 기록한다.

---

# 7. Skill / MCP 요구사항

## Skill

현재 경로:

```text
skills/factory-device-integration/SKILL.md
```

상태: `PASS` **초안 기준**

현재 포함된 내용:

- 도메인 용어
- 지원 범위 / 미지원 범위
- onboarding 판단 순서
- required fields
- write / approval 정책
- retry 원칙
- timeout / `RESULT_UNKNOWN`
- injection 차단 원칙
- Setup / Operator 판단 규칙
- local stop 경계
- human escalation

최종 도메인 경험 검증 결과가 바뀌면 Skill도 함께 수정해야 한다.

## MCP

PDF는 `mcp.server.fastmcp.FastMCP` 사용을 명시적으로 안내한다.

예정 tool:

```text
list_devices()
get_device(device_id)
list_capabilities(device_id)
get_device_status(device_id)
validate_device_spec(spec)
invoke_capability(device_id, capability_id, arguments, approval_token)
```

| 요구사항 | 상태 |
|---|---|
| FastMCP server | `TODO` |
| domain tool 구현 | `TODO` |
| tool description만 읽어도 사용 시점 명확 | `TODO` |
| Streamable HTTP `/mcp` | `TODO` |
| 실제 client 연결 확인 | `TODO` |
| tool 목록 제출 | `TODO` |
| 실제 호출 결과 제출 | `TODO` |
| 접근 제어 방식 README 기록 | `TODO` |
| 연결 스크린샷 | `TODO` |

---

# 8. 금지 / 제한 기술

## 금지

- **LangGraph**
- **RAG**

현재 상태: `PASS`

현재 저장소에는 해당 구현 코드 자체가 없으며, 문서에서 RAG/LangGraph를 이후 프로젝트 영역으로만 언급한다. 앞으로도 구현 의존성에 추가하지 않는다.

### RAG 판정 기준

다음 세 조건이 **모두** 참이면 RAG로 본다.

1. 지식이 문서 chunk 집합으로 저장됨
2. 질문마다 선택되는 chunk가 달라짐
3. 그 chunk를 prompt context에 넣어 생성함

Skill 전체 문서를 고정 prompt에 넣는 것과 MCP로 구조화 API/DB 값을 조회하는 것은 허용된다.

## 허용

- 모델 vendor SDK
- LangChain
- `langchain-mcp-adapters`
- embedding 기반 분류/라우팅/중복 탐지/추천 — 검색 결과를 생성 prompt에 넣는 RAG 구조가 아닌 경우

벤더 SDK를 쓰면 retry, structured output, exception 기본값과 Langfuse trace 가시성을 설명할 수 있어야 한다.

---

# 9. 제출물 체크리스트

| 제출물 | 마감 | 현재 상태 |
|---|---|---|
| **KDT 7기 GitHub org** 팀 repository | 10/8 | `BLOCKED` — 현재 repo는 `nanocode00/factory-agent-hub`; 팀 repo/org 정책 확정 후 이관 필요 |
| `.env.example`, secret 미커밋 | 10/8 | `PASS / 지속검증` |
| Vercel 서비스 URL | 10/8 | `TODO` |
| Cloud Run Agent API URL | 10/8 | `TODO` |
| `GET /health` | 10/8 | `TODO` |
| `POST /api/agent` | 10/8 | `TODO` |
| README — 10분 내 실행 절차 | 10/8 | `TODO` |
| `skills/.../SKILL.md` | 10/8 | `PASS` draft |
| MCP Server + `/mcp` 연결 방법 | 10/8 | `TODO` |
| MCP tool 목록 / 실제 호출 결과 | 10/8 | `TODO` |
| MCP 접근 제어 설명 | 10/8 | `TODO` |
| MCP 연결 스크린샷 | 10/8 | `TODO` |
| `EVAL_REPORT.md` | 10/8 | `TODO` |
| Langfuse 스크린샷 **3장 이상** | 10/8 | `TODO` |
| trace 상세 screenshot **1장 이상** | 10/8 | `TODO` |
| 데모 영상 — 정상 경로 1개 | 10/8 | `TODO` |
| 데모 영상 — 실패 경로 1개 | 10/8 | `TODO` |
| 발표 자료 PDF | 10/11 | `LATER` |
| 발표 | 10/12 | `LATER` |

**10/8 자정 이후 commit은 채점에 반영되지 않는다.** 10/9~11은 코드 수정 기간이 아니라 발표 자료 작성 기간으로 본다.

---

# 10. README 최종 요구

PDF는 README 상단에 특히 다음 세 가지를 요구한다.

| 항목 | 상태 |
|---|---|
| 한 줄 정의 — 누구의 어떤 문제를 어떻게 푸는가 | `PARTIAL` — 현재 한 줄 설명은 있으나 최종 3개월 경험 Gate 후 사용자 문장 확정 필요 |
| 지표 표 — 평가셋 통과율 / p95 / 요청당 비용 | `TODO` |
| 실행 방법 — `docker compose up` | `TODO` |

그 다음에 아키텍처와 데모 자료를 둔다.

추가로 README에 기록해야 할 것:

- Vercel URL
- Cloud Run URL
- `/health`, `/api/agent` 호출 예시
- `/mcp` 연결 방법
- MCP 접근 제어
- CORS / 인증 / frontend secret 노출 방지 방식
- model 선택 근거
- local run 재현 절차
- hardware/edge가 없는 환경의 동작 범위

---

# 11. 일정 Gate

| 날짜 | 요구 결과 | 현재 |
|---|---|---|
| **9/14~9/17** | 후보 3개, 사용자/대안 메모, 문제 정의 초안, eval 후보 10건 | `PARTIAL` |
| **9/18** | 팀 주제/역할/repo 규칙 확정 | `LATER` |
| **9/21~9/23** | 문제·범위, API/output/observability 계약, 30 eval + rubric 확정 | `TODO` |
| **9/24~9/27** | 연휴 — 비동기 조사/setup/prompt experiment | `LATER` |
| **9/28~10/2** | FastAPI/LLM/output contract/Docker/Langfuse 핵심 구현 | `TODO` |
| **9/30** | 문제정의·평가셋·아키텍처·뺀 기능 중간점검 | `LATER` |
| **10/6~10/8** | 실패 분석→prompt/model/logic 한 요소 변경→같은 eval 재측정→report | `TODO` |
| **10/8 24:00** | 코드/배포/리포트 동결 | `LATER` |
| **10/9~10/11** | 코드 수정 없이 발표 준비 | `LATER` |
| **10/12** | 발표 | `LATER` |

---

# 12. 현재 프로젝트에서 이미 강한 부분

아래는 Project2 요구사항과 방향이 잘 맞아 유지한다.

- 자연어 → declarative DeviceSpec / Capability Spec
- 미검증 spec의 실행 금지
- human review / approval
- deterministic validator / executor 경계
- timeout / disconnect / `RESULT_UNKNOWN`
- raw shell / raw serial 직접 실행 금지
- generic MCP discovery/invoke
- Skill에 도메인 규칙을 명시
- 실제 hardware state verification
- 코드/firmware freeze 후 신규 장비 onboarding이라는 반증 가능한 기술 가설

이들은 Project2의 **출력 계약 / 실패 경로 / Domain Skill / MCP / 증거 중심 평가**와 잘 맞는다.

---

# 13. 현재 가장 큰 Gap

현재 repository는 **기획과 안전 경계는 상세하지만 실행 가능한 LLM service는 아직 없는 상태**다.

우선순위는 다음 순서로 고정한다.

1. **3개월 직접 경험 Gate 증명**
2. 9/17 사전기획 후보 3개 완료
3. 최종 사용자/문제 정의 확정
4. 9/23까지 30건 Dataset + rubric 초안 확정
5. API / Pydantic output / failure / observability 계약 확정
6. Vercel + 빈 FastAPI/Cloud Run + Docker skeleton을 먼저 띄움
7. LLM contract / retry / model comparison
8. FastMCP `/mcp` + domain tools
9. Raspberry Pi Edge / 실제 장비 통합
10. Langfuse trace → prompt version 변경 → 동일 eval 재측정 → `EVAL_REPORT.md`

기능 확장은 이 목록이 닫힌 뒤에만 한다.

---

# 14. 문서 통합은 요구사항 정렬 후

현재는 `PROJECT_PLAN.md`, `PROJECT_PLAN.md`, `PROJECT_PLAN.md`, `IMPLEMENTATION_PLAN.md`, `HARDWARE_*` 등이 일부 중복된다.

하지만 **지금은 합치지 않는다.**

먼저 이 체크리스트에서 다음 상태가 되면 문서 통합을 시작한다.

- 주제 Gate `PASS`
- 최종 문제 정의 확정
- 30건 평가셋 구조 확정
- API/output/MCP/observability 계약 확정
- 구현 범위 Must/Cut 확정

그 뒤에 중복을 제거하고 최종 문서 구조를 단순화한다.
