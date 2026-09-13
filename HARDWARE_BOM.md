# Factory Agent Hub — Hardware BOM

> 상태: **2026-09-13 BOM v2 / 구매 최종안**  
> 기준: `HARDWARE_SPEC.md` v4의 Conveyor + Arduino 4-DOF Robot Arm + Raspberry Pi 3B+ 구성  
> 목적: **kit 자체 구성, 별도 구매 전자부품, 보유 재고, 수령 후 조건부 항목을 분리**해 불필요한 선구매를 막는다.

---

## 1. 최종 구매 구성

### DeviceMart

| 품목 | 수량 | 표시 단가 (VAT 별도) | 용도 |
|---|---:|---:|---|
| DRV8833 Motor Driver Module `VLT-MD012` | 1 | 1,700원 | Conveyor geared DC motor 제어 |
| DC 5.5×2.1 terminal connector `VLT-DC001` | 1 | 700원 | 5V servo PSU 출력을 screw terminal로 분배 |
| Regulated adapter 5V 5A, DC 5.5×2.1 | 1 | 7,800원 | Robot Arm servo 외부 전원 |
| 8자(C7) AC power cable | 1 | 2,000원 | 5V 5A adapter AC 입력 |
| **이엘사이언스 Arduino 집게 로봇팔 4관절** | 1 | 40,000원 | Robot Arm 기구 / servo testbed |

DeviceMart 장바구니 기준:

```text
상품 주문 금액   52,200원
부가세            5,220원
배송비            6,200원
--------------------------
결제 예정 금액   63,620원
```

배송비는 전자부품과 Robot Arm이 서로 다른 출고 그룹으로 잡힌 현재 장바구니 기준이다.

### Coupang

| 품목 | 수량 | 가격 | 배송 |
|---|---:|---:|---|
| **리브온 창의력 STEAM 목재 컨베이어 벨트** | 1 | 6,680원 | 현재 장바구니 무료배송 |

### 현재 구매 예정 총액

```text
DeviceMart  63,620원
Coupang      6,680원
------------------
합계        70,300원
```

가격과 배송비는 실제 결제 시점에 변동될 수 있으므로 주문 직전 다시 확인한다.

---

## 2. 구매하는 두 기구 kit

| 구분 | 선택품 | 수량 | 현재 판단 |
|---|---|---:|---|
| Conveyor | **리브온 목재 Conveyor kit** | 1 | frame / belt / roller / shaft / geared DC motor를 우선 그대로 사용 |
| Robot Arm | **이엘사이언스 Arduino 집게 로봇팔 4관절** | 1 | Arduino 제어 전제를 선택. MYLOOP 보드 버전은 사용하지 않음 |

Robot Arm의 servo는 사진상 SG90-class micro servo와 유사하지만 정확한 모델은 **수령 후 label 확인** 대상으로 남긴다.

---

## 3. 별도 구매 전자부품

| 품목 | 수량 | 상태 | 결정 |
|---|---:|---|---|
| DRV8833 `VLT-MD012` | 1 | **구매 최종안** | Conveyor motor driver |
| 5V 5A regulated adapter | 1 | **구매 최종안** | Robot Arm servo 전원 전용 |
| C7 AC cable | 1 | **구매 최종안** | 5V 5A adapter 입력 |
| VLT-DC001 5.5×2.1 terminal | 1 | **구매 최종안** | servo PSU +5V/GND 분배 |

**Step-down converter는 구매하지 않는다.** 5V 5A adapter는 Robot Arm servo 전원을 위한 것이며 Conveyor motor 전원은 kit 수령 후 별도로 확정한다.

---

## 4. 보유품 사용

| 품목 | 필요 수량 | 보유 상태 | 용도 |
|---|---:|---|---|
| Raspberry Pi 3B+ | 1 | 보유 | Factory Edge Gateway |
| Pi 전원 / microSD / 기본 부속품 | 1 set | 보유 | Pi 구동 |
| Arduino Uno | 2 | 9개 보유 | Conveyor / Robot 전용 controller |
| IR proximity sensor | 1 | 4개 보유 | Conveyor primary object detect |
| HC-SR04 | 0~1 | 13개 보유 | fallback / optional distance |
| SG90 | spare | 12개 보유 | Robot servo spare |
| FS90 | spare | 5개 보유 | Robot servo spare |
| MG996R | spare | 1개 보유 | 필요 시 고토크 실험 |
| LED / NeoPixel | 2 | 보유 | 상태 표시 |
| buzzer | optional | 보유 | fault / completion |
| switch / button / potentiometer | 적정량 | 보유 | local stop / local UI |
| RC522 | optional | 10개 보유 | demo 확장 시 identification |
| 608ZZ | optional | 9개 보유 | 기구 보강 필요 시 |

---

## 5. 재고 확인이 필요한 kit 밖 BOM

| 품목 | 수량 | 확인 내용 |
|---|---:|---|
| USB data cable | 2 | Pi ↔ Arduino Serial. 충전 전용 케이블 제외 |
| maintained 2-position switch | 2 권장 | local stop. 가능하면 NC 접점 |
| jumper / signal wire | 적정량 | sensor / switch / driver / servo signal |
| power wire | 적정량 | servo +5V / GND distribution |
| breadboard / terminal / distribution parts | 1~2 set | 배선 정리 |
| cable tie / 양면테이프 / hot glue | 필요 시 | sensor / switch 임시 고정 |
| 가벼운 test object | 2~3 | foam / cardboard / 3D print 등 |

---

## 6. 수령 후에만 결정하는 조건부 BOM

### Conveyor motor power

Conveyor motor는 사진상 3V급 geared DC motor 계열로 보이지만, **정확한 motor supply는 아직 구매하지 않는다.**

수령 후 확인:

```text
motor label / 기본 battery 또는 power 구성
rated voltage
no-load behavior
DRV8833 연결 시 안정성
30초 연속 운전 온도
```

필요하면 그때 motor 정격에 맞는 별도 저전압 DC 전원을 추가한다.

### Mechanical adapters

다음은 실제 기구 hole / 형상과 보유 부품이 맞지 않을 때만 준비한다.

- sensor bracket
- local-stop bracket
- Arduino mount
- spacer / shim
- cable management part

가능하면 3D print로 해결한다.

---

## 7. 현재 구매하지 않는 품목

| 품목 | 현재 판단 |
|---|---|
| Step-down converter | **구매 안 함** |
| Ø8 mm shaft | 구매 안 함 |
| custom PU/PVC endless flat belt | 구매 안 함 |
| 추가 608ZZ | 구매 안 함 — 9개 보유 |
| M3 bolt / nut / washer assortment | 선구매 안 함 |
| 추가 servo | 구매 안 함 — 보유 spare 사용 |
| coupler / pulley | 선구매 안 함 |
| 대형 Conveyor frame / roller 3D print | 하지 않음 |
| Robot Arm link / base 전체 3D print | 하지 않음 |
| RFID reader | 추가 구매 안 함 |
| HC-SR04 | 추가 구매 안 함 |

---

## 8. 장비별 조립 BOM

### Conveyor node

```text
[리브온 Conveyor mechanical kit]
        +
Arduino Uno ×1
DRV8833 VLT-MD012 ×1
IR proximity sensor ×1
local stop switch ×1
status LED / NeoPixel ×1
USB data cable ×1
motor power ×1        # 수령 후 정격 확인 뒤 확정
wiring / mount
```

기본 motor는 우선 유지한다. 단독 smoke에서 제어 불가, 토크 부족, 과열, 지나친 속도, 기구 문제 중 하나가 확인될 때만 교체한다.

### Robot Arm node

```text
[이엘사이언스 Arduino 4-DOF Gripper Arm]
        +
Arduino Uno ×1
5V 5A regulated adapter ×1
C7 AC cable ×1
VLT-DC001 terminal connector ×1
local stop switch ×1
status LED / NeoPixel ×1
USB data cable ×1
common GND wiring
```

servo를 Arduino Uno 5V regulator에서 직접 여러 개 구동하지 않는다. Servo signal은 Arduino에서 주고, 전원은 external 5V 5A PSU에서 공급한다.

### Edge Gateway

```text
Raspberry Pi 3B+ ×1
Pi power / microSD / network
USB data cable ×2
```

Pi에는 LLM을 올리지 않고 MCP / Registry / validation / deterministic executor / Serial routing / SQLite audit을 담당시킨다.

---

## 9. 수령 직후 BOM 확인 체크

### Conveyor

```text
actual overall size
belt width
motor exact type / label
rated voltage / basic power source
shaft / roller accessibility
motor ↔ roller coupling
DRV8833 smoke result
```

### Robot Arm

```text
servo model labels
servo count
included fasteners / horn / cable
joint mechanical limits
HOME candidate pose
5V 5A PSU load smoke
```

이 결과로 남은 조건부 BOM을 닫는다. **수령 전 확인할 수 없는 motor supply, fastener, adapter를 추정 구매하지 않는다.**
