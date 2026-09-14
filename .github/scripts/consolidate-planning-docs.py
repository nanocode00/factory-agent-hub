from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"target not found in {path}: {old[:140]}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


replace_once(
    "README.md",
    "자세한 정렬 기준은 [`PROJECT2_ALIGNMENT.md`](./PROJECT2_ALIGNMENT.md), 9/14~17 사전기획은 [`PREPLANNING.md`](./PREPLANNING.md)를 따른다.",
    "현재 프로젝트의 기획·범위·경험 근거·Project2 정렬 기준은 [`PROJECT_PLAN.md`](./PROJECT_PLAN.md)를 source of truth로 사용한다.",
)

replace_once(
    "README.md",
    "| [`PROJECT2_ALIGNMENT.md`](./PROJECT2_ALIGNMENT.md) | **Project2 필수 조건, 배포 구조, 일정, Evals 정렬 source of truth** |\n| [`PREPLANNING.md`](./PREPLANNING.md) | **9/14~17 개인 사전기획: 후보 3개 / 경험 Gate / 평가 입력 후보** |\n| [`PROJECT_PROPOSAL.md`](./PROJECT_PROPOSAL.md) | 제품 가설, ICP/JTBD, Build Gate, prototype 진행 상태, MVP, 안전 경계 |",
    "| [`PROJECT_PLAN.md`](./PROJECT_PLAN.md) | **프로젝트 기획, 직접 경험 근거, ICP/JTBD, 범위, 아키텍처, 안전 경계, 평가 계획 source of truth** |",
)

replace_once(
    "README.md",
    "1. ~~3개월 경험 근거 보강~~ → **완료: `PREPLANNING.md`에 공개 GitHub commit과 반복 사례 정리**",
    "1. ~~기획 문서와 3개월 경험 근거 정리~~ → **완료: `PROJECT_PLAN.md`로 통합**",
)

replace_once(
    "README.md",
    "> 제품 가설·Build Gate·prototype 진행 상태는 `PROJECT_PROPOSAL.md`를 따르고, **현재 하드웨어의 source of truth는 `HARDWARE_SPEC.md`와 `HARDWARE_BOM.md`**다.",
    "> 제품 가설·범위·Build Gate·Project2 정렬은 `PROJECT_PLAN.md`를 따르고, **현재 하드웨어의 source of truth는 `HARDWARE_SPEC.md`와 `HARDWARE_BOM.md`**다.",
)

p = Path("REQUIREMENTS_CHECKLIST.md")
s = p.read_text(encoding="utf-8")
s = s.replace(
    "- `LATER` — 마감 전 필요하지만 현재 단계에서는 아직 수행 시점이 아님",
    "- `LATER` — 마감 전 필요하지만 현재 단계에서는 아직 수행 시점이 아님\n- `DEFERRED` — 요구사항 자체는 남아 있지만 현재 프로젝트 정리 단계에서 의도적으로 보류함",
)
s = s.replace("`PREPLANNING.md`", "`PROJECT_PLAN.md`")
s = s.replace("`PROJECT2_ALIGNMENT.md`", "`PROJECT_PLAN.md`")
s = s.replace("`PROJECT_PROPOSAL.md`", "`PROJECT_PLAN.md`")
s = s.replace(
    "| 사전기획에서 개인별 문제 후보 **3개** 준비 | `PARTIAL` | `PROJECT_PLAN.md` Candidate A 작성, B/C 비어 있음 | Candidate B/C 작성 |",
    "| 사전기획에서 개인별 문제 후보 **3개** 준비 | `DEFERRED` | Factory Agent Hub 단일 주제를 기준으로 기획을 정리하기로 함. 형식만 채우기 위한 B/C는 만들지 않음 | 교육과정에서 3개 후보 제출을 실제 검수할 경우에만 별도로 보완 |",
)
s = s.replace(
    "| 후보별 사용자 상황·현재 대안·범위 정리 | `PARTIAL` | Candidate A와 `PROJECT_PLAN.md`에 일부 존재 | B/C 포함 동일 기준으로 정리 |",
    "| 후보별 사용자 상황·현재 대안·범위 정리 | `PASS` for selected topic | `PROJECT_PLAN.md`에 선택 주제의 사용자, JTBD, 현재 대안/가설, 범위와 제외 범위를 통합 | B/C 후보는 현재 작성하지 않음 |",
)
s = s.replace(
    "| 9/17까지 평가셋 후보 **10건** 준비 | `PASS` for A | `PROJECT_PLAN.md` Candidate A에 10건 존재 | 최종 주제가 A가 아닐 경우 새 후보로 다시 작성 |",
    "| 9/17까지 평가셋 후보 **10건** 준비 | `PASS` | `PROJECT_PLAN.md`에 선택 주제 대표 평가 케이스 10건과 30건 분포가 존재 | 9/23까지 실제 Dataset 30건으로 구체화 |",
)
p.write_text(s, encoding="utf-8")

for path in ["IMPLEMENTATION_PLAN.md", "AGENTS.md"]:
    p = Path(path)
    s = p.read_text(encoding="utf-8")
    s = s.replace("PROJECT2_ALIGNMENT.md", "PROJECT_PLAN.md")
    s = s.replace("PROJECT_PROPOSAL.md", "PROJECT_PLAN.md")
    s = s.replace("PREPLANNING.md", "PROJECT_PLAN.md")
    p.write_text(s, encoding="utf-8")

for path in ["PROJECT2_ALIGNMENT.md", "PROJECT_PROPOSAL.md", "PREPLANNING.md"]:
    Path(path).unlink()
