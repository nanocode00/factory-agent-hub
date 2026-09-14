# Factory Agent Hub

> **새 센서·액추에이터·외부 장비를 프로토타입 시스템에 연결할 때 반복되는 인터페이스 통합 작업을, 검증 가능한 DeviceSpec / Capability Spec과 Agent + MCP 흐름으로 구조화하는 Vertical Agent 실험 프로젝트**

현재 단계는 **AI Human 7th Project2 사전기획(2026-09-14~09-17) + 하드웨어 검증 준비**다. 기존 기술 가설과 테스트베드는 유지하지만, 새로 공개된 Project2 기준에 맞춰 **Vercel UI, Cloud Run/FastAPI, LLM output contract, Skill, Streamable HTTP MCP, Docker, Langfuse 3축, 30+ Evals**를 필수 범위로 반영했다.

> **3개월 경험 Gate: PASS.** 직접 경험 도메인은 **Embedded/IoT Device Integration**이다. `dudgns128/webos-gardening` 공개 기록에서 김재훈(`nanocode00`)의 2024-06-02~09-24 I²C 기반 센서·액추에이터 HW-SW 통합 작업을 확인했다. Factory는 적용 시나리오이며 제조 현장 경험을 주장하지 않는다. 이번 MVP의 text Serial Adapter는 동일한 Device Integration 문제를 검증하기 위한 구현 선택이다.

현재 프로젝트의 기획·범위·경험 근거·Project2 정렬 기준은 [`PROJECT_PLAN.md`](./PROJECT_PLAN.md)를 source of truth로 사용한다.

## What this project is testing

Factory Agent Hub의 핵심 질문은 단순히 “AI로 로봇팔과 컨베이어를 움직일 수 있는가?”가 아니다.

> **이미 지원되는 Serial Adapter와 고정된 장비 protocol 안에서, 플랫폼 코드를 수정하지 않고 새 장비를 자연어 설명 → 구조화 → 검증 → 사람 승인 → 제한 시험 → 등록의 흐름으로 온보딩하고, 기존 Operator가 MCP를 통해 다시 발견해 함께 사용할 수 있는가?**

핵심 경계는 다음과 같다.

- 자연어를 임의 Python/Shell/PLC 코드로 바로 실행하지 않는다.
- 자연어 → Pydantic output contract → DeviceSpec / Capability Spec → 결정적 validation → 사람 검토 → 제한된 Device Test → Registry 순서로 진행한다.
- 실제 장비 쓰기 동작은 approval, argument/range validation, timeout, audit log를 코드에서 강제한다.
- 장비 실시간 제어와 local stop은 Arduino 등 로컬 제어기가 담당한다.
- Skill은 도메인 판단 기준을 제공하고, MCP는 도메인 데이터·행동을 제공한다.
- `/api/agent`와 `/mcp`는 역할을 분리한다.
- “잘 된다”가 아니라 같은 평가셋에서 계약 준수율·실패 경로·지연·토큰·비용을 재측정한다.

## Project2 delivery architecture

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
  ├─ /mcp  (Streamable HTTP)
  ├─ Setup / Operator Agent Service
  ├─ Pydantic contracts / validation / retry
  ├─ Skill
  ├─ Langfuse tracing / prompt management / evals
  │
  └─ authenticated Edge client
       │
       ▼
Raspberry Pi 3B+ Edge Gateway
  ├─ Device Registry
  ├─ Policy / Deterministic Executor
  ├─ Serial Adapter
  ├─ SQLite / Audit Log
  │
  ├─ USB Serial → Arduino #1 → DRV8833 → Conveyor
  │                           ├─ IR sensor
  │                           └─ local stop
  │
  └─ USB Serial → Arduino #2 → 4-DOF Robot Arm
                              ├─ Servo ×4
                              └─ local stop
```

Cloud Run은 USB Serial에 직접 접근할 수 없으므로 physical device execution은 Raspberry Pi Edge Gateway가 담당한다. Cloud Run에서 Pi에 접근할 때는 인증된 HTTPS edge endpoint/tunnel을 사용하고, 임의 raw shell/serial API는 열지 않는다.

## Required Project2 evidence

최종 제출에서 최소 다음을 증거로 남긴다.

| 층 | 역할 | 증거 |
|---|---|---|
| Vercel / Next.js | 실제 사용자 입력·결과·실패 안내 | Vercel URL + 정상/실패 사용자 흐름 |
| Cloud Run / FastAPI | Agent 실행 + output contract + validation/retry | Cloud Run URL + `GET /health` + `POST /api/agent` |
| MCP Server | 도메인 데이터/행동 tool 제공 | `/mcp` 연결 방법 + tool 목록 + 실제 호출 결과 |
| Docker | 재현 가능한 실행 | Dockerfile + `docker compose up` |
| Skill | 도메인 규칙·판단·예외 처리 | `skills/factory-device-integration/SKILL.md` |
| Langfuse | trace → prompt version → 같은 eval 재측정 | trace + prompt v1/v2 + `EVAL_REPORT.md` |
| Evals | 30건 이상 회귀 측정 | Dataset + rubric + 변경 전후 score |
| Repo hygiene | 재현/보안 | `.env.example`, secret 미커밋, README |
| Intro page | 서비스 소개 | 별도 소개 페이지 URL |

## Current hardware testbed

2026-09-13 기준 구매안은 다음과 같다.

| 구분 | 선택 |
|---|---|
| Conveyor | 리브온 창의력 STEAM 목재 컨베이어 벨트 |
| Conveyor driver | DRV8833 `VLT-MD012` |
| Robot Arm | 이엘사이언스 Arduino 집게 로봇팔 4관절 |
| Robot servo power | 5V 5A regulated adapter + C7 cable + 5.5×2.1 terminal |
| Edge Gateway | Raspberry Pi 3B+ |
| Device controllers | Arduino Uno ×2 (+ spare 1 권장) |
| Object sensor | IR proximity sensor |
| Local stop | 동발보 `MSL-1C2P(중)-4mm` 3PIN / 1C2T slide switch ×2 |

local stop은 저전압 **logic input**으로 사용한다. 모터/servo 전원을 직접 차단하는 산업용 emergency stop이 아니며, Arduino firmware가 STOP 상태를 최우선으로 처리한다.

현재 장바구니 기준 구매 예정 총액은 약 **70,630원**이며 실제 결제 시 가격·배송비는 달라질 수 있다.

> 제품 가설·범위·Build Gate·Project2 정렬은 `PROJECT_PLAN.md`를 따르고, **현재 하드웨어의 source of truth는 `HARDWARE_SPEC.md`와 `HARDWARE_BOM.md`**다.

## Validation status

현재 독립 기획 리뷰의 제품 판정은 **INVESTIGATE**다. 이는 제품 가치 판정이며, 기술 prototype 구현 중단을 의미하지 않는다.

문서로 준비된 것:

- Embedded/IoT Device Integration으로 좁힌 직접 경험 도메인 정의
- `PROJECT_PLAN.md`에 2024-06-02~09-24 공개 GitHub 기록과 반복 통합 사례를 근거로 3개월 경험 Gate 정리
- 좁혀진 ICP / JTBD와 반증 가능한 제품 가설
- Pain 조사 Google Form / 응답 Sheet
- 수동 DeviceSpec vs 자연어 초안 비교 활동지
- 하드웨어 테스트베드와 구매 BOM
- Hardware Gate와 freeze 규칙
- timeout, disconnect, approval, result-unknown 등 실패 처리 원칙
- Project2 요구사항 정렬 문서
- 9/14~17 사전기획 문서
- `.env.example`

아직 필요한 증거:

- ~~3개월 경험 Gate 증빙~~ → **PASS: 실제 commit 링크와 반복 사례 정리 완료**
- 최근 실제 장비 통합 Pain과 반복 사례
- 자연어 방식의 총 작업시간 절감 여부
- 두 실제 장비의 단독 smoke와 Serial 안정성
- 동일 Serial Adapter / DeviceSpec 계약으로 두 장비를 표현 가능한지
- Vercel / Cloud Run / `/mcp` 실제 배포
- Pydantic contract validation / retry 결과
- Langfuse trace, Prompt Management v1→v2, 30+ Dataset 재측정
- freeze 이후 코드 수정 없는 신규 장비 온보딩 성공 여부

## Demo target

최종 기술 데모는 다음 흐름을 목표로 한다.

```text
Before
Registry = Conveyor only

Freeze platform + firmware + protocols

User → Vercel
→ POST /api/agent
→ Setup Agent structured output
→ DeviceSpec draft
→ structural / semantic / safety validation
→ human review
→ limited physical test via Edge Gateway
→ active Registry

After
Registry = Conveyor + Robot Arm

Same Operator / Same MCP / Same Adapter
→ discover both devices
→ approved finite PlanSpec
→ physical execution
→ state verification + audit log
```

예시 상위 시나리오는 `물체 감지 → Conveyor HALT → Robot pick/place → 상태 확인 → Conveyor 재가동`이다.

## Evaluation target

평가셋은 9/23 전 **30건 이상**으로 확정하고 변경 전후 같은 Dataset을 다시 측정한다.

초기 분포 후보:

- 정상 Setup
- 필수 정보 누락 / 모호함
- 타입·범위 오류
- command injection 성격 입력
- 미지원 protocol / capability
- unverified / approval 오류
- 정상 Operator Plan
- timeout / disconnect / result-unknown 판단

주요 지표는 output contract pass rate, unsafe action rejection, unsupported request rejection, plan validity, tool-call correctness, latency, tokens, cost다.

## Repository guide

| 문서 | 역할 |
|---|---|
| [`REQUIREMENTS_CHECKLIST.md`](./REQUIREMENTS_CHECKLIST.md) | **Project2 요구사항 충족 상태 체크리스트** |
| [`PROJECT_PLAN.md`](./PROJECT_PLAN.md) | **프로젝트 기획, 직접 경험 근거, ICP/JTBD, 범위, 아키텍처, 안전 경계, 평가 계획 source of truth** |
| [`reviews/proposal-review.md`](./reviews/proposal-review.md) | 독립 기획 리뷰 snapshot과 `INVESTIGATE` 판정 |
| [`HARDWARE_SPEC.md`](./HARDWARE_SPEC.md) | **현재 하드웨어 source of truth** |
| [`HARDWARE_BOM.md`](./HARDWARE_BOM.md) | 구매품 / 보유품 / 조건부 BOM / 현재 비용 |
| [`HARDWARE_PACKING_LIST.md`](./HARDWARE_PACKING_LIST.md) | 집에서 작업 장소로 가져갈 실제 부품 체크리스트 |
| [`IMPLEMENTATION_PLAN.md`](./IMPLEMENTATION_PLAN.md) | 하드웨어/Edge 중심 상세 WBS |
| [`knowledge/agent-engineering.md`](./knowledge/agent-engineering.md) | Agent / MCP / validation / retry / Langfuse 구현 지식 |
| [`knowledge/planning-review.md`](./knowledge/planning-review.md) | ICP / JTBD / evidence / Build Gate 기획 기준 |
| [`AGENTS.md`](./AGENTS.md) | 이 저장소에서 Agent/Codex가 따라야 할 작업 규칙 |
| [`reviews/history/`](./reviews/history/) | 기획 리뷰 이전 라운드 기록 |

## Immediate next steps

1. ~~기획 문서와 3개월 경험 근거 정리~~ → **완료: `PROJECT_PLAN.md`로 통합**
2. 9/17까지 개인 문제 후보 3개와 후보별 사용자/대안/평가 입력 10건을 준비한다.
3. Candidate A가 최종 선택되면 9/23까지 API/output/Skill/MCP/관측 계약과 30건 평가셋을 freeze한다.
4. 하드웨어 수령 후 각 장비를 Agent 없이 단독 bring-up한다.
5. 동시에 Vercel / FastAPI / Docker / Langfuse skeleton을 만든다.
6. Cloud Run ↔ Raspberry Pi edge 연결을 작은 smoke로 먼저 검증한다.
7. 실패 observation을 근거로 Prompt v1→v2를 바꾸고 같은 Dataset을 재측정한다.
8. 10/8 자정에 코드 동결하고 10/9~11은 발표 자료만 만든다.

## Scope

이번 MVP는 **Serial Adapter 1개 + 서로 다른 실제 장비 2개 + 검증 가능한 declarative contract + Project2 운영 증거**에 집중한다. Dynamic MCP Tool, PLC 대체, 임의 프로토콜 발명, 복잡한 multi-agent, vision, digital twin, 무인 생산라인 운영은 범위 밖이다.

---

**Current status:** `PROJECT2 PRE-PLANNING / DOMAIN EXPERIENCE = PASS / PRODUCT = INVESTIGATE / TECHNICAL VALIDATION PROTOTYPE = PROCEED`
