# Factory Agent Hub — Project Plan

> AI Human 7th Project2 기준으로 정리한 현재 프로젝트의 **기획·범위·아키텍처·검증 계획 source of truth**다.
>
> 공식 요구사항 원문은 `requirements/`, 요구사항 충족 상태는 `REQUIREMENTS_CHECKLIST.md`, 구현 세부 WBS는 `IMPLEMENTATION_PLAN.md`, 하드웨어 상세는 `HARDWARE_*.md`를 따른다.

## 1. 현재 결론

Factory Agent Hub는 **Embedded/IoT Device Integration**에서 반복되는 HW-SW 인터페이스 통합 작업을 줄이는 Vertical Agent를 검증한다.

핵심 가설은 다음과 같다.

> **새 센서·액추에이터·외부 장비를 기존 프로토타입 시스템에 붙일 때, 사람이 장비 문서에서 통신 방식·데이터·명령·파라미터·상태 확인 규칙을 다시 코드에 옮기고 기존 흐름을 수정하는 반복 작업을 줄일 수 있는가?**

사용자는 장비 정보를 자연어로 제공하고, Setup Agent는 이를 검증 가능한 `DeviceSpec / Capability Spec` 초안으로 구조화한다. 결정적 검증, 사람 검토, 제한된 실제 장비 시험을 통과한 기능만 Registry에 등록한다. Operator Agent는 MCP를 통해 등록된 기능만 발견·조합한다.

현재 상태는 다음과 같다.

- **Domain experience:** `PASS`
- **Product evidence:** `INVESTIGATE`
- **Technical validation prototype:** `PROCEED`
- **Factory Automation 실무 경험을 주장하지 않음**
- Conveyor / Robot Arm은 제품 도메인의 근거가 아니라 **physical testbed**임

## 2. 직접 경험 도메인과 3개월 Gate

### 직접 경험 도메인

**Embedded/IoT 프로토타이핑 환경에서 센서·액추에이터·외부 장비를 기존 시스템에 연결하고, 통신 규칙·데이터 형식·제어 인터페이스를 맞춰 통합하는 작업**

### 공개 증빙

경험자: 김재훈 (`nanocode00`)

공개 GitHub 기록으로 확인되는 직접 작업 기간은 **2024-06-02 ~ 2024-09-24, 약 3개월 3주**다.

대표 프로젝트:
- https://github.com/dudgns128/webos-gardening

실제 구성:
- Raspberry Pi 4 / webOS OSE
- Arduino
- DHT11
- 조도 센서
- 수위 센서
- 토양수분 센서
- NeoPixel
- 물펌프

실제 통신은 **Raspberry Pi(webOS) ↔ Arduino I²C**였다. 과거 경험을 Serial 경험으로 표현하지 않는다.

대표 commit:

1. I²C HW control 초기 통합 — 2024-06-02  
   https://github.com/dudgns128/webos-gardening/commit/a94a8fc01c9fc60d4263d4866e30fbeceb8e0a0e
2. 실장비 통신 timing / parsing 수정 — 2024-06-02  
   https://github.com/dudgns128/webos-gardening/commit/00e4febe4ae07d85350d39854b97256db8e53eac
3. dummy data → 실제 HW 데이터·제어 연결 — 2024-06-12  
   https://github.com/dudgns128/webos-gardening/commit/f2e890aab82d9b97055d717fa665fe1ec10bfb04
4. 실장비 연동 오류 수정 및 HW 제어 완성 — 2024-06-12  
   https://github.com/dudgns128/webos-gardening/commit/ea08aa6a93d63a9cf5e9e7fd43b7947137a95057
5. 프로젝트 후속 참여 기록 — 2024-09-24  
   https://github.com/dudgns128/webos-gardening/commit/5fa0831b9bac76b405b4d273a93da104a9ca450e

반복 사례:
- 여러 센서의 raw 값을 하나의 I²C payload 규칙으로 묶고 상위 서비스에서 의미 있는 값으로 변환했다.
- NeoPixel과 펌프를 command + argument 형태의 제어 규칙으로 정의해 기존 자동화 로직과 연결했다.
- mock/dummy 단계에서는 드러나지 않았던 read timing, callback, parameter/payload 형식 문제를 실제 장비에서 수정했다.

따라서 이번 프로젝트의 경험 근거는 **장비 통합 업무 자체**다. 이번 MVP의 text Serial Adapter는 같은 문제를 다른 인터페이스에서 검증하기 위한 구현 선택이다.

## 3. 사용자와 반복 업무

### 첫 사용자 가설

전담 자동화 팀 없이, 문서화된 장비를 프로토타입/실험 환경에 추가하거나 교체하는 **장비 통합 개발자**를 첫 사용자로 둔다.

이 사용자는 다음을 할 수 있어야 한다.
- 장비 문서와 기존 예제를 읽을 수 있음
- 연결 설정과 명령 의미를 확인할 수 있음
- 실제 장비 smoke test를 수행할 수 있음
- 최종 명세와 위험 동작을 검토할 책임이 있음

비전문가가 아무 정보 없이 장비를 연결하는 문제는 다루지 않는다.

### JTBD

> 새 장비가 들어왔을 때, 장비의 데이터·제어 인터페이스를 기존 시스템에 연결하고 검증 기록을 남겨 다음 실험/작업을 시작한다.

현재 반복 흐름:

```text
장비 문서 확인
→ 배선/연결 확인
→ 데이터·명령·파라미터 규칙 정리
→ 기존 코드/설정 수정
→ 상태 확인 규칙 연결
→ 실제 장비 테스트
→ 오류 수정
→ 기존 workflow에 기능 연결
```

Agent가 줄이려는 구간은 **명세 초안 작성, 누락/충돌 확인, 기존 Registry/MCP 흐름에 기능을 연결하는 작업**이다.

다음은 사라진다고 주장하지 않는다.
- 물리 배선
- 새 드라이버/프로토콜 구현
- 기구 보정
- 실제 장비 시험
- 사람의 안전 검토

## 4. 제품 가설과 현재 증거

현재 제품 판정은 `INVESTIGATE`다. 기술 prototype을 구현하는 것과 제품 가치가 검증된 것은 별개다.

### 확인된 것

- 3개월 이상 Device Integration 직접 경험 근거가 존재한다.
- 자연어 → 선언적 명세 → 검증 → 등록 → MCP discovery/invoke 구조를 기술적으로 검증할 테스트베드를 정했다.
- Pain 조사 Form/응답 Sheet와 수동 명세 vs 자연어 초안 비교 활동지가 준비되어 있다.
- Conveyor / Robot Arm / Raspberry Pi / Arduino 중심의 physical testbed와 구매안이 정리돼 있다.
- 실패 처리 원칙과 안전 경계를 문서화했다.

### 아직 확인되지 않은 것

- 최근 사용자에게 이 업무가 실제로 큰 Pain인지
- 명세 작성/연동 단계가 전체 통합 시간에서 큰 비중인지
- 자연어 초안이 수동 명세보다 **총 작업시간**을 줄이는지
- 두 실제 장비를 동일 Serial Adapter / DeviceSpec 계약으로 표현 가능한지
- platform/schema/prompt/firmware 변경 없이 두 번째 장비 온보딩을 재현할 수 있는지
- 모델/API 비용까지 포함했을 때 순이익이 있는지

### 주요 검증 가설

| 가설 | 실패하면 | 검증 |
|---|---|---|
| 명세 작성·기존 작업 연동이 반복 비용의 의미 있는 비중이다 | 핵심 고객 가치 약화 | 최근 실제 사례와 단계별 시간 수집 |
| 자연어 초안이 검토·수정·테스트까지 포함해 총시간을 줄인다 | 기존 폼/스크립트 대비 이점 약화 | 수동 vs 자연어 방식 비교 |
| 고정 Adapter + declarative contract가 서로 다른 장비를 표현한다 | 코드 무수정 온보딩 가설 실패 | 두 실제 장비에 동일 계약 적용 |
| 담당자가 명령·범위·시험 조건을 검토할 수 있다 | 안전한 검증 불가 | 문서/firmware와 명세 대조 |
| 초반에 하드웨어 경로를 안정화할 수 있다 | 일정 위험 | 단독 bring-up 및 Hardware Gate |

## 5. 해결 방식

### Setup workflow

```text
자연어 장비 설명 / 문서화된 protocol 정보
→ Setup Agent
→ DeviceSpec / Capability Spec draft
→ Structural Validation
→ Semantic / Safety Validation
→ Human Review
→ 제한된 Device Test
→ Active Registry
```

Setup Agent는 정보가 없으면 추측하지 않는다.

```text
DeviceSpecDraftResponse
  status: READY | NEEDS_INFO | REJECTED
  device_spec: DeviceSpec | null
  missing_fields[]
  warnings[]
  user_message
```

### Operator workflow

```text
자연어 작업 요청
→ Operator Agent
→ MCP Registry/Capability Discovery
→ PlanSpec draft
→ Validator / Policy Gate
→ Human Approval
→ Deterministic Executor
→ Edge Gateway / Device Adapter
→ 실제 장비
→ 상태 확인 / Audit Log
```

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

LLM 출력은 문자열 그대로 실행하지 않는다. Pydantic validation 실패 시 제한된 repair retry만 허용한다.

## 6. 지원 범위

이번 MVP는 **문서화된 text Serial 장비**로 범위를 제한한다.

포함:
- 미리 구현된 Serial Adapter 1개
- 허용 command token과 typed parameter
- 결정적으로 해석 가능한 상태 응답
- DeviceSpec / Capability Spec
- Registry
- generic MCP discovery/invoke
- 사람 검토/승인
- 제한 실제 시험
- Raspberry Pi Edge Gateway
- Arduino 기반 실제 장비 2개

제외:
- 임의 Python/Shell 실행
- LLM이 protocol/code를 새로 생성해 즉시 실행
- 바이너리 독자 protocol 자동 지원
- PLC/SCADA 대체
- 산업용 safety controller 대체
- 동적 MCP Tool 생성
- 복잡한 multi-agent 협상
- vision / digital twin
- 무인 생산라인 운영

### 코드 수정 없는 온보딩의 의미

평가 전 다음을 먼저 완성하고 freeze한다.
- Setup/Operator 코드
- system prompt / examples
- Pydantic schema
- MCP server
- Registry contract
- validator / executor
- Serial Adapter
- 테스트베드 firmware
- 장비 protocol

그 이후 두 번째 장비 온보딩에서 바꿀 수 있는 것은 사용자 설명, 검토 대상 DeviceSpec/Capability Spec, 승인·시험·Registry 데이터다.

새 장비 때문에 위 freeze 대상이 바뀌면 **코드 수정 없는 온보딩 실패**로 기록한다.

## 7. Project2 서비스 아키텍처

```text
User
  │
  ▼
Vercel / Next.js
  │ HTTPS
  ▼
Cloud Run / FastAPI
  ├─ GET  /health
  ├─ POST /api/agent
  ├─ /mcp                 # Streamable HTTP MCP
  ├─ Setup / Operator workflow
  ├─ Pydantic contracts / validator / retry
  ├─ Skill loader
  ├─ Langfuse tracing / prompt / eval
  │
  └─ authenticated edge client
       │ HTTPS
       ▼
Raspberry Pi 3B+ Edge Gateway
  ├─ Device Registry
  ├─ Policy / deterministic executor
  ├─ Serial Adapter
  ├─ Audit Log
  ├─ Arduino #1 → Conveyor
  └─ Arduino #2 → Robot Arm
```

Cloud Run은 로컬 USB Serial에 직접 접근하지 않는다. 실제 장비 실행은 Pi가 담당한다.

Cloud Run ↔ Pi 연결은 인증된 HTTPS 경로를 사용한다. URL/token을 코드에 하드코딩하지 않는다.

### `/api/agent`와 `/mcp` 경계

`POST /api/agent`
- 사용자 UI용 서비스 API
- 자연어 입력
- Agent orchestration
- 구조화 응답과 `trace_id`

`/mcp`
- Agent/MCP client가 사용하는 domain tool endpoint
- Registry 조회와 검증된 capability 실행
- 공개 demo REST API 역할을 대신하지 않음

초기 MCP tool:

```text
list_devices()
get_device(device_id)
list_capabilities(device_id)
get_device_status(device_id)
validate_device_spec(spec)
invoke_capability(device_id, capability_id, arguments, approval_token)
```

## 8. Safety / HITL

이번 프로젝트의 안전 주장은 **교육용 prototype의 제어 경계**에 한정한다.

- 미검증 draft는 실행하지 않는다.
- write action은 대상, spec version, arguments, plan에 묶인 승인이 필요하다.
- spec/plan 변경 시 기존 승인을 무효화한다.
- argument type/range를 executor에서 다시 검증한다.
- command template에 자유 문자열·복수 명령·개행 주입을 허용하지 않는다.
- timeout / 응답 유실은 `RESULT_UNKNOWN`으로 처리한다.
- write timeout 후 자동 재전송하지 않는다.
- 실제 상태 확인 전 후속 동작을 중단한다.
- stable operation key / audit log로 중복 실행을 방지한다.
- local stop은 Agent/MCP 요청보다 우선한다.

현재 local stop은 Arduino가 읽는 **logic-level stop input**이다. 산업용 E-stop이나 독립 안전회로가 아니다.

실시간 motor/servo 제어와 stop/interlock은 LLM이 담당하지 않는다.

## 9. 테스트베드

현재 테스트베드:

| 역할 | 선택 |
|---|---|
| Conveyor | 리브온 창의력 STEAM 목재 컨베이어 |
| Conveyor driver | DRV8833 `VLT-MD012` |
| Robot Arm | 이엘사이언스 Arduino 4관절 집게 로봇팔 |
| Robot servo power | 5V 5A regulated adapter |
| Edge Gateway | Raspberry Pi 3B+ |
| Device controller | Arduino Uno ×2 |
| Object sensor | IR proximity sensor |
| Local stop | `MSL-1C2P(중)-4mm` slide switch ×2 |

하드웨어 상세와 구매/포장 정보는 `HARDWARE_SPEC.md`, `HARDWARE_BOM.md`, `HARDWARE_PACKING_LIST.md`를 따른다.

## 10. 평가 계획

### Project2 필수 평가

- Langfuse tracing
- Prompt Management
- Dataset 30건 이상
- 동일 Dataset 변경 전/후 재측정
- LLM-as-judge 포함 평가
- output contract 준수율 측정
- 실패 경로 측정
- latency / tokens / cost 측정
- 최소 2개 모델 동일 조건 비교

초기 평가 분포:

| 유형 | 후보 수 |
|---|---:|
| 정상 Setup | 8 |
| 필수 정보 누락 / 모호함 | 5 |
| 타입·범위 오류 | 4 |
| injection / 위험 자유 문자열 | 3 |
| 미지원 protocol / capability | 3 |
| unverified / approval 오류 | 3 |
| 정상 Operator plan | 2 |
| timeout / disconnect / result unknown | 2 |

초기 대표 케이스:
1. 완전한 Conveyor 설명 → valid DeviceSpec
2. 완전한 Robot Arm 설명 → valid DeviceSpec
3. baudrate 누락 → `NEEDS_INFO`
4. response rule 누락 → `NEEDS_INFO`
5. joint range 모호 → 질문
6. command injection → 거부
7. 미지원 binary protocol → 거부
8. unverified capability invoke → 장비 전송 없이 거부
9. write timeout → 자동 retry 없이 `RESULT_UNKNOWN`
10. 두 등록 장비 조합 → valid PlanSpec

주요 metric:
- output contract pass rate
- required-field recall
- unsafe action rejection rate
- unsupported request rejection rate
- plan validity
- tool-call correctness
- latency
- tokens
- cost

최종 `EVAL_REPORT.md`는 다음 흐름을 보여야 한다.

```text
baseline / prompt v1
→ 실패 observation
→ 변경 근거
→ prompt/model/logic v2
→ 같은 Dataset 재측정
→ 비교 결과
```

## 11. UI / 제출 범위

Vercel UI 최소 화면:

### Setup
- 장비 설명 입력
- 부족 정보 질문
- DeviceSpec 요약
- validation 상태
- 시험/등록 가능 여부
- 실패 안내

### Operate
- 자연어 작업 입력
- PlanSpec
- 승인 필요 항목
- 실행 결과/장비 상태
- `RESULT_UNKNOWN` 포함 실패 안내

### Evidence / About
- 문제 정의
- 아키텍처
- 지원 범위와 안전 경계
- Vercel / Cloud Run / GitHub 링크
- 평가 결과 요약

Cloud Run/FastAPI:
- `GET /health`
- `POST /api/agent`
- `/mcp`
- `/docs`
- 구조화 로그

Docker:
- `docker compose up` 한 줄로 로컬 재현 가능

Langfuse:
- input/output
- model
- prompt version
- tokens
- latency
- cost
- user/session id
- validation/retry/tool call/final status/error category

## 12. 일정

| 기간 | 목표 |
|---|---|
| 09/14–09/17 | 문제/경험 근거/평가 입력 정리 |
| 09/18–09/23 | 문제 정의 + API/output/Skill/MCP/관측 계약 + 30건 평가셋 freeze |
| 09/28–10/02 | FastAPI + LLM + Docker + Vercel + Cloud Run + Langfuse + MCP + Edge 통합 |
| 10/06–10/08 | 실패 분석 → 개선 → 동일 Dataset 재측정 → EVAL_REPORT / README 정리 |
| 10/08 자정 | 코드 동결 |
| 10/09–10/11 | 발표 자료 작성 |
| 10/12 | 발표 |

세부 구현 WBS는 `IMPLEMENTATION_PLAN.md`를 따른다.

## 13. 현재 우선순위

1. 프로젝트 문서 중복 제거 및 source of truth 정리
2. 최근 실제 Device Integration Pain / 현재 대안 증거 보강
3. 30건 평가셋과 rubric 확정
4. 두 실제 장비 단독 bring-up
5. Serial protocol / DeviceSpec contract freeze
6. FastAPI / Docker / Vercel / Langfuse skeleton 구현
7. MCP + Edge 실제 통합
8. baseline 측정 → 실패 분석 → 개선 → 재측정

## 14. 문서 운영 원칙

- `requirements/` — 공식 원문. 수정하지 않는다.
- `REQUIREMENTS_CHECKLIST.md` — 요구사항 충족 여부만 기록한다.
- `PROJECT_PLAN.md` — 제품/프로젝트 기획과 현재 결정의 source of truth.
- `IMPLEMENTATION_PLAN.md` — 구현 순서와 작업 WBS.
- `HARDWARE_*.md` — 하드웨어 상세.
- `skills/` — 도메인 Skill.
- `knowledge/` — 참고 지식.
- `reviews/` — 과거 검토와 기록.

문서가 충돌하면 위 우선순위를 따른다.
