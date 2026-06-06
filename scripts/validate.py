#!/usr/bin/env python3
"""
paper-engine self-check validator (v2.5).

실행:
    python scripts/validate.py .                       # SKILL.md 자체 검증
    python scripts/validate.py --check-output FILE     # 산출물 NO_WORK_LABEL 스캔 (보조)

NO_WORK_LABEL — 사람용 정본 references/writing-standard.md §3 표현금지
  세부 백본: references/no-work-label.md
  본질 게이트는 LLM 자체 판정질문: "이 단어, 이 대화 밖 사람이 사전 없이 읽을 수 있나?"
  본 스캐너는 자주 새는 단어를 사전·패턴으로 잡는 '보조 게이트'.

루프 하드캡: 검증 실패 시 호출자가 수정 후 1회 재실행. 2회차 실패 → STOP + 사용자 보고.
"""

import json
import re
import sys
from pathlib import Path


REQUIRED_FRONTMATTER = ["name", "version", "description", "vault_dependency"]
REQUIRED_SECTIONS = ["CHANGELOG", "STEALTH", "Self-Check"]
EXAMPLE_HEADING_PATTERN = re.compile(r"^##\s*예시", re.MULTILINE)


# ============================================================
# NO_WORK_LABEL — 보조 사전·패턴 (v2.5, INV 13)
# 단일 권위는 references/no-work-label.md
# 이 사전은 자주 새는 단어를 1차 검출하는 보조 도구.
# ============================================================

# 1. 형이 명시한 1순위 라벨 (구조 라벨)
LABEL_STRUCTURE = [
    "레이어", "트랙", "범주축", "페이즈",
]
# "축" 단독은 너무 일반어 → 패턴(N축)으로만

# 2. 산출물 구조 라벨 (NYT 내부어)
LABEL_NYT = [
    "Headline", "Lead", "Kicker", "Nut graf",
    "압정", "Pin↔Body", "역피라미드", "모래시계",
]
# "Pin", "Body", "Lead"는 일반어 충돌 — Pin↔Body·Headline·Lead 인접 패턴 위주로

# 3. 모드·분기 코드
LABEL_MODE = [
    "DOC_TYPE",
    "DELIVER", "DIAGNOSE", "EVALUATE", "CONVERGE",
    "EXPAND", "SINGLE", "MULTI", "METAPHOR",
]
# DEEP/LIGHT/TURBO는 일반어 충돌 가능 → 패턴으로

# 4. 사고도구·검증 라벨
LABEL_TOOLS = [
    "spine", "triage",
    "Claim-Evidence-Warrant", "C+E+W",
    "EVIDENCE_INJECTION", "NUMBER_PROVENANCE",
    "SOURCE_CONTRAST", "CLAIM_PROVENANCE", "EVIDENCE_BODY",
]

# 5. 운영·게이트키퍼 어휘
LABEL_OPS = [
    "게이트키퍼", "STEALTH", "PREFLIGHT", "핸드오프",
    "BANNED_VOCAB", "NO_WORK_LABEL",
]

LABELS = LABEL_STRUCTURE + LABEL_NYT + LABEL_MODE + LABEL_TOOLS + LABEL_OPS

# 패턴 — 작업 라벨 패턴(단어+숫자 조합)
LABEL_PATTERNS = [
    (r"\b\d+축\b", "N축 패턴 (예: 4축·7축·18축)"),
    (r"\b\d+트랙\b", "N트랙 패턴 (예: 3트랙)"),
    (r"\b\d+레이어\b", "N레이어 패턴"),
    (r"\bINV\s*\d+\b", "INV 코드 (예: INV 13)"),
    (r"\bMODE_[SML]\b", "MODE 코드 (MODE_S/M/L)"),
    (r"\bDOC_TYPE\b", "DOC_TYPE 라벨"),
    (r"\b\d+항\s*QC\b", "N항 QC"),
    (r"\b\d+패스\b", "N패스 (3패스 등)"),
    (r"v\d+\.\d+(?:\.\d+)?\s*(?:페이퍼엔진|paper.?engine)\s*통과", "메타 통과 표기"),
    (r"압정\s*\d+\s*[:.]\s*\d+\s*[:.]\s*\d+", "압정 비율 표기"),
    (r"\b[CEW]\s*[+]\s*[CEW]", "C+E+W 사고도구 표기"),
    (r"\bPin\s*[↔↑→]\s*Body\b", "Pin↔Body 라벨"),
    (r"\b페이퍼엔진\b", "페이퍼엔진 (스킬 이름) 산출물 메타 표기"),
]

# ============================================================
# ALLOW 화이트리스트 — 업계 전문용어·고유명사·법조문
# 이 단어들은 라벨처럼 보여도 통과 (no-work-label.md §3)
# ============================================================
ALLOW_INDUSTRY = {
    "BEP", "KPI", "MECE", "MVP", "ROI", "ROAS", "CAC", "LTV",
    "OKR", "MOU", "NDA", "IPO", "M&A", "SAFE", "SHA", "ESOP",
    "JTBD", "AARRR", "RCA",  # 업계인이 사전 없이 읽음
    "p-value", "GDPR",
    "Lead",  # 영어 단어 lead는 일반어
    "Pin",   # 단독은 일반어 (Pin↔Body 패턴만 차단)
    "Body",  # 단독은 일반어 (본문 의미)
    "DEEP", "LIGHT", "TURBO",  # 일반어 충돌
}

# 자기참조 면제 라인 마커 (스킬 본문 자체 스캔 시)
SELF_REF_MARKERS = [
    "NO_WORK_LABEL", "no-work-label.md",
    "INV 13", "v2.5",
    "BANNED_VOCAB",  # legacy
]


def parse_frontmatter(text: str):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).split("\n"):
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm


def scan_labels(text: str, allow_self_ref: bool = False):
    """라벨 사전·패턴 스캔. (line_no, line, matches) 리스트 반환."""
    hits = []
    lines = text.split("\n")
    for i, line in enumerate(lines, 1):
        if allow_self_ref and any(m in line for m in SELF_REF_MARKERS):
            continue
        matches = []
        # 사전
        for w in LABELS:
            if w in ALLOW_INDUSTRY:
                continue
            if re.match(r"^[A-Za-z]", w):
                if re.search(r"\b" + re.escape(w) + r"\b", line):
                    matches.append(w)
            else:
                if w in line:
                    matches.append(w)
        # 패턴
        for pat, label in LABEL_PATTERNS:
            if re.search(pat, line):
                matches.append(f"[패턴] {label}")
        if matches:
            hits.append((i, line.rstrip(), matches))
    return hits


def check_output(file_path: Path):
    """산출물 NO_WORK_LABEL 스캔. exit 0 통과, 1 적발."""
    if not file_path.exists():
        print(json.dumps({"status": "FAIL", "error": f"파일 없음: {file_path}"},
                         ensure_ascii=False, indent=2))
        sys.exit(2)
    text = file_path.read_text(encoding="utf-8")
    hits = scan_labels(text, allow_self_ref=False)
    result = {
        "target": str(file_path),
        "hits_count": len(hits),
        "status": "PASS" if not hits else "FAIL",
        "guidance": (
            "1차 게이트는 LLM 자체 판정질문 — "
            "'이 단어, 이 대화 밖 사람이 사전 없이 읽을 수 있나?'. "
            "본 스캐너는 자주 새는 단어를 1차 검출하는 보조다. "
            "스캐너 통과해도 LLM 판정으로 한 번 더 훑어라."
        ),
        "hits": [
            {"line": ln, "matches": sorted(set(ms)), "text": txt[:200]}
            for ln, txt, ms in hits
        ],
        "verdict": (
            "통과 — 보조 사전 적발 0개 (단, LLM 판정 1회 추가 권장)"
            if not hits
            else f"적발 {len(hits)}개 라인 — 전수 재작성 필요. 부분 치환 ✗"
        ),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if not hits else 1)


def check(skill_path: Path):
    errors = []
    warnings = []

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        errors.append(f"SKILL.md 부재: {skill_md}")
        return errors, warnings

    content = skill_md.read_text(encoding="utf-8")

    # 1. Frontmatter
    fm = parse_frontmatter(content)
    for field in REQUIRED_FRONTMATTER:
        if field not in fm:
            errors.append(f"frontmatter 필드 누락: {field}")

    # 2. references/
    ref_dir = skill_path / "references"
    if not ref_dir.exists() or not list(ref_dir.glob("*.md")):
        warnings.append("references/ 스포크 없음 (허브스포크 권장)")

    # 2-b. no-work-label.md (v2.5 단일 권위)
    no_label_doc = ref_dir / "no-work-label.md"
    if not no_label_doc.exists():
        errors.append("references/no-work-label.md 부재 (v2.5 INV 13 본질 사전)")

    # 3. evals/cases.json
    eval_file = skill_path / "evals" / "cases.json"
    if not eval_file.exists():
        errors.append("evals/cases.json 부재")
    else:
        try:
            data = json.loads(eval_file.read_text(encoding="utf-8"))
            n = len(data.get("cases", []))
            if n < 3:
                errors.append(f"evals cases {n}건 < 3건 최소 요구")
        except json.JSONDecodeError as e:
            errors.append(f"evals/cases.json 파싱 실패: {e}")

    # 4. Required sections
    for sec in REQUIRED_SECTIONS:
        if sec not in content:
            errors.append(f"필수 섹션 부재: {sec}")

    # 5. 예시 섹션 라벨 누출 점검 (학습 오염 방지)
    m = EXAMPLE_HEADING_PATTERN.search(content)
    if m:
        example_text = content[m.start():]
        next_h = re.search(r"\n##\s", example_text[3:])
        if next_h:
            example_text = example_text[: next_h.start() + 3]
        ex_hits = scan_labels(example_text, allow_self_ref=False)
        if ex_hits:
            for ln, txt, ms in ex_hits[:5]:
                warnings.append(
                    f"예시에 라벨 잔존 (라인 {ln}): {sorted(set(ms))[:3]}"
                )

    # 6. Size advisory
    size = skill_md.stat().st_size
    if size > 12288:  # v2.5 INV 13 추가로 12KB 완화
        errors.append(f"SKILL.md {size}B > 12KB (허브 슬림 기준 위반)")
    elif size > 5120:
        warnings.append(f"SKILL.md {size}B > 5KB (목표 미달)")

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/validate.py <skill_path>")
        print("  python scripts/validate.py --check-output FILE")
        sys.exit(2)

    if sys.argv[1] == "--check-output":
        if len(sys.argv) < 3:
            print("FAIL: --check-output FILE 인자 필요")
            sys.exit(2)
        check_output(Path(sys.argv[2]).resolve())
        return

    skill_path = Path(sys.argv[1]).resolve()
    errors, warnings = check(skill_path)

    result = {
        "target": str(skill_path),
        "errors": errors,
        "warnings": warnings,
        "status": "PASS" if not errors else "FAIL",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
