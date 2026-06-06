# ABSTRACT_BAN — 추상명사 차단 정본 (v4.3, INV 29)

> 상위 정본: `references/writing-standard.md` §2 문장. 본 문서는 해당 섹션의 세부 백본.

§B-PRE ⑩번째 룰. 본문 추상명사 차단·UTTER 블록만 ALLOW.

정본 BAN 리스트는 `lexicon-ban.md §2-9` 참조. 본 파일 = SKILL.md §B-PRE ⑩에서 호출되는 운영 가이드.

---

## 1. 본질 1줄

**RULE:** DELIVER·CONVERGE·DIAGNOSE·EVALUATE 본문 = 추상명사 BAN. UTTER 블록만 ALLOW. 같은 문서 안에서도 block-level 분기.

---

## 2. 3대 FAIL 조건 (본문)

1. **첫 등장 정의 누락** — 추상명사 본문 등장 시 *첫 등장에 일상어 정의 1줄* 의무. 정의 없이 반복 = FAIL
2. **1문장 합성** — 1문장에 추상명사 2+ 동시 = FAIL
   - 예: "디지털 페르소나 자산" / "알고리즘 주권 회복" / "자기 구축형 창작자 OS"
3. **합성 명사** — 영문+한자·한자+한자 추상명사 결합 본문 노출 = FAIL
   - 예: "Algorithm Sovereignty"·"Creator OS"·"Digital Persona"

---

## 3. 자가합리화 차단 (UP)

| 마커 | 판정 |
|---|---|
| "컨셉이니 예외" | ✗ |
| "외래어 아니니 OK" | ✗ |
| "마케팅 업계어니 OK" | ✗ |
| "박웅현이 쓸 법하니 ALLOW" | ✗ (UTTER 명시 ✗ = BAN) |
| **🆕 "내 검증 끝났으니 OK"** | ✗ (수동 grep·화이트리스트 누락·section ID 축소 = false-clean. `humanize_check.py scan_abstract()` 자동 grep만 인정) |

→ UTTER 모드는 *블록 호출 시 명시*만 인정. 추론·암묵 ✗.

---

## 4. UTTER 면제 메커니즘

**block-level 명시 = ALLOW.** 같은 .md/.html 안에서도:
- 본문 (DELIVER) → BAN
- 카피 블록·매니페스토 블록·슬로건 블록 (UTTER) → ALLOW

**자동 인식 마커 (`humanize_check.py` UTTER_BLOCK_MARKERS):**
`UTTER`·`박웅현`·`매니페스토`·`MANIFESTO`·`캠페인 카피`·`헤로카피`·`Hero 카피`·`슬로건`·`Sub-Message`·`copy-block`·`copy-list`·`copy-row`·`manifesto-block`

직전 6줄 윈도우에 마커 1+ 등장 시 면제.

---

## 5. ❌WRONG / ✅CORRECT

```
❌ 본문(DELIVER): "C8 = 자기 구축형 창작자 OS. 디지털 페르소나 자산을 통한 알고리즘 주권 회복."
   → 추상명사 5개·일상어 정의 0개·1문장 합성 폭주

✅ 본문(NYT/DELIVER):
   "C8은 창작자가 일하는 곳입니다.
    작업물·이력·연결을 한 곳에 모읍니다.
    SNS 알고리즘이 잘게 자른 자기를, 다시 묶습니다."

✅ 카피 블록(UTTER, 면제):
   "알고리즘 주권 회복"
   ← UTTER 블록 명시 = ALLOW
```

---

## 6. 자가검사 (② 진입 직전)

"이 문서의 본문 블록과 카피 블록을 *지금* 분리하고 작성하나, 작성 후 분리하나?"
→ 후자 = FAIL → ② 재진입.

---

## 7. CHECK (송출 직전)

`python scripts/humanize_check.py FILE` → ABSTRACT_BAN HIGH 0 / MID는 정의 1줄 동반 확인 후 통과.
