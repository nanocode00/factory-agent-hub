# Factory Agent Hub — Hardware Testbed Specification

> 상태: **2026-09-12 설계안 v3**  
> 목적: 기구부를 직접 설계·제작하는 데 시간을 쓰기보다, 저가 기성 기구 kit + 보유 전자부품을 결합해 실제 Conveyor / Robot Arm 테스트베드를 빠르게 확보한다.
>
> 이 문서는 현재 하드웨어 구현의 기준 문서다. `PROJECT_PROPOSAL.md`의 과거 L-LINE 후보보다 **현재 테스트베드 구성에 대해서는 이 문서를 우선**한다. kit 밖의 세부 부품 목록과 구매 상태는 [`HARDWARE_BOM.md`](./HARDWARE_BOM.md)를 따른다.

---

## 1. 현재 결정사항

### 1.1 테스트베드 전략

기존의 `축 + 베어링 + 평벨트 + 3D 프린트 프레임` 방식으로 Conveyor를 직접 제작하고 Robot Arm을 직접 모델링하는 계획은 **보류**한다.

현재 기준은 다음과 같다.

- Conveyor: **리브온 창의력 STEAM 목재 만들기 컨베이너벨트 267 × 66 × 76 mm**를 우선 구매 SKU로 사용한다.
  - 기구 frame / belt / roller / shaft는 kit 구조를 우선 유지한다.
  - 기본 motor도 **우선 유지**하고, 단독 smoke에서 제어 불가·토크 부족·과열·과속·driver 부적합이 확인될 때만 교체한다.
  - belt 폭과 motor 전기 사양은 공개 판매정보로 확인되지 않으므로 수령 후 실측한다.
- Robot Arm: **SciPia G56 4-DOF Arduino Robot Arm Starter Kit**를 사용한다.
  - 6-DOF 고하중 arm보다 비용, 전원, calibration, 충돌 위험을 줄인다.
  - 매우 가벼운 물체의 pick-and-place / sorting만 목표로 한다.
  - 추가 servo는 선구매하지 않고 보유 SG90 / FS90 등을 spare로 둔다.
- Conveyor object sensor: **IR proximity sensor를 주 센서**로 사용한다.
  - HC-SR04는 fallback / optional distance sensor로 남긴다.
- Local stop: **상태 유지형 2-position switch**를 사용한다.
  - 보유품 중 가능하면 NC 접점이 있는 switch를 우선한다.
  - 일반 switch를 산업용 emergency stop이라고 부르지 않고 `local stop`으로 정의한다.
- Edge Gateway: **Raspberry Pi 3B+ 1대**를 사용한다.
- Device controller: **Arduino Uno 2대**를 장비별로 분리한다.
- shaft, custom endless flat belt, M3 assortment 등은 **선구매하지 않는다**. kit 조립 후 실제 부족분만 산다.

구매 기준 상품:

- Conveyor: https://item.gmarket.co.kr/Item?goodsCode=4532930639
- G56: https://scipia.com/product/detail.html?product_no=591

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
| Servo | SG90 | 12 | spare / auxiliary actuator |
| Servo | FS90 | 5 | spare / gripper |
| Servo | EF92A | 1 | spare |
| Servo | MG996R | 1 | spare high-torque axis |
| Stepper | 28BYJ-48 | 7 | Conveyor motor fallback |
| Stepper driver | 모델 미확인 | 7 | 28BYJ-48 구동 |
| DC motor | 소형 DC motor | 13 | Conveyor motor fallback |
| Motor | 기타 소형 motor | 20 | spare |
| Bearing | 608ZZ | 9 | 필요 시 기구 보강 / spare |
| Distance | HC-SR04 | 13 | fallback distance/object detect |
| Distance | SRF05 | 2 | fallback distance |
| Proximity | IR proximity sensor | 4 | **Conveyor primary object detect** |
| RFID | RC522 | 10 | optional object/card identification |
| Display | LCD | 11 | local status optional |
| Status | NeoPixel / LED 계열 | 다수 | READY/RUNNING/ERROR |
| Input | joystick | 7 | manual jog / calibration |
| Input | switch / button / potentiometer | 다수 | local stop / manual control |
| Alert | buzzer | 다수 | fault / completion |
| 기타 | MPU-6050, DHT, PIR, microphone, RTC, relay 등 | 다수 | spare Device / sensor station |

LED, 저항, 포텐쇼미터, 부저, 스위치 등 기본 수동소자도 충분히 보유한 것으로 본다. Raspberry Pi 전원과 기본 부속품도 별도 보유한다.

---

## 3. Conveyor v3

### 3.1 선택 기구

우선 구매 SKU:

```text
리브온 창의력 STEAM 목재 만들기 컨베이너벨트
외형: 267 × 66 × 76 mm
수량: 1
```

판매 페이지에서 외형 크기는 확인되지만 **belt 폭, motor 정격 전압·전류, motor driver 방식은 확인되지 않는다.** 이 값은 수령 후 측정한다.

### 3.2 유지 / 교체 정책

```text
Conveyor kit
 ├─ Frame      → 유지
 ├─ Belt       → 유지
 ├─ Roller     → 유지
 ├─ Shaft      → 유지
 └─ Motor      → 우선 유지
                    │
                    ├─ smoke 통과 → 그대로 사용
                    └─ smoke 실패 → 보유 motor + 적합 driver로 교체
```

motor 교체 조건:

- Arduino에서 안전하게 제어할 방법이 없음
- 저하중 이송에도 토크 부족
- 30초 운전에서 비정상 과열
- 감속 없이 지나치게 빨라 demo 제어가 어려움
- 적합 driver를 구하기보다 보유 motor/driver 조합이 더 단순함

motor는 Arduino GPIO에서 직접 구동하지 않는다.

### 3.3 Sensor / local interface

기본 구성은 다음으로 고정한다.

```text
IR proximity sensor       → primary OBJECT detect
HC-SR04                   → fallback / optional distance
maintained local switch   → local stop
NeoPixel / LED            → state indication
buzzer                     → optional fault / completion
potentiometer              → optional manual speed
```

Local stop은 Agent/MCP 상태와 무관하게 Arduino의 deterministic path에서 처리한다. driver에 enable/standby 입력이 있으면 가능한 경우 motor disable에도 사용한다.

### 3.4 Serial protocol 초안

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

`SPEED` 범위와 실제 timeout은 motor/driver smoke 후 freeze한다.

---

## 4. Robot Arm v3 — G56 4-DOF

### 4.1 선택

**SciPia G56 4-DOF Arduino Robot Arm Starter Kit**를 사용한다.

- 4-DOF로 Factory Agent Hub의 capability onboarding 검증에 충분하다.
- 고하중 작업은 범위 밖이다.
- 작은 sponge cube, 빈 plastic block, RFID tag가 붙은 매우 가벼운 test object만 다룬다.
- 실제 servo 모델은 판매 페이지 텍스트에서 확정할 수 없으므로 수령 후 label로 확인한다.
- servo 추가 구매는 하지 않는다. 보유 SG90 / FS90 등을 spare로 사용한다.

### 4.2 제어 구성

```text
Arduino Uno
 ├─ base servo
 ├─ shoulder servo
 ├─ elbow servo
 └─ gripper servo
```

여러 servo를 Arduino Uno 5V regulator에서 직접 공급하지 않는다. **외부 regulated 5V servo power**를 사용하고 Arduino와 common GND를 구성한다. 보유 전원의 적합 여부를 먼저 확인하고, 없을 때만 약 4A급 전원을 추가 구매한다.

### 4.3 Serial protocol 초안

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

각 joint의 safe angle은 **수령 후 실제 기구 간섭을 측정해서만 확정**한다. `0..180` 전체를 기본 허용하지 않는다.

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

USB device path가 재부팅마다 바뀔 수 있으므로 `/dev/ttyACM*` 문자열을 영구 ID로 사용하지 않는다. VID/PID, USB serial, udev symlink 등을 이용해 **stable device mapping**을 확보한다.

---

## 6. 구매 계획 — v3

세부 BOM은 [`HARDWARE_BOM.md`](./HARDWARE_BOM.md)에 분리한다.

### Buy Now

| 품목 | 수량 | 상태 |
|---|---:|---|
| 리브온 267 × 66 × 76 mm Conveyor kit | 1 | **구매 대상으로 결정** |
| SciPia G56 4-DOF Robot Arm kit | 1 | **구매 대상으로 결정** |

### Inventory Check First

| 품목 | 판단 |
|---|---|
| USB data cable ×2 | 충전 전용이 아닌 data cable인지 확인 |
| maintained local switch ×2 | 가능하면 NC 접점 여부 확인 |
| regulated 5V ~4A servo power | G56용 보유 여부 확인 |
| jumper / power wiring / terminal | 실제 조립에 충분한지 확인 |
| Conveyor용 motor driver | kit motor 사양 측정 후 보유 driver 적합성 확인 |

### Do Not Pre-buy

- M3 bolt / nut / washer assortment
- Ø8 shaft
- custom flat belt
- 추가 bearing
- coupler / pulley
- 추가 servo
- 대형 3D printed mechanical parts

---

## 7. 3D Printing 범위

기구 전체 제작이 아니라 **필요한 adapter/bracket만 출력**한다.

```text
Arduino mount
IR sensor bracket
local-stop bracket
Pi / cable management bracket
Conveyor motor adapter       # motor 교체 시에만
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
- belt 폭 실측
- hand rotation 확인
- motor 종류 / label / 정격 확인
- motor 단독 구동
- belt slip / derailment 확인

Robot Arm:

- kit 구성품 inventory 기록
- servo model label 기록
- servo center 확인
- 축별 단독 sweep
- safe angle 범위 측정
- 매우 가벼운 물체 pick/place 확인

### Stage B — Arduino integration

Conveyor:

- 적합 motor driver 연결
- IR object sensor 연결
- maintained local stop 연결
- LED state indication
- Serial command smoke

Robot Arm:

- 외부 servo power / common GND 확인
- Arduino control
- local stop 연결
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
- [ ] IR object sensor가 반복 감지된다.
- [ ] local stop이 Agent/MCP와 독립적으로 동작한다.
- [ ] USB Serial command / response smoke가 통과한다.
- [ ] `HALT` 후 실제 물리 정지가 확인된다.

### Robot Arm

- [ ] 모든 servo가 개별 동작한다.
- [ ] servo model / power 구성을 기록했다.
- [ ] safe angle 범위를 실측했다.
- [ ] 구조 간섭 없이 HOME이 가능하다.
- [ ] 저하중 pick/place 또는 sorting을 반복할 수 있다.
- [ ] local stop / `STOP` 또는 safe pose 동작이 확인된다.
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

## 11. 수령 전 남은 미확정 항목

결정 가능한 항목은 v3에서 닫았다. 실제 kit가 없으면 확정할 수 없는 항목만 아래에 남긴다.

| 항목 | 수령 후 확정 방법 |
|---|---|
| Conveyor 실제 belt 폭 | 실측 |
| Conveyor motor 종류 / 정격 전압 / 소비·정지 전류 | label 확인 + 안전한 단독 측정 |
| Conveyor motor driver | 위 motor 사양과 보유 driver를 대조한 뒤 결정 |
| G56 실제 servo 모델 / 세부 구성품 | 포장·servo label·구성품 inventory 확인 |
| G56 각 joint safe angle / HOME pose | 저속 sweep와 물리 간섭 실측 |
| 보유 local stop switch의 NC 가능 여부 | 부품 확인 / continuity test |
| G56용 외부 5V servo 전원의 보유품 적합성 | 정격 출력 확인 후 부하 smoke |

다음 항목은 더 이상 미확정이 아니다.

```text
Conveyor SKU       = 리브온 267 × 66 × 76 mm 모델
Conveyor motor     = 기본 motor 우선 유지, 실패 시에만 교체
Object sensor      = IR proximity primary / HC-SR04 fallback
Local stop policy  = maintained 2-position switch, NC preferred
Robot Arm          = SciPia G56 4-DOF
Edge Gateway       = Raspberry Pi 3B+
Device controller  = Arduino Uno ×2
```

수령 후에는 **kit inventory → 단독 smoke → 조건부 BOM 확정 → Hardware Gate** 순서로 진행한다.
