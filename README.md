# Factory Agent Hub

> **자연어로 설명한 새 설비를 검증 가능한 DeviceSpec / Capability Spec으로 변환하고, 사람 검토·실장비 테스트 후 Registry에 등록하여 기존 장비와 함께 발견·실행하는 Agent Platform 실험 프로젝트**

현재 단계는 **검증 준비 / 하드웨어 구매·bring-up 직전**이다. 문서 구조와 테스트베드 계획은 구현 가능한 수준까지 정리되었지만, 고객 Pain·순절감·실장비 성공 결과는 아직 관측되지 않았다. 따라서 **제품 판정은 `INVESTIGATE`를 유지하고, 증거 수집을 위한 기술 검증 prototype은 `PROCEED`한다.**

## What this project is testing

Factory Agent Hub의 핵심 질문은 단순히 “AI로 로봇팔과 컨베이어를 움직일 수 있는가?”가 아니다.

> **이미 지원되는 Serial Adapter와 고정된 장비 protocol 안에서, 플랫폼 코드를 수정하지 않고 새 장비를 자연어 설명 → 검증 → 제한 시험 → 등록의 흐름으로 온보딩하고, 기존 Operator가 다시 발견해 함께 사용할 수 있는가?**

핵심 경계는 다음과 같다.

- 자연어를 임의 Python/Shell/PLC 코드로 바로 실행하지 않는다.
- 자연어 → 선언적 DeviceSpec / Capability Spec → 결정적 validation → 사람 검토 → 제한된 Device Test → Registry 순서로 진행한다.
- 실제 장비 쓰기 동작은 approval, argument/range validation, timeout, audit log를 코드에서 강제한다.
- 장비 실시간 제어와 local stop은 Arduino 등 로컬 제어기가 담당한다.
- MCP는 장비 기능 discovery/invoke 경계이며 안전 검증을 대신하지 않는다.

## Current architecture

```text
Laptop
  Setup Agent / Operator Agent / LLM / Langfuse
        │
        │ Wi-Fi / Ethernet · Streamable HTTP
        ▼
Raspberry Pi 3B+
  Factory Edge Gateway
  ├─ MCP Server
  ├─ Device Registry
  ├─ Validator / Policy
  ├─ Deterministic Executor
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

## Current hardware testbed

2026-09-13 기준 최종 구매안은 다음과 같다.

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

> 제품 가설·Build Gate·prototype 진행 상태는 `PROJECT_PROPOSAL.md`를 따르고, **현재 하드웨어의 source of truth는 `HARDWARE_SPEC.md`와 `HARDWARE_BOM.md`**다.

## Validation status

현재 독립 기획 리뷰의 최종 판정은 **INVESTIGATE**다. 이는 제품 가치 판정이며, 현재 기술 prototype 구현 중단을 의미하지 않는다.

문서로 준비된 것:

- 좁혀진 ICP / JTBD와 반증 가능한 제품 가설
- Pain 조사 Google Form / 응답 Sheet
- 수동 DeviceSpec vs 자연어 초안 비교 활동지
- 하드웨어 테스트베드와 구매 BOM
- 2주 구현 계획과 Hardware Gate
- firmware / protocol / Adapter / schema / prompt freeze 규칙
- timeout, disconnect, approval, result-unknown 등 실패 처리 원칙
- Langfuse 기반 관측·평가 지식 정리

아직 필요한 증거:

- 최근 실제 장비 통합 Pain과 반복 사례
- 자연어 방식의 총 작업시간 절감 여부
- 두 실제 장비의 단독 smoke와 Serial 안정성
- 동일 Serial Adapter / DeviceSpec 계약으로 두 장비를 표현 가능한지
- freeze 이후 코드 수정 없는 신규 장비 온보딩 성공 여부

## Demo target

최종 기술 데모는 다음 흐름을 목표로 한다.

```text
Before
Registry = Conveyor only

Freeze platform + firmware + protocols

Natural-language Robot Arm description
→ Setup Agent draft
→ structural / semantic / safety validation
→ human review
→ limited physical test
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

## Repository guide

| 문서 | 역할 |
|---|---|
| [`PROJECT_PROPOSAL.md`](./PROJECT_PROPOSAL.md) | 제품 가설, ICP/JTBD, Build Gate, prototype 진행 상태, MVP, 안전 경계 |
| [`reviews/proposal-review.md`](./reviews/proposal-review.md) | 독립 기획 리뷰 snapshot과 `INVESTIGATE` 판정 |
| [`HARDWARE_SPEC.md`](./HARDWARE_SPEC.md) | **현재 하드웨어 source of truth** |
| [`HARDWARE_BOM.md`](./HARDWARE_BOM.md) | 구매품 / 보유품 / 조건부 BOM / 현재 비용 |
| [`HARDWARE_PACKING_LIST.md`](./HARDWARE_PACKING_LIST.md) | 집에서 작업 장소로 가져갈 실제 부품 체크리스트 |
| [`IMPLEMENTATION_PLAN.md`](./IMPLEMENTATION_PLAN.md) | 2주 구현 순서, Gate, freeze, demo 계획 |
| [`knowledge/agent-engineering.md`](./knowledge/agent-engineering.md) | Agent / MCP / validation / retry / Langfuse 구현 지식 |
| [`knowledge/planning-review.md`](./knowledge/planning-review.md) | ICP / JTBD / evidence / Build Gate 기획 기준 |
| [`AGENTS.md`](./AGENTS.md) | 이 저장소에서 Agent/Codex가 따라야 할 작업 규칙 |
| [`reviews/history/`](./reviews/history/) | 기획 리뷰 이전 라운드 기록 |

## Immediate next steps

1. 최종 하드웨어 주문
2. 집에서 가져갈 부품을 `HARDWARE_PACKING_LIST.md` 기준으로 선별
3. 배송 대기 중 DeviceSpec schema / Serial Adapter / Registry / MCP skeleton 선행 구현
4. 수령 후 각 장비를 Agent 없이 단독 bring-up
5. Hardware Gate 통과 후 두 firmware / protocol과 플랫폼 경계를 freeze
6. Setup Agent onboarding / Operator 조합 실행 / 실패 회귀 테스트
7. 준비된 A/B 활동지와 Pain 조사로 제품 가치 증거 수집

## Scope

이번 MVP는 **Serial Adapter 1개 + 서로 다른 실제 장비 2개 + 검증 가능한 declarative contract**에 집중한다. Dynamic MCP Tool, PLC 대체, 임의 프로토콜 발명, 복잡한 multi-agent, vision, digital twin, 무인 생산라인 운영은 범위 밖이다.

---

**Current status:** `PRODUCT = INVESTIGATE / TECHNICAL VALIDATION PROTOTYPE = PROCEED`
