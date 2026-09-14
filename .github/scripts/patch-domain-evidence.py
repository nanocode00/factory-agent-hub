from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"target not found in {path}: {old[:120]}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


# PROJECT2_ALIGNMENT.md
replace_once(
    "PROJECT2_ALIGNMENT.md",
    "| 버티컬 도메인 | 소규모 연구실/장비 통합을 ICP 후보로 둠 | 직접 경험 도메인을 **Embedded/IoT Device Integration**으로 좁힌다. Factory는 적용 시나리오이며 제조 현장 경험을 주장하지 않는다. 2024.03~2024.11 webOS 스마트 화분 프로젝트를 주 근거로 사용하고 산출물 링크를 보강한다. |",
    "| 버티컬 도메인 | 소규모 연구실/장비 통합을 ICP 후보로 둠 | 직접 경험 도메인을 **Embedded/IoT Device Integration**으로 좁힌다. Factory는 적용 시나리오이며 제조 현장 경험을 주장하지 않는다. 공개 저장소에서 `nanocode00`의 2024-06-02~09-24 HW-SW 통합 작업을 확인했다. |",
)
replace_once(
    "PROJECT2_ALIGNMENT.md",
    "**Embedded/IoT 프로토타이핑 환경에서 새 센서·액추에이터·Serial 장비를 기존 시스템에 연결하고, 데이터·명령·파라미터·상태 확인 규칙을 맞춰 통합하는 작업**",
    "**Embedded/IoT 프로토타이핑 환경에서 센서·액추에이터·외부 장비를 기존 시스템에 연결하고, 통신 규칙·데이터 형식·명령·파라미터·상태 확인 규칙을 맞춰 통합하는 작업**",
)
replace_once("PROJECT2_ALIGNMENT.md", "- 경험 기간: **2024.03~2024.11, 약 8개월**", "- 공개 기록으로 확인되는 직접 작업 기간: **2024-06-02~2024-09-24, 약 3개월 3주**")
replace_once("PROJECT2_ALIGNMENT.md", "- 대표 프로젝트: **webOS 스마트 화분**", "- 대표 프로젝트: **webOS Smart Home Gardening** — https://github.com/dudgns128/webos-gardening")
replace_once("PROJECT2_ALIGNMENT.md", "- 실제 구성: Raspberry Pi, 센서, 급수 액추에이터, UI/소프트웨어 연동", "- 실제 구성: Raspberry Pi 4 / webOS OSE, Arduino, DHT11, 조도·수위·토양수분 센서, NeoPixel, 물펌프")
replace_once("PROJECT2_ALIGNMENT.md", "- 반복 업무: 장비 연결, 센서 데이터 규격 정리, 제어 로직 작성, HW-SW 통합 및 테스트", "- 반복 업무: I²C command/data contract 작성, raw sensor data 변환, actuator 제어 연결, 상위 service 통합, 실제 HW timing/API 디버깅")
replace_once("PROJECT2_ALIGNMENT.md", "- 반복 문제: 값/단위/전송 규칙 차이, 제어 조건 조율, 실제 HW-SW 인터페이스 연동", "- 과거 프로젝트 통신: **I²C**. Serial 통합 경험으로 과장하지 않는다.")
replace_once("PROJECT2_ALIGNMENT.md", "- 남은 증빙: 실제 코드/문서/commit 링크와 대표 반복 사례 2~3개 정리", "- 대표 commit: `a94a8fc` (I²C HW control), `00e4febe` (timing/parsing fix), `f2e890aa` (dummy→real HW), `ea08aa6a` (HW integration complete)\n- 이번 MVP의 **text Serial Adapter는 과거 경험 그 자체가 아니라, 같은 Device Integration 문제를 다른 물리 인터페이스에서 검증하기 위한 구현 선택**이다.")
replace_once(
    "PROJECT2_ALIGNMENT.md",
    "> **새 센서·액추에이터·Serial 장비를 프로토타입 시스템에 반복적으로 연결하는 개발자가, 장비마다 연결 방식·데이터·명령·파라미터·상태 확인 규칙을 다시 코드에 옮기고 통합해야 하는 반복 작업을 줄이기 위해, 자연어 장비 설명을 검증 가능한 DeviceSpec으로 만들고 승인된 기능만 기존 Agent가 재사용하도록 한다.**",
    "> **새 센서·액추에이터·외부 장비를 프로토타입 시스템에 반복적으로 연결하는 개발자가, 장비마다 통신 방식·데이터·명령·파라미터·상태 확인 규칙을 다시 코드에 옮기고 통합해야 하는 반복 작업을 줄이기 위해, 자연어 장비 설명을 검증 가능한 DeviceSpec으로 만들고 승인된 기능만 기존 Agent가 재사용하도록 한다. 이번 MVP는 그 검증 범위를 문서화된 text Serial 장비로 제한한다.**",
)
replace_once("PROJECT2_ALIGNMENT.md", "1. **이 도메인을 3개월 이상 직접 경험했다고 설명할 팀원이 누구인지** 확인", "1. ~~이 도메인의 3개월 이상 직접 경험자 확인~~ → **완료: 김재훈(`nanocode00`), 공개 GitHub 기록 2024-06-02~09-24**")

# REQUIREMENTS_CHECKLIST.md
replace_once(
    "REQUIREMENTS_CHECKLIST.md",
    "| 팀원 중 해당 버티컬 도메인을 **3개월 이상 직접 경험**한 사람이 있어야 함 | `PARTIAL` | 직접 경험 도메인을 **Embedded/IoT Device Integration**으로 좁혔고, `PREPLANNING.md`에 2024.03~2024.11 webOS 스마트 화분 프로젝트의 장비 통합 경험을 기록함 | 실제 코드/문서/commit 링크와 대표 반복 사례 2~3개를 붙여 증빙 완료 |",
    "| 팀원 중 해당 버티컬 도메인을 **3개월 이상 직접 경험**한 사람이 있어야 함 | `PASS` | `dudgns128/webos-gardening`에서 김재훈(`nanocode00`)의 2024-06-02~09-24 직접 HW-SW 통합 기록 확인. I²C sensor/actuator contract, 실제 데이터 변환, service 연동, timing/API 수정 commit을 `PREPLANNING.md`에 링크함 | 최종 발표/README에서 동일 근거를 짧게 제시 |",
)
replace_once(
    "REQUIREMENTS_CHECKLIST.md",
    "**판정:** Candidate A의 3개월 기간 자체는 **Embedded/IoT Device Integration 경험으로 충족 가능**하다고 본다. 다만 평가자가 확인할 수 있도록 실제 코드/문서/commit 링크와 반복 사례를 붙이기 전까지는 `PARTIAL`로 유지한다. Factory Automation 실무 경험을 근거로 주장하지 않는다.",
    "**판정:** Candidate A의 **3개월 직접 경험 Gate는 PASS**로 본다. 공개 GitHub 기록만으로도 2024-06-02~09-24의 Embedded/IoT HW-SW 통합 작업이 확인된다. 과거 경험은 I²C 기반이며, 이번 MVP의 Serial Adapter는 검증용 구현 선택으로 구분한다. Factory Automation 실무 경험을 근거로 주장하지 않는다.",
)

# README.md
replace_once(
    "README.md",
    "> **중요 Gate:** Project2는 팀원이 해당 사용자·업무 흐름·예외 상황을 **3개월 이상 직접 경험한 버티컬 도메인**이어야 한다. 이 조건을 구체적인 경험과 산출물로 증명하지 못하면 Factory Agent Hub를 최종 주제로 확정하지 않는다.",
    "> **3개월 경험 Gate: PASS.** 직접 경험 도메인은 **Embedded/IoT Device Integration**이다. `dudgns128/webos-gardening` 공개 기록에서 김재훈(`nanocode00`)의 2024-06-02~09-24 I²C 기반 센서·액추에이터 HW-SW 통합 작업을 확인했다. Factory는 적용 시나리오이며 제조 현장 경험을 주장하지 않는다. 이번 MVP의 text Serial Adapter는 동일한 Device Integration 문제를 검증하기 위한 구현 선택이다.",
)
replace_once("README.md", "- **3개월 이상 도메인 직접 경험 Gate**", "- ~~3개월 이상 도메인 직접 경험 Gate~~ → **PASS: `PREPLANNING.md`에 공개 GitHub 근거 정리 완료**")
replace_once(
    "README.md",
    "1. `PREPLANNING.md`의 **3개월 경험 Gate**를 먼저 채운다.\n2. 9/17까지 개인 문제 후보 3개와 후보별 사용자/대안/평가 입력 10건을 준비한다.",
    "1. ~~`PREPLANNING.md`의 3개월 경험 Gate~~ → **완료. 공개 GitHub 근거 확보.**\n2. 9/17까지 개인 문제 후보 3개와 후보별 사용자/대안/평가 입력 10건을 준비한다.",
)
