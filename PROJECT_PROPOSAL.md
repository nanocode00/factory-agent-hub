# 설비를 가르칠 수 있는 AI Agent Platform 기획서 초안

> 프로젝트명(가칭): **Factory Agent Hub**  
> 한 줄 소개: **사용자가 설비의 연결 방법과 기능을 자연어로 설명하면, AI Agent가 이를 검증 가능한 Capability로 변환하고 MCP를 통해 다른 Agent가 해당 설비를 발견·제어할 수 있게 하는 확장형 설비 Agent 플랫폼**

---

## 1. 프로젝트 배경

제조·연구·메이커 환경에서는 서로 다른 제조사와 세대의 장비가 함께 사용된다.  
컨베이어, 로봇팔, 센서, 포장기, 모터 등은 각자 다른 통신 방식과 명령 체계를 가지기 때문에 새로운 설비를 기존 자동화 시스템에 연결하려면 반복적인 통합 작업이 필요하다.

특히 전담 자동화 엔지니어가 부족한 소규모 제조업체, 연구실, 메이커스페이스에서는 다음 문제가 발생한다.

- 새 설비를 추가할 때마다 매뉴얼 및 통신 프로토콜을 다시 파악해야 한다.
- 장비별 SDK, Serial 명령, GPIO, HTTP API 등을 별도로 구현해야 한다.
- 기존 자동화 로직에 새 설비를 연동하는 작업이 어렵다.
- LLM Agent를 도입하더라도 Agent가 각 장비의 기능과 사용법을 미리 알아야 한다.
- 생성형 AI가 임의의 명령이나 코드를 직접 실행하게 할 경우 안전성을 보장하기 어렵다.

즉, 문제는 단순히 **“공장에 AI가 없다”**가 아니라  
**“새로운 설비의 기능을 AI와 자동화 시스템에 연결하는 마지막 통합 작업(last-mile integration)이 어렵다”**는 것이다.

---

## 2. 해결하고자 하는 문제

### 핵심 문제

> 설비마다 연결 방식과 기능 정의가 달라, 새로운 장비를 자동화 시스템에 통합할 때 반복적인 엔지니어링 작업이 필요하다.

### 주요 고객

- 소규모 제조업체 및 생산라인
- 자동화 전문 인력이 부족한 중소기업
- 연구실 / 메이커스페이스
- 다양한 장비를 고객사에 연결해야 하는 소규모 SI 업체
- 교육용 스마트팩토리 및 로보틱스 환경

---

## 3. 제안 솔루션

사용자가 새로운 설비의 사용법을 **자연어로 설명**하면 Setup Agent가 이를 구조화된 `DeviceSpec`과 `Capability`로 변환한다.

예시 입력:

> 이 컨베이어는 USB Serial로 연결돼 있어.  
> 115200 baud를 사용하고 START를 보내면 시작해.  
> STOP을 보내면 멈추고 SPEED 뒤에 0~100 숫자를 보내면 속도를 바꿀 수 있어.  
> STATUS를 보내면 현재 상태를 알려줘.

Agent가 생성하는 개념적 결과:

```yaml
device:
  name: conveyor_01
  adapter: serial
  baudrate: 115200

capabilities:
  - name: start
    command: START

  - name: stop
    command: STOP

  - name: set_speed
    command: "SPEED {value}"
    parameters:
      value:
        type: integer
        minimum: 0
        maximum: 100

  - name: get_status
    command: STATUS
```

이 명세는 검증 및 실제 장비 테스트를 거친 뒤 Capability Registry에 등록된다.

이후 다른 Agent는 장비별 프로토콜을 직접 알 필요 없이 MCP를 통해 등록된 Capability를 검색하고 실행할 수 있다.

---

## 4. 핵심 가치

### 4.1 자연어 기반 설비 온보딩

사용자는 코드 대신 장비의 연결 방법과 기능을 자연어로 설명한다.

### 4.2 코드 수정 없는 기능 확장

새로운 설비가 추가되어도 Operator Agent 자체를 수정하지 않고 Registry에 Capability를 추가하여 사용할 수 있도록 한다.

### 4.3 장비 기능의 표준화

Serial, GPIO 등 서로 다른 인터페이스를 Agent가 사용할 수 있는 공통 Capability 형태로 추상화한다.

### 4.4 통제 가능한 AI 제어

LLM이 임의의 Python/Shell 코드를 생성해 실행하는 것이 아니라, 미리 구현된 Adapter와 검증된 Capability만 실행할 수 있도록 한다.

### 4.5 여러 설비의 Agent 기반 조합

Agent는 각각 등록된 장비 기능을 조합하여 하나의 작업을 수행할 수 있다.

예:

> 물체가 도착하면 컨베이어를 멈추고 로봇팔로 오른쪽 박스에 옮긴 뒤 다시 컨베이어를 가동해.

---

## 5. 기존 솔루션과의 차별점

기존 산업 자동화 및 AI 솔루션도 PLC, Robot, IoT Device 연결과 자연어 기반 엔지니어링 기능을 제공한다.

본 프로젝트는 대규모 산업 플랫폼 전체를 대체하는 것이 아니라 다음 지점에 집중한다.

> **기존 시스템: 지원되는 Connector/Driver에 장비를 맞춰 등록**  
> **제안 시스템: 사람에게 장비 사용법을 알려주듯 자연어로 Agent에게 새로운 장비의 Capability를 가르침**

### 주요 차별점

1. **Natural Language → Declarative DeviceSpec**
   - 코드를 직접 생성하는 대신 구조화되고 검증 가능한 명세를 생성한다.

2. **Capability 중심 확장**
   - Agent가 알지 못했던 장비도 런타임에 새로운 Capability로 등록할 수 있다.

3. **MCP 기반 Agent 연동**
   - 등록된 Capability를 표준 Tool 인터페이스를 통해 Agent가 검색하고 실행한다.

4. **안전한 실행 구조**
   - 파라미터 범위, 위험도, 사용자 승인 여부 등을 실행 계층에서 강제한다.

5. **기존 제어기를 대체하지 않는 구조**
   - PLC/Arduino는 실시간 장비 제어를 담당하고 AI Agent는 상위 orchestration을 담당한다.

---

## 6. 시스템 구조

```text
사용자
  │
  │ 자연어 설비 설명
  ▼
┌─────────────────┐
│   Setup Agent   │
│ NL → DeviceSpec │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Spec Validator  │
│ 타입/범위/위험도 │
└────────┬────────┘
         │
         │ 사용자 확인 / 테스트
         ▼
┌─────────────────┐
│ Device Registry │
│ Device/Capability│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   MCP Gateway   │
│ generic invoke  │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Device Adapters │
│ Serial / GPIO   │
└────────┬────────┘
         ▼
 Arduino / Raspberry Pi
         │
 ┌───────┴─────────┐
 ▼                 ▼
Conveyor        Robot Arm
```

평상시 운용:

```text
사용자 자연어
    ↓
Operator Agent
    ↓
Capability 검색
    ↓
MCP Gateway
    ↓
Validator / Policy
    ↓
Device Adapter
    ↓
실제 설비
```

---

## 7. 핵심 구성 요소

### Setup Agent

새 장비 설명을 분석해 DeviceSpec을 생성한다.

역할:

- 장비 종류 파악
- 연결 방식 파악
- Capability 추출
- 파라미터 타입/범위 추출
- 누락 정보 확인 및 추가 질문
- 위험도 초안 생성

### DeviceSpec

자연어와 실제 하드웨어 사이의 중간 표현이다.

LLM이 실행 코드를 만드는 대신 선언적 명세만 생성하도록 제한한다.

### Spec Validator

등록 전에 다음을 검증한다.

- 필수 정보 존재 여부
- 파라미터 타입 및 범위
- 지원 Adapter 여부
- 잘못된 Command Template
- 위험한 Capability
- 연결 설정

### Capability Registry

등록된 설비와 기능을 관리한다.

예:

```text
conveyor_01
 ├─ start
 ├─ stop
 ├─ set_speed
 └─ get_status

robot_arm_01
 ├─ home
 ├─ pick
 ├─ place
 └─ get_position
```

### Device Adapter

실제 하드웨어 통신은 플랫폼에서 구현한 안전한 Adapter만 사용한다.

MVP:

- Serial Adapter
- GPIO Adapter

추후 확장:

- HTTP
- MQTT
- Modbus
- OPC-UA

### MCP Gateway

MVP에서는 장비마다 MCP Tool을 동적으로 생성하기보다 다음과 같은 범용 Tool을 우선 구현한다.

```text
list_devices()
get_device(device_id)
list_capabilities(device_id)
invoke_capability(device_id, capability, arguments)
get_device_status(device_id)
```

### Operator Agent

사용자의 자연어 작업 지시를 해석하고 등록된 Capability를 검색·조합하여 실행한다.

---

## 8. 안전 설계

AI의 판단과 실제 설비 실행 사이에 반드시 코드 기반 검증 계층을 둔다.

Capability별 위험 수준 예:

```text
READ_ONLY
SAFE
NORMAL
DANGEROUS
```

예:

```text
get_temperature  → READ_ONLY
start_fan        → SAFE
set_speed        → NORMAL
emergency_stop   → DANGEROUS / 사용자 승인 필요
```

추가 원칙:

- LLM의 임의 코드 실행 금지
- 등록되지 않은 명령 실행 금지
- Parameter Schema 기반 값 검증
- 위험 명령 사용자 확인
- 실제 실시간 안전 제어는 Arduino/PLC 담당
- AI Agent는 상위 수준 작업 orchestration 담당

---

## 9. 하드웨어 데모 구성

### 기본 구성

- Raspberry Pi 3B
- Arduino
- 컨베이어벨트 키트
- 로봇팔 키트
- 거리/IR/컬러 센서
- LED / 부저
- 필요 시 온도센서

### 역할

**Arduino**
- Sensor 읽기
- Motor / Servo 제어
- 빠른 로컬 제어

**Raspberry Pi 또는 노트북**
- MCP Server
- Device Registry
- Device Adapter
- Agent Backend

**LLM**
- Setup Agent
- Operator Agent

---

## 10. 대표 사용자 시나리오

### Scenario A — 새로운 설비 등록

사용자:

> 새 로봇팔을 추가할게. USB Serial이고 115200 baud야.  
> HOME을 보내면 초기 위치로 돌아가고 PICK 1을 보내면 1번 위치의 물체를 집어.

Setup Agent:

1. 자연어 분석
2. DeviceSpec 생성
3. 누락된 정보 질문
4. 사용자에게 Capability 미리보기
5. 연결 테스트
6. 각 기능 테스트
7. Registry 등록

### Scenario B — 새 설비 즉시 사용

사용자:

> 현재 사용할 수 있는 설비 알려줘.

Agent:

```text
1. 생산라인 컨베이어
2. 분류 로봇팔
```

사용자:

> 컨베이어에서 물체가 감지되면 멈추고 로봇팔로 오른쪽 박스에 옮긴 다음 다시 가동해.

Agent:

```text
1. conveyor.get_status
2. conveyor.stop
3. robot_arm.pick
4. robot_arm.place
5. conveyor.start
```

등록 직후 기존 Agent 코드 수정 없이 두 설비를 연동하는 것을 시연한다.

---

## 11. MVP 범위

2주 프로젝트에서는 범위를 다음과 같이 제한한다.

### 반드시 구현

- 자연어 → DeviceSpec
- 누락 정보 추가 질문
- DeviceSpec Validator
- Device / Capability Registry
- Serial Adapter
- 범용 MCP Tool
- Operator Agent
- 컨베이어 실제 제어
- 두 번째 장비 등록 및 연동
- 사용자 확인 기반 안전 기능

### 가능하면 구현

- GPIO Adapter
- 웹 기반 설비 등록 UI
- Capability별 Risk Level
- 실행 로그
- Workflow 저장

### 확장 아이디어

- HTTP / MQTT / Modbus / OPC-UA Adapter
- Dynamic MCP Tool 생성
- 자연어 Workflow 생성
- 조건 기반 자동화
- 설비 매뉴얼/PDF 기반 자동 Capability 추출
- Digital Twin 연동
- Vision Agent 기반 품질 검사
- 다중 Agent 구조

---

## 12. 기술 스택 후보

| 영역 | 후보 |
|---|---|
| Backend | Python + FastAPI |
| Agent | LLM Tool Calling |
| MCP | MCP Python SDK |
| Structured Output | Pydantic v2 |
| Registry | SQLite |
| Serial | pyserial |
| Hardware | Arduino + Raspberry Pi |
| Frontend | React/Vite 또는 간단한 Web UI |
| LLM | API 또는 Ollama |

---

## 13. 2주 개발 계획

### 1주차 — 핵심 기능 구현

**Day 1–2**
- 하드웨어 조립
- Arduino ↔ Python Serial 통신
- 컨베이어 기본 제어

**Day 3**
- DeviceSpec 정의
- Device Adapter 구조
- SQLite Registry

**Day 4**
- Capability Executor
- Validator
- MCP Gateway

**Day 5**
- Operator Agent
- 자연어 명령 → 실제 컨베이어 제어

**Day 6–7**
- Setup Agent
- 자연어 → DeviceSpec
- 등록 및 테스트 흐름

### 2주차 — 통합 및 검증

**Day 8–9**
- 로봇팔 연결
- 자연어 기반 신규 설비 등록

**Day 10**
- 컨베이어 + 로봇팔 연동

**Day 11**
- 안전 정책 / 승인 Flow
- 오류 처리

**Day 12**
- UI 및 실행 로그 정리

**Day 13**
- 다양한 자연어 입력 테스트
- 예외 상황 테스트

**Day 14**
- 최종 통합 테스트
- 발표 시나리오 및 영상 준비

---

## 14. 최종 데모 목표

발표에서 다음 순서를 보여주는 것을 목표로 한다.

1. 초기에는 컨베이어만 Agent에 등록되어 있음
2. Agent에게 현재 사용할 수 있는 설비 조회
3. 발표 도중 새로운 로봇팔 연결
4. 로봇팔 사용법을 자연어로 설명
5. Setup Agent가 Capability 자동 추출
6. 사용자 확인 및 실제 장비 테스트
7. Registry 등록
8. 다시 장비 목록 조회 → 로봇팔 추가 확인
9. 자연어로 컨베이어 + 로봇팔 복합 작업 요청
10. Agent가 두 장비의 Capability를 조합해 실제 공정 실행

### 핵심 데모 메시지

> **우리가 컨베이어와 로봇팔을 지원하도록 Agent를 만든 것이 아니라, Agent가 처음 보는 장비의 사용법을 사람이 자연어로 가르쳐 즉시 활용할 수 있게 만들었다.**

---

## 15. 프로젝트 성공 기준

- [ ] 컨베이어를 실제 MCP Tool을 통해 제어할 수 있다.
- [ ] 사용자 자연어 설명으로 새로운 DeviceSpec을 생성할 수 있다.
- [ ] 정보가 부족하면 Agent가 추측하지 않고 추가 질문을 한다.
- [ ] 생성된 Capability가 Validator를 통과한 뒤에만 등록된다.
- [ ] Agent 코드 수정 없이 두 번째 장비를 등록할 수 있다.
- [ ] Operator Agent가 여러 장비 Capability를 조합할 수 있다.
- [ ] 위험하거나 범위를 벗어난 명령을 실행 계층에서 차단할 수 있다.
- [ ] 최종 데모에서 컨베이어 + 로봇팔 복합 동작을 성공시킨다.

---

## 16. 아직 결정해야 할 사항

- 프로젝트 최종 이름
- 구매할 컨베이어/로봇팔 키트
- 실제 사용할 센서 종류
- LLM: API vs Local Ollama
- Raspberry Pi를 MCP Gateway로 사용할지 노트북에서 직접 실행할지
- 팀원별 역할 분담
- 웹 UI 구현 범위
- Dynamic MCP Tool을 MVP에 포함할지 여부

---

## 핵심 요약

**Problem**

> 새로운 제조 설비를 자동화 시스템에 추가할 때 장비마다 다른 프로토콜과 기능으로 인해 반복적인 통합 개발이 필요하다.

**Solution**

> 사용자가 설비의 사용법을 자연어로 설명하면 AI Agent가 이를 검증 가능한 Capability로 변환하고 MCP를 통해 다른 Agent가 즉시 사용할 수 있도록 한다.

**Differentiation**

> 특정 장비를 미리 지원하는 제어 Agent가 아니라, 사용자가 새로운 장비의 기능을 자연어로 Agent에게 가르쳐 확장할 수 있는 플랫폼을 지향한다.
