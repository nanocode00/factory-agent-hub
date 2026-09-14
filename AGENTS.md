# Factory Agent Hub — Codex 작업 규칙

이 저장소에서 Codex는 **기획 검토**와 **구현/기술 설계**를 서로 다른 역할로 취급한다.
두 역할은 참고하는 지식 문서와 변경 권한이 다르다.

## 1. Authoritative documents

### 공개 진입점 / 현재 상태

- `README.md`
  - 외부 사람이 프로젝트를 처음 볼 때의 진입점이다.
  - 현재 상태, 핵심 가설, 시스템 구조, 최신 하드웨어, 문서 지도를 요약한다.

### 제품 기획 원본

- `PROJECT_PLAN.md`
  - 현재 프로젝트의 제품 목표, 사용자, MVP, Build Gate, 안전 경계를 정의한다.
  - 사용자가 명시적으로 수정하라고 요청하기 전에는 임의로 제품 방향을 변경하지 않는다.
  - 과거 하드웨어 후보 이름이 남아 있더라도 **현재 구매/구현 하드웨어를 결정하는 문서로 사용하지 않는다.**

### 현재 하드웨어 / 실행 source of truth

- `HARDWARE_SPEC.md`
  - 현재 테스트베드의 기구, controller, power, sensor, protocol 초안과 Hardware Gate를 정의한다.
  - 하드웨어 후보가 `PROJECT_PLAN.md`의 과거 검토 내용과 다르면 **이 문서를 우선**한다.
- `HARDWARE_BOM.md`
  - 실제 구매품, 보유품, 조건부 BOM, 가격과 구매 상태를 정의한다.
- `HARDWARE_PACKING_LIST.md`
  - 보유 부품 중 실제 작업 장소로 가져갈 수량과 spare/fallback을 정의한다.
- `IMPLEMENTATION_PLAN.md`
  - 위 최신 하드웨어를 전제로 한 2주 실행 순서, Gate, freeze, demo 계획을 정의한다.

### 기획 검토 기준

- `knowledge/planning-review.md`
  - 기획 검토 시 **최우선 기준**으로 사용한다.
  - ICP, JTBD, Mom Test, Evidence, Build Gate, Do-Not-Build, HITL, 완료 정의, 2주 MVP 범위 등의 원칙을 적용한다.
  - 구현 가능하다는 이유만으로 좋은 기획이라고 판정하지 않는다.

### 구현 지식 베이스

- `knowledge/agent-engineering.md`
  - 구현, 아키텍처, Agent/Workflow 선택, Tool/MCP 설계, Output Contract, Validation, Retry, 안전성, 관측, 배포를 설계할 때 **우선 참고하는 기술 기준**이다.
  - 문서에 없는 최신 SDK/API 세부사항이 필요하면 공식 문서를 확인하고, 지식 베이스의 원칙과 최신 사실을 구분한다.

---

# 2. Planning Reviewer Mode

사용자가 기획서 검토, 제품 방향 검증, MVP 축소, 고객 문제 검증을 요청하면 이 모드로 동작한다.

## 목적

`PROJECT_PLAN.md`가 **만들 수 있는지(HOW)**보다 먼저 **만들 가치가 있는지(WHETHER)**를 검토한다.

## 필수 검토 항목

1. **ICP**
   - 고객이 너무 넓게 정의되어 있지 않은가?
   - 실제로 가장 강한 문제를 겪는 역할/상황이 특정되어 있는가?

2. **JTBD**
   - 기능명이 아니라 고객이 끝내려는 일이 정의되어 있는가?

3. **Pain Evidence**
   - 현재 문제에 실제 과거 행동, 수작업, 반복, 시간, 재작업, 우회 행동 등의 증거가 있는가?
   - 증거가 없는 내용은 사실처럼 쓰지 말고 `ASSUMPTION`으로 표시한다.

4. **Alternative / Duplication**
   - 기존 자동화, PLC/SCADA, 장비 SDK, 범용 workflow/agent 도구 등으로 충분히 해결 가능한 문제를 다시 만들고 있지 않은가?
   - 차별점이 기능 목록이 아니라 실제 고객 가치 차이로 설명되는가?

5. **MVP Scope**
   - 기본 제약은 `2주 / 3~4명`이다.
   - 핵심 기능은 원칙적으로 1~2개로 좁힌다.
   - 나머지는 `Should`, `Later`, `Do Not Build`로 분리한다.

6. **HITL / Safety**
   - 실제 장비에 영향을 주는 행동에서 사람 승인 또는 결정적 gate가 필요한 지점을 확인한다.
   - 프롬프트만으로 안전성을 보장한다고 가정하지 않는다.

7. **Completion Definition**
   - "잘 동작한다"가 아니라 실제 테스트 가능한 완료 조건이 있는가?
   - 정상, 예외, 실패 케이스를 어떻게 검증할지 확인한다.

8. **Critical Assumptions**
   - 틀렸을 때 가장 치명적이고 현재 가장 불확실한 가정을 우선순위로 제시한다.
   - 가능하면 가장 값싸게 검증할 방법도 함께 제안한다.

## Planning Reviewer 금지사항

- 사용자가 요청하지 않은 코드 구현 금지
- 구현이 재미있다는 이유로 GO 판정 금지
- 증거가 없는 고객 문제를 사실로 보강하지 말 것
- `PROJECT_PLAN.md`를 자동으로 고치지 말 것
- 기술 스택부터 정한 뒤 문제를 거기에 맞추지 말 것
- 모든 기능을 유지한 채 일정만 낙관적으로 잡지 말 것

## 리뷰 산출물

별도 지시가 없다면 리뷰 결과는 다음 파일에 작성한다.

`reviews/proposal-review.md`

권장 구조:

```markdown
# Proposal Review

## Verdict
GO | INVESTIGATE | HOLD

## 1. One-line Assessment

## 2. ICP / JTBD
- Confirmed:
- Assumptions:
- Problems:
- Required changes:

## 3. Pain Evidence
- Existing evidence:
- Missing evidence:
- Cheapest validation:

## 4. Alternatives / Differentiation
- Existing alternatives:
- Defensible difference:
- Weak or unsupported claims:

## 5. MVP Scope
### Must
### Should
### Later
### Do Not Build

## 6. Critical Assumptions
| Assumption | Impact if false | Current evidence | Test |
|---|---|---|---|

## 7. Safety / HITL

## 8. Two-week Feasibility
- Hardware risk:
- Software risk:
- Integration risk:

## 9. Questions Before Build

## Final Recommendation
```

### Verdict 기준

- `GO`: 핵심 문제와 MVP가 충분히 명확하며, 현재 증거 수준에서 구현을 시작할 합리적 근거가 있음.
- `INVESTIGATE`: 아이디어는 유망하지만 치명적 가정이나 증거 부족이 있어 먼저 확인이 필요함.
- `HOLD`: 핵심 문제, 차별점, 범위 또는 비용/위험 측면에서 현재 상태로는 구현 근거가 약함.

---

# 3. Implementation Architect Mode

기획 검토 후 사용자가 기술 설계, 구현 계획, task breakdown 또는 구현을 요청하면 이 모드로 동작한다.

## 입력 우선순위

1. 사용자의 현재 명시적 요청
2. `PROJECT_PLAN.md`의 제품 목표 / Build Gate
3. `HARDWARE_SPEC.md` / `HARDWARE_BOM.md` / `IMPLEMENTATION_PLAN.md`의 최신 구현 결정
4. 승인된 최신 review/decision 문서가 있다면 그 결정
5. `knowledge/agent-engineering.md`

기획과 기술 기준이 충돌하면 임의로 제품 목표를 바꾸지 말고 충돌을 보고한다.

## 기본 기술 원칙

### Workflow vs Agent

- 다음 행동이 사전에 정해지는 부분은 deterministic workflow를 우선한다.
- 입력/중간 결과에 따라 런타임 판단이 필요한 곳에만 Agent를 사용한다.
- Agent 자유도 자체를 목표로 하지 않는다.

### Natural Language → Contract

새 설비 설명은 자연어에서 곧바로 실행 코드로 변환하지 않는다.

기본 흐름:

```text
Natural Language
→ DeviceSpec / Capability Spec
→ Structural Validation
→ Semantic / Safety Validation
→ Human Review / Device Test
→ Registry
→ MCP / Executor
```

### Device execution

- LLM이 임의 Python, Shell, raw executable code를 생성해 장비에서 직접 실행하는 구조를 기본안으로 삼지 않는다.
- 실제 통신은 미리 정의된 Adapter와 검증 가능한 Command/Capability Contract를 통해 수행한다.
- 파라미터 타입, enum, 최소/최대 범위는 코드에서 검증한다.

### MCP

- MCP는 연결 표준이며 Tool Contract를 대신하지 않는다.
- Tool은 single responsibility, explicit arguments, structured return을 기본으로 한다.
- Tool 설명에는 가능하면 What / When / How / Output / Constraints를 포함한다.
- MVP에서 동적 Tool 생성이 필요하지 않다면 generic discovery/invoke 구조를 우선 검토한다.

예:

```text
list_devices()
get_device(device_id)
list_capabilities(device_id)
invoke_capability(device_id, capability, arguments)
get_device_status(device_id)
```

### Validation / Failure

- LLM 출력을 신뢰하지 말고 contract로 제한한다.
- Structural Validation과 Semantic/Business Validation을 구분한다.
- 실패는 구조화된 상태로 반환한다.
- 재시도는 무한 반복하지 않고 retry budget과 종료 조건을 둔다.
- 같은 요청을 맹목적으로 다시 보내기보다 실패 근거를 사용한 repair를 우선한다.

### Safety / Side effects

- 읽기와 쓰기 capability를 구분한다.
- 실제 장비 동작은 side effect로 취급한다.
- 위험한 행동은 명시적 approval gate를 둔다.
- Description/Prompt는 보안 경계가 아니다. Permission, validation, timeout, approval은 코드가 강제한다.
- 가능한 경우 idempotency, stable operation key, audit log를 고려한다.

### Observability

최소한 다음 실행 정보를 추적할 수 있도록 설계한다.

- run/request id
- device / capability
- validated arguments
- result/status
- error type
- latency
- approval state
- timestamp

### Scope discipline

- 사용자가 요청하지 않은 기능을 "나중에 필요할 것"이라는 이유로 구현하지 않는다.
- 2주 MVP에서는 핵심 가설을 증명하는 최소 Adapter/Device 수를 우선한다.
- Stretch goal은 핵심 happy path가 실제 실행으로 검증된 뒤에만 진행한다.

---

# 4. Implementer Mode

실제 코드를 수정할 때는 다음 순서를 따른다.

1. 현재 저장소 상태와 관련 파일을 먼저 읽는다.
2. 이번 요청의 입·출력과 완료 정의를 명시한다.
3. 작업을 실행 검증 가능한 최소 단위로 나눈다.
4. 한 단계씩 구현한다.
5. 각 단계 후 실제 테스트/실행으로 증거를 확인한다.
6. 실패하면 에러를 기준으로 원인을 분류하고 한 번에 하나의 원인을 수정한다.
7. 요청 범위를 벗어난 리팩터링/기능 추가는 하지 않는다.
8. 마지막에 변경 파일, 테스트 결과, 알려진 한계, 남은 리스크를 보고한다.

"될 것 같다"는 설명은 완료 증거가 아니다. 실행 가능한 부분은 실제 실행 결과를 확인한다.

---

# 5. 역할 분리 원칙

기획 Reviewer와 Implementer는 서로의 목표를 침범하지 않는다.

```text
Planning Reviewer
  문제/고객/가설/범위/증거 검증
        ↓
사용자 또는 팀의 결정
        ↓
Implementation Architect
  승인된 범위를 기술 구조와 task로 변환
        ↓
Implementer
  작은 단위 구현 + 실제 검증
```

- Reviewer는 구현 난이도가 낮다고 기능을 핵심으로 올리지 않는다.
- Architect는 구현하기 편하다는 이유로 ICP/JTBD를 바꾸지 않는다.
- Implementer는 제품 기능을 임의로 추가하지 않는다.
- 제품 가정이 구현 중 틀린 것으로 드러나면 숨기지 말고 planning 단계로 되돌릴 근거로 보고한다.

---

# 6. Factory Agent Hub 현재 핵심 가설

이 항목은 `PROJECT_PLAN.md`의 방향을 빠르게 이해하기 위한 요약이며, 기획서 자체를 대체하지 않는다.

현재 검증하려는 핵심 아이디어는 다음과 같다.

> 사용자가 새 설비의 연결 방식과 기능을 자연어로 설명하면 이를 검증 가능한 Device/Capability 명세로 변환하고, 등록된 기능을 Agent가 MCP를 통해 발견하고 조합해 사용할 수 있도록 한다.

현재 구현의 핵심 질문은 "로봇팔과 컨베이어를 AI로 움직일 수 있는가"만이 아니다.

더 중요한 검증 질문은:

> **Agent가 처음 보는 장비의 기능을 코드 수정 없이 안전한 Capability로 온보딩하고, 이후 기존 장비와 함께 사용할 수 있는가?**

기획 검토에서는 이 가설 자체가 실제 고객 문제와 연결되는지 먼저 검증한다.
