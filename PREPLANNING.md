# Project2 사전기획 — 2026-09-14~09-17

> 목적: 9/18 팀 착수 전에 **문제 후보 3개, 사용자/대안 메모, 문제 정의 초안, 평가셋 후보 10건**을 개인 단위로 준비한다.
>
> 주의: 아래 후보 중 어떤 것도 자동으로 최종 주제가 아니다. 각 후보는 **3개월 이상 직접 경험한 도메인**이라는 근거가 있어야 한다.

## Candidate A — Factory Agent Hub / Embedded·IoT Device Integration Agent

### 도메인 정의

이번 후보의 직접 경험 도메인은 **Factory Automation 자체가 아니라 Embedded/IoT 프로토타이핑 환경의 Device Integration**으로 정의한다.

Factory, Conveyor, Robot Arm은 이 문제를 검증하기 위한 **적용 시나리오와 physical testbed**다. 제조 현장 작업자나 PLC/SCADA 운영 경험이 있다고 주장하지 않는다.

### 한 문장

새 센서·액추에이터·외부 장비를 프로토타입 시스템에 반복적으로 연결하는 개발자가, 장비마다 통신 방식·데이터 형식·명령·파라미터·상태 확인 규칙을 다시 코드에 옮기고 통합해야 하는 반복 작업을 줄이도록 돕는 Agent. 이번 MVP의 물리 장비 연결은 문서화된 text Serial Adapter로 제한한다.

### 사용자 상황

- 새 센서, 액추에이터, 보드 또는 외부 장비를 기존 프로토타입에 붙인다.
- 장비 문서나 기존 예제에서 연결 방식과 명령/데이터 규칙을 확인한다.
- 센서 이름, 단위, 범위, 전송 주기 또는 actuator command 같은 인터페이스를 기존 시스템에 맞춘다.
- 코드나 설정에 제어 조건과 상태 확인 규칙을 다시 옮긴다.
- 실제 장비에서 smoke test를 하고 HW-SW 연동 문제를 수정한다.
- 기존 UI/backend/control workflow에 새 기능을 연결한다.

### 현재 대안

- 장비별 Python/Arduino script 직접 작성
- vendor SDK/example code 복사 후 수정
- 장비별 config/schema 수동 작성
- 센서/액추에이터 인터페이스 규칙을 코드에 직접 반영
- 장비별 wrapper/tool 직접 추가

### 해결 가설

자연어 장비 설명과 문서화된 protocol 정보를 `DeviceSpec / Capability Spec`으로 구조화하고, 결정적 validation + 사람 검토 + 제한 실제 테스트를 통과한 capability만 Registry에 등록한다. 기존 Operator는 generic MCP tool로 새 장비를 다시 발견한다.

### 3개월 경험 Gate

**판정: `PASS` — 공개 GitHub 기록만으로도 3개월 이상의 직접 HW-SW 통합 작업을 확인할 수 있다.**

- [x] 경험자: 김재훈 (`nanocode00`)
- [x] 근거가 확인되는 직접 작업 기간: **2024-06-02 ~ 2024-09-24, 약 3개월 3주**
- [x] 대표 프로젝트: **webOS Smart Home Gardening**
- [x] 프로젝트 저장소: https://github.com/dudgns128/webos-gardening
- [x] 실제 구성: Raspberry Pi 4 / webOS OSE + Arduino + DHT11 + 조도·수위·토양수분 센서 + NeoPixel + 물펌프
- [x] 실제 통신: **Raspberry Pi(webOS) ↔ Arduino I²C**. 과거 경험을 Serial 경험으로 표현하지 않는다.
- [x] 반복한 업무: 센서/액추에이터 연결, I²C command/data contract 작성, 센서 raw data 변환, 상위 서비스 로직 연결, 실제 HW 테스트와 timing/API 수정
- [x] 현재 우회 방식: 장비별 통신/API 코드를 직접 작성·수정하고 상위 서비스가 기대하는 데이터·제어 인터페이스를 수동으로 맞춤

#### 공개 증빙

1. **I²C HW control 초기 통합 — 2024-06-02**  
   https://github.com/dudgns128/webos-gardening/commit/a94a8fc01c9fc60d4263d4866e30fbeceb8e0a0e
   - Arduino 측 DHT/analog sensor, NeoPixel, pump를 하나의 I²C command/data 규칙으로 구성했다.
2. **실장비 통신 timing / parsing 수정 — 2024-06-02**  
   https://github.com/dudgns128/webos-gardening/commit/00e4febe4ae07d85350d39854b97256db8e53eac
   - write 후 read timing을 수정하고 10-byte sensor payload를 humidity/temperature/light/water-level/soil-moisture로 해석했다.
3. **dummy data → 실제 HW 데이터·제어 연결 — 2024-06-12**  
   https://github.com/dudgns128/webos-gardening/commit/f2e890aab82d9b97055d717fa665fe1ec10bfb04
   - 기존 random sensing 값을 실제 I²C sensor read로 교체하고, 자동 광량 조절과 물주기 로직을 NeoPixel/pump 제어에 연결했다.
4. **실장비 연동 오류를 수정해 HW 제어 완성 — 2024-06-12**  
   https://github.com/dudgns128/webos-gardening/commit/ea08aa6a93d63a9cf5e9e7fd43b7947137a95057
   - webOS service API의 parameter/payload 형식과 callback 처리를 실제 동작 형태에 맞춰 수정하고 제어를 다시 활성화했다.
5. **프로젝트 후속 참여 기록 — 2024-09-24**  
   https://github.com/dudgns128/webos-gardening/commit/5fa0831b9bac76b405b4d273a93da104a9ca450e

#### 반복 사례 요약

- **센서 데이터 통합:** 여러 센서의 서로 다른 raw 값을 고정된 10-byte I²C payload로 묶고 상위 webOS 서비스에서 의미 있는 값으로 다시 변환했다.
- **액추에이터 제어 통합:** NeoPixel과 물펌프를 mode + argument 형태의 I²C 명령으로 정의하고, 기존 자동화 로직과 연결했다.
- **실장비 디버깅:** mock/dummy 환경에서는 드러나지 않던 read timing, callback, parameter/payload 형식 문제를 실제 Raspberry Pi–Arduino 환경에서 수정했다.

### Gate 해석

이번 프로젝트에서 주장하는 경험은 다음이다.

> **Embedded/IoT 프로토타입에서 센서·액추에이터와 외부 장비를 기존 시스템에 연결하고, 통신 규칙·데이터 변환·제어 인터페이스를 맞추는 업무를 3개월 이상 직접 경험했다. 공개 저장소에서 2024-06-02~09-24의 직접 작업 기록을 확인할 수 있다.**

다음은 경험 근거로 주장하지 않는다.

- 제조 공장 운영 경험
- PLC/SCADA 통합 실무 경험
- 산업용 로봇 운영 경험
- 생산라인 안전 시스템 구축 경험

따라서 제품명 `Factory Agent Hub`는 유지할 수 있지만, 문제 정의와 사용자 설명은 **Device Integration / Prototyping workflow**에서 시작한다.

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
| 3개월 직접 경험을 증명할 수 있음 | **PASS — 공개 GitHub 증빙 확보** |  |  |
| 반복 업무가 구체적임 | **예** |  |  |
| 현재 대안/우회가 관찰됨 | **예** |  |  |
| 30건 평가셋을 만들 수 있음 | **예상 가능** |  |  |
| LLM output contract를 정의할 수 있음 | **예** |  |  |
| MCP tool이 실제 domain 행동/데이터를 제공함 | **예** |  |  |
| 10/8까지 배포 가능함 | **검토 중** |  |  |
| 실패 경로를 재현 가능함 | **예** |  |  |

기술적으로 재미있는 주제보다 **직접 경험 + 반복 업무 + 평가 가능성**을 우선한다.
