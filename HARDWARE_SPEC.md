# Factory Agent Hub — Hardware Testbed Specification

> 상태: **2026-09-12 설계안 v2**  
> 목적: 기구부를 직접 설계·제작하는 데 시간을 쓰기보다, 저가 기성 기구 키트 + 보유 전자부품을 결합해 실제 Conveyor / Robot Arm 테스트베드를 빠르게 확보한다.
>
> 이 문서는 현재 하드웨어 구현의 기준 문서다. `PROJECT_PROPOSAL.md`의 과거 L-LINE 후보보다 **현재 테스트베드 구성에 대해서는 이 문서를 우선**한다. 제품 가설과 Build Gate 자체는 `PROJECT_PROPOSAL.md`를 따른다.

---

## 1. 현재 결정사항

### 1.1 테스트베드 전략

기존의 `축 + 베어링 + 평벨트 + 3D 프린트 프레임` 방식으로 Conveyor를 직접 제작하고 Robot Arm을 직접 모델링하는 계획은 **보류**한다.

현재 우선 전략은 다음과 같다.

- Conveyor: **5천~7천 원대 교육용 소형 목재 Conveyor kit**를 기구부로 사용한다.
  - belt / roller / frame / 기본 motor를 우선 그대로 활용한다.
  - 기본 motor가 제어에 적합하지 않으면 보유 motor/driver로 교체한다.
  - 정확한 SKU는 구매 직전 구성품·크기·motor 접근성을 확인하고 확정한다.
- Robot Arm: **SciPia G56 4-DOF Arduino Robot Arm Starter Kit**를 우선 구매 후보로 사용한다.
  - 6-DOF 고하중 arm보다 비용, 전원, calibration, 충돌 위험을 줄인다.
  - 매우 가벼운 물체의 pick-and-place / sorting만 목표로 한다.
- Edge Gateway: **Raspberry Pi 3B+ 1대**를 사용한다.
- Device controller: **Arduino Uno 2대 이상**을 장비별로 분리한다.
- 전자부품, sensor, local UI 부품, Raspberry Pi 전원/부속품은 **보유품 우선**으로 사용한다.
- shaft, custom endless flat belt, M3 assortment 등은 **선구매하지 않는다**. 실제 kit 조립 후 부족분만 산다.

### 1.2 시스템 구조

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
  ├─ USB Serial → Arduino #1 → Conveyor
  └─ USB Serial → Arduino #2 → G56 Robot Arm
```

원칙:

- LLM은 Raspberry Pi나 Arduino에 임의 raw command를 직접 보내지 않는다.
- Agent는 generic MCP capability interface를 사용한다.
- Raspberry Pi가 DeviceSpec / Capability 검증과 deterministic execution을 담당한다.
- Arduino는 실제 sensor / motor / servo 제어와 local stop을 담당한다.
- Raspberry Pi에는 LLM을 올리지 않는다. Pi는 Edge Gateway 역할에 집중한다.
- 평가 전에 firmware / Serial protocol / Adapter / schema / Agent prompt를 동결한다.

---

## 2. 확인된 주요 보유 부품

Google Drive `부품 목록`을 기준으로 현재 핵심 재고는 다음과 같다.

| 분류 | 모델 / 품목 | 수량 | 우선 용도 |
|---|---|---:|---|
| MCU | Arduino Uno | 9 | 장비별 controller |
| MCU | Arduino Nano | 1 | 보조 controller |
| Edge | Raspberry Pi 3B | 1 | 예비 Gateway |
| Edge | Raspberry Pi 3B+ | 2 | **주 Edge Gateway 후보** |
| Edge | Raspberry Pi Zero W | 1 | Later / 보조 node |
| Servo | SG90 | 12 | 예비 / 교체 / auxiliary actuator |
| Servo | FS90 | 5 | 예비 / gripper |
| Servo | EF92A | 1 | 예비 |
| Servo | MG996R | 1 | 예비 고토크 축 |
| Stepper | 28BYJ-48 | 7 | Conveyor motor 대체 후보 |
| Stepper driver | 모델 미확인 | 7 | 28BYJ-48 구동 |
| DC motor | 소형 DC motor | 13 | Conveyor motor 대체 후보 |
| Motor | 기타 소형 motor | 20 | 예비 |
| Bearing | 608ZZ | 9 | 필요 시 기구 보강 / 예비 |
| Distance | HC-SR04 | 13 | object detect / distance |
| Distance | SRF05 | 2 | object detect / distance |
| Proximity | IR 근접 sensor | 4 | Conveyor object detect |
| RFID | RC522 | 10 | object/card identification |
| Display | LCD | 11 | local status |
| Status | NeoPixel / LED 계열 | 다수 | READY/RUNNING/ERROR |
| Input | Joystick | 7 | manual jog / calibration |
| Input | switch / button / potentiometer | 다수 | local stop / manual control |
| Alert | buzzer | 다수 | fault / completion |
| 기타 | MPU-6050, DHT, PIR, microphone, RTC, relay 등 | 다수 | 예비 Device / sensor station |

LED, 저항, 포텐쇼미터, 부저, 스위치 등 기본 수동소자도 충분히 보유한 것으로 본다.

---

## 3. Conveyor v2

### 3.1 목표

- 저가 교육용 Conveyor kit의 **기계 구조를 재사용**한다.
- 작은 블록, RFID tag 부착 물체, 가벼운 테스트 물체만 운반한다.
- Agent onboarding / orchestration 검증이 목적이며 산업용 하중·속도 성능은 목표가 아니다.
- kit 자체 전자제어가 있다면 그대로 신뢰하지 않고, Arduino를 통해 우리가 정의한 protocol로 제어한다.

### 3.2 유지 / 교체 판단

```text
교육용 Conveyor kit
 ├─ Frame      → 우선 유지
 ├─ Belt       → 유지
 ├─ Roller     → 유지
 ├─ Shaft      → 유지
 └─ Motor      → 단독 smoke 후 유지/교체 결정
                    │
                    ├─ 유지 가능 → Arduino + 적합 driver 연결
                    └─ 부적합     → 보유 28BYJ-48 또는 DC motor로 교체
```

기존 계획의 아래 구매는 **현재 보류**한다.

- Ø8 × 150 mm shaft
- 60 × 800 mm custom endless flat belt
- 추가 608ZZ
- 대형 3D printed frame / roller

### 3.3 Sensor / local interface

우선 구성:

```text
IR proximity 또는 HC-SR04 → object detect
switch                    → local stop
NeoPixel / LED            → state indication
buzzer                     → fault / completion
potentiometer              → optional manual speed
```

일반 switch를 산업용 emergency stop이라고 부르지 않는다. 이 테스트베드에서는 **local stop**으로 정의한다.

### 3.4 Serial protocol 초안

아래는 구현 전 초안이며 단독 smoke 후 freeze한다.

```text
RUN
HALT
SPEED <level>
OBJECT?
STATUS?
```

예상 응답 예시:

```text
OK RUN
OK HALT
OK SPEED 2
OBJECT 1
STATE RUNNING SPEED=2 OBJECT=0
ERR ARG_RANGE
```

`SPEED` 범위는 실제 motor/driver 제어 방식 확인 후 확정한다.

---

## 4. Robot Arm v2 — G56 4-DOF

### 4.1 선택 이유

Robot Arm 기구부 직접 모델링은 보류하고 **SciPia G56 4-DOF kit**를 우선 사용한다.

선택 이유:

- 6-DOF arm보다 구매비가 낮다.
- servo 전류와 calibration 부담이 적다.
- collision case와 firmware 복잡도가 줄어든다.
- Factory Agent Hub 검증에는 4-DOF로 충분하다.
- 목표가 robot mechanics가 아니라 capability onboarding이므로 기구 설계 시간을 줄이는 것이 유리하다.

### 4.2 동작 범위

대상 물체:

- 작은 sponge cube
- 빈 plastic block
- RFID tag가 붙은 매우 가벼운 test object

고하중 pick-and-place는 범위 밖이다.

### 4.3 제어 구성

```text
Arduino Uno
 ├─ base servo
 ├─ shoulder servo
 ├─ elbow servo
 └─ gripper servo
```

실제 kit servo 구성과 각 축의 safe angle은 조립 후 확인한다.

### 4.4 Serial protocol 초안

```text
HOME
J <joint> <angle>
CLAW OPEN
CLAW CLOSE
POSE?
STOP
```

예상 응답 예시:

```text
OK HOME
OK J 2 90
OK CLAW OPEN
POSE J1=90 J2=80 J3=110 CLAW=OPEN
ERR JOINT_RANGE
ERR ANGLE_RANGE
```

각 joint의 실제 안전 범위는 물리 간섭을 확인한 뒤 firmware에 결정적으로 제한한다. `0..180` 전체를 무조건 허용하지 않는다.

---

## 5. Raspberry Pi Edge Gateway

주 Gateway는 **Raspberry Pi 3B+ 1대**다. 전원과 기본 부속품은 보유품을 사용한다.

Pi 역할:

```text
MCP Server
Device Registry
DeviceSpec loader
Structural / semantic validation
Policy / approval state
Deterministic Executor
USB Serial device routing
SQLite audit ledger
Health / device status
```

Laptop 역할:

```text
Setup Agent
Operator Agent
LLM calls
Development UI / CLI
Langfuse observability
```

Arduino 역할:

```text
Sensor read
Motor / Servo actuation
Local deterministic control
Local stop handling
Frozen text Serial protocol
```

USB device path가 재부팅마다 바뀔 수 있으므로 `/dev/ttyACM*` 문자열을 그대로 영구 ID로 쓰지 않는다. 실제 구현에서 VID/PID, USB serial, udev symlink 등 **stable device mapping**을 확보한다.

---

## 6. 구매 계획 — v2

### Buy Now

| 품목 | 상태 | 비고 |
|---|---|---|
| 교육용 소형 Conveyor kit | **구매 예정** | 5천~7천 원대 후보. 정확한 SKU는 크기/구성품 확인 후 확정 |
| SciPia G56 4-DOF Robot Arm kit | **구매 예정** | 4-DOF 우선. 실제 구성품/servo 포함 여부 최종 확인 후 주문 |

### 보유품 사용

- Raspberry Pi 3B+
- Raspberry Pi 전원/부속품
- Arduino Uno
- sensor / RFID / LED / buzzer / switch / potentiometer
- SG90 / FS90 / MG996R 등 spare servo
- motor / driver 예비품
- 608ZZ

### 구매 보류

아래는 kit 조립 후 실제 부족할 때만 산다.

- M3 bolt / nut / washer assortment
- Ø8 shaft
- custom flat belt
- 추가 bearing
- coupler / pulley
- 대형 3D printed mechanical parts

`kit을 받기 전에 범용 부품을 미리 쌓아두지 않는다`를 원칙으로 한다.

---

## 7. 3D Printing 범위

기구 전체 제작이 아니라 **필요한 adapter/bracket만 출력**한다.

가능한 출력물:

```text
Arduino mount
sensor bracket
local-stop bracket
Pi / cable management bracket
Conveyor motor adapter (필요 시)
Robot test-object / jig
RFID tag holder
small spacer / shim
```

Major frame / roller / robot link는 기성 kit를 우선 사용한다.

---

## 8. Hardware Bring-up 순서

### Stage A — kit 자체 동작

Conveyor:

- frame / belt / roller 조립
- hand rotation 확인
- motor 단독 구동
- belt slip / derailment 확인

Robot Arm:

- kit 조립
- servo center 확인
- 축별 단독 sweep
- safe angle 범위 기록
- 매우 가벼운 물체 pick/place 확인

### Stage B — Arduino integration

Conveyor:

- motor driver 연결
- object sensor 1개 연결
- local stop 연결
- LED state indication
- Serial command smoke

Robot Arm:

- servo power / common GND 확인
- Arduino control
- HOME / joint move / claw / STOP 구현
- Serial command smoke

### Stage C — Raspberry Pi integration

- Arduino 2대 동시 연결
- stable device mapping
- serial open/read/write timeout 확인
- device health endpoint
- Registry 등록 전 raw adapter smoke

---

## 9. Hardware Gate

### Conveyor

- [ ] belt가 손으로 부드럽게 회전한다.
- [ ] motor로 30초 이상 안정적으로 운전한다.
- [ ] belt 이탈/심한 slip이 없다.
- [ ] object sensor가 반복 감지된다.
- [ ] local stop이 Agent/MCP와 독립적으로 동작한다.
- [ ] USB Serial command / response smoke가 통과한다.
- [ ] `HALT` 후 실제 물리 정지가 확인된다.

### Robot Arm

- [ ] 모든 servo가 개별 동작한다.
- [ ] safe angle 범위를 실측했다.
- [ ] 구조 간섭 없이 HOME이 가능하다.
- [ ] 저하중 pick/place 또는 sorting을 반복할 수 있다.
- [ ] `STOP` 또는 safe pose 동작이 확인된다.
- [ ] USB Serial command / response smoke가 통과한다.

### Edge Gateway

- [ ] Raspberry Pi 3B+ boot / network가 안정적이다.
- [ ] Arduino 2대 이상을 동시에 식별한다.
- [ ] stable device mapping이 확보된다.
- [ ] serial timeout / disconnect를 감지한다.
- [ ] Registry / MCP discovery / invoke smoke가 통과한다.
- [ ] Pi 재시작 후 상태 복원 정책을 확인한다.

---

## 10. 평가용 Protocol Freeze

Hardware Gate 통과 후 Conveyor와 Robot Arm의 firmware / protocol을 먼저 동결한다.

Freeze 대상:

```text
Conveyor firmware + Serial protocol
Robot Arm firmware + Serial protocol
Setup Agent code / system prompt / examples
Operator Agent code / system prompt / examples
DeviceSpec / Capability schema
Serial Adapter
MCP Gateway
Validator / Policy / Executor
```

평가 중 허용 변경:

```text
user natural-language description
reviewed DeviceSpec / Capability data
approval / test records
Registry data
```

평가 중 firmware, Adapter, schema, system prompt, hidden mapping을 바꿔 신규 장비를 맞추면 해당 시도는 **no-code onboarding 실패**로 기록한다.

---

## 11. 현재 미확정 항목

실제 kit 수령 전에는 다음을 사실처럼 고정하지 않는다.

- Conveyor kit 정확한 SKU / 크기 / belt 폭
- Conveyor 기본 motor 전압·전류·driver 필요 여부
- Conveyor 기본 motor를 유지할지 교체할지
- G56 실제 servo 모델 / 구성품 세부 내역
- 각 Robot joint의 safe angle
- Conveyor object sensor를 IR과 HC-SR04 중 무엇으로 주력할지
- local stop의 최종 switch 형식

이 항목들은 **수령 → 단독 smoke → Hardware Gate** 순서로 확정한다.
