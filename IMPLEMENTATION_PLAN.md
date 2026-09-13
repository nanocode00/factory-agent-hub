# Factory Agent Hub — 2주 구현 계획안

> 상태: **2026-09-13 실행안 v3 / local stop 구매안 반영**  
> 전제: `HARDWARE_SPEC.md` v4와 `HARDWARE_BOM.md` v3의 **리브온 Conveyor + 이엘사이언스 Arduino 4-DOF Robot Arm + Raspberry Pi 3B+** 구성을 사용한다.
>
> 목표는 멋진 로봇을 만드는 것이 아니라 **서로 다른 실제 장비 2개를 고정된 Serial Adapter와 선언적 DeviceSpec으로 등록하고, 같은 MCP 경계에서 발견·승인·실행할 수 있음을 검증하는 것**이다.

---

## 1. 완료 정의

2주 종료 시 아래가 모두 가능해야 MVP 기술 경로를 완료한 것으로 본다.

1. Conveyor와 Robot Arm이 각각 Arduino 단독 Serial 명령으로 안정 동작한다.
2. Raspberry Pi 3B+가 두 Arduino를 동시에 식별하고 deterministic Serial Adapter로 호출한다.
3. 두 장비는 **서로 다른 고정 text protocol**을 사용한다.
4. 첫 번째 장비는 수동/기준 DeviceSpec으로 Registry에 등록되어 있다.
5. 두 번째 장비는 firmware/protocol을 동결한 뒤 자연어 설명만으로 Setup Agent가 DeviceSpec / Capability Spec 초안을 만든다.
6. Structural / semantic / safety validation과 사람 검토, 제한된 Device Test를 통과한 spec만 active가 된다.
7. Operator Agent는 같은 MCP의 generic discovery/invoke를 사용해 두 장비를 발견한다.
8. 승인된 짧은 작업 계획을 실제 장비에서 실행하고 물리 상태를 확인한다.
9. timeout / disconnect / invalid argument / unverified capability / write result unknown 같은 필수 실패 경로를 재현한다.
10. firmware / Adapter / schema / system prompt를 신규 장비에 맞춰 평가 중 수정하지 않았음을 commit/hash로 증명한다.

---

## 2. 팀 역할 권장

3명 기준:

| 역할 | 주 책임 | 보조 책임 |
|---|---|---|
| A — Hardware / Firmware | Conveyor, Robot Arm, Arduino firmware, local stop, physical smoke | Serial protocol 문서화 |
| B — Setup / Contract | DeviceSpec schema, Setup Agent, validation, review/test state | A/B 활동지·명세 baseline |
| C — Edge / Operator | Raspberry Pi, Serial Adapter, Registry, MCP, Operator, executor | logging / integration test |

4번째 인원이 있으면 **Evaluation / Evidence**를 별도 담당해 시간 측정, 회귀 테스트, demo script, Langfuse/실행 기록, 독립 재현을 맡긴다.

작성자가 자기 명세만 검토하지 않도록 가능하면 다른 팀원이 review한다.

---

## 3. Day 0 — 구매 / 준비

### Hardware Purchase

최종 구매안은 `HARDWARE_BOM.md`를 따른다.

- [ ] 리브온 목재 Conveyor kit 주문
- [ ] 이엘사이언스 Arduino 집게 로봇팔 4관절 주문
- [ ] DRV8833 `VLT-MD012` 주문
- [ ] 5V 5A regulated adapter 주문
- [ ] C7 AC cable 주문
- [ ] VLT-DC001 5.5×2.1 terminal connector 주문
- [ ] `MSL-1C2P(중)-4mm` 3PIN / 1C2T local stop switch ×2 주문

### Inventory Check

집에서 가져갈 세부 수량은 `HARDWARE_PACKING_LIST.md`를 따른다.

- [ ] Raspberry Pi 3B+ / 기존 전원 / microSD / network 준비
- [ ] Arduino Uno 3대 선별 — 장비 2대 + spare 1대
- [ ] USB **data** cable 3개 확인 — 장비 2대 + spare 1개
- [ ] IR proximity sensor 2개 준비 — primary + spare
- [ ] LED / NeoPixel 준비
- [ ] jumper / signal / power wire 확인
- [ ] breadboard 2개 준비
- [ ] servo / motor fallback 소량 준비
- [ ] multimeter / screwdriver 등 기본 공구 준비
- [ ] test object 준비

### Software

- [ ] 개발 laptop에서 repo clone / dependency 설치
- [ ] Raspberry Pi OS / Python runtime 확인
- [ ] Git branch/commit 규칙 정리
- [ ] `hardware/`, `firmware/`, `specs/`, `src/` 예상 구조 합의

**중단 조건:** 두 실제 장비를 첫 주 안에 받을 수 없으면 mock만으로 실제장비 검증을 대체하지 않는다. 배송 지연 시 범위를 저위험 실제 Serial 장비 2개로 축소한다.

---

## 4. Day 1–2 — Hardware Bring-up

### Conveyor

목표: Agent 없이 단독으로 안정 동작.

1. kit 조립
2. belt / roller / frame 상태 확인
3. motor label / 기본 power 구성 확인
4. 실제 motor supply 결정
5. DRV8833 연결
6. 30초 이상 연속 구동 smoke
7. IR object sensor 연결
8. `MSL-1C2P` local stop 연결
9. local stop이 Arduino input에서 안정적으로 읽히는지 확인
10. STOP 상태에서 motor output 즉시 disable
11. LED state indication 연결
12. Arduino Serial command 구현

초기 protocol:

```text
RUN
HALT
SPEED <level>
OBJECT?
STATUS?
```

기본 motor는 우선 유지한다. DRV8833 조합에서 제어 불가, 토크 부족, 비정상 과열, 지나친 속도, 기구 문제가 확인될 때만 보유 motor로 교체한다.

### Robot Arm

1. 이엘사이언스 4-DOF kit 조립
2. 실제 servo model label 기록
3. 5V 5A external servo PSU 구성
4. Arduino와 servo PSU common GND 확인
5. 각 servo center 맞춤
6. 각 joint를 아주 좁은 범위부터 sweep
7. 물리 간섭 지점 측정
8. HOME pose 정의
9. gripper open/close 정의
10. `MSL-1C2P` local stop 연결
11. motion을 작은 step으로 나눠 stop input을 반복 확인하도록 firmware 구성
12. STOP 상태에서 새 motion command를 거부하고 마지막 안전한 command 위치에서 hold
13. Serial command 구현

초기 protocol:

```text
HOME
J <joint> <angle>
CLAW OPEN
CLAW CLOSE
POSE?
STOP
```

`MSL-1C2P`는 **저전압 logic input용 local stop**으로 사용하며 motor/servo 전원을 직접 끊지 않는다. 가능하면 `INPUT_PULLUP` 기반으로 RUN 위치에서 GND에 연결하고, open/wire-disconnect 상태를 STOP으로 해석한다. 산업용 emergency stop으로 간주하지 않는다.

### Day 2 종료 Gate

- [ ] Conveyor 30초 이상 연속 구동
- [ ] HALT 시 실제 정지
- [ ] IR sensor 반복 감지
- [ ] Conveyor local stop → motor output disable 확인
- [ ] Robot 모든 축 개별 동작
- [ ] 5V 5A external servo power 안정
- [ ] HOME 성공
- [ ] 가벼운 물체 pick/place 3회 이상 성공
- [ ] Robot motion 중 local stop 입력을 넣었을 때 추가 trajectory 진행이 중단됨
- [ ] local stop 입력 배선 open 상태를 STOP으로 해석하는지 확인
- [ ] 두 장비 모두 USB Serial request/response 성공

실패하면 Agent 개발보다 hardware 안정화를 우선한다. Day 2에 Hardware Gate가 닫히지 않으면 Robot 노출 joint 수, sensor 수, 동작 범위를 줄인다.

---

## 5. Day 3 — Protocol / Firmware Freeze 준비

두 장비의 protocol은 일부러 같게 만들지 않는다.

```text
Conveyor
RUN
HALT
SPEED 2
OBJECT?
STATUS?

Robot
HOME
J 2 85
CLAW OPEN
POSE?
STOP
```

각 command에 대해 아래를 문서화한다.

| 항목 | 기록 내용 |
|---|---|
| command syntax | 정확한 text grammar |
| argument type | int / enum / none |
| range | 실제 허용 범위 |
| write/read | side effect 여부 |
| risk | READ_ONLY / SAFE / NORMAL / DANGEROUS |
| success response | 결정적인 success pattern |
| error response | invalid/range/busy 등 |
| timeout | 실제 timeout |
| state verification | 실행 후 무엇을 읽어 확인하는지 |

이날 **수동 기준 DeviceSpec**도 작성한다. 이 baseline은 자연어 방식과 비교할 때 정답/검토 기준으로 사용한다.

---

## 6. Day 4–5 — Raspberry Pi Edge Core

### Serial Adapter

MVP는 Serial 하나만 지원한다.

```text
port / stable device id
baudrate
encoding
line ending
request
response matcher
timeout
```

필수 조건:

- arbitrary shell/code 실행 없음
- newline / multi-command injection 차단
- 정의되지 않은 command template 호출 불가
- argument type/range 검사
- write timeout 시 자동 재전송 금지
- read retry는 제한된 횟수만 허용

### Stable device mapping

- 두 Arduino 동시 연결
- `/dev/ttyACM0` 같은 순번만 신뢰하지 않음
- udev symlink 또는 식별 가능한 stable mapping 구성

### Registry / Audit

최소 저장:

```text
device_id
spec_version
capability_id
verified state
request/run id
operation key
validated arguments
approval status
result/error
physical state verification
latency
```

### Day 5 종료 Gate

- [ ] Pi에서 두 장비 health 조회
- [ ] Adapter로 두 protocol 모두 호출
- [ ] invalid command / invalid range 차단
- [ ] disconnect 감지
- [ ] write timeout을 `result unknown`으로 종료

---

## 7. Day 6 — DeviceSpec / Validator / Registry

DeviceSpec / Capability Spec 최소 계약을 확정한다.

```text
device
  id
  version
  adapter
  connection

capability
  id / name
  description
  command template
  parameters schema
  read/write
  risk
  success condition
  state verification
  verified state
```

상태 전이는 최소 다음으로 제한한다.

```text
DRAFT
→ VALIDATED
→ REVIEWED
→ TEST_APPROVED
→ VERIFIED
→ ACTIVE
```

미검증 capability는 Operator discovery/invoke 대상에서 제외한다.

---

## 8. Day 7 — 최소 End-to-End + Freeze

이날까지 최소 경로를 한 번 끝낸다.

```text
manual DeviceSpec
→ validation
→ Registry
→ MCP list_devices
→ list_capabilities
→ invoke_capability
→ Adapter
→ Arduino
→ actual hardware
→ state verification
→ audit log
```

동시에 평가용 freeze commit을 만든다.

Freeze 대상:

```text
Conveyor firmware / protocol
Robot firmware / protocol
Serial Adapter
DeviceSpec schema
Validator / Policy / Executor
MCP Gateway
Setup Agent system prompt/examples
Operator Agent system prompt/examples
```

**Day 7 이후 신규 장비에 맞추기 위한 hidden code change는 금지한다.**

---

## 9. Day 8–9 — Setup Agent 온보딩 검증

추천 demo 순서:

1. Conveyor만 Registry에 active 상태로 등록한다.
2. Robot Arm firmware/protocol은 이미 freeze됐지만 Registry에는 넣지 않는다.
3. 사용자가 Robot Arm 사용법을 자연어로 제공한다.
4. Setup Agent가 DeviceSpec / Capability Spec 초안을 만든다.
5. 누락/모호한 내용은 질문한다.
6. Structural / semantic validation을 수행한다.
7. 사람이 diff와 위험 수준을 검토한다.
8. 제한된 Device Test를 승인한다.
9. 실제 Robot Arm에서 제한 command만 시험한다.
10. 성공한 capability만 active Registry에 등록한다.
11. 동일 Operator/MCP를 다시 조회해 Robot Arm이 새로 발견되는 것을 확인한다.

성공 기준은 **Robot을 움직였다는 것**이 아니라 **새 장비 등록 때문에 Setup/Operator/MCP/Adapter 코드를 수정하지 않았다는 것**이다.

---

## 10. Day 10 — Operator Plan / 두 장비 조합

Operator가 직접 raw command를 생성하지 않고 machine-readable PlanSpec을 만든다.

```text
PlanSpec
  steps:
    - capability_id
      arguments
      expected_state
```

짧은 demo flow:

```text
1. Conveyor RUN
2. OBJECT? 로 물체 확인
3. Conveyor HALT
4. Robot HOME
5. Robot move
6. CLAW CLOSE
7. Robot place
8. CLAW OPEN
9. Conveyor RUN
```

MVP에서는 자유로운 event loop보다 **짧은 유한 순서**로 제한한다.

각 write step은 target/spec version/arguments/plan에 묶인 approval 이후 실행한다.

---

## 11. Day 11 — 실패 / 안전 회귀 테스트

반드시 재현할 실패:

- invalid integer range
- unknown capability
- unverified capability invoke
- command injection 시도
- Arduino disconnect
- read timeout
- write timeout / lost response
- approval 없는 write
- approval 후 argument 변경
- spec version 변경 후 old approval 재사용
- local stop 작동
- local stop input wire disconnect

write timeout은:

```text
result = UNKNOWN
no automatic resend
halt downstream steps
require physical state check
```

로 처리한다.

---

## 12. Day 12 — 비교 실험 / 관측

준비된 활동지를 사용해 manual DeviceSpec vs natural-language draft를 비교한다.

측정 범위:

- 자료 읽기 시간
- 입력/설명 시간
- generation wait
- review 시간
- correction 횟수/시간
- Validator pass까지 총시간
- 최종 오류
- 주관 난이도

같은 사람이 같은 장비를 두 방식으로 연속 수행해 학습효과가 생기지 않도록 교차 배정한다.

Langfuse는 trace / tool / generation / latency / token/cost 관측에 사용하되, 안전 gate로 사용하지 않는다.

---

## 13. Day 13–14 — 독립 재현 / 발표 준비

### 독립 재현

- clean restart
- Pi reboot
- Arduino reconnect
- Registry reload
- 동일 자연어 onboarding 재현
- demo flow 재실행

### 발표에서 보여줄 증거

```text
Before:
Registry = Conveyor only

Freeze commit/hash

Natural-language Robot description
→ generated spec
→ validator
→ human review
→ limited physical test
→ active registry

After:
Registry = Conveyor + Robot

Same Operator / Same MCP / Same Adapter
→ combined physical task
```

함께 보여줄 것:

- DeviceSpec diff
- validation rejection 예시
- approval record
- actual command/result log
- physical state verification
- failure case 1~2개
- freeze commit/hash
- comparison experiment 결과

---

## 14. 범위 축소 규칙

일정이 밀리면 아래 순서로 제거한다.

1. LCD / NeoPixel 등 장식 UI
2. RFID 연동
3. potentiometer / manual jog 등 부가 local UI
4. Robot joint 수를 논리적으로 덜 노출
5. Conveyor speed 단계 축소
6. 웹 UI
7. 복잡한 multi-device 자동화

끝까지 남겨야 하는 것:

```text
2 physical devices
2 different frozen Serial protocols
1 generic Serial Adapter
DeviceSpec / Capability contract
validation / review / limited test / Registry
MCP discovery / invoke
approval + deterministic execution
failure handling + audit
no-code onboarding evidence
```

---

## 15. 다음 즉시 행동

1. 최종 구매안 결제
2. `HARDWARE_PACKING_LIST.md` 기준 집에서 가져갈 부품 선별
3. 팀원별 역할 확정
4. repo에 firmware / edge / agent 작업 skeleton 생성
5. hardware 도착 전 Serial protocol과 DeviceSpec schema 초안 작성
6. 도착 즉시 Day 1–2 Hardware Bring-up 수행

Hardware 배송을 기다리는 동안에도 schema, validator, mock serial transport, Registry, MCP interface는 개발할 수 있다. 단, mock 성공을 실제 Hardware Gate 통과로 세지 않는다.