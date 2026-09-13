# Factory Agent Hub — Hardware Testbed Specification

> 상태: **2026-09-13 설계안 v4 / 구매 최종안 반영**  
> 목적: 기구부를 직접 설계·제작하는 데 시간을 쓰기보다, 기성 교육용 기구 kit + 보유 전자부품을 결합해 실제 Conveyor / Robot Arm 테스트베드를 빠르게 확보한다.
>
> 이 문서는 현재 하드웨어 구현의 기준 문서다. `PROJECT_PROPOSAL.md`의 과거 L-LINE 후보보다 **현재 테스트베드 구성에 대해서는 이 문서를 우선**한다. 세부 구매 수량·가격·재고 상태는 [`HARDWARE_BOM.md`](./HARDWARE_BOM.md)를 따른다.

---

## 1. 현재 확정된 테스트베드

### 1.1 Conveyor

**리브온 창의력 STEAM 목재 만들기 컨베이어 벨트**를 사용한다.

```text
외형: 약 267 × 66 × 76 mm
구매처: 쿠팡
최종 장바구니 가격: 6,680원
```

기본 frame / belt / roller / shaft / geared DC motor는 kit 구조를 우선 유지한다.

제품 사진상 motor는 **3V급 소형 brushed DC motor + 감속 gearbox 계열로 보이지만**, 실제 정격은 수령 후 label / 기본 전원 구성 / 단독 smoke로 확정한다.

motor driver는 다음으로 확정한다.

```text
DRV8833 Motor Driver Module
Model: VLT-MD012
구매처: DeviceMart
```

motor는 Arduino GPIO에서 직접 구동하지 않는다.

### 1.2 Robot Arm

기존 SciPia G56 후보 대신 **이엘사이언스 Arduino 집게 로봇팔 4관절**을 사용한다.

```text
제품: [이엘사이언스] 아두이노 집게 로봇팔
상품번호: 14062177
구매처: DeviceMart
가격: 40,000원 (VAT 별도)
```

MYLOOP 제어보드 기반 버전도 같은 계열 기구로 보이지만, 이번 프로젝트는 보유 Arduino Uno에 직접 firmware를 올리고 USB Serial protocol을 정의하므로 **Arduino 버전을 기준 제품으로 선택**한다.

제품 사진의 servo는 SG90-class micro servo와 유사하지만, **정확한 servo 모델은 실물 label 확인 전까지 확정하지 않는다.** 추가 servo는 선구매하지 않고 보유 SG90 / FS90을 spare로 둔다.

### 1.3 Edge / Controller

```text
Raspberry Pi 3B+ ×1  → Factory Edge Gateway
Arduino Uno ×2       → Conveyor / Robot Arm 전용 controller
```

Raspberry Pi 전원과 기본 부속품은 보유품을 사용한다.

### 1.4 Sensor / Local Interface

- Conveyor primary object sensor: **IR proximity sensor**
- HC-SR04: fallback / optional distance sensor
- Local stop: **상태 유지형 2-position switch**, 가능하면 NC 접점 우선
- Status: LED 또는 NeoPixel
- Buzzer / potentiometer / LCD 등은 필요할 때만 추가

일반 switch를 산업용 emergency stop이라고 부르지 않고 `local stop`으로 정의한다.

---

## 2. 시스템 구조

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

원칙:

- LLM은 Raspberry Pi나 Arduino에 임의 raw command를 직접 보내지 않는다.
- Agent는 generic MCP capability interface를 사용한다.
- Raspberry Pi가 DeviceSpec / Capability 검증과 deterministic execution을 담당한다.
- Arduino는 실제 sensor / motor / servo 제어와 local stop을 담당한다.
- Raspberry Pi에는 LLM을 올리지 않는다.
- 평가 전에 firmware / Serial protocol / Adapter / schema / Agent prompt를 동결한다.

---

## 3. 확인된 주요 보유 부품

Google Drive `부품 목록` 기준 핵심 재고:

| 분류 | 모델 / 품목 | 수량 | 우선 용도 |
|---|---|---:|---|
| MCU | Arduino Uno | 9 | 장비별 controller |
| MCU | Arduino Nano | 1 | 보조 controller |
| Edge | Raspberry Pi 3B+ | 2 | 주 Gateway / 예비 |
| Edge | Raspberry Pi 3B | 1 | 예비 |
| Edge | Raspberry Pi Zero W | 1 | Later |
| Servo | SG90 | 12 | spare / auxiliary actuator |
| Servo | FS90 | 5 | spare / gripper |
| Servo | MG996R | 1 | spare high-torque axis |
| Stepper | 28BYJ-48 | 7 | Conveyor motor fallback |
| DC motor | 소형 DC motor | 13 | Conveyor motor fallback |
| Bearing | 608ZZ | 9 | 필요 시 기구 보강 |
| Distance | HC-SR04 | 13 | fallback distance/object detect |
| Proximity | IR proximity sensor | 4 | Conveyor primary object detect |
| RFID | RC522 | 10 | optional identification |
| Display | LCD | 11 | optional local status |
| Status | NeoPixel / LED | 다수 | READY/RUNNING/ERROR |
| Input | switch / button / potentiometer | 다수 | local stop / manual control |
| Alert | buzzer | 다수 | fault / completion |

LED, 저항, 점퍼선 계열, 스위치류 등은 보유품을 우선 확인하고 부족분만 구매한다.

---

## 4. Conveyor v4

### 4.1 기구 유지 정책

```text
Conveyor kit
 ├─ Frame      → 유지
 ├─ Belt       → 유지
 ├─ Roller     → 유지
 ├─ Shaft      → 유지
 └─ Motor      → 기본 geared DC motor 우선 유지
```

motor 교체는 다음 중 하나가 확인될 때만 한다.

- Arduino + DRV8833 조합에서 안정적인 제어가 불가능
- 저하중 이송에도 토크 부족
- 30초 운전에서 비정상 과열
- 지나치게 빨라 demo 제어가 어려움
- 기구 연결이 불안정하거나 파손 위험이 큼

### 4.2 Motor Driver

**DRV8833 VLT-MD012**를 사용한다.

```text
Arduino GPIO / PWM
        │
        ▼
      DRV8833
        │
        ▼
Conveyor geared DC motor
```

기본 firmware capability 초안:

```text
RUN
HALT
SPEED <level>
OBJECT?
STATUS?
```

예상 응답:

```text
OK RUN
OK HALT
OK SPEED 2
OBJECT 1
STATE RUNNING SPEED=2 OBJECT=0
ERR ARG_RANGE
```

`SPEED` 범위, motor supply voltage, 실제 timeout은 수령 후 smoke에서 확정한다.

### 4.3 Sensor / Local Stop

```text
IR proximity sensor      → primary OBJECT detect
maintained switch        → local stop
LED / NeoPixel           → status
HC-SR04                  → fallback only
```

local stop은 Agent/MCP와 무관하게 Arduino의 deterministic path에서 최우선 처리한다.

---

## 5. Robot Arm v4 — Arduino 4-DOF Gripper Arm

### 5.1 목표

- 4-DOF로 capability onboarding 검증에 필요한 pick-and-place만 수행한다.
- 작은 sponge cube, 빈 plastic block, RFID tag가 붙은 매우 가벼운 test object만 다룬다.
- 고하중 작업, 빠른 동작, 넓은 workspace 최적화는 범위 밖이다.

### 5.2 제어 구성

```text
Arduino Uno
 ├─ base servo
 ├─ shoulder servo
 ├─ elbow servo
 └─ gripper servo
```

servo signal은 Arduino가 담당하지만, 여러 servo의 전원은 Arduino Uno 5V regulator에서 공급하지 않는다.

### 5.3 Servo Power

Robot Arm용 외부 전원은 다음으로 확정한다.

```text
AC 220V
  ↓
8자(C7) AC cable
  ↓
5V 5A regulated adapter
  ↓  DC 5.5 × 2.1 mm
VLT-DC001 terminal connector
  ↓
Servo +5V / GND rail
```

구매품:

- 5V 5A regulated adapter, DC 5.5 × 2.1 mm
- 8자(C7) AC power cable
- DC 5.5 × 2.1 terminal connector `VLT-DC001`

Arduino와 servo 전원은 **GND를 공통**으로 연결한다. 외부 5V adapter를 Arduino USB 전원과 임의로 병렬 역급전하지 않는다.

### 5.4 Serial Protocol 초안

```text
HOME
J <joint> <angle>
CLAW OPEN
CLAW CLOSE
POSE?
STOP
```

예상 응답:

```text
OK HOME
OK J 2 90
OK CLAW OPEN
POSE J1=90 J2=80 J3=110 CLAW=OPEN
ERR JOINT_RANGE
ERR ANGLE_RANGE
```

각 joint의 safe angle과 HOME pose는 **실물 조립 후 저속 sweep와 물리 간섭 측정으로만 확정**한다. `0..180` 전체를 기본 허용하지 않는다.

---

## 6. 전원 분리 원칙

전원을 역할별로 분리한다.

```text
Raspberry Pi 3B+
└─ 기존 Pi 전원

Arduino Uno ×2
└─ Raspberry Pi USB 연결

Robot Arm Servo ×4
└─ 신규 5V 5A external PSU

Conveyor motor
└─ kit 수령 후 motor 정격과 기본 전원 구성을 확인해 별도 확정
```

**5V 5A adapter의 1차 목적은 Robot Arm servo 전원**이다. Conveyor motor 전원을 이 PSU에서 파생하는 것을 기본안으로 두지 않는다.

---

## 7. 구매 계획 — v4

상세 가격과 구매처는 `HARDWARE_BOM.md`를 따른다.

### Final Buy List

| 품목 | 수량 | 상태 |
|---|---:|---|
| 리브온 목재 Conveyor kit | 1 | **구매 최종안** |
| 이엘사이언스 Arduino 집게 로봇팔 4관절 | 1 | **구매 최종안** |
| DRV8833 `VLT-MD012` | 1 | **구매 최종안** |
| DC 5.5×2.1 terminal `VLT-DC001` | 1 | **구매 최종안** |
| 5V 5A regulated adapter | 1 | **구매 최종안** |
| 8자(C7) AC cable | 1 | **구매 최종안** |

### Inventory Check

- USB data cable ×2
- maintained local switch ×2
- jumper / signal / power wire
- breadboard / terminal / distribution parts
- LED / NeoPixel
- test object

### Do Not Pre-buy

- M3 bolt / nut / washer assortment
- Ø8 shaft
- custom flat belt
- 추가 bearing
- coupler / pulley
- 추가 servo
- 대형 3D printed mechanical parts
- step-down converter

---

## 8. 3D Printing 범위

기구 전체 제작이 아니라 필요한 adapter/bracket만 출력한다.

```text
Arduino mount
IR sensor bracket
local-stop bracket
Pi / cable management bracket
Robot test-object / jig
RFID tag holder
small spacer / shim
```

Major frame / roller / robot link는 기성 kit를 사용한다.

---

## 9. Hardware Bring-up 순서

### Stage A — Kit Inventory / Mechanical Smoke

Conveyor:

- frame / belt / roller 조립
- belt 폭 실측
- motor label / 기본 전원 구성 기록
- hand rotation
- motor 단독 구동
- belt slip / derailment 확인

Robot Arm:

- 구성품 inventory 기록
- servo model label 기록
- servo center 확인
- 축별 아주 좁은 범위부터 sweep
- safe angle / HOME 후보 기록

### Stage B — Arduino Integration

Conveyor:

- DRV8833 연결
- motor supply 결정
- IR sensor 연결
- local stop 연결
- Serial command smoke

Robot Arm:

- 5V 5A external servo power 구성
- common GND 확인
- Arduino control
- local stop 연결
- HOME / joint / claw / STOP 구현
- Serial command smoke

### Stage C — Raspberry Pi Integration

- Arduino 2대 동시 연결
- stable device mapping
- serial open/read/write timeout 확인
- device health endpoint
- Registry 등록 전 raw adapter smoke

---

## 10. Hardware Gate

### Conveyor

- [ ] belt가 손으로 부드럽게 회전한다.
- [ ] motor 정격/전원 구성을 기록했다.
- [ ] DRV8833으로 30초 이상 안정적으로 운전한다.
- [ ] belt 이탈/심한 slip이 없다.
- [ ] IR object sensor가 반복 감지된다.
- [ ] local stop이 Agent/MCP와 독립적으로 동작한다.
- [ ] USB Serial command / response smoke가 통과한다.
- [ ] `HALT` 후 실제 물리 정지가 확인된다.

### Robot Arm

- [ ] 모든 servo가 개별 동작한다.
- [ ] servo model을 기록했다.
- [ ] 5V 5A external PSU에서 안정적으로 구동된다.
- [ ] safe angle 범위를 실측했다.
- [ ] 구조 간섭 없이 HOME이 가능하다.
- [ ] 저하중 pick/place 또는 sorting을 반복할 수 있다.
- [ ] local stop / `STOP` 또는 safe pose 동작이 확인된다.
- [ ] USB Serial command / response smoke가 통과한다.

### Edge Gateway

- [ ] Raspberry Pi 3B+ boot / network가 안정적이다.
- [ ] Arduino 2대를 동시에 식별한다.
- [ ] stable device mapping이 확보된다.
- [ ] serial timeout / disconnect를 감지한다.
- [ ] Registry / MCP discovery / invoke smoke가 통과한다.
- [ ] Pi 재시작 후 상태 복원 정책을 확인한다.

---

## 11. 평가용 Freeze

Hardware Gate 통과 후 다음을 commit/hash로 동결한다.

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

## 12. 수령 전 남은 미확정 항목

구매 선택은 닫혔고, 실물이 없으면 확정할 수 없는 값만 남긴다.

| 항목 | 수령 후 확정 방법 |
|---|---|
| Conveyor 실제 belt 폭 | 실측 |
| Conveyor motor 정확한 정격 전압 / 전류 | label / 기본 전원 / 단독 측정 |
| Conveyor motor supply | motor 사양과 kit 구성 확인 후 결정 |
| Robot Arm 실제 servo 모델 | servo label 확인 |
| Robot joint safe angle / HOME pose | 저속 sweep / 물리 간섭 실측 |
| local stop switch의 실제 접점 형식 | continuity test |
| USB data cable / 배선 재고 | 현물 확인 |

다음 항목은 더 이상 미확정이 아니다.

```text
Conveyor kit       = 리브온 목재 Conveyor
Motor driver       = DRV8833 VLT-MD012
Object sensor      = IR proximity primary
Robot Arm          = 이엘사이언스 Arduino 집게 로봇팔 4관절
Servo PSU          = regulated 5V 5A external adapter
PSU connector      = DC 5.5×2.1 + VLT-DC001
AC cable           = C7 figure-8 cable
Edge Gateway       = Raspberry Pi 3B+
Device controller  = Arduino Uno ×2
```

수령 후에는 **kit inventory → 단독 smoke → 남은 전원/배선 확정 → Hardware Gate** 순서로 진행한다.
