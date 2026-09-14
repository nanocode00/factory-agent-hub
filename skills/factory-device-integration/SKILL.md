# Factory Device Integration Skill

> Status: **DRAFT — Project2 subject/domain-experience gate pending**
>
> Purpose: 문서화된 Serial 장비를 프로토타입/실험 환경에 온보딩할 때 Agent가 따라야 하는 도메인 규칙, 판단 기준, 용어, 예외 처리를 정의한다. 이 문서는 장비 driver나 safety controller가 아니며, MCP/Executor의 결정적 검증을 대체하지 않는다.

## 1. Domain vocabulary

- **DeviceSpec**: 장비 식별, Adapter, 연결 설정, capability 집합을 담는 선언적 명세.
- **Capability**: 검증 가능한 하나의 장비 기능. 명령 template, parameter schema, read/write, risk, success/state verification을 포함한다.
- **Registry**: 검토와 시험을 통과한 DeviceSpec/Capability의 현재 상태를 보관하는 저장소.
- **DRAFT**: Agent가 만든 초안. 실행 불가.
- **VALIDATED**: 구조/형식 검증 통과. 실행 불가.
- **REVIEWED**: 사람이 의미와 위험을 검토함. 아직 운영 실행 불가.
- **TEST_APPROVED**: 제한된 실제 시험이 승인됨.
- **VERIFIED**: 제한 시험과 상태 확인을 통과함.
- **ACTIVE**: Operator discovery/invoke 대상.
- **RESULT_UNKNOWN**: write 요청 전송 여부/실제 실행 여부를 안전하게 확정할 수 없는 상태. 자동 재전송 금지.

## 2. Supported domain boundary

현재 MVP가 지원하는 장비는 다음 조건을 모두 만족해야 한다.

1. 미리 구현된 **text Serial Adapter**로 통신 가능하다.
2. command grammar가 문서화되어 있다.
3. parameter type/range를 결정적으로 정의할 수 있다.
4. response 또는 별도 status read로 성공/상태 확인 기준을 만들 수 있다.
5. 장비 담당자가 실제 시험 조건과 허용 동작을 검토할 수 있다.

다음은 이번 MVP에서 지원하지 않는다.

- binary proprietary protocol
- 임의 protocol 자동 추론/발명
- 임의 Python/Shell/PLC code 생성 후 실행
- 자유 문자열 raw serial 실행
- 미문서화 장비
- Agent가 실시간 servo/motor control loop를 직접 수행하는 구조
- safety-critical 산업 운전

지원 밖 입력은 그럴듯한 spec을 만들어 통과시키지 말고 `UNSUPPORTED` 또는 `NEEDS_INFO`로 종료한다.

## 3. Onboarding reasoning order

새 장비 설명을 받으면 다음 순서로 판단한다.

1. **장비와 사용 목적 식별**
2. **연결 정보 확인**: adapter, port 식별 방식, baudrate, encoding, line ending 등
3. **capability 후보 추출**
4. 각 capability의 **command syntax** 확인
5. 각 argument의 **type/range/enum** 확인
6. **read/write** 분류
7. **risk**와 승인 필요 여부 확인
8. **success response / state verification** 확인
9. **timeout / retry 의미** 확인
10. 누락/충돌을 질문
11. 충분한 경우에만 DeviceSpecDraft 생성

Agent는 누락된 실제 장비 정보를 일반 상식이나 추측으로 채우지 않는다.

## 4. Required information

DeviceSpec 초안에 최소 다음이 필요하다.

```text
device
  id
  version
  adapter
  connection

capability
  id
  name
  description
  command_template
  parameters_schema
  read_write
  risk
  success_condition
  state_verification
  timeout
  verified_state
```

다음 중 하나라도 실제 실행 안전성에 영향을 주는데 값이 없으면 `READY`로 만들지 않는다.

- command grammar
- parameter range/enum
- write 여부
- timeout
- success/state verification
- 위험 동작의 승인 조건

## 5. Risk and execution rules

위험도 label은 UI 설명용일 수 있지만 실제 허용/차단은 코드 policy가 강제한다.

원칙:

- READ는 write보다 낮은 위험으로 볼 수 있으나 정보 누락/오판을 허용한다는 뜻이 아니다.
- WRITE는 대상 장비, spec version, capability, arguments, plan에 묶인 승인이 필요하다.
- 승인 뒤 arguments 또는 spec version이 바뀌면 기존 승인을 재사용하지 않는다.
- `ACTIVE`가 아닌 capability는 운영 실행할 수 없다.
- 시험 권한과 운영 권한은 구분한다.

## 6. Retry rules

### LLM structured output

- schema/format repair는 최대 1회.
- 누락된 실제 장비 정보는 retry로 발명하지 않는다.
- repair 후에도 계약을 지키지 못하면 실패로 종료한다.

### Device read

- read retry는 제한된 횟수만 허용한다.
- 동일 실패가 반복되면 장비/연결 상태 확인으로 전환한다.

### Device write

- write timeout 또는 response loss에서 **자동 재전송하지 않는다**.
- `RESULT_UNKNOWN`으로 기록한다.
- downstream step을 중단한다.
- 사람이 물리 상태 또는 결정적 status read로 확인하기 전 재개하지 않는다.

## 7. Injection / malformed input

다음은 명세로 승인하지 않는다.

- newline로 여러 command를 삽입하려는 문자열
- command template 바깥의 raw text
- schema가 허용하지 않는 expression/code
- argument type/range 위반
- capability가 문서에 없는 command를 임의 생성하는 경우

Agent가 거부 이유를 자연어로 설명할 수는 있지만, 실제 전송 차단은 Validator/Adapter가 결정적으로 수행한다.

## 8. Setup Agent output policy

가능한 상태:

```text
READY
NEEDS_INFO
REJECTED
```

- `READY`: 계약 작성에 필요한 핵심 정보가 충분함. 아직 실제 실행 승인을 뜻하지 않는다.
- `NEEDS_INFO`: 누락/모호/충돌 정보가 있어 사용자에게 질문해야 함.
- `REJECTED`: 지원 범위 밖이거나 안전/계약상 현재 경로에서 다룰 수 없음.

답변에는 사용자에게 필요한 다음 행동을 명확히 포함한다.

## 9. Operator planning policy

Operator는 raw command를 직접 작성하지 않는다.

오직 Registry의 `ACTIVE` capability를 조회해 다음 형태의 PlanSpec을 만든다.

```text
steps[]
  capability_id
  arguments
  expected_state
```

규칙:

- Registry에 없는 기능을 추측하지 않는다.
- capability description과 parameter schema를 우선 사용한다.
- write step은 approval 없이 실행하지 않는다.
- 이전 step 결과가 `FAILED` 또는 `RESULT_UNKNOWN`이면 후속 write를 중단한다.
- 실시간 센서 loop나 motion control을 LLM plan으로 구현하지 않는다.

## 10. Local stop vs software stop

- **local stop**: Arduino input을 firmware가 직접 읽어 Agent/MCP/network와 무관하게 우선 처리하는 prototype-level stop.
- **software STOP/HALT**: 정상 software command 경로.

현재 local stop은 산업용 emergency stop이나 독립 safety circuit이 아니다. Agent가 이를 산업 안전 장치로 표현하거나 안전 인증을 암시하지 않는다.

## 11. MCP usage

MCP는 domain tool interface다.

기본 tool 후보:

```text
list_devices
get_device
list_capabilities
get_device_status
validate_device_spec
invoke_capability
```

MCP tool이 있다고 해서 안전성이 생기는 것은 아니다. Tool 내부에서도 Registry state, validation, approval, timeout, audit 규칙을 적용한다.

## 12. Evidence mindset

다음 문장을 피한다.

- “잘 동작한다”
- “안전하다”
- “범용 장비를 지원한다”
- “시간을 크게 줄인다”

대신 측정 가능한 증거로 말한다.

- N건 중 output contract pass N건
- unsafe request N건 중 차단 N건
- unsupported request N건 중 올바른 거부 N건
- prompt v1 vs v2 같은 30+ eval Dataset score
- latency / token / cost
- physical test 성공/실패 횟수
- code/freeze hash 전후 변경 여부

## 13. Escalation to human

다음은 사람 확인으로 넘긴다.

- 장비 command/range 문서가 서로 충돌함
- 물리 간섭/전원/배선 위험
- write 결과 불명
- unsupported protocol
- capability risk를 결정할 근거 부족
- state verification 방법 없음
- 실제 시험 조건이 정의되지 않음

Agent의 역할은 이 불확실성을 숨기는 것이 아니라 **명시적으로 드러내고 안전한 다음 단계로 연결하는 것**이다.
