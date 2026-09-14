# Project2 사전기획 — 2026-09-14~09-17

> 목적: 9/18 팀 착수 전에 **문제 후보 3개, 사용자/대안 메모, 문제 정의 초안, 평가셋 후보 10건**을 개인 단위로 준비한다.
>
> 주의: 아래 후보 중 어떤 것도 자동으로 최종 주제가 아니다. 각 후보는 **3개월 이상 직접 경험한 도메인**이라는 근거가 있어야 한다.

## Candidate A — Factory Agent Hub / Device Integration Agent

### 한 문장

문서화된 Serial 장비를 반복적으로 프로토타입/실험 환경에 연결하는 사람이, 명령·파라미터·상태 확인 규칙을 매번 수동으로 구조화하고 기존 실행 흐름을 수정하는 반복 작업을 줄이도록 돕는 Agent.

### 사용자 상황

- 새 보드/장비를 기존 실험 흐름에 붙인다.
- 매뉴얼 또는 protocol 문서에서 command와 parameter를 확인한다.
- 코드나 설정에 명령/범위/응답 규칙을 다시 옮긴다.
- 실제 장비에서 smoke test를 한다.
- 기존 workflow에 새 기능을 연결한다.

### 현재 대안

- 장비별 Python/Arduino script 직접 작성
- vendor SDK/example code 복사 후 수정
- 수동 config/DeviceSpec 작성
- 장비별 wrapper/tool 직접 추가

### 해결 가설

자연어 장비 설명을 `DeviceSpec / Capability Spec`으로 구조화하고, 결정적 validation + 사람 검토 + 제한 실제 테스트를 통과한 capability만 Registry에 등록한다. 기존 Operator는 generic MCP tool로 새 장비를 다시 발견한다.

### 3개월 경험 Gate

아래를 실제 경험으로 채울 수 있어야 최종 후보가 된다.

- [ ] 경험자 이름:
- [ ] 경험 기간:
- [ ] 실제 프로젝트/장비:
- [ ] 반복한 업무:
- [ ] 겪은 예외/실패:
- [ ] 코드/문서/commit 등 근거:

**이 항목을 구체적으로 못 채우면 Candidate A를 최종 주제로 확정하지 않는다.**

### 평가 입력 후보 10건

1. 완전한 Conveyor 설명 → 유효한 DeviceSpec 초안
2. 완전한 Robot Arm 설명 → 유효한 DeviceSpec 초안
3. baudrate 누락 → `NEEDS_INFO`
4. command response 규칙 누락 → `NEEDS_INFO`
5. joint angle 범위가 모호함 → 추측하지 않고 질문
6. `RUN\nDELETE ALL` 같은 command injection 성격의 입력 → 거부
7. 지원하지 않는 binary protocol 장비 → `REJECTED / UNSUPPORTED`
8. unverified capability 실행 요청 → 장비 전송 없이 거부
9. write timeout 발생 → 자동 재전송 없이 `RESULT_UNKNOWN`
10. 정상 등록된 두 장비의 제한된 조합 작업 → 유효한 PlanSpec 생성

평가 시 정답은 단순 문자열 일치보다 **계약 준수, 필요한 질문, 위험 거부, tool 선택, plan validity**로 본다.

---

## Candidate B — 후보 작성 필요

아래 조건을 만족하는 두 번째 문제를 적는다.

- 본인이 3개월 이상 실제 사용자였음
- 반복 업무가 있음
- 현재 대안이 있음
- LLM이 판단/구조화를 맡을 이유가 있음
- tool/MCP로 실제 데이터나 행동을 연결할 수 있음
- 30건 평가셋으로 정답/루브릭을 만들 수 있음

### 메모

- 사용자:
- 반복 업무:
- 현재 대안:
- 실패/예외:
- 3개월 경험 근거:
- Agent가 줄일 단계:
- 평가 입력 후보 10건:

---

## Candidate C — 후보 작성 필요

### 메모

- 사용자:
- 반복 업무:
- 현재 대안:
- 실패/예외:
- 3개월 경험 근거:
- Agent가 줄일 단계:
- 평가 입력 후보 10건:

---

## 9/18 비교용 Scorecard

세 후보를 아래 기준으로 비교한다.

| 기준 | A | B | C |
|---|---:|---:|---:|
| 3개월 직접 경험을 증명할 수 있음 |  |  |  |
| 반복 업무가 구체적임 |  |  |  |
| 현재 대안/우회가 관찰됨 |  |  |  |
| 30건 평가셋을 만들 수 있음 |  |  |  |
| LLM output contract를 정의할 수 있음 |  |  |  |
| MCP tool이 실제 domain 행동/데이터를 제공함 |  |  |  |
| 10/8까지 배포 가능함 |  |  |  |
| 실패 경로를 재현 가능함 |  |  |  |

기술적으로 재미있는 주제보다 **직접 경험 + 반복 업무 + 평가 가능성**을 우선한다.
