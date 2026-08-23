# Audit — ppt-slides-writer (v1)

감사자: wizard-evaluator-p2 (2026-08-19). 대상: SKILL.md + workflows/01~07 + references/ 9 + templates/ 3 + scripts/ 4.
근거: article-coverage-checklist.md(전 행), skill-spec.md(동결본), 원문 기사 WebFetch 재확인, **독립 픽스처 스크립트 재실행**(Generator 픽스처 미사용).

## Verdict: FAIL

기사 커버리지 35행 전부 실물 위치 확인(무단 누락 0), 스크립트 4종 독립 재실행 양방향 통과.
그러나 **변환 계약(스킬의 존재 이유인 HTML→PPTX 충실도 경로)에서 기계 검증이 못 잡는 무음 결함 2건(HIGH)** 을 실측으로 확인했다. 둘 다 스킬 자신의 "기계 우선 검증" 원칙(SKILL.md 원칙 4)과 변환기 오류 정책(conversion-rules §4 "부분 변환물 금지")에 위배되는 경로다. 수정 범위는 좁다(아래 Recommended Next Focus).

---

## Article Coverage Table

| 행 | 요소 | 요구 산출물 | 발견 위치 | 판정 |
|---|---|---|---|---|
| V1-1 | GAN식 역할 분리, 별도 Agent 호출 | 오케스트레이터가 P/G/E를 각각 파견 | SKILL.md:33-35(원칙 3 "각각 별도 Agent 호출…파일로만 통신"), 플로우 3(:85)·5(:88)·6(:92) — "Agent 호출 #1/#2/#3" 명시 | PASS |
| V1-2 | 4~6기준, 1~5점 | rubric 기준 표 | references/rubric.md:460-468(재현 기준 5개 C1~C5), 점수 가이드 1~5(:473-481), evaluator-prompt.md:286("기준 5개를 1~5점으로 채점") | PASS |
| V1-3 | weak축 2× 가중+근거 | 가중치·근거 열 | rubric.md 표 — C1·C2 **2×** + "weak-by-default 근거" 열(균질 불릿 수렴/AI slop 드리프트), C3~C5 1×. evaluator-prompt.md:296-297 "C1·C2가 2×인 이유" 재서술 | PASS |
| V1-4 | 품질 서술만, 브랜드 참조 금지 | rubric 작성 규칙 | rubric.md:456-458 — "McKinsey급/Apple풍…스타일 자석…금지" + planner-prompt.md:30-31(무드 품질 언어) 기준·앵커 본문에 브랜드명 0건(grep 확인) | PASS |
| V1-5 | few-shot 1/3/5 앵커 | 캘리브레이션 파일 | references/evaluator-calibration.md — `grep -c '^\- \*\*[135]/5\*\*'` = **15** (C1~C5 × 1/3/5), 스펙 §5.4 문안과 대조 일치(아래 Spec Fidelity) | PASS |
| V1-6 | 반복 상한 5~15 "범위" | 단일 값 금지+하한 경고 | SKILL.md:94("5~15회 범위(하한 고정 금지)"), :122-124, workflows/03:25, 04:27-29. 단일 고정값 표기 0건(grep) | PASS |
| V1-7 | wall-clock ~4h 허용 | 서두름 금지 | SKILL.md:125-126 "wall-clock 최대 ~4시간까지 허용…인위적 서두름 금지" — 기사 "stretched up to four hours" 대응(WebFetch 확인) | PASS |
| V1-8 | Evaluator 튜닝 few-shot 템플릿 | §Tuning | evaluator-prompt.md:150-165 — "도메인 few-shot 추가 템플릿" 서식(관찰/X점 앵커/교훈) + 전형적 괴리 4패턴. calibration 말미 "운영 중 추가된 앵커" 수용부(:440-450) | PASS |
| V1-9 | REFINE/PIVOT/ESCALATE | Strategic Decision 블록 | generator-prompt.md:57-79 — 3분기 + `REDIRECT:`/design_memo.md 없는 PIVOT 금지(:77-79) + "동결 design-system 변경은 사용자 게이트 재실행 사안, Generator 단독 변경 절대 금지"(:71-73, 스펙 §5.2 게이트 룰 반영) | PASS |
| V1-10 | Dutch Art Museum 10회차 도약 | iteration wisdom | SKILL.md:123-124 "Dutch Art Museum 사례에서 품질 도약은 10회차에 발생…이른 종료는 도약 직전에 멈추는 것" — 기사 원문(iteration 10) 일치 | PASS |
| V1-11 | 중간 반복 > 최종 가능 | Iteration Quality Note | evaluator-prompt.md:120(출력 섹션) + :335-338("중간 반복본이 최종본보다 나을 수 있다…최선본 선택 근거"), SKILL.md:127-129 | PASS |
| V1-12 | Planner 야심적 스코프 | be ambitious | planner-prompt.md:27-29 "Be ambitious…청중 분석·예상 반론 대응·증거 전략까지…설득 완결성이 기준" | PASS |
| V1-13 | product-level hard rule | 구현 상세 금지 | planner-prompt.md:22-27 — "발표 제품 수준에 머문다…HTML/CSS 구현·좌표·픽셀·원고 문장 금지…사양에 원고를 쓰기 시작하면 역할 침범" | PASS |
| V1-14 | 도메인 차별화 훅 | 훅 섹션 필수 | planner-prompt.md:31("최소 2개 필수") + 섹션 7(:72-79, 후보 5종) + workflows/01:69(오케스트레이터가 훅 실재 확인) | PASS |
| V1-15 | 핸드오프 전 자체 검증 | READY_FOR_QA 전 체크 | generator-prompt.md:59-60(규칙 5 "모든 체크 스스로 통과 확인 전 절대 완료 선언 금지") + 프로세스 d(lint ERROR 0)·e(21~26 1차 실행 후 핸드오프) | PASS |
| V1-16 | 적대적 프로브+증거 | 프로브·인용 의무 | evaluator-prompt.md:247-276(프로브 9종, 스펙 §5.3과 1:1) + :278-284 "증거 캡처 의무"(장표번호+data-role/리포트 인용/pptx diff, 추측 서술 금지) | PASS |
| V1-17 | 기준별 하드 임계 | verdict logic | rubric.md:485-494 — "2×<4 FAIL / 1×<3 FAIL / DoD 미검증 FAIL / 21~26 실패 FAIL(하드 게이트) / 민감정보 미해소 PASS 불가" — 스펙 §3 문안 그대로. evaluator-prompt.md:299-305 동일 삽입 | PASS |
| V1-18 | 스프린트 계약 협상 | 양쪽 프롬프트 Mode | generator-prompt.md:23-28(규칙 2: 계약 기록 (a)~(c)+Evaluator 승인 대기), evaluator-prompt.md:28-29(약한 계약 반려), workflows/03 §1·04 스프린트 구성 | PASS |
| V1-19 | 파일 기반 통신만 | File Handoff Contract | SKILL.md:66-69 — 11파일 목록(spec/design-system/storyline/sprint_contract/generator_report/critique/design_memo/handoff/lint_report/verify_report/status) = 스펙 §4 목록과 동일. 원칙 3 "역할 간 대화·추론 공유 금지" | PASS |
| V1-20 | 런 간 Evaluator 튜닝 루프 | 운영 섹션 | SKILL.md:174-186 "Evaluator tuning workflow" (a)~(d) 번호 절차(읽기→괴리 특정→앵커·프로브 보강→재실행 수렴) | PASS |
| V1-21 | 컨텍스트 불안→handoff | 불안 신호+리셋 | generator-prompt.md:90-96 — 슬라이드 도메인 신호 4종(재요약/후반 분량 급감/"유사하게 구성" 직전/검증 건너뛰기) → `HANDOFF_NEEDED:`. workflows/04 "컨텍스트 리셋" 절 | PASS |
| V1-22 | 리셋 ≠ 컴팩션 | 명시 경고 | SKILL.md:38("**컴팩션 금지 — 컴팩션은 불안 상태를 그대로 보존한다**"), generator-prompt.md:97, workflows/04:73 — 3곳 일관 | PASS |
| V2-1 | 스프린트 제거(Simplified 시) | tier=Full이면 N/A+기록 | **N/A — tier=Full(스펙 §8 확정)**. 근거 기록 확인: SKILL.md:204-208 "Simplified로 전환한다면: 스프린트 분해와 sprint_contract.md 협상이 제거 1순위(단일 연속 Generator 세션)" | N/A(정당) |
| V2-2 | 단일 종료 Evaluator 패스 | 동상 | **N/A — tier=Full**. SKILL.md:205-206 "스프린트별 Evaluator는 단일 종료 패스(3~5라운드 캡)로 바뀜" 기록 + 유지 항목(사람 게이트·기계 검증·단일 원천)의 과업 귀속 논거 | N/A(정당) |
| V2-3 | Evaluator 비용은 가변 | 과업-모델 경계 | SKILL.md:209-212 "Evaluator 비용은 고정 yes/no가 아니다…과업-모델 경계…가장 먼저 얇아질 구성요소" | PASS |
| V2-4 | 모델별 가이드 표 | 표 복사 | SKILL.md:198-202 — Sonnet 4.5(Strong/Full)·Opus 4.5(Largely eliminated/Simplified)·Opus 4.6(Eliminated/Simplified or Single-session) 3행 표 | PASS |
| G-1 | 구성요소=가정 | 하나씩 제거 지침 | SKILL.md:39-41(원칙 6) + :195-196("가정을 인코딩…모델이 좋아지면 낡는다") | PASS |
| G-2 | 급진적 단순화 실패 | V1vsV2 기록 | SKILL.md:213-215 "급진적 단순화는 실패했다…한 번에 하나씩 제거하고 영향을 측정" | PASS |
| G-3 | 단순성 원칙 인용 | 원문 인용 | SKILL.md:41-42 및 :216-217 — *"find the simplest solution possible, and only increase complexity when needed"* 2회, 출처 표기. WebFetch로 원문 문자열 일치 확인 | PASS |
| G-4 | 트레이스 읽고 실험 | 번호 운영 루프 | SKILL.md:178-186 (a)~(d) — V1-20과 동일 실체, "수렴까지 반복" 명시 | PASS |
| G-5 | 하네스 공간은 이동 | 마무리 지침 | SKILL.md:218-221 "하네스의 공간은 사라지지 않고 **이동한다**…지울 때는 그 공간이 어디로 이동했는지 기록" | PASS |
| P-1 | 감각 한계 사람 체크포인트 | 게이트+이관 규칙 | SKILL.md 게이트 ①(:86)②(:90)③(:95)④(:104) + "시각 채널 한계 대응" 절(:110-117) + evaluator-prompt.md:68-70·118(시각 잔차 채점 보류→"사람 게이트 확인 항목" 이관) | PASS |
| P-2 | ambition+차별화 훅 | 둘 다 | planner-prompt.md:27-29 + :72-79 (V1-12·V1-14 참조) | PASS |
| P-3 | (a)~(d) 운영 절차 | 한 문장 아님 | SKILL.md:178-186 — 4단계 번호 절차 + 룰 승격 절차(:188-190, design-rules.md §8 연동) | PASS |

**커버리지 판정: 35/35 (적용 33 PASS, N/A 2 정당 — 공란 0).**

---

## Adversarial Probes (프로브별 결과+증거)

| 프로브 | 결과 | 증거 |
|---|---|---|
| Placeholder sweep | **clean** | `grep -rn '\[DOMAIN\]\|\[OUTPUT_TYPE\]\|TBD\|TODO\|PLACEHOLDER' SKILL.md workflows references templates scripts` → no matches (exit 1). templates/의 `{…}` 슬롯은 사용자 런타임 서식, `{WORK_DIR}/{SKILL_DIR}`는 SKILL.md:75-77 및 각 프롬프트 파일 상단에 치환 규약 정의됨 — 배포 프롬프트 placeholder 아님 |
| Tier 일관성 (Full) | **PASS** | sprint_contract 협상: generator-prompt:23-28 + evaluator-prompt:28-29 + workflows/03 §1·04. per-sprint Evaluator: workflows/03 §2(스토리라인), 04 Maker-Reviewer 루프, SKILL.md 플로우 5·6. 반복 상한 4곳 모두 "5~15회 범위"(단일 고정값 0건) |
| 캘리브레이션 구체성 | **PASS** | 앵커 15개, 전부 슬라이드 도메인 실물 서술("연 3.2억 손실 수치가 해법 장표 절감 근거와 CTA ROI에 재등장", "radius가 장표마다 다르고", "많은 관심 부탁드립니다") — 추상 "좋다/나쁘다" 0건. 스펙 §5.4 대비 diff: 문안 동일(개행·조사 수준만 상이) |
| Strategic Decision | **PASS** | REFINE/PIVOT/ESCALATE 3분기(generator-prompt:57-79), PIVOT 증거 규칙(`REDIRECT:` 또는 승인 design_memo, :77-79), **디자인 시스템 변경=사용자 게이트 재실행**(:71-73) — 스펙 §5.2 3요소 전부. evaluator 측 대응 규칙도 존재(evaluator-prompt:344-345 "REDIRECT가 아니라 게이트 ① 재실행 필요를 Blocking Issue로") |
| 모델 표 | **PASS** | SKILL.md:198-202, Sonnet 4.5/Opus 4.5/Opus 4.6 + context anxiety/tier/notes 3열 |
| Building Effective Agents 인용 | **PASS** | SKILL.md:41-42·216-217, 원문과 문자열 일치(WebFetch 대조) |
| 감각 한계 사람 게이트 | **PASS** | 게이트 ①스타일(:86) ②스토리라인(:90) ③HTML 렌더(:95) ④최종 PPTX/PDF(:104) 전부 STOP 규칙 포함. evaluator-prompt:68-70 시각 잔차→사람 게이트 이관 규칙 + 출력 섹션(:118) 실재 |
| Planner ambition+훅 | **PASS** | 위 P-2 행 |
| 튜닝 운영화 | **PASS** | (a)~(d) 번호 절차(:178-186) + 룰 승격(2회 반복→규칙 승격→lint/프롬프트 차단, :188-190 + design-rules.md §8) |
| 자기완결성(역할 프롬프트) | **PASS** | 3개 프롬프트 모두 skill-spec.md·위자드 파일 참조 0건. 참조 파일은 전부 배포 payload({SKILL_DIR}/references/*, templates/*) 또는 실행 시 생성물({WORK_DIR}/*). evaluator의 SSOT 경로 `{SKILL_DIR}/resources/ai-slop-checklist.md` 실재 확인 + 부재 시 내장 6항목 축소 동작 명시(:254) |
| 파일 계약 명칭 일관성 | **PASS** | 11파일명 SKILL.md/workflows/프롬프트 3종 간 grep 대조 일치. lint·verify·변환 명령 시그니처도 SKILL.md·workflows/04·05·06·generator-prompt 간 동일(3 위치 인자 + --report) |
| 안전 게이트 3종 | **PASS** | 민감정보 STOP: SKILL.md:146-149 + workflows/01 §3 + 07 게이트④ #3 + lint 체크 18(안전 플래그 별도 기록 — 재실행으로 확인) + evaluator 프로브 3. 인젝션 방어: SKILL.md:150-152 + workflows/02 §A3 + evaluator 프로브 8. 외부 공유물 사람 검토: SKILL.md:153-155 + workflows/07 §2·3 |
| 기존 산출물 무접촉 | **PASS** | mtime: upgrade-notes.md 08-18 01:28, resources/ai-slop-checklist.md 06-21, skills/*/SKILL.md 08-17 — 전부 생성일(08-19) 이전. 생태계 참조 5행(doc-converter/image-gen/diagram-builder/slide-reviewer/ai-slop SSOT) 전부 실경로 존재 + 폴백 명시 |
| Frontmatter | **PASS** | yaml.safe_load 파싱 성공. name/version/context:fork/allowed-tools 정상, 트리거 **14개**(EN 6+KO 8) 계수 확인. SKILL.md **253줄** ≤500(wc) |
| px→EMU 일관성 | **PASS** | conversion-rules.md §2 "1px = 9525 EMU…EMU = round(px × 9525)" == html2pptx.py `EMU_PER_PX = 9525`, `emu()` round 구현, 슬라이드 12192000×6858000 동일. pt=px×0.75 0.5 반올림도 양쪽 일치(`pt_from_px`) |
| lint 20항 스펙 충실도 | **PASS**(1건 LOW 제외) | 스펙 §7.3 레벨 대조: 1·2·4·5·6·7·8·12·14·17·19 ERROR / 3 ERROR+enum외 WARN / 9·10·11·13·15·16·20 WARN / 18 WARN+안전 플래그 — 코드와 전부 일치. 예외: 체크 19 불릿 하한(3개 미만) 미검출 — Non-Blocking #2 |

---

## Script Re-run Evidence (독립 픽스처 — Generator 픽스처 미사용)

픽스처: `<scratchpad>/p2-audit-fixture/` — 자체 제작 3장 덱(cover/evidence/cta; 표·이미지·도형·노트·source 포함), design-system.md(자체 팔레트 #0E634F 계열 — Generator 픽스처와 다른 값), storyline.md(5분, spine 표), assets/trend.png(순수 파이썬 생성 800×450 = 배치 400×225의 정확히 2x). 의존성: python-pptx 1.0.2 / bs4 4.15.0 / pypdf 6.16.1 확인.

**1) lint_slides.py — clean 방향**
```
$ python3 scripts/lint_slides.py deck.html design-system.md storyline.md
lint: ERROR 0 / WARN 0 → lint_report.md   EXIT=0
- 렌더 검사: 실행됨 (/Applications/Google Chrome.app/.../Google Chrome)
| 4 | INFO | 렌더 오버플로 검사 통과 (Chrome 측정). |
```

**2) lint_slides.py — violation-catch 방향** (그라데이션 + data-role 제거 + 이모지 + 캔버스 이탈 4종 주입):
```
lint: ERROR 7 / WARN 2   EXIT=1
| 3 | ERROR | S2: data-role 누락. |
| 4 | ERROR | S3 `el-text`: 캔버스(1280x720) 이탈 — left+width=1400, top+height=750. |
| 4 | ERROR | 렌더 오버플로 — S3 `section.slide`: scroll 1400x750 > client 1280x720 |
| 6 | ERROR | 팔레트 외 색 사용: #6366f1 ... / #8b5cf6 ... |
| 8 | ERROR | 금지 CSS — 그라데이션 (금지 1항): `linear-gradient` |
| 9 | WARN  | 인디고/바이올렛 대역 단색 #6366f1 / #8b5cf6 — AI slop 시그니처 |
| 12 | ERROR | S3: 이모지 디자인 요소 검출: 🚀 |
```
주입 4종 전부 검출(그라데이션은 6·8·9 삼중 검출, 이탈은 정적+렌더 이중 검출).

**3) html2pptx.py — clean + 재오픈 덤프**
```
$ python3 scripts/html2pptx.py deck.html dist/deck.pptx
PPTX 저장 완료 (native, 3장)   EXIT=0
slide size EMU: 12192000 x 6858000
S1: [AUTO_SHAPE, TEXT_BOX(수동 발주가…), TEXT_BOX(재고 자동…), TEXT_BOX(구매기획팀 · 2026년 8월)] / notes: 안녕하십니까…
S2: [TEXT_BOX(결품률 4.1%는…), TEXT_BOX(월평균 결품 217건…), TABLE, PICTURE, TEXT_BOX(출처: 사내…)] / notes: 결품률 4.1%는…
S3: [AUTO_SHAPE, TEXT_BOX×5] / notes: 파일럿은 창고…
```
텍스트가 개별 TEXT_BOX(편집 가능), 표=TABLE, 이미지=PICTURE, 노트 전 장표 이관 — 네이티브 계약 충족.

**4) html2pptx.py — 오류 정책 방향** (파싱 집합 외 직계 div + colspan 주입):
```
변환 오류 — PPTX를 저장하지 않는다:
  - S1: 파싱 집합 외 직계 요소 <div class=['floating-quote']> — …만 허용.
  - S2 .el-table: colspan/rowspan 미지원 — 셀 분해 필요.
CONV_BAD_EXIT=2   (partial pptx 미저장 확인)
```

**5) html2pdf.sh** (Chrome 존재 — SKIP 아님):
```
PDF 저장 완료: dist/deck.pdf   EXIT=0  (236,884 bytes)
```

**6) verify_conversion.py — clean 방향**
```
verify: FAIL 0 / WARN 0   EXIT=0
| 21~26 | 전부 PASS | (재오픈 3==3 / 텍스트 손실 0 / 노트 일치 / 이미지 1건 하한 충족 / PDF 3페이지+전 페이지 텍스트 레이어 / round-trip 성공) |
```

**7) verify_conversion.py — 불일치 검출 방향** (변조 HTML vs 원본 PPTX):
```
verify: FAIL 1   EXIT=1
| 22 | FAIL | 텍스트 손실 1건: S3: "🚀 파일럿 목표: 결품률" |
```

**8) --image-slides**: 생성 성공, 장당 PICTURE 1개 + 노트 3장 전부 이관 확인.

**9) 엣지 프로브(중첩 리스트)** — Blocking #1의 실측 근거:
```
li 안에 <ul><li>야간 발주는…</li></ul> 주입 → 변환 EXIT=0 (오류 아님), PPTX 문단 덤프:
'발주 판단이 담당자 경험에 의존하고 있습니다.야간 발주는 익일 반영됩니다.'   ← 부모 li 문단에 흡수
'야간 발주는 익일 반영됩니다.'                                                ← 동일 텍스트 별도 문단 재출력
```

Generator 자기보고(generator_report.md) 대조: 253줄·앵커 15·placeholder 0·mtime 무접촉·스크립트 통과 주장 — **전부 독립 재검증으로 사실 확인**(표면 신뢰 아님).

---

## Spec Fidelity Notes

- §2.1 frontmatter: 스펙 확정 텍스트와 동일(트리거 14, context: fork, allowed-tools 8종). §2.2 트리 24파일 전부 실재.
- §3 루브릭·verdict·2차 점검 3렌즈, §5.4 앵커 15개: 스펙 문안 그대로 이식 확인.
- §5.1~5.3 역할 프롬프트: hard rule/ambitious/훅, 프로세스 a~e, 불안 신호 4종, 프로브 9종, 증거 의무, 시각 잔차 이관 — 스펙 항목별 대조 일치.
- §6 오케스트레이터 11단계: 순서·게이트 위치·STOP 조건 일치. §7.2 px→EMU, §7.5 명령·크롬 탐색 순서 일치. §9.1 검증 21~26 구현·실행 절차(Generator 1차→Evaluator 재실행) 일치. §9.2 3단 검증 일치. §10 시나리오 4종의 요구 동작이 workflows/01(vague·범위 밖)·01§3+07(민감정보)에 반영.
- 스펙 대비 일탈 확인 3건(전부 아래 Blocking/Non-Blocking에 계상): 표 기본 폰트 14px(스펙에 없는 Generator 추가 — 자체 최소 폰트 규칙과 모순, Blocking #3), 체크 19 불릿 하한 미검출(스펙 표기 "3~5 초과"의 좁은 해석 — Non-Blocking #2), S1 스프린트에 lint 명령 무조건 적용 문구(스펙 §5.2 문안을 그대로 이식한 것으로 스펙 유래 — Non-Blocking #3).

---

## Blocking Issues

1. **[HIGH] html2pptx.py 중첩 리스트 무음 텍스트 중복** — Where: `scripts/html2pptx.py` `add_text_element`/`add_runs` (blocks 수집이 중첩 li를 이중 방문). Actual: li 내부에 ul/ol이 있으면 부모 li 문단에 자식 텍스트가 흡수되고 같은 텍스트가 별도 문단으로 한 번 더 출력된다(위 실측 로그 9). verify 22는 ⊆ 판정이라 중복을 못 잡고, html-spec §6은 ul·li를 허용하면서 중첩을 금지하지 않아 Generator가 다단 불릿을 쓰면 납품 PPTX가 조용히 오염된다. Expected: 변환기 오류 정책(§4 — colspan은 exit 2로 거부)과 동일하게 "충실 변환 불가 구조는 거부"이거나 올바른 다단 불릿 변환. Fix direction: (택1) add_text_element에서 중첩 ul/ol 검출 시 오류 목록+exit 2 & html-spec §6에 "리스트 중첩 금지(1단만)" 명문화, 또는 최상위 블록만 순회하고 중첩 li는 들여쓰기 문단으로 변환.
2. **[HIGH] font-family 캐스케이드 유실 — 배포 boilerplate 기본 경로에서 발생** — Where: `scripts/html2pptx.py` `block_ctx`(인라인만 해석) × `templates/slide-boilerplate.html`(body에만 `font-family: var(--font-body)`, 본문 .el-text에 인라인 font-family 없음) × `references/html-spec.md` §6(.el-text 규칙이 "폰트 크기·색·정렬"만 인라인 요구 — 패밀리 누락). Actual: 독립 픽스처에서 본문·출처 TEXT_BOX의 run.font.name이 None → PPTX 테마 기본 폰트로 렌더. 템플릿 기본 사용 시 전 본문이 design-system 폰트 토큰을 잃으며, 브랜드 템플릿형(경로 A)에서 사용자 브랜드 폰트가 최종 납품물에서 무음 소실된다(C2 2× 축 직격). 기계 검증(21~26)·lint 어느 쪽도 검출하지 않고 conversion-rules §7 잔차 목록에도 없어 사람 게이트 ④ 확인 항목으로도 유도되지 않는다. Expected: HTML 렌더와 PPTX의 폰트 패밀리 일치 또는 최소한 잔차로 명시·유도. Fix direction: (권장) html2pptx가 `body`/`.el-text` CSS 규칙의 font-family를 기본값으로 파싱해 폴백 체인(블록 인라인 → .el-* 인라인 → body 규칙) 적용 + boilerplate 전 .el-text에 인라인 font-family 명시; 차선책은 html-spec §6에 "모든 .el-text에 font-family 인라인 필수"를 ERROR 규칙으로 추가하고 lint 체크를 보강.
3. **[MEDIUM] 표 기본 폰트 14px ↔ 최소 폰트 18px 자기모순** — Where: `references/conversion-rules.md` §3(".el-table … 미지정 시 기본 14px") vs `references/html-spec.md` §7·lint 체크 14(본문 <18px = ERROR, 예외는 .source/.caption뿐). Actual: 문서가 안내하는 기본값(14px)을 인라인으로 명시하면 lint ERROR가 나고, 명시를 생략하면 같은 14px가 lint에 보이지 않은 채 PPTX로 들어간다 — 규칙 우회 경로이자 Generator를 lint 반려 루프에 빠뜨릴 수 있는 상충 지침. 스펙 §7.4에는 14px 기본값이 없다(Generator 추가). Expected: 단일 규칙. Fix direction: 표 셀 최소 크기를 확정(예: 표 셀은 14px 허용으로 lint 체크 14에 .el-table 예외 추가, 또는 변환기 기본값을 18px로 상향)하고 conversion-rules·html-spec 동기화.

## Non-Blocking Notes

1. `.el-image`의 `object-fit: contain`(boilerplate)과 PPTX add_picture(강제 스트레치)의 종횡비 불일치 잔차가 conversion-rules §7 잔차 목록에 없음 — 목록에 1줄 추가 권장(비율 불일치 이미지는 브라우저=레터박스, PPTX=왜곡).
2. lint 체크 19가 불릿 상한(>5)만 검출하고 하한(<3)은 미검출 — html-spec §7 "불릿 3~5개" 문구와 어긋남. 스펙 표기("3~5 초과")의 좁은 해석이므로 문서 문구를 "3~5개, 초과 시 ERROR"로 정리하거나 하한 WARN 추가.
3. generator-prompt 프로세스 d "매 스프린트 종료 전 lint 실행"이 S1(스토리라인 스프린트 — deck.html 부재)에도 문면상 적용됨. 스펙 §5.2 문안 유래라 충실도 문제는 아니나 "S2 이후 스프린트"로 한정하는 1어절 수정 권장(workflows/03의 S1 계약에는 lint가 없어 실운영 모순은 낮음).
4. 격식체(체크 20)·계좌번호(체크 18) 휴리스틱의 오탐 가능성(예: "제어요소"의 '어요' 매칭)은 WARN+과탐 설계로 수용 가능 — generator_report Known limitations에 이미 정직하게 기재됨.
5. templates/design-system.md §5의 "(lint는 Evaluator 프로브 6이 검출)" 문구가 어색함(템플릿 리듬은 lint가 아니라 Evaluator 담당) — 표현만 정리.
6. workflows의 `<SKILL_DIR>` 표기와 프롬프트의 `{SKILL_DIR}` 표기 혼재 — 통일 권장(치환 규약은 양쪽 다 정의되어 있어 동작 문제는 아님).

## Recommended Next Focus

1. **Blocking #1**: html2pptx에 중첩 ul/ol 가드 추가(colspan과 동일한 exit 2 정책이 최소 수정) + html-spec §6에 중첩 규칙 1줄. 회귀 확인: 중첩 리스트 픽스처가 exit 2가 되는지(또는 올바른 들여쓰기 문단이 되는지)와 기존 clean 픽스처 여전히 통과.
2. **Blocking #2**: html2pptx font-family 폴백 체인(body/.el-text CSS 규칙 파싱) + boilerplate 본문 .el-text 인라인 font-family 명시 + conversion-rules §7 잔차 목록 갱신. 회귀 확인: 재오픈 덤프에서 본문 run.font.name이 design-system 첫 패밀리와 일치.
3. **Blocking #3**: 표 셀 폰트 규칙 단일화(conversion-rules §3·html-spec §7·lint 체크 14 삼자 동기화).
4. 여력이 있으면 Non-Blocking 1~3 문서 정리(각 1~2줄 수정).

이외 항목(기사 커버리지·역할 프롬프트·안전 게이트·lint/verify 본체)은 재작업 불필요 — 위 3건은 전부 변환 계약 국소 수정이며 아키텍처 변경을 요구하지 않는다.
