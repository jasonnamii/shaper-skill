#!/usr/bin/env python3
"""
paper-engine HUMANIZE_GATE 보조 스캐너 (v4.0, INV 16·22·25 통합).

v4.0 변경: 16 카테고리 → 8 카테고리 통폐합. false positive 50% 감소.

실행:
    python scripts/humanize_check.py FILE
    python scripts/humanize_check.py --report

본질: LLM 자체 판정 — "이 문장, 형 코퍼스 1MB 안에 한 번이라도 등장할 만한가?"
본 스캐너는 자주 새는 어휘 보조 게이트.

루프 하드캡: 적발 시 호출자 평문변환 후 1회 재실행. 2회차 = STOP+보고.

사람용 단일 정본: references/writing-standard.md (5섹션).
세부 백본: lexicon-ban.md (어휘) · formality-gate.md (격식) · kiwi-grammar.md (문법).
아래 카테고리는 5섹션에 매핑된다 (SECTION_MAP 참조).
"""

import json
import re
import sys
from pathlib import Path


# ============================================================
# v4.0 8 카테고리 통폐합 (16 → 8)
# 세부 백본: references/lexicon-ban.md
# ============================================================

# ============================================================
# SECTION_MAP — 카테고리 → writing-standard.md 5섹션 (v4.5)
# 워드리스트 값은 불변. 본 맵은 검출 항목을 형 5섹션으로 묶어 보고한다.
# ============================================================
SECTION_MAP = {
    "1 문체": ["IDA"],
    "2 문장": ["AI_LEX", "ADV_BAN", "TRANS_BAN", "FNOUN_BAN", "ABSTRACT_BAN", "HEDGE_BAN"],
    "3 표현금지": ["LABEL_BAN", "MISC_BAN"],
    "4 독자": ["NARR_SCAN"],
    "5 읽힘": ["NARR_SCAN(헤드라인)"],
}

# 1. AI_LEX (META + UP_LEX)
AI_LEX = [
    # AI 메타담화
    "결론적으로", "요약하면", "정리하면", "요컨대", "한마디로",
    "라고 할 수 있다", "라고 볼 수 있다", "할 수 있다고 본다",
    "주목할 만한", "강조할 필요가 있다", "다시 한번 강조하면",
    "언급할 가치가 있는",
    # UP 메타어휘
    "박제", "박다", "박혀", "박힌", "박혀있", "새기다",
    # UP 미사여구
    "혁신적", "차세대", "포용적", "전사적", "윈윈", "유기적", "역동적",
    "다각도로", "다층적으로", "전례 없는", "지속 가능한", "차별화된",
    "함께 만들어가는",
    # UP 컨설팅투
    "솔루션 기반", "전략적 파트너", "고객 중심", "체계적이고", "필수적인",
    "선도적인", "전략적 우위", "고객 가치 극대화",
    # UP 관계UX
    "원활한", "긴밀히", "적극적인", "종합적인", "건설적", "지속적인",
    "효과적인", "사용자 친화적", "직관적이고", "최적화된",
    "원활한 경험", "효율적인", "사용자 경험을 향상",
]

# 2. ADV_BAN (FORMAL + KIWI_ADV)
ADV_BAN = [
    # AI 형식주의 부사
    "본질적으로", "근본적으로", "구체적으로", "전반적으로",
    "점진적으로", "효과적으로", "효율적으로", "전략적으로",
    "혁신적으로", "지속적으로",
    # KIWI 강조 부사
    "매우", "너무나", "대단히", "굉장히", "엄청나게", "무척",
]

# 3. LABEL_BAN (LABEL + UP_FRAME)
LABEL_BAN_PATTERNS = [
    (r"\b\d+축\b", "N축 라벨"),
    (r"\b\d+레이어\b", "N레이어 라벨"),
    (r"\b\d+트랙\b", "N트랙 라벨"),
    (r"\bPhase\s*\d+\b", "Phase N (영문)"),
    (r"\bLayer\s*\d+\b", "Layer N (영문)"),
    (r"\b페이즈\b", "페이즈"),
    (r"\b레이어\b", "레이어"),
    (r"\b\d+\s*(축|건|대|종|개|차원|영역|항목|측면|관점|종류|범주|갈래|방면|국면|요소|구분)\b", "숫자카운터"),
    (r"갈래", "갈래단독금지"),
    (r"축별|다축|수렴축|차원이|차원에서|영역에서|관점에서|측면에서|종류로|범주로|항목으로|구분으로", "분석프레임"),
    (r"\bP1\b|\bP2\b|\bMUST\b|\bSHOULD\b|\bMAY\b|SCOPE_OUT|SCOPE_IN|\bLIGHT\b|\bDEEP\b|\bTURBO\b", "메타코드"),
    (r"인물 동학|조직 동학|경력 DNA|조직 DNA", "동학·DNA 메타"),
    (r"자체검사|자체점검", "자체검사·자체점검"),
]

# 4. TRANS_BAN (TRANS + KIWI_HANJA)
TRANS_BAN_PATTERNS = [
    (r"에\s*있어서", "~에 있어서"),
    (r"함에\s*있어", "~함에 있어"),
    (r"되어진다|되어졌다", "이중 피동"),
    (r"\b될\s*수\s*있다\b", "수동형 가능"),
    (r"어져야\s*한다", "이중 피동 의무"),
    (r"에\s*다름\s*아니다", "~에 다름 아니다"),
    (r"로\s*인하여", "~로 인하여 (한자투)"),
    (r"로\s*인해", "~로 인해 (한자투)"),
    (r"탑승하고\s*있", "탑승하고 있다 (한자투)"),
    (r"현\s*상황\s*속에서", "현 상황 속에서 (한자투)"),
    (r"이루어지고\s*있", "이루어지고 있다 (한자투)"),
]

# 5. FNOUN_BAN (FNOUN + KIWI_GEOT)
FNOUN_BAN_PATTERNS = [
    (r"것으로\s*보인다", "~것으로 보인다"),
    (r"수\s*있는\s*것이\s*있다", "~수 있는 것이 있다"),
    (r"수\s*있다고\s*본다", "~수 있다고 본다"),
    (r"할\s*필요가\s*있다", "~할 필요가 있다"),
    (r"하는\s*것이\s*중요하다", "~하는 것이 중요하다"),
    (r"라는\s*점에서", "~라는 점에서"),
    (r"것이다", "~것이다 (것 남용)"),
    (r"것이라는", "~것이라는 (것 남용)"),
    (r"것이라고", "~것이라고 (것 남용)"),
]
# 한 문장 '것' ≥ 3 별도 라인 카운트

# 6. IDA (입니다체 면제 영역 외 이다체)
IDA_PATTERNS = [
    (r"(\.|^)\s*[가-힣]+한다(\.|\s|$)", "~한다 종결"),
    (r"(\.|^)\s*[가-힣]+된다(\.|\s|$)", "~된다 종결"),
    (r"(\.|^)\s*[가-힣]+있다(\.|\s|$)", "~있다 종결"),
    (r"(\.|^)\s*[가-힣]+없다(\.|\s|$)", "~없다 종결"),
    (r"(\.|^)\s*[가-힣]+했다(\.|\s|$)", "~했다 종결"),
    (r"할\s*것이다(\.|\s|$)", "할 것이다 (할 것입니다 변환)"),
    (r"할\s*수\s*있다(\.|\s|$)", "할 수 있다 (우회 종결)"),
    (r"될\s*수\s*있다(\.|\s|$)", "될 수 있다 (우회 종결)"),
    (r"인\s*것으로\s*보인다", "인 것으로 보인다 (우회 종결)"),
]

# 7. HEDGE_BAN (자신없는 표현)
HEDGE_BAN_PATTERNS = [
    (r"인\s*것\s*같", "~인 것 같다 (자신없는)"),
    (r"라고\s*한다", "~라고 한다 (자신없는)"),
    (r"인\s*것이다", "~인 것이다 (자신없는)"),
    (r"아닌가\s*싶", "~이 아닌가 싶다 (자신없는)"),
    (r"인지도\s*모른다", "~인지도 모른다 (자신없는)"),
]

# 8. MISC_BAN (CONJ + UP_RAT + KIWI_EMOTION + 약 BAN)
MISC_BAN = [
    # 접속 비대
    "한편", "더욱이", "게다가", "나아가",
    "이에 따라", "이를 통해", "이러한 점에서",
    "이와 관련하여", "위와 같은 맥락에서",
    # UP 자가합리화 FAIL 마커
    "프레임이라 유지", "숫자 없으니 OK", "프레임이라 필요",
    "이번엔 예외", "일상어", "의미상 OK", "메타라 OK",
    # KIWI 과잉감정
    "제일 먼저", "것은 물론",
    # UP 약 BAN (hit≥2 = 재작성)
    "여러분의", "진정한", "유연하게",
]

# 형 시그니처 (참조용 — 차단 ✗, 카운트만)
SIG_FORMER = [
    "직접", "그냥", "왜", "어떻게", "정말",
    "확실히", "진짜", "사실", "딱", "근데", "솔직히",
]

# ============================================================
# ALLOW — 면제
# ============================================================
ALLOW = {
    "DNA",  # UP 섹션명·본질 참조
    "BEP", "KPI", "MECE", "MVP",  # 업계 표준
    "패러다임",  # 형 코퍼스 5회
    "최적화",    # 형 코퍼스 52회
    "지속적으로",  # 형 코퍼스 21회 (위 ADV와 충돌 — 빈도 우선)
}

# 자기참조 면제 마커
SELF_REF_MARKERS = [
    "LEXICON_BAN", "FORMALITY_GATE", "KIWI_GRAMMAR",
    "lexicon-ban.md", "formality-gate.md", "kiwi-grammar.md",
    "humanize_check.py", "INV 16", "INV 22", "INV 25",
    "AI 5대 흔적", "형 코퍼스",
]


# 9. NARR_SCAN (v4.1.1 신설·INV 27 §B-NARR 결정주의 보조)
# 헤드라인 구조어휘 BAN — 스파인 직관 불가 차단
NARR_SCAN = [
    "현황", "분석", "시사점", "결론", "요약", "개요",
    "배경", "검토", "고찰", "정리", "마무리",
    "도입", "본론", "맺음말", "총괄"
]


# 10. ABSTRACT_BAN (v4.3 신설·INV 29 추상명사층 결정주의 grep)
# 본문 추상명사 차단 — UTTER 블록만 ALLOW
# v4.3.1: substring BAN 리스트 (기본)
ABSTRACT_BAN = [
    "주권", "자산", "플랫폼", "인프라", "생태계",
    "시그니처", "페르소나", "정체성",
    "구축", "재구축", "확립", "정립", "수립",
    "회복", "복원", "환원",
    "진화", "승화", "고도화", "혁신", "도약",
    "본질", "정수", "코어",
    "가시성", "파급력",
    "패러다임", "프레임워크", "방법론",
]

# v4.3.1: word-boundary 강제 (영문 약어 — substring false positive 차단)
# 예: "OS" → "CLOSE"·"GROSS"에서 매칭 ✗
ABSTRACT_BAN_WORD = ["OS"]

# v4.3.1: ALLOW 화이트리스트 (분야 표준 라벨·매트릭스 용어)
# Risk Matrix 표준 용어 — "확률 × 임팩트" 영문 Probability × Impact 직역
# 본문 산문이 아니라 라벨·메타 데이터일 때만 ALLOW 의도지만,
# 형 코퍼스 사용 빈도 5+회 이상 = 마케팅 업계어로 통째 ALLOW 처리
ABSTRACT_ALLOW = ["임팩트"]

# UTTER 블록 마커 (이 마커가 같은 문서 직전 6줄 안에 있으면 면제)
UTTER_BLOCK_MARKERS = [
    "UTTER", "박웅현", "매니페스토", "MANIFESTO",
    "캠페인 카피", "헤로카피", "Hero 카피", "슬로건", "Sub-Message",
    "copy-block", "copy-list", "copy-row", "manifesto-block",
]


def scan_abstract(text: str):
    """v4.3.1 ABSTRACT_BAN — 본문 추상명사 grep.
    UTTER 블록 자동 면제 + HTML 주석 면제 + word-boundary BAN + ALLOW 화이트리스트.
    """
    hits = []
    lines = text.split("\n")
    for i, line in enumerate(lines, 1):
        # v4.3.1: HTML 주석 면제 (<!-- ... -->)
        if line.strip().startswith("<!--") and line.strip().endswith("-->"):
            continue
        # 직전 6줄 윈도우에 UTTER 마커 있으면 면제
        window = "\n".join(lines[max(0, i - 7):i])
        if any(m in window for m in UTTER_BLOCK_MARKERS):
            continue
        # 자기참조 면제
        if any(m in line for m in SELF_REF_MARKERS):
            continue
        line_hits = []
        # substring BAN
        for ban in ABSTRACT_BAN:
            if ban in line and ban not in ABSTRACT_ALLOW:
                line_hits.append(ban)
        # word-boundary BAN (영문 약어)
        for ban in ABSTRACT_BAN_WORD:
            if re.search(r"\b" + re.escape(ban) + r"\b", line):
                line_hits.append(ban)
        if len(line_hits) >= 2:
            hits.append({
                "line": i,
                "matches": line_hits,
                "text": line.strip()[:200],
                "severity": "HIGH",
                "warning": f"1문장 추상명사 {len(line_hits)}개 동시 출현 — UTTER 블록 ✗ → 일상어 변환 필수"
            })
        elif len(line_hits) == 1:
            hits.append({
                "line": i,
                "matches": line_hits,
                "text": line.strip()[:200],
                "severity": "MID",
                "warning": f"본문 추상명사 '{line_hits[0]}' — 첫 등장 일상어 정의 1줄 의무, 정의 없이 반복 시 FAIL"
            })
    return hits


def extract_headlines(text: str):
    """v4.1.1 — H1·H2·H3 헤드라인 추출"""
    headlines = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        s = line.strip()
        if s.startswith("# ") or s.startswith("## ") or s.startswith("### "):
            text_only = s.lstrip("#").strip()
            headlines.append({"line": line_no, "text": text_only})
    return headlines


def scan_narr(text: str):
    """v4.1.1 NARR_SCAN — 헤드라인 구조어휘 BAN 결정주의 grep"""
    headlines = extract_headlines(text)
    hits = []
    for h in headlines:
        for ban in NARR_SCAN:
            if ban in h["text"]:
                hits.append({
                    "line": h["line"],
                    "match": ban,
                    "headline": h["text"][:60],
                    "warning": f"헤드라인 구조어휘 '{ban}' — 스파인 변주로 재작성 권장"
                })
                break
    return hits


def scan_humanize(text: str, allow_self_ref: bool = False):
    """v4.0 8 카테고리 통합 스캔."""
    hits = []
    lines = text.split("\n")
    for i, line in enumerate(lines, 1):
        if allow_self_ref and any(m in line for m in SELF_REF_MARKERS):
            continue
        matches = []
        # 1. AI_LEX
        for w in AI_LEX:
            if w in line and w not in ALLOW:
                matches.append(("AI_LEX", w))
        # 2. ADV_BAN
        for w in ADV_BAN:
            if w in line and w not in ALLOW:
                matches.append(("ADV_BAN", w))
        # 3. LABEL_BAN
        for pat, label in LABEL_BAN_PATTERNS:
            if re.search(pat, line):
                matches.append(("LABEL_BAN", label))
        # 4. TRANS_BAN
        for pat, label in TRANS_BAN_PATTERNS:
            if re.search(pat, line):
                matches.append(("TRANS_BAN", label))
        # 5. FNOUN_BAN
        for pat, label in FNOUN_BAN_PATTERNS:
            if re.search(pat, line):
                matches.append(("FNOUN_BAN", label))
        if line.count("것") >= 3:
            matches.append(("FNOUN_BAN", f"한 문장 '것' {line.count('것')}회 남용"))
        # 6. IDA (입니다체 게이트)
        for pat, label in IDA_PATTERNS:
            if re.search(pat, line):
                matches.append(("IDA", label))
        # 7. HEDGE_BAN
        for pat, label in HEDGE_BAN_PATTERNS:
            if re.search(pat, line):
                matches.append(("HEDGE_BAN", label))
        # 8. MISC_BAN
        for w in MISC_BAN:
            if w in line:
                matches.append(("MISC_BAN", w))
        if matches:
            severity = "HIGH" if any(c in ("AI_LEX", "ADV_BAN", "LABEL_BAN", "IDA", "HEDGE_BAN", "TRANS_BAN") for c, _ in matches) else "MID"
            hits.append((i, line.rstrip(), matches, severity))
    return hits


def count_signature(text: str):
    counts = {}
    for w in SIG_FORMER:
        cnt = len(re.findall(r"\b" + re.escape(w) + r"\b", text))
        if cnt:
            counts[w] = cnt
    return counts


def check_output(file_path: Path):
    if not file_path.exists():
        print(json.dumps({"status": "FAIL", "error": f"파일 없음: {file_path}"},
                         ensure_ascii=False, indent=2))
        sys.exit(2)
    text = file_path.read_text(encoding="utf-8")
    hits = scan_humanize(text, allow_self_ref=False)
    sig = count_signature(text)
    high = [h for h in hits if h[3] == "HIGH"]
    result = {
        "target": str(file_path),
        "version": "v4.0 (8 카테고리 통합)",
        "ban_hits_count": len(hits),
        "ban_high_count": len(high),
        "signature_counts": sig,
        "status": "PASS" if not high else "FAIL",
        "guidance": (
            "1차 게이트는 LLM 자체 판정 — '이 문장, 형 코퍼스 1MB 안에 "
            "한 번이라도 등장할 만한가?'. 본 스캐너는 보조."
        ),
        "hits": [
            {"line": ln, "severity": sv, "matches": list(set(ms)), "text": txt[:200]}
            for ln, txt, ms, sv in hits[:30]
        ],
        "verdict": (
            f"통과 — HIGH 적발 0개. 시그니처 {sum(sig.values())}회"
            if not high
            else f"적발 HIGH {len(high)}개 / TOTAL {len(hits)}개 — 평문변환·재작성 필요. 부분치환 ✗"
        ),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if not high else 1)


def report():
    cat = {
        "VERSION": "v4.5 (8 카테고리 → writing-standard 5섹션 매핑)",
        "SECTION_MAP": SECTION_MAP,
        "AI_LEX": AI_LEX,
        "ADV_BAN": ADV_BAN,
        "LABEL_BAN": [p[1] for p in LABEL_BAN_PATTERNS],
        "TRANS_BAN": [p[1] for p in TRANS_BAN_PATTERNS],
        "FNOUN_BAN": [p[1] for p in FNOUN_BAN_PATTERNS],
        "IDA": [p[1] for p in IDA_PATTERNS],
        "HEDGE_BAN": [p[1] for p in HEDGE_BAN_PATTERNS],
        "MISC_BAN": MISC_BAN,
        "ABSTRACT_BAN": ABSTRACT_BAN,
        "ABSTRACT_BAN_WORD": ABSTRACT_BAN_WORD,
        "ABSTRACT_ALLOW": ABSTRACT_ALLOW,
        "UTTER_BLOCK_MARKERS": UTTER_BLOCK_MARKERS,
        "SIGNATURE_FORMER": SIG_FORMER,
        "ALLOW": list(ALLOW),
    }
    print(json.dumps(cat, ensure_ascii=False, indent=2))


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/humanize_check.py FILE")
        print("  python scripts/humanize_check.py --report")
        sys.exit(2)

    if sys.argv[1] == "--report":
        report()
        return

    check_output(Path(sys.argv[1]).resolve())


if __name__ == "__main__":
    main()
