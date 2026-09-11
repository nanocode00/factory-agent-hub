# Factory Agent Hub — Hardware Testbed Specification

> 상태: **2026-09-11 기준 설계안 v1**  
> 목적: 16만 원대 교육용 키트를 구매하지 않고, 보유 전자부품 + 3D 프린팅 기구부 + 최소 기계부품 구매로 실제 Conveyor / Robot Arm 테스트베드를 구성한다.
>
> 이 문서는 현재 하드웨어 구현의 기준 문서다. `PROJECT_PROPOSAL.md`에 남아 있는 L-LINE 키트 후보 내용보다 **현재 테스트베드 구성에 대해서는 이 문서를 우선**한다. 제품 가설과 Build Gate 자체는 `PROJECT_PROPOSAL.md`를 따른다.

---

## 1. 현재 결론

기성 L-LINE 컨베이어/로봇팔 키트 구매는 **보류**한다.

현재 보유 부품이 충분하므로 다음 구조를 우선한다.

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
  └─ USB Serial → Arduino #2 → Robot Arm / Sorter
```

원칙:

- LLM은 Raspberry Pi나 Arduino를 직접 raw command로 제어하지 않는다.
- Agent는 MCP의 generic capability interface를 사용한다.
- Raspberry Pi가 검증된 DeviceSpec / Capability를 바탕으로 실행 계층을 제공한다.
- Arduino는 실제 센서·모터의 로컬 제어와 정지 동작을 담당한다.
- Raspberry Pi에는 LLM을 올리지 않는다. Pi는 Edge Gateway 역할에 집중한다.
- 실제 평가 전에 firmware / Serial protocol / Adapter / schema / Agent prompt를 동결한다.

---

## 2. 확인된 주요 보유 부품

Google Drive의 `부품 목록`을 기준으로 현재 확인된 핵심 재고다.

| 분류 | 모델 / 품목 | 수량 | 우선 용도 |
|---|---|---:|---|
| MCU | Arduino Uno | 9 | 장비별 로컬 컨트롤러 |
| MCU | Arduino Nano | 1 | 소형 보조 컨트롤러 |
| Edge | Raspberry Pi 3B | 1 | 예비 Gateway |
| Edge | Raspberry Pi 3B+ | 2 | **주 Edge Gateway 후보** |
| Edge | Raspberry Pi Zero W | 1 | Later / 보조 노드 |
| Servo | SG90 | 12 | Robot Arm / Gripper / Diverter |
| Servo | FS90 | 5 | Robot Arm / Gripper |
| Servo | EF92A | 1 | 예비 |
| Servo | MG996R | 1 | Robot Arm 고하중 축 |
| Stepper | 28BYJ-48 | 7 | Conveyor 구동 후보 |
| Stepper driver | 모델 미확인 | 7 | 28BYJ-48 구동 |
| DC motor | 소형 DC motor | 13 | Conveyor 대체 구동 / 보조 |
| Motor | 기타 소형 motor | 20 | 예비 |
| Bearing | 608ZZ | 9 | Conveyor roller / 회전 지지 |
| Distance | HC-SR04 | 13 | 물체 감지 / 거리 |
| Distance | SRF05 | 2 | 물체 감지 / 거리 |
| Proximity | IR 근접센서 | 4 | Conveyor object detect |
| RFID | RC522 | 10 | 물체/카드 식별 장비 |
| Display | LCD | 11 | 로컬 상태 표시 |
| Status | NeoPixel / LED 계열 | 다수 | READY/RUNNING/ERROR 표시 |
| Input | Joystick | 7 | 수동 jog / calibration |
| Input | Switch / button / potentiometer | 다수 | local stop / manual control |
| Alert | Buzzer | 다수 | 오류/완료 알림 |
| 기타 | MPU-6050, DHT 계열, PIR, microphone, RTC, relay 등 | 다수 | 예비 Device / sensor station |

추가로 LED, 저항, 포텐쇼미터, 부저, 스위치 등 기본 수동소자는 충분히 보유한 것으로 확인했다.

---

## 3. Conveyor v1 기구 명세

### 3.1 목표

- 탁상형 소형 Conveyor
- 작은 블록, RFID 카드 부착 물체, 가벼운 테스트 물체 운반
- 복잡한 산업용 기구가 아니라 Agent onboarding / orchestration을 검증하기 위한 testbed
- 부품 고장이나 벨트 슬립이 생겨도 쉽게 분해·재출력 가능하도록 모듈형으로 구성

### 3.2 기준 치수

| 항목 | v1 권장값 |
|---|---:|
| Belt width | **60 mm** |
| Belt endless circumference | **약 800 mm** |
| Belt thickness | **약 0.8~1.5 mm 권장** |
| Belt material | PU 또는 PVC 계열 평벨트 |
| Roller diameter | **Ø32 mm 전후** |
| Roller usable width | **70 mm** |
| Roller center distance | **약 350 mm nominal** |
| Overall length | **약 420~450 mm** |
| Overall width | **약 100~110 mm** |
| Shaft | **Ø8 mm × 150 mm × 2** |
| Bearing | **608ZZ × 4** |
| Tension adjustment | **총 15~20 mm 정도** |
| Frame printed wall/thickness | 약 4~5 mm부터 시작 |

벨트 길이와 롤러 중심거리는 아래를 초기값으로 사용한다.

```text
Belt length ≈ 2 × center_distance + π × roller_diameter

800 ≈ 2C + π × 32
C ≈ 350 mm
```

실제 구매한 벨트의 실측 둘레를 기준으로 CAD의 center distance / tension slot을 최종 조정한다.

### 3.3 Roller / Bearing 구조

608ZZ 표준 치수는 다음을 기준으로 설계한다.

```text
ID  = 8 mm
OD  = 22 mm
W   = 7 mm
```

권장 구조는 **고정 Ø8 mm shaft + roller 내부 608ZZ** 방식이다.

```text
Frame       Rotating Roller                    Frame
 │        ┌──────────────────────────┐           │
 ├─8mm──[608ZZ]                  [608ZZ]──8mm────┤
 │        └──────────────────────────┘           │
```

- Shaft는 프레임에 고정한다.
- Bearing outer race를 roller에 끼워 roller가 shaft 주위를 회전한다.
- Drive gear는 drive roller 측면에 체결한다.
- 608ZZ 9개 중 기본 Conveyor에 4개 사용하고 5개는 예비/Robot Base용으로 남긴다.

### 3.4 Conveyor actuator

우선순위 1은 보유한 `28BYJ-48 + 전용 driver`다.

```text
28BYJ-48
   │
3D printed small gear
   ⚙
    ⚙ 3D printed large gear
        │
   Drive Roller
```

이유:

- 저속 제어가 쉽다.
- 방향 전환이 쉽다.
- 보유 driver를 그대로 사용할 수 있다.
- 별도 DC motor driver 구매가 필요하지 않다.
- 데모 속도/위치 제어가 결정적이다.

단독 smoke에서 토크가 부족하면 보유 DC motor + 적합 driver 방식으로 전환한다. 전환 시 firmware/Serial protocol freeze 전에 결정한다.

### 3.5 Conveyor sensor / local interface

우선 후보:

```text
IR proximity or HC-SR04 → object detect
Switch                  → local stop
Potentiometer           → optional manual speed
NeoPixel / LED          → state indication
Buzzer                  → fault / completion
```

Agent/MCP와 별개로 **local stop**을 둔다. 일반 택트/토글 스위치를 산업용 emergency stop이라고 부르지 않는다.

---

## 4. Robot Arm / Sorter v1 기구 명세

### 4.1 목표

- 복잡한 고하중 Robot Arm보다 **짧고 가벼운 pick-and-place / sorting arm**을 우선한다.
- 대상 물체는 작은 스펀지 큐브, 빈 플라스틱 블록, RFID 카드가 붙은 매우 가벼운 물체를 기준으로 한다.
- Servo 토크 한계를 넘기지 않는 것이 기능 수보다 중요하다.

### 4.2 초기 치수

| 항목 | v1 권장값 |
|---|---:|
| Base footprint | 약 **100 × 100 mm** |
| Upper arm joint distance | **90~100 mm** |
| Forearm joint distance | **80~90 mm** |
| Wrist section | **40~60 mm** |
| Gripper overall width | 약 **60~70 mm** |
| Target reach | 약 **200~250 mm 이하** |

### 4.3 Servo 배치 후보

```text
MG996R      → Shoulder (가장 큰 하중)
SG90/FS90   → Base rotation
SG90        → Elbow
SG90/FS90   → Wrist
SG90/FS90   → Gripper
```

Base는 남는 608ZZ로 하중을 지지하고 Servo는 회전 토크 위주로 담당하도록 설계하는 것을 우선 검토한다.

Robot Arm이 일정 위험을 만들 경우 `Robot Arm`을 완성하려고 무리하지 않고 **1~2축 Sorter / Diverter + Gripper**로 축소한다. 핵심 검증은 기구 자유도가 아니라 서로 다른 실제 장비의 capability onboarding이다.

---

## 5. Raspberry Pi Edge Gateway

주 후보는 **Raspberry Pi 3B+ 1대**다. 전원과 기본 부속품은 보유 중이다.

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

---

## 6. 구매해야 할 기계부품 — 현재 기준

전자부품은 현재 추가 구매하지 않는 것을 기본으로 한다.

### Buy Now

| 품목 | 권장 규격 | 수량 | 이유 |
|---|---|---:|---|
| Precision / linear shaft | **Ø8 mm × 150 mm** | 2개, 예비 포함 시 3개 | 608ZZ용 Conveyor roller shaft |
| Endless flat belt | **폭 60 mm, 둘레 약 800 mm, PU/PVC, 0.8~1.5 mm** | 1개 | Conveyor belt |
| M3 machine screw assortment | M3×8/10/12/16/20/25/30 중심 | 1세트 | Frame/printed part assembly |
| M3 nuts | 일반 + 가능하면 nyloc 일부 | 1세트 | 풀림 방지 |
| M3 washers | 평와셔 중심 | 1세트 | PLA/PETG 표면 하중 분산 |

### Optional / CAD 확정 후

| 품목 | 조건 |
|---|---|
| M3 heat-set insert | 반복 분해가 많은 3D printed joint에 사용하고 싶을 때 |
| M4 bolt/nut/washer | tensioner / frame 일부를 M4로 설계할 때만 |
| Spacer / collar | shaft 위치 고정이 출력 spacer만으로 불안정할 때 |
| 추가 belt | 첫 벨트가 너무 미끄럽거나 두께/최소 pulley 직경이 맞지 않을 때 |

### 구매하지 않음

- 608ZZ: 9개 보유
- Arduino / Raspberry Pi
- SG90 / FS90 / MG996R Servo
- 28BYJ-48 / driver
- HC-SR04 / IR sensor / RFID / LCD / LED
- switch / potentiometer / buzzer / resistor
- 기성 Robot Arm / Conveyor kit

---

## 7. 3D 프린팅 대상

Conveyor:

```text
bearing-fit test coupon
side frame / bearing holder
drive roller
idler roller
stepper mount
small / large drive gear
tension slider / slot block
sensor bracket
local-stop bracket
cable clips / spacers
```

Robot Arm:

```text
base
bearing-supported turntable if used
servo brackets
upper-arm link
forearm link
wrist bracket
gripper fingers / body
cable guides
```

### Bearing fit 시험

전체 부품보다 먼저 작은 coupon을 출력한다.

```text
Ø22.0 mm
Ø22.2 mm
Ø22.4 mm
```

실제 프린터/재료에서 608ZZ가 적당히 들어가는 치수를 고른 뒤 production STL에 반영한다.

---

## 8. 아직 Freeze하지 않은 항목

다음은 실제 부품 구매/시험 후 확정한다.

- 구매 Belt의 정확한 material / thickness / measured circumference
- 실제 28BYJ-48 gearbox 출력축 치수와 gear fit
- 보유 stepper driver 모델명
- 3D printer의 소재(PLA/PETG), nozzle, 실제 치수 공차
- Robot Arm 최종 DOF
- MG996R 및 SG90/FS90의 실제 상태/토크 편차
- Conveyor object sensor를 IR과 HC-SR04 중 무엇으로 주력할지
- Frame를 전량 출력할지, 평판 재료 + 출력 bracket의 hybrid로 갈지

이 항목은 **구매/단독 smoke 전에 사실처럼 고정하지 않는다.**

---

## 9. Hardware Gate

### Conveyor

- [ ] 608ZZ ×4 회전/끼움 확인
- [ ] Ø8 shaft fit 확인
- [ ] Belt 장력 조정 범위 확보
- [ ] 28BYJ-48 단독 구동 성공
- [ ] Motor/driver 과열 없음
- [ ] object sensor 반복 감지
- [ ] local stop이 Agent/MCP와 독립적으로 동작
- [ ] USB Serial command / response smoke

### Robot Arm / Sorter

- [ ] Servo 개별 sweep / center 확인
- [ ] 외부 Servo 전원 사용 및 common GND 확인
- [ ] 최대 자세에서 구조 간섭 없음
- [ ] 저하중 pick/place 또는 sorting 반복 동작
- [ ] local stop / safe pose 확인
- [ ] USB Serial command / response smoke

### Edge Gateway

- [ ] Raspberry Pi 3B+ boot / network 안정
- [ ] Arduino 2대 이상 USB Serial 동시 식별
- [ ] 장비별 stable device mapping
- [ ] Registry / MCP discovery / invoke smoke
- [ ] Pi 재시작 후 상태 복원 정책 확인

---

## 10. 평가 시 Freeze 기준

실제 no-code onboarding 평가를 시작하기 전에 다음을 commit/hash로 고정한다.

```text
Setup Agent code / system prompt / examples
Operator Agent code / system prompt / examples
DeviceSpec / Capability schema
Serial Adapter
MCP Gateway
Validator / Policy / Executor
Conveyor firmware + Serial protocol
Robot/Sorter firmware + Serial protocol
```

평가 중 허용 변경:

```text
user natural-language description
reviewed DeviceSpec / Capability data
approval / test records
Registry data
```

평가 중 firmware, Adapter, schema, system prompt, hidden mapping을 바꿔 새 장비를 맞추면 해당 시도는 **no-code onboarding 실패**로 기록한다.
