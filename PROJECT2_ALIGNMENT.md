# Factory Agent Hub — AI Human 7th Project2 정렬안

> 기준: Checkpoint `2차 프로젝트 — 동작 가능한 버티컬 AGENT 만들기` / 가이드 v3 (2026-09-11)
>
> 이 문서는 기존 Factory Agent Hub 기획을 폐기하지 않고, **교육과정의 필수 제출 구조와 평가 방식에 맞게 무엇을 유지하고 무엇을 바꿔야 하는지**를 정리한 source of truth다.

## 1. 결론

현재 아이디어의 핵심인 **자연어 장비 설명 → 검증 가능한 DeviceSpec → 등록 → MCP로 discovery/invoke → 실제 장비 실행**은 Project2의 `Domain LLM + Skill + MCP Server` 방향과 잘 맞는다.

다만 기존 기획에는 Project2 기준과 충돌하거나 빠진 항목이 있다.

| 항목 | 기존 상태 | Project2 반영 |
|---|---|---|
| 버티컬 도메인 | 소규모 연구실/장비 통합을 ICP 후보로 둠 | 직접 경험 도메인을 **Embedded/IoT Device Integration**으로 좁힌다. Factory는 적용 시나리오이며 제조 현장 경험을 주장하지 않는다. 공개 저장소에서 `nanocode00`의 2024-06-02~09-24 HW-SW 통합 작업을 확인했다. |
| 사용자 UI | CLI/파일만으로도 된다고 봄 | **Vercel / Next.js UI 필수**. 입력·결과·실패 안내를 실제 사용자가 볼 수 있어야 함 |
| Agent API | 로컬 Agent 중심 | **Cloud Run / FastAPI**에 `GET /health`, `POST /api/agent` 제공 |
| MCP | Raspberry Pi의 로컬 경계 중심 | 외부 제출용 **Streamable HTTP `/mcp`**를 제공. `/api/agent`와 역할을 섞지 않음 |
| Docker | 구체 제출 조건 없음 | **`docker compose up` 한 줄로 재현 가능한 패키징** |
| LLM | Setup/Operator Agent 사용 예정 | **LLM API를 핵심 로직에 사용**, Pydantic 출력 계약 + 검증 + 제한 재시도 필수 |
| Skill | 명시적 산출물 없음 | `SKILL.md`에 도메인 규칙·판단 기준·용어·예외 처리 작성 |
| Langfuse | trace/latency/token/cost 관측 예정 | **Tracing + Prompt Management + Evals 세 축 모두 필수** |
| 평가셋 | 실패 케이스 중심 기술 검증 | **30건 이상 Dataset**, prompt/model/logic 변경 전후 같은 평가셋 재측정 |
| 소개 페이지 | 없음 | **별도 소개 페이지** 구성 |
| `.env.example` | 없음 | 필수 추가, 실제 secret 커밋 금지 |
| 일정 | 2주 구현 중심 | 9/14~17 사전기획 → 9/18~23 계약/평가 확정 → 9/28~10/2 핵심 구현 → 10/6~8 재측정/리포트 |

## 2. 가장 먼저 닫아야 하는 Gate — 3개월 도메인 경험

Project2의 첫 체크포인트는 기술이 아니라 다음 질문이다.

> **이 Agent가 다루는 반복 업무를 팀원이 3개월 이상 직접 경험했는가?**

따라서 `Factory`라는 이름이나 제조업 확장 가능성 자체를 경험 근거로 쓰지 않는다. 이번 MVP의 도메인을 더 좁게 정의한다.

### 확정한 직접 경험 도메인

**Embedded/IoT 프로토타이핑 환경에서 센서·액추에이터·외부 장비를 기존 시스템에 연결하고, 통신 규칙·데이터 형식·명령·파라미터·상태 확인 규칙을 맞춰 통합하는 작업**

주 경험 근거는 다음과 같다.

- 경험자: 김재훈
- 공개 기록으로 확인되는 직접 작업 기간: **2024-06-02~2024-09-24, 약 3개월 3주**
- 대표 프로젝트: **webOS Smart Home Gardening** — https://github.com/dudgns128/webos-gardening
- 실제 구성: Raspberry Pi 4 / webOS OSE, Arduino, DHT11, 조도·수위·토양수분 센서, NeoPixel, 물펌프
- 반복 업무: I²C command/data contract 작성, raw sensor data 변환, actuator 제어 연결, 상위 service 통합, 실제 HW timing/API 디버깅
- 과거 프로젝트 통신: **I²C**. Serial 통합 경험으로 과장하지 않는다.
- 대표 commit: `a94a8fc` (I²C HW control), `00e4febe` (timing/parsing fix), `f2e890aa` (dummy→real HW), `ea08aa6a` (HW integration complete)
- 이번 MVP의 **text Serial Adapter는 과거 경험 그 자체가 아니라, 같은 Device Integration 문제를 다른 물리 인터페이스에서 검증하기 위한 구현 선택**이다.

`Factory`는 이 직접 경험을 과장하는 표현으로 사용하지 않는다. Conveyor와 Robot Arm은 **이미 경험한 Device Integration 문제를 재현·검증하는 physical testbed**로 둔다. 제조 공장 운영, PLC/SCADA 통합, 산업용 로봇 운영 경험은 본 프로젝트의 직접 경험 근거로 주장하지 않는다.

## 3. Project2용 한 문장 문제 정의

현재 가설을 Project2 형식으로 줄이면 다음과 같다.

> **새 센서·액추에이터·외부 장비를 프로토타입 시스템에 반복적으로 연결하는 개발자가, 장비마다 통신 방식·데이터·명령·파라미터·상태 확인 규칙을 다시 코드에 옮기고 통합해야 하는 반복 작업을 줄이기 위해, 자연어 장비 설명을 검증 가능한 DeviceSpec으로 만들고 승인된 기능만 기존 Agent가 재사용하도록 한다. 이번 MVP는 그 검증 범위를 문서화된 text Serial 장비로 제한한다.**

아직 Pain과 순절감은 검증 전이므로 제품 효과를 확정적으로 표현하지 않는다.

## 4. Project2 제출 아키텍처

기존 Raspberry Pi Edge Gateway는 유지하되, **서비스 plane과 장비 제어 plane을 분리**한다.

```text
User
  │
  ▼
Vercel / Next.js
  │ HTTPS
  ▼
Cloud Run / FastAPI
  ├─ GET  /health
  ├─ POST /api/agent        # 사용자용 Agent API
  ├─ /mcp                   # Streamable HTTP MCP endpoint
  ├─ Agent Service
  │   ├─ Setup workflow
  │   └─ Operator workflow
  ├─ Pydantic contracts / validator / retry
  ├─ Skill loader
  ├─ Langfuse tracing / prompt / eval
  │
  └─ Edge client
       │ HTTPS + auth
       ▼
Raspberry Pi 3B+ Edge Gateway
  ├─ Device Registry
  ├─ Policy / deterministic executor
  ├─ Serial Adapter
  ├─ Audit Log
  ├─ Arduino #1 → Conveyor
  └─ Arduino #2 → Robot Arm
```

Cloud Run은 USB Serial에 직접 접근할 수 없으므로 실제 장비 실행은 Raspberry Pi가 담당한다. Edge Gateway는 임의 shell/raw serial 실행 API를 열지 않고, 검증된 `capability_id + arguments + spec_version`만 받는다.

개발/데모에서 외부 Cloud Run이 로컬 Pi에 접근해야 할 경우에는 **Pi가 외부로 여는 인증된 HTTPS tunnel**을 사용한다. 구현체는 팀 환경에 맞게 선택하되 URL과 secret을 코드에 하드코딩하지 않는다.

## 5. `/api/agent`와 `/mcp` 역할 분리

### `POST /api/agent`

사용자 UI가 호출하는 서비스 API다.

예상 입력:

```json
{
  "session_id": "...",
  "mode": "setup | operate",
  "message": "...",
  "context": {}
}
```

응답은 자유 문자열만 반환하지 않는다.

```text
AgentResponse
  status
  message
  data
  errors[]
  trace_id
```

### `/mcp`

MCP client가 연결하는 **도메인 tool endpoint**다. 공개 데모 REST API처럼 사용하지 않는다.

초기 tool 후보:

```text
list_devices()
get_device(device_id)
list_capabilities(device_id)
get_device_status(device_id)
validate_device_spec(spec)
invoke_capability(device_id, capability_id, arguments, approval_token)
```

새 장비마다 Tool을 동적으로 생성하지 않는다. Registry와 DeviceSpec이 데이터로 늘어나고 generic tool이 이를 조회/실행한다.

## 6. LLM 출력 계약

Project2에서는 LLM의 문자열 응답을 그대로 실행하지 않는다.

### Setup Agent

```text
DeviceSpecDraftResponse
  status: READY | NEEDS_INFO | REJECTED
  device_spec: DeviceSpec | null
  missing_fields[]
  warnings[]
  user_message
```

### Operator Agent

```text
PlanResponse
  status: READY | NEEDS_APPROVAL | REJECTED
  plan:
    steps[]:
      capability_id
      arguments
      expected_state
  warnings[]
  user_message
```

Pydantic validation 실패 시 제한된 repair retry만 허용한다. 실제 장비 정보 누락, 미지원 protocol, 위험 조건은 재시도로 발명하지 않고 사용자 확인 또는 `REJECTED`로 떨어진다.

## 7. Skill 산출물

루트 또는 `skills/factory-device-integration/SKILL.md`에 다음을 명시한다.

- 도메인 용어: DeviceSpec, Capability, Registry, verified state, result unknown 등
- 장비 onboarding 판단 순서
- 필수 정보와 누락 시 질문 규칙
- read/write와 위험 등급 규칙
- 지원 protocol 경계
- timeout / disconnect / 결과 불명 처리
- approval 무효화 조건
- 미검증 capability 금지
- local stop과 software stop의 차이
- **LLM이 해서는 안 되는 것**: 임의 command/protocol/code 생성, raw shell, 안전 gate 완화

Skill은 도메인 판단 기준이고, MCP는 그 판단에 필요한 데이터/행동 도구라는 역할을 유지한다.

## 8. Langfuse / Evals 완료 정의

Langfuse는 마지막에 로그만 찍는 용도가 아니다.

### Observability

각 `/api/agent` 실행에서 최소 다음을 남긴다.

```text
user_id / session_id
mode
model
prompt_version
input / structured output
validation result
retry count
MCP/tool calls
latency
tokens
cost
final status
error category
```

### Prompt Management

Setup/Operator의 system prompt를 코드 문자열에서 분리한다.

- `setup-agent:v1`
- `operator-agent:v1`
- 변경 후 `v2`

변경 이유를 실패 observation과 연결한다.

### Dataset / Evals

**30건 이상**을 초기에 확정하고, 변경 전후 같은 Dataset으로 재측정한다.

권장 분포:

| 유형 | 최소 후보 |
|---|---:|
| 정상 Setup 설명 | 8 |
| 필수 정보 누락 / 모호함 | 5 |
| 타입·범위 오류 | 4 |
| 명령 주입 / 자유 문자열 위험 | 3 |
| 미지원 protocol / capability | 3 |
| unverified / approval 오류 | 3 |
| Operator 정상 계획 | 2 |
| timeout / disconnect / result-unknown 판단 | 2 |

평가 축 후보:

- output contract pass rate
- required-field recall
- unsafe action rejection rate
- unsupported request rejection rate
- plan validity
- tool-call correctness
- latency
- tokens / cost

최종 `EVAL_REPORT.md`에는 **v1 → 변경 근거 → v2 → 동일 30건 재측정**이 보여야 한다.

## 9. Vercel UI 최소 범위

UI는 화려할 필요가 없지만 실제 서비스 흐름은 보여야 한다.

### 화면 1 — Setup

- 장비 설명 입력
- 부족 정보 질문
- 생성된 DeviceSpec 요약
- validation 상태
- 시험/등록 가능 여부
- 실패 안내

### 화면 2 — Operate

- 사용자 자연어 작업 입력
- Agent가 만든 PlanSpec
- 승인 필요 항목 표시
- 실행 결과 / 장비 상태
- 실패 및 `result unknown` 안내

### 화면 3 — Evidence / About

- 서비스 설명
- 아키텍처
- 지원 범위/안전 경계
- Vercel / Cloud Run / GitHub 링크
- 평가 결과 요약

소개 페이지를 별도 배포하라는 요구와 실제 서비스 UI를 혼동하지 않는다. 필요하면 하나의 Next.js repo에서 `/` 소개, `/app` 서비스를 분리해도 된다.

## 10. Docker / 환경변수

최종 repository는 최소 아래를 목표로 한다.

```text
apps/web/                 # Next.js
services/api/             # FastAPI / Agent API / MCP
edge/                     # Raspberry Pi gateway
skills/.../SKILL.md
experiments/evals/
EVAL_REPORT.md
Dockerfile
docker-compose.yml
.env.example
README.md
```

`docker compose up`으로 최소 API와 로컬 개발용 의존성이 떠야 한다. 실제 physical edge가 연결되지 않은 환경에서는 health에 `edge=unavailable`을 명확히 표시하고, 장비 실행 성공으로 위장하지 않는다.

`.env.example`에는 key 이름만 둔다.

## 11. Project2 실제 일정에 맞춘 실행 순서

| 기간 | 반드시 끝낼 것 |
|---|---|
| **9/14~9/17** | 개인별 문제 후보 3개, 3개월 경험 근거, 사용자/대안 메모, 문제정의 초안, 평가셋 후보 10건 |
| **9/18** | 팀에서 최종 한 문장, 역할, 저장소 규칙 확정 |
| **9/21~9/23** | API 계약, Pydantic output contract, Skill, MCP tool contract, 관측 계약, **평가셋 30건 + rubric** 확정 |
| **9/24~9/27** | 휴일. 각자 환경 setup / prompt experiment / hardware 준비만 병렬 진행 |
| **9/28~10/2** | FastAPI + LLM + contract + Docker + Vercel + Cloud Run + Langfuse trace + MCP + Edge 통합 |
| **9/30 중간점검** | 문제 정의, 평가셋, 아키텍처, **무엇을 빼기로 했는지** 확인 |
| **10/6~10/8** | 실패 trace 분석 → prompt v2 → 동일 eval 재측정 → EVAL_REPORT → 배포/README 정리 |
| **10/8 자정** | 코드 동결 |
| **10/9~10/11** | 코드 수정 없이 발표 자료 작성 |
| **10/12** | 발표 |

기존 `IMPLEMENTATION_PLAN.md`의 Hardware Day 1~14는 **실행 세부 WBS**로 활용하되, 위 교육 일정 안에 재배치한다.

## 12. Scope 조정

### Must

- 3개월 도메인 경험 Gate 통과
- Vercel UI
- Cloud Run FastAPI `GET /health`, `POST /api/agent`
- Streamable HTTP `/mcp`
- LLM API 핵심 사용
- Pydantic contract / validation / retry
- Skill
- Docker / compose
- Langfuse trace + prompt management + evals
- 30+ 평가셋과 변경 전후 재측정
- `.env.example`
- 소개 페이지
- 최소 한 개의 실제 장비 경로 또는 실제 domain tool 결과를 증거로 남김

### Keep from current project

- declarative DeviceSpec / Capability Spec
- human review / approval
- generic MCP discovery/invoke
- deterministic Serial Adapter
- Raspberry Pi + Arduino real hardware
- result-unknown / timeout / disconnect 처리
- 코드 수정 없는 신규 장비 onboarding 가설

### Cut / Later

- 임의 protocol 자동 생성
- PLC/SCADA 대체
- complex multi-agent
- vision / digital twin
- 범용 workflow engine
- 무인 생산라인
- UI polish beyond minimum usability

## 13. 지금 당장 필요한 결정

1. ~~이 도메인의 3개월 이상 직접 경험자 확인~~ → **완료: 김재훈(`nanocode00`), 공개 GitHub 기록 2024-06-02~09-24**
2. 9/17 제출용 개인 후보 3개를 준비
3. 이 아이디어를 유지한다면 사용자 문장을 `factory operator`가 아니라 실제 경험이 있는 **device integration / prototyping workflow**에 맞춰 좁힘
4. 9/23 전에 평가셋 30건을 먼저 확정
5. Cloud Run ↔ Raspberry Pi 연결 방식은 구현 전에 작은 smoke로 검증

이 5개가 닫히기 전에는 하드웨어 기능을 더 늘리지 않는다.
