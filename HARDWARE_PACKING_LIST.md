# Factory Agent Hub — Hardware Packing List

> 상태: **2026-09-13 이동 준비 체크리스트 v2**  
> 기준: `HARDWARE_SPEC.md` v4 / `HARDWARE_BOM.md` v3  
> 목적: 이미 집에 보유한 부품 중 **실제 구현 장소로 가져갈 것만 선별**한다. 부품 상자 전체를 옮기지 않는다.

---

## 1. 반드시 가져갈 것

| 품목 | 권장 수량 | 용도 / 메모 |
|---|---:|---|
| Raspberry Pi 3B+ | 1 | Factory Edge Gateway |
| Raspberry Pi 전원 | 1 | Pi 전용 전원 |
| microSD | 1 + 예비 1 가능 | Pi OS / runtime |
| Arduino Uno | **3** | Conveyor 1 + Robot 1 + 예비 1 |
| USB-B **data** cable | **3** | Arduino 2대 + 예비. 충전 전용 제외 |
| IR proximity sensor | **2** | Conveyor primary sensor + spare |
| jumper wire M-M | 1 묶음 | driver / breadboard 연결 |
| jumper wire M-F | 1 묶음 | sensor / module 연결 |
| jumper wire F-F | 1 묶음 | module 간 연결 |
| breadboard | **2** | Conveyor / Robot 장비별 배선 |
| LED / NeoPixel | 2~4 | READY / RUNNING / ERROR |
| LED 저항 | 적정량 | status LED용 |
| 전원용 wire | 적정량 | Servo +5V / GND distribution |
| 일반 signal wire | 적정량 | switch / sensor / driver wiring |

Arduino는 실제 사용 수량 2개보다 **1개 더 가져간다.** USB Serial, regulator, pin 이상이 생겼을 때 즉시 교체하기 위한 spare다.

`MSL-1C2P` local stop switch 2개는 DeviceMart 구매품이므로 집에서 찾거나 가져올 필요가 없다.

---

## 2. 강력 추천 spare / fallback

작은 봉투나 부품 케이스 하나에 아래만 묶어 간다.

| 품목 | 권장 수량 | 용도 |
|---|---:|---|
| SG90 | **3~4** | Robot Arm servo spare / auxiliary actuator |
| FS90 | 1~2 | gripper spare 후보 |
| 소형 DC motor | **2** | Conveyor 기본 motor 실패 대비 |
| HC-SR04 | 1~2 | IR sensor fallback |
| buzzer | 1~2 | fault / completion feedback |
| potentiometer | 1~2 | manual speed / calibration 테스트 |
| push button / extra switch | 2~3 | 임시 local input / debug. local stop 대체용은 아님 |
| RC522 | 1 | 시간이 남을 때 identification demo |
| 28BYJ-48 + driver | 1 set | Conveyor motor의 최후 fallback |

현재 프로젝트에서 쓰지 않을 가능성이 높은 spare는 많이 가져가지 않는다.

---

## 3. 공구 / 조립 보조품

| 품목 | 권장 | 이유 |
|---|---|---|
| 멀티미터 | **가져가기 권장** | motor 전압, continuity, common GND, local stop pin mapping 확인 |
| 소형 드라이버 세트 | 권장 | kit 조립 / terminal 체결 |
| 니퍼 / wire stripper | 권장 | 전원·신호선 가공 |
| 절연테이프 | 권장 | 임시 절연 |
| 케이블타이 | 약간 | 배선 정리 |
| 양면테이프 | 약간 | sensor / board 임시 고정 |
| hot glue gun | 선택 | 기구 고정이 꼭 필요할 때만 |
| USB hub | 선택 | Pi USB 포트/배선 편의가 필요할 때 |

220V mains 배선이나 노출형 AC 전원모듈은 사용하지 않는다. 새로 구매하는 Robot servo PSU는 완제품 5V 5A adapter를 사용한다.

---

## 4. 가져가지 않아도 되는 대량 재고

아래는 현재 MVP에 직접 필요하지 않으므로 **전부 들고 가지 않는다.** 필요해지면 추가로 가져온다.

- 608ZZ bearing 9개 전체
- RC522 10개 전체
- LCD 11개 전체
- HC-SR04 13개 전체
- SG90 12개 전체
- FS90 5개 전체
- 28BYJ-48 7개 전체
- DHT / PIR / microphone / RTC / soil sensor / MPU-6050 등 기타 sensor 대량
- 축 / custom belt 관련 과거 직접제작 부품
- MG996R 등 고하중 부품 여러 종류

`일단 다 가져간다`보다 **핵심 장비 + spare 1~2개**를 원칙으로 한다.

---

## 5. 실제 포장 단위 권장

### A. Pi / controller pouch

```text
Raspberry Pi 3B+
Pi power
microSD + spare
Arduino Uno ×3
USB-B data cable ×3
```

### B. Core electronics box

```text
IR sensor ×2
breadboard ×2
M-M / M-F / F-F jumper
LED / resistor / NeoPixel
power wire / signal wire
```

### C. Fallback pouch

```text
SG90 ×3~4
FS90 ×1~2
small DC motor ×2
HC-SR04 ×1
28BYJ-48 + driver ×1 set
buzzer / potentiometer / extra switch
RC522 ×1
```

### D. Tool pouch

```text
multimeter
screwdriver
nipper / stripper
insulation tape
cable tie
small double-sided tape
```

---

## 6. 출발 전 최종 체크

- [ ] Pi 3B+가 실제 boot 되는지 확인
- [ ] Pi power / microSD 함께 넣음
- [ ] Uno 3개 모두 USB 인식 여부 확인 가능하면 확인
- [ ] USB-B cable이 **data cable**인지 확인
- [ ] IR sensor 2개 준비
- [ ] jumper 3종 / breadboard / 전원선 준비
- [ ] SG90 spare 3~4개 준비
- [ ] 소형 DC motor spare 2개 준비
- [ ] 멀티미터 / 드라이버 준비
- [ ] 구매 예정품과 중복되는 5V PSU / motor driver / local stop switch를 불필요하게 추가 포장하지 않음

---

## 7. 구매품과 역할 구분

집에서 가져가는 목록과 새 구매품은 다음처럼 분리한다.

```text
새로 구매
├─ 리브온 Conveyor kit
├─ 이엘사이언스 Arduino 4-DOF Robot Arm
├─ DRV8833 VLT-MD012
├─ 5V 5A servo adapter
├─ C7 AC cable
├─ VLT-DC001 terminal
└─ MSL-1C2P local stop switch ×2

집에서 가져감
├─ Raspberry Pi 3B+
├─ Arduino Uno ×3
├─ IR / fallback sensors
├─ wiring / breadboard / status parts
├─ servo / motor spares
└─ tools
```

Conveyor motor용 실제 전원은 kit 수령 후 정격과 기본 구성을 확인한 뒤 결정한다.