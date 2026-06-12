## v5.1.0 (2026-06-12) — 시점 분리: 생성은 긍정 가이드, 자국 점검은 Self-Check 전용

**근본 진단:** 생성 시점에 금지 목록(ban 계열)을 컨텍스트에 펼치면 그 토큰이 산출물에 묻어 나온다 — 프라이밍·문체 전이·메타 누설. v5.0까지는 작성과 퇴고가 같은 참조 묶음을 봐서, 본문을 쓰는 손이 금지 패턴 원문에 노출됐다.

**처방 1 — `references/good-sentences.md` 신설 (작성용 긍정 가이드):**
- 좋은 문장 12유형 — 유형·기준·좋은 예만 수록, 나쁜 예 원문 0건.
- 예외 조건 6가지(능동태·명사화·단문·두괄식·상대 주어·쉬운 말의 예외 자리).
- 적용 우선순위: ①결론 선행 ②수치 구체화 ③주어 점검.
- 근거: `Temp/기획서-제안서-문장유형-리서치_2026-06-12/00_종합_문장유형-카탈로그.md` (5축 교차 리서치).

**처방 2 — 시점 분리 명문화:**
- `SKILL.md` '작성·퇴고 기본 기준' — 작성 중에는 good-sentences.md(향할 곳)만 보고, ban 계열 참조(lexicon-ban·abstract-ban·kiwi-grammar·no-work-label·humanize-gate)는 Self-Check 때만 연다.
- '작성 순서' 4번(단별 본문 작성)에 good-sentences.md 참조 추가.
- 참조 목록 — good-sentences.md를 작성용으로 §2 문장 백본 위에 추가, ban 계열 §2·§3 백본에 '(셀프체크 전용)' 표기. 참조 파일 삭제 없음.
- `references/writing-standard.md` — 섹션별 [작성]/[퇴고] 시점 라벨 부여, §2 작성 항목을 긍정형(결론 선행·수치·주어)으로 전환하고 자국 점검은 퇴고 블록으로 이동, §3 표현금지·§매핑을 퇴고 전용으로 고정.

**처방 3 — 검수 정본 연결:**
- Self-Check 말미 1줄 — 검수 자국의 정본은 submission-cleanup의 sentence-catalog, 제출 직전 문서는 그쪽으로 넘긴다.

**파일 변경:**
- `SKILL.md` — version 5.1, 시점 분리·작성 순서 4번·참조 목록·Self-Check·CHANGELOG 갱신.
- `references/good-sentences.md` — 신설.
- `references/writing-standard.md` — 작성/퇴고 시점 분리 개편.

---

## v5.0.0 (2026-06-12) — 흐름 정본 + 시각화 폴백

**근본 진단:** v4.x는 문장·서사 게이트(스파인 1줄·NARR 4종·5섹션)는 강하지만, 문서 *전체 배열*의 정본이 없었다. 결과적으로 흐름은 DOC_TYPE 골격에 의존했고, 미괄식·나열형 같은 배열 선택과 기획안 고유 규율(상대 세계관)이 비어 있었다.

**처방 1 — 흐름 정본 신설 (`references/flow-skeleton.md`):**
- 8단 기본 흐름: 요약 → 접근 → 발견 → 전략 → 통찰 → 액션아이템 → 요약(말미) → 첨부. 모든 문서는 이 흐름의 변형.
- 두 요약의 역할 분리 (서두=결론 예고 / 말미=결정·다음 행동, 문장 재사용 금지).
- 첨부 = 오컴의 집행 장치 (깎은 것은 삭제가 아니라 강등).
- 배열 3종: 두괄식(기본) · 미괄식(아이디어·컨셉이 상품인 기획안의 클라이맥스 전용, 동어 빌드업 금지) · 나열형(전체 조명 1화면 → 하나씩, 골격 반복=리듬·내용 반복=결함).
- 기획안 규율: 상대가 듣고 싶어하는 세계관 안의 독창성, 다른 산 금지, 창의 안의 논리, 쉬움이 관문.
- 고정과 자유 강도 설계: 강제는 결함 차단까지만, 유니크함이 사는 자리(어휘·리듬·사례·배열·밀도)는 비워 둠.
- doc-types와의 관계 명시: 전체 배열=flow-skeleton, 섹션 내부 의무(근거 컬럼·교차비교)=doc-types.

**처방 2 — 시각화 폴백 신설 (`references/viz-fallback.md`):**
- 디자인 스킬(apple-canvas·prism-design·editorial-design·box-cut-design·teenage-design) 미발동 md 문서에서 본문 시각화를 셰이퍼가 메움.
- 정보 유형 → md 장치 매핑 (벤또 지도 표·단계 플로우·근거 컬럼 표·수치 라인·인용 블록·mermaid).
- 장치에 넣은 정보의 산문 반복 금지. 디자인 스킬 발동 문서엔 개입 금지.

**파일 변경:**
- `SKILL.md` — §흐름·§시각화 폴백 신설, 흐름설계 모드 추가, 작성 순서 6단 개편, 트리거(세이퍼·흐름 잡아줘·구조 잡아줘·미괄식 등)·NOT 경계(planning-skill·디자인 5종·visualize-skill·html-finisher·c8-pl-hub) 재정비, Self-Check §0 흐름 추가.
- `references/flow-skeleton.md` — 신설.
- `references/viz-fallback.md` — 신설.
- `references/writing-standard.md` — 문장 기준 vs 구조 기준 권위 분리 포인터 추가.

---

## v3.2.0 (2026-05-01) — PT_FORMAT_GUARD + 도구함 자연주입

**INV 21 신설:** PT 산출물 형식 가드 2종 강제 + 도구함 9종 자연주입.

**박제 사유:** 형 PT 패턴 진단서 v1 (209덱 15,183 슬라이드 정량 + 11덱 deep-dive). G-1~G-5 구조 그대로 반영.

**박제 방식:**
- **강제 = 2종 (G-5 형식 가드):** placeholder ✗ · 불릿위주 ✗
  - 209덱 placeholder 활용률 ≈ 0% 정량 근거
  - PT 산출물 한정 (md/html 본문 ✗)
- **자연주입 = 9종 + 골격 2종:** 명시 호출시만 활성, 강제 ✗
  - G-1 골격 (SCQA·Duarte) · G-2 강조 (반복압박·Triplet·인용·침묵) · G-3 전환 (Old vs New·발상전환·비유캐스케이드) · G-4 결말 (단일·다중옵션·열린질문)
  - 트리거: "PT 패턴", "형 스타일", "PT_DOC", "PT 모드"
  - 0개 선택 허용

**평균화 트랩 회피:** 룰화 ✗ → 데이터화 ○. 도구 자체는 references에 카탈로그, SKILL.md 본문은 호출 1줄만. 진화 압력 = 코퍼스 갱신으로 위임 (SKILL.md 본체 안정성 보존).

**파일 변경:**
- `SKILL.md` — INV 21 추가 + §B-PRE 확장 + 절대규칙 (20)→(21)
- `references/jason-pt-toolkit.md` — 신설 (220줄, 골격 2종·도구 9종·표준 매핑)

**미박제 (의도적 제외):**
- 시그니처 슬라이드 ("By 최남tel.com") — 형 개인 의존, 일반 룰화 ✗
- 표준 60~100장 — 강제시 부작용
- 레퍼런스 적금 표지 — 형 포트폴리오 의존
- 위치 결정론 5단 강제 — 평균화 트랩 우려, 골격 권장으로 약화

**헤리티지:** 형 컨펌 (2026-05-01) — "PT_DOC 분리 ✗ · 강제 ✗ · 도구함 ✓ · 자연주입 ✓ · 사전생성형".

---

# CHANGELOG

## v4.4.0 (2026-05-07) — BIZ_DOC 모드 신설

**근본 진단:** 기존 5종 (DELIVER·DIAGNOSE·EVALUATE·CONVERGE·UTTER)으론 외부 독자 비즈니스 문서 본문 영토 부재. DELIVER는 보도·1pager 중심·UTTER는 카피·매니페스토. 그 사이 빈자리(투자제안·전략설명서·기획안 본문·IR 본문)에서 카피 톤 침범 또는 박웅현 톤 침범으로 메모형 변질.

**처방:** DOC_TYPE 6번째 BIZ_DOC 신설.
- §B-PRE ① 단문 강제 OFF (20~40자 권장)
- §B-PRE ② 시그니처(직접·그냥·왜·정말·진짜·근데) OFF — 외부 독자 위화감
- §B-PRE ④ 1문장 1명제 → 종속절·연결조사 ALLOW (단, 명제 2+ 동시 ✗)
- §B-PRE ⑤ 문단 ≤80자 → 문장 ≤60자·문단 ≤200자
- §B-PRE ⑥ 격식 LV3 강제 (외부 독자)
- §B-PRE ③⑦⑧⑨⑩ 유지
- §B-NARR N1·N2·N3·N4 풀강제 (외부 독자에 서사층이 더 중요)
- PERSONA: 작성자=유시민·편집자=이오덕 (CONVERGE와 동일)
- block-level 분기: 같은 문서 안 카피 블록은 UTTER 명시 면제 (manifesto-block·copy-block·copy-list·hero-copy 등 마커)

**검증:** c8-launching-campaign.html 본문 — GPT 제안 50건+ 검토 결과 BIZ_DOC 룰과 100% 정합. v4.4 적용 시 같은 산출물 1턴 생성 가능.

**파일 변경:**
- `references/biz-doc-mode.md` — 신규 정본
- `references/doc-types.md` — 4종류 → 5종류
- `references/pre-write-guard.md` — §1-bis BIZ_DOC 분기 신설
- `SKILL.md` — version 4.3.1 → 4.4.0·INV 30 추가·§A-2/§A-3/§B-PRE/§B-NARR/Gotchas/WRONG-CORRECT/예시 3 추가

**우선순위 갱신:** 22 > 16 > 13 > 25 > 27 > 29 > **30** > 17·18

---

 — shaper-skill

## v3.1.0 (2026-05-01) — PRE_WRITE_GUARD: 사전생성형 전환

### 배경

형 핵심 진단: "현재 메커니즘은 LLM이 일단 쓴 뒤 9패스로 사후교정 = 1번. 근본적이지 않은 심각한 오류."

v3.0 분석 결과 형 진단 정확:
- ③ §B 작성 단계 = 구조 명세만, 생성 룰 부재
- ④~⑦ = 사후 교정·압축·게이트
- 결과: LLM 평소 verbosity → 9패스 사후 깎기 → AI식 골격은 그대로

v3.1 목표: 사전생성형 전환 (1번 → 2번 메커니즘)

### 변경

- **INV 19 신설** — PRE_WRITE_GUARD. §B 작성 진입 전 5종 룰 강제 적용. 첫 단어부터 룰 박힌 상태.
- **5종 룰** — ① 단문 8~20자 ② 시그니처 자연주입 ③ BAN 사전회피 ④ 1문장 1명제 ⑤ 문단 ≤80자.
- **메타룰 6** — 토큰 직전 자기검열: "이 문장, 형 코퍼스 1MB에 등장할 만한가?" NO → 재생성.
- **§B-PRE 신설** — §B 구조 진입 전 5종 룰 활성화.
- **§G 파이프라인 재설계** — ③ §B-PRE 활성화 → §B 작성[5종 강제] → ④ §C 9패스(안전망). 사후교정 ✗·사전생성 ○.
- **§H 자체 스캔** — 6중 → 7중 (INV 19 추가).
- **references/pre-write-guard.md 신설** — 본질·5종 룰 상세·예시·§B 단계별 생성 룰·자체검사 절차·Gotchas. 9.8KB.
- **절대 규칙** — 18개 → 19개.
- **description 갱신** — P1에 "사전가드·작성가드", P3에 "pre-write guard" 추가.
- **Gotchas** — "사후교정 의존 (1번 메커니즘)" 추가.

### 메커니즘 전환

| | v3.0 | v3.1 |
|---|---|---|
| ③ §B 작성 | 구조 명세만 | **5종 룰 강제** |
| ④ §C 9패스 | 메인 게이트 | 마지막 안전망 |
| 비율 | 30% 사전 + 70% 사후 | 80% 사전 + 20% 사후 |

### 자체검사

- validate.py: PASS (errors=[])
- humanize_check.py SKILL.md 자체: PASS (HIGH 적발 0)
- SKILL.md 12,104B (12KB 슬림 통과)

### 호환성

기존 v2.6·v3.0 모두 보존. INV 13~18 그대로. v3.1은 §B 작성 단계 *진입 시점*에 룰을 박는 추가 층.

---

# CHANGELOG — shaper-skill

## v3.0.0 (2026-05-01) — HUMANIZE_GATE: AI 문서티 0에 수렴

### 배경

형 직접 지시: "AI가 쓴 문서티를 0.1%도 내지 않는 것이 목표."

형 명시 3대 증상:
1. AI 문서는 30%만 핵심, 70%는 쓰레기 (반복·중복·과장·장황한 늘림)
2. 문체가 점점 영어 번역투. 문체 수준이 너무 낮음
3. 축·대·레이어·페이즈 같은 단어를 굳이 쓰지 않아도 됨

### 리서치 (research-frame DEEP+EXPAND)

- 5축 리서치: AI탐지 학술논문(GPTZero·DetectGPT·burstiness) · 한국어 번역투 코퍼스 · 한국 명문 산문(김훈·박완서·신영복·유시민) · AI 장황 메커니즘(RLHF length bias) · 한국 비즈 산문 품질 기준
- 형 코퍼스 23개 PDF·1MB·19,874줄 실측: AI 5대 흔적 단어("결론적으로·요약하면·함에 있어·라고 할 수 있·주목할") = 0회 · 형 시그니처("직접·그냥·왜·어떻게·정말·확실히·진짜·딱·근데·솔직히") = 합 196회 · 작업라벨(1축·2축·3축·레이어·페이즈) = 0회
- 리서치 박제: VAULT/_skills research/paper-engine_humanize_2026-05.md + VAULT/_skills research/shaper-skill/2026-05-01_humanize-gate-design.md

### 변경

- **INV 16 신설** — BAN_LEXICON. AI 5대 흔적·형식부사·접속비대·번역투·형식명사 어휘 60+ grep 차단. 형 코퍼스 1MB 실측 0회 검증된 어휘 우선.
- **INV 17 신설** — STYLE_NORTH_STAR. 한국 명문 산문 + 형 시그니처 융합 10조. 평균 문장 8~20자·구체명사 70%+·능동형·한자어 50% 이하·종결어미 다양화·시그니처 어휘 자연주입·수치+출처 박싱.
- **INV 18 신설** — ANTI_BLOAT. 기존 §C 3패스 → 9패스 강화. 질문재술·서문과잉·헤징캐스케이드·동의어나열·예시과다·3항강박·"수있다"우회·수식어누적·산출직전70%절단. 50%+ 감축 목표.
- **§C-NEW** — 9패스 압축 표 (기존 3패스 대체).
- **§G 파이프라인 ⑦** — 자체 스캔 6중 통합 (INV 13·14·15·16·17·18).
- **§H 자체 스캔** — 6 INV 통합 검사 표.
- **references/humanize-gate.md 신설** — INV 16·17·18 본질 단일 권위. 형 코퍼스 실측 데이터·3중 게이트 본질·STYLE 10조·9패스·파이프라인 통합·Gotchas.
- **references/banwords-lexicon.md 신설** — BAN_LEXICON 사전. 7카테고리 60+ 어휘 + 평문 변환표 + 형 시그니처 빈도표.
- **scripts/humanize_check.py 신설** — 산출물 휴머나이즈 보조 스캐너. BAN_META·FORMAL·CONJ·TRANS·FNOUN·LABEL 6분류 + 형 시그니처 카운트.
- **description 갱신** — v3.0 휴머나이즈 키워드 추가 (휴머나이즈·AI문서티·번역투·장황·압축).
- **Gotchas 통합** — 기존 6항 휴머나이즈 가타를 INV 16·17·18 단일 포인터로.
- **절대 규칙 16·17·18 추가** — 15개 → 18개.

### 자체검사

- validate.py: PASS (errors=[])
- humanize_check.py SKILL.md 자체: PASS (HIGH 적발 0)
- SKILL.md 12233B (12KB 슬림 기준 통과)

### 호환성

기존 v2.6 INV 13·14·15 전부 보존. v3.0은 위에 *얹는* 층. DOC_TYPE 4분기·HERO 형식·작업라벨 본질보호·어조 룰 그대로.

---

# CHANGELOG — shaper-skill

## v2.6.0 (2026-04-26) — HERO 형식 기본 모드 + 어조 룰

### 배경

KISAS 방향전환 정리 작업에서 형의 명시적 룰 도출:
- "각 섹션 첫 줄에 HERO 한 문장. HERO만 쭉 읽어도 방향성을 알 수 있게."
- "선언적 멋짐 금지. 담담하게."
- "HERO 한 줄들이 분석 → 핵심 → 아이템 서사로 흐른다. 본문은 NYT·모래시계 등 내용 구조와 직교."
- "장사 어휘(팔다·전환·만석) 금지. 인물 호칭(피디님·박사) 금지. 버전 라벨(v3.2·SoT) 금지. 작업 약자(LTV·NPS) 풀어쓰기."

### 변경

- **INV 14 신설** — HERO 형식. 모든 본문 섹션 첫 줄 = 압축 한 문장. HERO만 차례로 읽으면 분석→핵심→아이템 서사. 한 섹션이라도 누락 = FAIL. 담담 톤.
- **INV 15 신설** — 어조 룰. 인물 호칭·버전 라벨·장사 어휘·작업 라벨·작업 약자 금지. 업계 표준 약자(BEP·KPI·MECE·MVP)는 한 번 정의 후 통과.
- **§B-1 갱신** — Body 정의에 HERO 한 줄 의무 추가.
- **§B-4 신설** — HERO 서사 흐름 (분석→핵심→아이템). 마지막 묶음 분석 면제.
- **§E-1·E-2 갱신** — 강제·금지 항목에 HERO·어조 룰 추가.
- **§G 파이프라인 ⑩-b 확장** — 작업라벨(INV 13) + HERO 서사(INV 14) + 어조(INV 15) 3중 자체 스캔.
- **§I 자체 스캔** — 3 INV 통합 검사 표.
- **references/hero-format.md 신설** — 본질 4줄·HERO 룰·서사 흐름·담담 톤·어조 사전·결합 예·Gotchas.
- **description 압축** — 853자 → 500자 미만. P3에 영문 키워드 추가(NYT inverted pyramid·CEW·document type router·hero format).
- **Gotchas 확장** — HERO 누락·카피 톤·서사 깨짐·인물 호칭·장사 어휘·약자 풀어쓰기 누락 6항.

### 직교 원리

HERO는 형식 층, DOC_TYPE은 내용 층. 전달형·진단형·평가형·수렴형 어느 것이든 HERO를 입을 수 있다. NYT 압정 본문 + HERO, 5Whys 진단 본문 + HERO, 다소스 매트릭스 본문 + HERO 모두 가능.

### 호환성

기존 v2.5의 INV 1~13 모두 유지. v2.5 산출물은 v2.6에서 INV 14·15 추가 검사 시 HERO 누락·어조 위반으로 FAIL 가능 → 재작성 필요.

---

## v2.5.0 (2026-04-25) — NO_WORK_LABEL 본질보호 게이트

형 진단(양평 v3 사례 `00_기획종합분석_v3.md`): **"산출물에 축·레이어·트랙 같은 작업 라벨 단어가 한 글자라도 나오면 페일이다. 1만 페이지에 1단어라도 = FAIL."**

내가 처음 잡은 방향(BANNED_VOCAB 사전 30+개)은 형이 직접 정정 — 사전식은 누락이 곧 구멍, 본질은 판정질문 1개. 본 버전은 NO_WORK_LABEL 5줄 본질을 채택하고 사전·패턴은 보조 위치로 격하.

### INV 13 — NO_WORK_LABEL 5줄 (단일 권위)

| | |
|---|---|
| RULE | 산출물·대화 = 인간 언어. 작업 라벨 ZERO. (1만 페이지 1단어 = FAIL) |
| 판정 | "이 단어, 이 대화 밖 사람이 사전 없이 읽을 수 있나?" — NO → 라벨 → 금지 |
| ALLOW | 업계 전문용어 (BEP·KPI·MECE·MVP 등) · 고유명사 · 법조문 |
| CONVERT | 라벨 → 실명·평문 풀어쓰기 (Y2 → "2년차" / 4축 → 실제 4개 이름 / C:E:W → 평문) |
| SELF_CHECK | 산출 직전 자체 스캔. 1개라도 = 차단·전수재작성. 부분치환 ✗ |

### 신규 파일

- `references/no-work-label.md` (단일 권위) — 5줄 본질 + ALLOW 화이트리스트 + CONVERT 치환표 + 양평 v3 ANTI-PATTERN

### 수정 파일

- `SKILL.md` — 절대규칙 12→13개, INV 13 신설, §I 스캔 섹션 추가, §G 파이프라인 ⑩-b 추가, Gotchas 4행 추가
- `scripts/validate.py` — `--check-output FILE` 모드 신설, 사전·패턴 보조 게이트, ALLOW 화이트리스트 반영, 자기참조 면제
- `evals/cases.json` — C9·C10·C11 신규 3건 (구조라벨 위반·메타라벨 위반·ALLOW 통과)

### 양평 v3 사례 검증 결과

`scripts/validate.py --check-output sample.md` → **10개 라인 적발 FAIL**:
- DNA 4축 / 마지막 레이어 / 3트랙 진입점·관계 설계 / Pin↔Body 매핑 / 압정 / CONVERGE MODE_L / v3.1 페이퍼엔진 통과 / DEEP 4항 QC

처리: **부분치환 ✗ → 전수 재작성**. 라벨을 라벨로 바꾸지 말고 실명·평문으로(`4축` → `정원·물·문학·휴식 네 가지`, `3트랙` → `살롱·교육·메가 세 사업`, `흑자축` → `흑자 사업`, 메타블록 자체 삭제).

### 우선순위

INV 13은 다른 모든 규칙(Pin↔Body 표 의무·CEW 한 줄 등)보다 **상위**. 다른 규칙이 라벨을 요구하면 그 다른 규칙을 자연어로 풀어쓴다.

---

## v2.3.0 (2026-04-25)

**DOC_TYPE 분기 + Claim-Evidence-Warrant + 반대주장 박스 + Pin↔Body + 의사결정 매핑 + 수치맥락**

형 진단: "압정만 적층되고 본문 휘발·등급만 박혀있음·논증 부재". 양평 _research/ 16편(특히 종합·수렴) 안티패턴 직격.

### 시스템 의무 4 (다소스·압축 단절 차단)
- **INV 9 DOC_TYPE 분기:** 길이만이 아닌 종류 분기. DELIVER(1:7:2)·DIAGNOSE(1:6:3)·EVALUATE(1:5:4)·CONVERGE(1:4:5) 압정비율 차등. EVALUATE/DIAGNOSE = MODE_S 금지·CONVERGE = MODE_L 강제. (`references/doc-types.md` 신규)
- **INV 10 EVIDENCE_INJECTION (§D-5):** 평가표 등급(강·중·약·★·점수) 옆 근거 1줄 컬럼 의무. 미명시 = FAIL. 양평 §2 비교표 안티패턴 차단.
- **NUMBER_PROVENANCE (§D-6, §D-1):** 모든 수치 옆 (출처·가정·기준·비교) 의무. `3,200명` → `3,200명 (KOSIS 2024-12, 전년比 +45%, 군평균 800명)`. `+42억` → `+42억 (가정: 단가·캐파·점유율, 시나리오)`.
- **MULTI_SOURCE_PROTOCOL (§F-2):** 3편+ 통합 시 다소스 교차비교 매트릭스 의무 (편·결론·합의·모순·빈자리). 단순 인덱스화 = FAIL. 양평 종합 §G 15편 인덱스 안티패턴 차단.

### 본질 의무 5 (진짜 페이퍼 본질)
- **INV 10 Claim-Evidence-Warrant (§E-3):** 모든 주장 = C(주장)+E(증거 1+)+W(왜 E가 C 지지) 단위. Toulmin 모델 압축형. 셋 중 하나라도 ✗ = FAIL. 양평 종합 "강·중·약·즉사" 등급만 = E·W 부재 = 이 룰 위반. 불릿 압축 OK: `[C]: [E] → [W]`.
- **INV 11 Pin↔Body 매핑 (§B-3):** 압정(상단 결론) 주장 N개 ↔ Body 섹션 N개 1:1 매핑 의무. 매핑표(압정 주장·Body §X·증거 위치) 작성. 압정에만 있고 Body에 ✗ = FAIL. 양평 종합 §A "특이사항 7개" 떠있음 차단.
- **INV 12 반대주장 박스 (§E-4):** MODE_M·L에서 Body 섹션당 반대주장 박스 1+ 의무. 형식: 반대주장·반박 근거(E')·현 결론 우위 사유(W'). 단언만 = 선전문 = NYT 위반.
- **수치 맥락 (§D-1):** 수치 = 값 + 기준점 + 비교/증감 + (출처/가정). 단독 수치 금지.
- **의사결정 1줄 (§B-1):** Headline 직후 "이 문서가 바꾸는 의사결정 1줄" 의무. research-frame §1-1과 동일 사상. 미작성 = FAIL.

### 신규 파일
- `references/doc-types.md` (130줄) — 4종 정의·트리거·골격·매트릭스·평가표 템플릿

### 수정 파일
- `SKILL.md` — 절대규칙 7→12개 확장, §A ROUTER에 DOC_TYPE 추가, §B에 의사결정1줄+Pin↔Body, §D 4항→6항 QC, §E에 CEW+반대주장박스, §F에 MULTI_SOURCE
- `references/cascade-protocol.md` §3 — 참조형 폴백을 DOC_TYPE 분기로 통합
- `evals/cases.json` — C4~C8 신규 5건 (DOC_TYPE·CEW·Pin↔Body·반대주장 검증)

### 영향
- **양평 종합·수렴 같은 산출물 차단:** 등급만 적층·압정만·논증 부재·다소스 인덱스화 모두 v2.3에서 FAIL
- **출력 의무 ↑:** EVALUATE/CONVERGE 산출물 토큰 +30~40% 예상 (CEW·Pin↔Body·반대주장·교차비교)
- **DELIVER는 v2.0 호환:** 압정 1:7:2·전달형 산출은 영향 없음

### 호환
- v2.0~v2.2 DELIVER 산출은 종류 미명시 시 디폴트로 호환
- 명시적 트리거("비교·종합·통합·진단") 시 v2.3 신규 의무 발동
- biz·hit·human·ads·person·ruby·management·sales·brand·copy·nego·contract·startup·holdings·risk·benchmark·app-and-jang·data·policy·consulting 21 spoke spoke 자동 cascade 시 DOC_TYPE 자동 판정

---

## v2.0.0 (2026-04-21)

**NYT 스타일 전면 재설계 (Major)**. 산문체 금지 강제, 역피라미드·압정(pin) 구조·3패스 삭제·4항 밀도QC 5층 구조화.

### 변경
- 형 요청: "NYT처럼 산문체 무조건 탈피"
- §A MODE_ROUTER 신설 (S/M/L 길이 분기)
- §B NYT_STRUCTURE 신설 (Headline·Lead·Nut graf·Body 4층, 압정 비율 1:7:2, 자르기 30% 테스트)
- §C DELETION_FIRST_EDIT 신설 (3패스: 형용사·부사 80%, 연결어, 동의반복)
- §D DENSITY_CHECK 신설 (4항: 주제문·모호동사·중복·구체사실 밀도)
- §E FORMAT 신설 (강제: 불릿·헤더·인용·수치 / 금지: 긴 문장·수동태·모호동사·설명형)
- §F Cascade 3티어 유지 (구 §0), 시각소스 감지 훅 유지
- 기존 §2~§5 (매크로·메조·제목·파일) 구조는 §B~§E에 흡수, 산문체 유도 조항 전부 삭제
- INVARIANT 5→7항 확장 (산문체 FORBIDDEN·역피라미드·3패스·4항 QC 추가)
- "모래시계" → "압정(pin)" 재명명, 별칭 유지
- version 1.1.0 → 2.0.0

### 왜
UP v39.6와 정합. UP §6 OUTPUT_COMPRESSION은 대화 출력 ≤33% 압축. paper-engine은 문서 산출물용으로 별도 구조 필요. 한국 보고서 관성(배경→현황→분석→결론 귀납구조·긴 문장·산문체)이 AI 산출물 품질 주 병목. NYT 100년 편집 경험치(역피라미드·리드·단문·수치)를 DSL화하여 관성 무력화. Strunk & White "Omit needless words" + McKinsey Top-Down + Hemingway 단문 원칙 통합.

### 연동
- UP v39.6 §6: MODE_S(≤500자)는 UP §6 3블록(CONCLUSION·CASE·GROUND) 공유
- design-skill v1.4: HTML 시각소스 감지 훅(§F) 유지, C9 cascade 호환

**NYT 스타일 전면 재설계 (Major)**. 산문체 금지 강제, 역피라미드·압정(pin) 구조·3패스 삭제·4항 밀도QC 5층 구조화.

### 변경
- 형 요청: "NYT처럼 산문체 무조건 탈피"
- §A MODE_ROUTER 신설 (S/M/L 길이 분기)
- §B NYT_STRUCTURE 신설 (Headline·Lead·Nut graf·Body 4층, 압정 비율 1:7:2, 자르기 30% 테스트)
- §C DELETION_FIRST_EDIT 신설 (3패스: 형용사·부사 80%, 연결어, 동의반복)
- §D DENSITY_CHECK 신설 (4항: 주제문·모호동사·중복·구체사실 밀도)
- §E FORMAT 신설 (강제: 불릿·헤더·인용·수치 / 금지: 긴 문장·수동태·모호동사·설명형)
- §F Cascade 3티어 유지 (구 §0), 시각소스 감지 훅 유지
- 기존 §2~§5 (매크로·메조·제목·파일) 구조는 §B~§E에 흡수, 산문체 유도 조항 전부 삭제
- INVARIANT 5→7항 확장 (산문체 FORBIDDEN·역피라미드·3패스·4항 QC 추가)
- "모래시계" → "압정(pin)" 재명명, 별칭 유지
- version 1.1.0 → 2.0.0

### 왜
UP v39.6와 정합. UP §6 OUTPUT_COMPRESSION은 대화 출력 ≤33% 압축. paper-engine은 문서 산출물용으로 별도 구조 필요. 한국 보고서 관성(배경→현황→분석→결론 귀납구조·긴 문장·산문체)이 AI 산출물 품질 주 병목. NYT 100년 편집 경험치(역피라미드·리드·단문·수치)를 DSL화하여 관성 무력화. Strunk & White "Omit needless words" + McKinsey Top-Down + Hemingway 단문 원칙 통합.

### 연동
- UP v39.6 §6: MODE_S(≤500자)는 UP §6 3블록(CONCLUSION·CASE·GROUND) 공유
- design-skill v1.4: HTML 시각소스 감지 훅(§F) 유지, C9 cascade 호환
- 스킬 충돌: UP §5 "§6 > skill_defaults" 규칙상 대화 출력은 UP §6 우선, 문서 산출은 shaper-skill §A~§E 우선

---

## v1.1.0 (2026-04-20)

**시각소스 감지 훅 신설**. HTML/웹MD 산출물의 "타이포만 예쁜" 문제 구조적 해결.

### 변경
- description: 시각소스 감지 훅 명시, P4에 HTML 시각요소 요청 조건 추가
- §0 Cascade 3티어: ⓔ 디자인 위임 단계에 "HTML시 시각소스 목록 동반" 추가
- §0 시각소스 감지 훅 섹션 신설 (V1~V10 태깅 → design-skill C9 브릿지)
- references/cascade-protocol.md: §12 "시각소스 감지 훅" 신설 (감지 프로토콜·전달 포맷·과잉방지)
- Gotchas 2항 추가: HTML 표·문장만, 시각소스 감지 누락
- version 1.0.0 → 1.1.0

### 왜
설계자 경험: HTML 산출물이 타이포·여백은 Apple급인데 시각요소가 0개. 수치비교·시간축·프로세스·핵심수치 등 "시각소스"는 있는데 전부 표·문장으로만 처리됨. 원인은 paper-engine이 시각소스를 감지·전달하지 않고, design-skill이 HTML 생성 시 시각 전환을 규범으로 요구하지 않았기 때문. 양쪽 동시 보강.

### 연동
- design-skill v1.4 (C9 시각 전환 CORE 신설, visualization-html.md 스포크)
- 두 스킬은 한 쌍으로 작동: paper-engine이 감지·태깅, design-skill이 전환·렌더

---

## v1.0.0 (2026-04-17)

**개명 + 리팩터**. deliverable-engine → shaper-skill.

### 변경
- skill-doctor 67.7 → 100점 대응 완료 (🔴 0, 🟠 0)
- 허브 슬림화: 13.7KB → <5KB (references/ 분할 확대)
- P1 일반 키워드 제거: "정리·분석·작성" → P2 동사로 이관 (문서화 의도 아닌 요청 오발동 차단)
- STEALTH 섹션 신설 (내부 라벨 노출 금지)
- Self-Check 섹션 신설 (validate.py + evals/cases.json 3건+)
- 절대 규칙 섹션 신설 (게이트키퍼·PREFLIGHT·재검증 명시)
- version 1.0.0 명시
- evals/cases.json 추가 (회귀 검증 3 케이스)
- scripts/validate.py 추가 (frontmatter·섹션·VOCAB 자동 검사)
- references/cascade-protocol.md 확장 (§1~§11)
- Gotchas 확장: 엣지케이스·장기대화·이름 변경 이력 혼선

### 구간
- v0.x — deliverable-engine 시절 (changelog 미기록 구간)

---

## v4.0.0 (2026-05-03) — 메이저 통폐합

**기조:** skill-doctor v3.4 진단 R1·R2·R3 근본 해소. **추가 0 · 통폐합만**.

### 통폐합 매핑
- INV 25 → 18 (-28%):
  - INV 13 (작업라벨) + INV 24 §1 (UP 작업프레임) → INV 13 통합
  - INV 16 (BAN_LEXICON) + INV 24 §2 (UP AI어휘) + INV 25 어휘 → INV 16 통합
  - INV 22 (입니다체) + INV 23 (관계격식) → INV 22 통합
  - INV 24 = §3·§4 잔존 (UP 정본 핵심)
  - INV 25 = KIWI 문법만 잔존
- references 15 → 11 (-27%):
  - 신설 3: lexicon-ban.md, formality-gate.md, kiwi-grammar.md
  - _archive 5: banwords-lexicon.md, up-ban-dictionary.md, kiwi-writing-rules.md, imnida-gate.md, relation-formality.md
- humanize_check.py 카테고리 16 → 8 (-50%):
  - META+UP_LEX → AI_LEX
  - FORMAL+KIWI_ADV → ADV_BAN
  - LABEL+UP_FRAME → LABEL_BAN
  - TRANS+KIWI_HANJA → TRANS_BAN
  - FNOUN+KIWI_GEOT → FNOUN_BAN
  - IDA / KIWI_HEDGE→HEDGE_BAN 유지
  - CONJ+UP_RAT+KIWI_EMOTION → MISC_BAN
- §B-PRE 11종 → 8종 (-27%)
- 본질 6종 → 5종 (B5+B6 어휘 통합)

### v4.0 헤리티지 박스 (SKILL.md에서 본 CHANGELOG로 이관)
- v3.4.0 (2026-05-03): KIWI 글쓰기 5법칙 통합 (INV 25). 본질 5→6종·§B-PRE 8→11종·humanize_check KIWI 5카테고리.
- v3.3.1 (2026-05-03): skill-doctor 처방 — 본질 5종 박스·banwords §7→§13 통폐합·cases INV 22·23·24 +3.
- v3.3 (2026-05-03): 입니다체 100% + 관계격식 4LV + UP BAN 4섹션. INV 22·23·24 신규. §B-PRE 5→8종.
- v3.2 (2026-05-01): PT_FORMAT_GUARD + 도구함 9종 자연주입.
- v3.1: PRE_WRITE_GUARD 사전생성형.
- v3.0: HUMANIZE_GATE 3중·BAN_LEXICON.
- v2.6: HERO 형식 + 어조 룰.
- v2.5: 작업라벨 본질보호.
- v2.3: DOC_TYPE 4분기·CEW·반대주장.

### 진단 점수 목표
- v3.4: 74/100
- v4.0 목표: 90+/100

## v4.1.0 — 2026-05-05 — 서사층 신설 (§B-NARR + INV 27)

### 변이 동기
형 피드백 — "단어와 문장 수준에서는 잘 준비되어 있는데, 맥락적·흐름적·서사적인 부분이 약해. 중복 회피·스파인-백본 정합·홈즈 통찰·아날로지 귀납이 잘 잡혀야해." → v4.0이 단어층(어휘·격식·문법)만 통폐합·서사층 ZERO. cleanup의 콘텐츠불변 원칙으로 사후 재구성 ✗ → shaper에 사전강제 필수.

### 추가 (3건)

1. **INV 27 신설** — §B-NARR 단일우산 4종 (스파인응결·에디터페어·반박자동석·CEWA진화)
2. **§A-5 SPINE 응결** — 라우터에 신설. Claude 제안→형 컴펌 1회. MODE_M·L 강제·MODE_S 면제
3. **§B-NARR 섹션** — §B-PRE(미시) 직후·§B-구조 직전 강제. 거시 4문 자기검열

### 룰 진화 (2건)

1. **INV 10 CEW → CEWA** — Analogy 슬롯 의무 추가. 주장당 유사 성공사례 1+
2. **INV 11 Pin↔Body 강화** — 매핑표에 "스파인 변주" 컬럼. 헤드라인-only 통독으로 스파인 직관 가능 강제

### 신규 references (2종)

- `narr-gate.md` — 서사층 1정본 (4종 룰·거시 4문·SCOPE·충돌해소·cleanup 직교)
- `rhetoric-deck.md` — 6수사 카드덱 (Holmes·Pathos·Analogy·Numbers·Story·Image)

### 확장

- `_common/persona-corpus.md §2-EXT` — 편집자 페르소나 듀얼 캐스팅 (이오덕 디폴트·작성자=편집자 충돌 시 자동 전환)
- `§G 파이프라인` — ④ §B-NARR 단계 추가·12 단계로 확장
- `§H 자체스캔` — 9중으로 확장 (NARR_SCAN 1문 LLM 판정 추가)

### 1차 출처

`VAULT/_skills research/shaper-skill/2026-05-05_R-NARR-LIGHT.md` — 4축 LIGHT 리서치 (스파인-백본·홈즈수사·반복회피·에디터페어). Minto 1985·강원국 2014·유시민 2015·Cialdini 1984·Aristotle BC 350·Heath 2007·Kahneman 2011·Pound/Eliot 1922·Pixar Catmull 2014·Klein 2007.

### cleanup 직교성

shaper §B-NARR = 사전강제·재작성. cleanup 축15(v1.2 신설) = 사후검출·경고만·콘텐츠 불변. cleanup 적발 시 shaper로 *되돌려* §B-NARR 재진입.

### 효과

- 단어층(§B-PRE 8) + 서사층(§B-NARR 4) 이중 사전게이트
- 토큰 1.3~1.5배 증가 (편집자 4문·반박자 자문) — 자문은 *내적*만·본문 출력 ✗로 출력 부담 ZERO
- 산출물 거시 결함 4종(스파인부재·헤드라인비백본·중복·논리편중) 사전 박멸

## v4.1.1 — 2026-05-05 — NARR_SCAN 결정주의화 (skill-doctor P1·P4·P5)

### 변이 동기
skill-doctor v2.1 진단 결과 — ②-4 부정확·확장 FAIL (NARR_SCAN LLM 1문 비결정주의·INV 25 위배), ⑤-3 비대·유지 FAIL (SKILL.md 10198B), ⑦-3 진화불능·유지 WARN (9중 스캔 매핑 모호).

### 변경 (3건)

1. **P1 NARR_SCAN 결정주의화** — `humanize_check.py` 9번째 카테고리 신설. 헤드라인(H1·H2·H3) 추출 + 구조어휘 BAN(현황·분석·시사점·결론·요약·개요·배경·검토·고찰·정리·마무리·도입·본론·맺음말·총괄) grep. LLM 1문 제거·재현성 확보. INV 25 결정성 우선 정합.

2. **P4 SKILL.md 압축** — 10198B → 9217B (-9.6%). §H 매핑 명시(8 카테고리+NARR_SCAN=9)·예시 단일화·상세 INV 표 통합. 본질 5종+거시 4문 *불변*.

3. **P5 9중 스캔 매핑 명시** — §H에 9 카테고리 명시 (8 grep + NARR_SCAN grep). v4.1 "9중" 명목·v4.1.1 결정주의 9 카테고리 정합.

### 효과

- skill-doctor 점수 78→90+ 목표
- humanize_check 9 카테고리 결정주의 일관성
- 같은 산출물 재현성 100%
