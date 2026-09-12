# Factory Agent Hub — Hardware BOM

> 상태: **2026-09-12 BOM v1**  
> 기준: `HARDWARE_SPEC.md`의 저가 Conveyor kit + SciPia G56 4-DOF + Raspberry Pi 3B+ 구성  
> 목적: **기구 kit 자체에 기대하는 부품과 Factory Agent Hub가 별도로 준비해야 하는 부품을 분리**해, 불필요한 선구매를 막는다.

---

## 1. 구매하는 두 기구 kit

| 구분 | 선택품 | 수량 | 현재 확인된 정보 |
|---|---|---:|---|
| Conveyor | **리브온 창의력 STEAM 목재 만들기 컨베이너벨트** | 1 | 완성 크기 267 × 66 × 76 mm. belt 폭과 motor 전기 사양은 수령 후 실측 |
| Robot Arm | **SciPia G56 4-DOF Arduino Robot Arm Starter Kit** | 1 | 4-DOF, 판매가 43,900원 기준. 실제 servo 모델과 세부 구성품은 수령 후 확인 |

Conveyor 후보 링크: https://item.gmarket.co.kr/Item?goodsCode=4532930639  
G56 공식 상품 링크: https://scipia.com/product/detail.html?product_no=591

두 kit는 **기구 구조를 빠르게 확보하기 위한 testbed**다. 제품 가설은 kit 성능이 아니라, 서로 다른 실제 장비를 고정 Serial Adapter / DeviceSpec / MCP 경계에서 등록·발견·실행할 수 있는지로 검증한다.

---

## 2. Kit 밖에서 반드시 필요한 BOM

| 품목 | 수량 | 상태 | 용도 / 결정 |
|---|---:|---|---|
| Raspberry Pi 3B+ | 1 | **보유 확인** | Factory Edge Gateway |
| Raspberry Pi 전원 / microSD / 기본 부속품 | 1 set | **보유 확인** | Pi 구동 |
| Arduino Uno | 2 | **보유 확인 (9개)** | Conveyor / Robot 각각 전용 controller |
| USB data cable | 2 | **재고 확인 필요** | Pi ↔ Arduino Serial. 충전 전용 케이블 제외 |
| IR proximity sensor | 1 | **보유 확인 (4개)** | Conveyor 주 object sensor |
| maintained 2-position switch | 2 권장 | **형식 확인 필요** | 장비별 local stop. 가능하면 NC 접점 우선 |
| LED 또는 NeoPixel | 2 | **보유 확인** | 장비별 READY / RUNNING / ERROR 상태 표시 |
| jumper wire / signal wire | 적정량 | **재고 확인 필요** | Arduino ↔ sensor / switch / driver / servo |
| breadboard 또는 terminal / distribution 부품 | 1~2 set | **재고 확인 필요** | 전원·신호 배선 정리 |
| GND / power distribution wiring | 적정량 | **재고 확인 필요** | 외부 전원과 Arduino common GND 구성 |
| 가벼운 test object | 2~3 | 제작 가능 | pick/place 및 Conveyor 이송용. 3D print / foam / cardboard 가능 |

`maintained switch`는 순간 복귀형 push button보다 **상태가 유지되는 토글/락킹 방식**을 우선한다. 일반 switch를 산업용 emergency stop이라고 부르지 않고, 본 프로젝트에서는 `local stop`으로 정의한다.

---

## 3. 재고 확인 후에만 구매하는 조건부 BOM

| 품목 | 조건 | 권장 방향 |
|---|---|---|
| Robot servo 외부 전원 | G56용으로 적합한 보유 전원이 없을 때 | **5V regulated, 약 4A급 권장**. Arduino 5V regulator로 여러 servo를 공급하지 않음 |
| Conveyor motor driver | kit 기본 motor를 유지하고, 보유 driver가 그 motor에 맞지 않을 때 | motor 전압/정지전류 측정 후 결정. 소형 DC motor라면 TB6612FNG / DRV8833 계열 우선 검토 |
| Conveyor 별도 motor 전원 | kit 기본 전원 방식이 Arduino integration에 부적합할 때 | motor 실측 전압·전류에 맞춰 구매 |
| connector / terminal block | 보유 jumper/breadboard만으로 배선이 불안정할 때 | 저전압 DC용 소형 terminal 사용 |
| cable tie / 양면테이프 / hot glue | kit에 sensor/switch를 고정할 수단이 없을 때 | 임시 testbed 고정용 |
| 3D printed bracket | 실제 kit hole/형상과 sensor가 맞지 않을 때 | sensor / Arduino / switch adapter만 출력 |

Conveyor motor driver는 **kit 수령 전 선구매하지 않는다.** motor가 DC인지, 요구 전압·전류가 얼마인지 확인한 뒤 결정한다.

---

## 4. 현재 구매하지 않는 품목

아래는 직접 기구를 제작하던 v1 계획에서는 후보였지만, 기성 kit 전략으로 변경하면서 기본 BOM에서 제거한다.

| 품목 | 현재 판단 |
|---|---|
| Ø8 mm shaft | 구매 안 함 |
| custom PU/PVC endless flat belt | 구매 안 함 |
| 추가 608ZZ | 구매 안 함 — 9개 보유 |
| M3 bolt / nut / washer assortment | **선구매 안 함** — kit 조립 후 정말 필요할 때만 |
| 추가 SG90 / FS90 / MG996R | 구매 안 함 — 보유 spare 사용 |
| 대형 Conveyor frame / roller 3D print | 하지 않음 |
| Robot Arm link / base 전체 3D print | 하지 않음 |
| RFID reader | 추가 구매 안 함 — RC522 10개 보유, demo 확장 시 사용 |
| HC-SR04 | 추가 구매 안 함 — 13개 보유, IR sensor의 fallback |

---

## 5. 장비별 조립 BOM

### Conveyor node

```text
[Conveyor mechanical kit]
        +
Arduino Uno ×1
IR proximity sensor ×1
local stop switch ×1
status LED / NeoPixel ×1
USB data cable ×1
motor driver ×1       # 조건부: kit motor와 보유 driver 확인 후
motor power ×1        # 조건부
wiring / mount
```

기본 motor는 **우선 유지**한다. 단독 smoke에서 제어 불가, 토크 부족, 과열, 지나친 속도, driver 부적합 중 하나가 확인될 때만 보유 motor로 교체한다.

### Robot Arm node

```text
[G56 4-DOF mechanical/servo kit]
        +
Arduino Uno ×1
local stop switch ×1
status LED / NeoPixel ×1
USB data cable ×1
external regulated servo power ×1   # 보유 여부 확인
common GND wiring
```

G56의 servo를 Arduino Uno 5V regulator에서 직접 여러 개 구동하지 않는다. Robot의 joint safe angle은 조립 후 물리 간섭을 측정하여 firmware에 제한한다.

### Edge Gateway

```text
Raspberry Pi 3B+ ×1
Pi power / microSD / network
USB data cable ×2
```

Pi에는 LLM을 올리지 않고 MCP / Registry / validation / deterministic executor / Serial routing / SQLite audit을 담당시킨다.

---

## 6. 수령 직후 BOM 확인 체크

Conveyor 수령 직후 기록:

```text
actual overall size
belt width
motor type
motor label / rated voltage if present
no-load current / stall-current estimate where safely measurable
included power source
shaft / roller accessibility
motor ↔ roller coupling
```

G56 수령 직후 기록:

```text
servo model labels
servo count
included fasteners / horn / cable
Arduino 포함 여부
전원 관련 구성품
joint mechanical limits
HOME candidate pose
```

이 결과로 조건부 BOM을 닫는다. **수령 전에 확인할 수 없는 값을 추정해서 driver, power supply, fastener를 선구매하지 않는다.**
