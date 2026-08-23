# Generator Report — frentis 10-스킬 고도화

작성일: 2026-08-17. 스펙: `skill-wizard-output/skill-spec.md` (전문 숙지 후 실행).

## 스프린트 실행 로그

| 스프린트 | 완료 체크 명령 | 실제 출력 요약 | 상태 |
|----------|---------------|---------------|------|
| S0 스캐폴드+전역 검증 | `rsync -a --exclude='.DS_Store'` 2회 → `diff -r --exclude='.DS_Store' 원본 산출` | skills diff 0건, resources diff 0건, 복사 131개 파일. 검증 로그 표에 Claude(#1)/Gemini(#2~4)/OpenAI(#5~8,#10,#11)/npm(#9) 행 기록 | PASS |
| S1 image-gen | `python3 -m py_compile generate.py`; `grep -rn '\-preview'`; `diff -rq` | py_compile EXIT 0; `-preview` 0건; 변경 파일 3개(SKILL.md/generate.py/openai.md)만 diff; 가격 셀 전부 검증 로그 #4·#10·#11 대응(마킹 필요 셀 0건 — 전 수치가 원본과 일치 재확인됨) | PASS |
| S2 remotion-slide-builder | `wc -l SKILL.md`; 이동 3구간 substring 대조; `diff -u package.json` | SKILL.md 488줄(≤500); 3구간(895/2,761/482자) 바이트 동일 substring PASS; package.json diff는 버전 문자열 6줄만 | PASS |
| S3 slide-reviewer+curriculum-builder | 상대 경로 존재 확인 5곳; `grep "Fable 5" structure-rules.md` | `../remotion-slide-builder/references/review-rules.md`·`../../resources/ai-slop-checklist.md`(3곳)·`../remotion-slide-builder/references/lo-as-slide-source.md` 전부 해석 OK; 280행에 현행 라인업 반영 확인 | PASS |
| S4 slide-builder+diagram-builder | `grep claude-sonnet schema.md`; `grep '^model:\|^version:'` | schema.md:161 `claude-sonnet-5`; 두 SKILL.md `model:` 0건 + `version: 1.0.0` 존재 | PASS |
| S5 doc-converter+example-builder | `grep -rnw 'Task' <두 스킬> --include='*.md'`; 청크 표 grep | Task 0건; 신규 수치 3행(~30페이지 chars<90,000 / 31~90 / 91+) 반영 확인 | PASS |
| S6 pdf-builder+self-study-assistant | `grep '^version:'`; `grep -c '^model:'` | version 2.2.0/1.0.0 확인; `model:` 줄 0건/0건 | PASS |
| S7 후처리+최종 검증 | 아래 5개 규칙 + 검증 1~9 재실행 | ① version 형식 통일(10/10, 따옴표 없음·name/description 다음 줄) ② A2 스냅샷 날짜 2026-08 통일(잔존 `2026-05` 2건은 정책 개정 이력 날짜 2026-05-09로 대상 아님 — upgrade-notes 기록) ③ 매핑표 열 순서·용어 통일 ④ `grep -rnw 'Task' skills --include='*.md'` → 0건 ⑤ 스킬 간 참조 grep 재실행(아래 검증 5) | PASS |

- 사람 게이트 자료 생성: `skill-wizard-output/human-gate-diff-summary.md` (diff 통계 표 + 대표 발췌 3건 + 승인 요청 항목 a/b/c + 개선 제안 별첨).

## 스펙 매핑

| 스펙 섹션 | 구현 위치 |
|-----------|----------|
| §2 산출 레이아웃 | `ppt-slides-writer/skills/`(10개), `resources/ai-slop-checklist.md`(verbatim), `upgrade-notes.md`(§2 스키마 준수: 검증 로그/스킬별 매핑/환경 의존/개선 제안 4섹션) |
| §3-1 (A1) | upgrade-notes 검증 로그 #1; curriculum structure-rules.md:280, slide-builder schema.md:161 |
| §3-2 (A2 모델) | 검증 로그 #2·#3·#5·#6; image-gen SKILL.md·generate.py·openai.md. gpt-image-2-mini 미존재 확인 → 매핑 유지 |
| §3-3 (A2 가격) | 검증 로그 #4·#7·#10·#11; 가격 수치 전부 재검증 — 원본 값과 일치, 날짜 표기만 갱신, 마킹 셀 0건 |
| §3-4 (A3) | 검증 로그 #9; remotion templates/package.json 버전 문자열 6건, typescript 상위 메이저는 개선 제안 기록 |
| §3-5 (C8) | 10개 SKILL.md version (1.0.0 ×8, 2.2.0, 0.2.0), name/description 다음 줄 배치 |
| §3-6 (B5) | model 핀 제거 5건(curriculum/slide-builder/diagram/pdf/self-study), doc-converter haiku 유지(서브에이전트 블록 4곳 포함), 핀 없는 4개 무변경 |
| §3-7 (B7) | allowed-tools 치환 3+7건(SKILL 3, workflows 7), 본문 표현 치환 doc-converter 4곳·example-builder 3곳(SKILL 1+workflow 2) |
| §3-8/§4 (C11) | slide-reviewer 4곳, curriculum 1곳, remotion references 2곳 상대화. 런타임 경로·이름 참조는 원문 유지+환경 의존 표 기록 |
| §4 R7 | `remotion-slide-builder/references/layout-library.md` 신규(131줄), SKILL.md 606→488줄 |
| §4 C10 | slide-reviewer 체크리스트 2항목, self-study 체크리스트 1항목 — 괄호 참조 추가만(기존 문장 무삭제) |
| §5 S0~S7 | 위 실행 로그. 순서 준수(S2를 S3보다 먼저), 순차 실행이므로 S7 후처리 포함 수행 |
| §7 사람 게이트 자료 | `skill-wizard-output/human-gate-diff-summary.md` |

## Self-check (spec §6-1 checks 1–9, 실제 실행 결과)

| # | 결과 | 증거 (명령+출력 요약) |
|---|------|----------------------|
| 1 | PASS | `diff <(find 원본) <(find 산출)` → 유일 diff `77a78 remotion-slide-builder/references/layout-library.md`(R7, upgrade-notes 기록). `diff 원본/산출 ai-slop-checklist.md` → 0건 |
| 2 | PASS | 10/10 스킬 name=폴더명=원본 name, description 존재, version 존재 (개별 출력 로그 확인: 전부 [OK]) |
| 3 | PASS | `diff -rq` 전수: 변경 24파일+신규 1 — 전부 upgrade-notes 매핑표 행과 1:1 대응, 매핑표에 있는데 diff 없는 행 0건. 파일별 `diff -u` hunk도 §6-2 허용 9유형 내 |
| 4 | PASS | 매핑표의 A1/A2/A3 근거 행 전부 검증 출처 열에 검증 로그 #(URL 대응) 기재. 로그 URL은 §3 확정 출처와 부합(모델 overview/ai.google.dev/developers.openai.com/npm) |
| 5 | PASS | 링크+인라인 코드 경로 추출(126건 검사, `.claude/skills`→`skills/` 치환 포함). 산출 미해석 목록과 원본 미해석 목록 `comm` 대조 → **신규 파손 0건, 집합 완전 동일**(전부 vault 산출물 파일명 예시·이름 참조 — 환경 의존 표에 범주 기록). C11 수정 경로 5곳+2곳 전부 실제 파일로 해석 |
| 6 | PASS(설명 필요 3건 — 2회차 정정) | 파일별 `grep -cio remotion` 원본 대비: 감소 3건(1차 자기신고 2건 → **2026-08-18 2회차 정정, audit_v1 Non-Blocking #1 반영**)은 모두 §4 명령 편집의 직접 결과 — ① lo-as-slide-source.md 2→1 (C11로 경로 문자열 내 "remotion-slide-builder" 제거) ② SKILL.md 54→53 (R7 이동으로 `npx remotion studio` 1회가 layout-library.md로 이동; SKILL 53+library 2=55≥54) ③ information-architecture.md 1→0 (C11 경로 상대화 — information-architecture.md:14의 `.claude/skills/remotion-slide-builder/references/…` → `lo-as-slide-source.md` — 로 경로 문자열 내 "remotion" 1회 제거; 1차 보고에서 누락). 대체 스택 어휘 신설 0건: reveal.js 2→2, Marp 11→11, "HTML 덱" 0→0 |
| 7 | PASS | `wc -l` 10개: 100~488줄, 전부 ≤500 (최대 remotion 488) |
| 8 | PASS | `python3 -m py_compile` 4종 전부 종료코드 0 (generate.py, section-scanner.py, extract_pdf.py, extract_hwp.py). 검증 후 `__pycache__` 제거로 트리 오염 방지 |
| 9 | PASS | CAT/CU/LO/vault/합쇼체/격식체/`los/` — 원본 등장 파일 전수 대비 산출 동일 파일 grep: 소실 0건 |

## Known limitations / ambiguities

1. **스펙 파일 개수 라벨 불일치 (ESCALATE 미발동 판단)**: 스펙 §2/§4의 개수 라벨이 실제와 다름 — curriculum-builder "20개"(실제·스펙 자체 열거 모두 17개), remotion "34개"(실제 40), pdf-builder "29개/templates 25개"(실제 35/31). 원본 git log·mtime 확인 결과 최신 변경이 2026-06-21로 스펙 작성일(2026-08-17) 이전 — **원본 드리프트 아님**. curriculum은 스펙 자체 열거(17개)와 라벨(20)이 스펙 내부에서 모순이므로 라벨을 Planner 산술 오류로 판단. §4에 열거된 편집 대상 파일은 전부 존재하고 트리 전체를 rsync verbatim 복사하므로 라벨은 작업에 비영향 — §6-4 조건 1(누락·신규 발견)에 해당하지 않는다고 보고 진행. Evaluator 재판단 요망.
2. **검증 6의 기계적 per-file 판정**: 위 표 #6 — 감소 건들은 §4가 명령한 C11·R7 편집의 필연적 결과로, 절차를 문자 그대로 적용하면 스펙 내부 모순이 됨. 의미상 Remotion 서술 무손실(합산 보존, 치환 서술 0건). *(2회차 정정: 1차 보고의 "감소 2건"은 오기 — 실제 3건이며 information-architecture.md 1→0이 누락됐었음. 상세는 위 표 #6 및 하단 Round 2 절.)*
3. **curriculum workflows/session-plan.md:178** `` `.claude/skills/curriculum-builder/templates/curriculum-delivery.md` ``: §3-8의 "동일 스킬 내 절대형 정리" 문구와 §4 화이트리스트(미포함)가 상충. 워크플로우 실행 시 프로젝트 루트 기준 Read되는 런타임 템플릿 경로로 판단해 **원문 유지** 선택(§3-8 런타임 경로 예외 + 화이트리스트 우선). staging 치환 검증 통과. upgrade-notes에 기록.
4. **layout-library.md 구조 글루**: verbatim 이동 3구간 외에 파일 서두에 `# 레이아웃 라이브러리` 제목 + 2줄 안내 인용문을 추가함(신규 파일이 독립 문서로 성립하기 위한 최소 구성). 이동 구간 자체는 바이트 동일. 파일 내 배치는 원본 SKILL.md 등장 순서 그대로: ③ 표준 레이아웃 패턴·카드 내부 공통 구조 → ① 레이아웃 컴포넌트 라이브러리 → ② 컴포넌트 업데이트 메모.
5. **OpenAI 장당 가격의 출처 특성**: pricing 페이지는 토큰 단가만 게시(#7), 장당 표는 image-generation guide(#10)에서 확인 — 원본 openai.md가 이미 이 출처를 명기하고 있어 출처 구조는 원문과 일치. quality×size 장당 값 전부 guide에서 재검증됨(마킹 불요).
6. **Gemini Batch 장당 셀**: 3.1 계열 per-image Batch 값은 페이지에 직접 게시되지 않고 "Batch=표준 50%" 규칙으로 게시됨 — 원본 셀 값이 검증된 표준가의 50% 반올림과 일치하여 유지(upgrade-notes 검증 로그 하단 기록).
7. **극단 배너 비율(4:1/8:1/1:4/1:8)의 "2.5 전용" 표기**: 현행 문서에는 어떤 모델에도 미기재(#2) — 스펙 §3-2 확정("2.5 전용")을 따름. 2.5 레거시의 14종 지원은 원본 기재 유지분.
8. `.axt-profile.json`, `skill-wizard-output/`, `.claude/`는 산출 루트에 이미 존재하던 세션 부산물로 이번 산출 대상 아님(스펙 §2 레이아웃 외 — 건드리지 않음).

## Retry context (재시도인 경우만)

해당 없음 (1차 실행).

## Round 2 (audit_v1 반영)

작성일: 2026-08-18. 입력: `skill-wizard-output/audit_v1.md` (Verdict PASS, Non-Blocking Notes #1~#7). 작업 범위: 문서 산출물(generator_report·upgrade-notes·human-gate-diff-summary)만 — **제품 트리 `skills/`·`resources/` 편집 0건**.

| Note | 조치 | 증거 |
|------|------|------|
| #1 (LOW) | **정정 적용** — 본 문서 Self-check #6 행 및 Known limitations 2를 "(2회차 정정)" 명시 표기로 수정: 감소 2건 → 실제 3건, 누락분 information-architecture.md 1→0 (원인 = C11 경로 상대화, information-architecture.md:14) 추가. 1차 기록을 무언 삭제하지 않고 정정임을 문면에 남김 | diff 발췌: `-| 6 | PASS(설명 필요 2건) | … 감소 2건은 …` → `+| 6 | PASS(설명 필요 3건 — 2회차 정정) | … 감소 3건(1차 자기신고 2건 → **2026-08-18 2회차 정정, audit_v1 Non-Blocking #1 반영**) … ③ information-architecture.md 1→0 …` |
| #2 (LOW) | **행 추가** — upgrade-notes.md 환경 의존 참조 표에 개별 행 1건 추가 | diff 발췌: `+| skills/pdf-builder/references/render.md:34 | \`uv run .claude/scripts/lit-to-bib.py\` | 외부 스크립트 — \`.claude/scripts/\` 접두로 §3-8 \`.claude/skills/\` 치환 규칙 밖, 배포 환경 스크립트에 의존 |` (render.md:34 실물 재확인 후 기재) |
| #3 (LOW) | **전문 전재** — human-gate-diff-summary.md §2의 참조 링크를 upgrade-notes.md "스킬별 변경 매핑" 섹션 verbatim 전재로 교체 (스펙 §7-2 "매핑표 전문" 충족). 전재 출처 1줄 명기 | 기계 대조: 양쪽 섹션 awk 추출 후 `diff` → `VERBATIM MATCH` (공행 제외 전 행 동일) |
| #4 (INFO) | no action — audit이 layout-library.md 스캐폴딩(제목+안내 2행)을 R7 포인터 스캐폴딩 허용 범위로 확정 판정 | — |
| #5 (INFO) | no action — openai.md "Imagen 4 기반" 교정·"14종" 세대 구분은 §3-2 전역 지시 소급으로 허용 확정 판정 | — |
| #6 (INFO) | no action — 극단 배너 비율 "(2.5 레거시 전용)" 표기는 모순 아닌 부재(§6-4-2 미해당)로 확정 판정 | — |
| #7 (INFO) | **고지 추가** — human-gate-diff-summary.md §1에 투명성 고지 1줄 추가: 스펙 파일 개수 라벨(20/34/29)은 Planner 산술 오류, 실제 17/40/35 (audit_v1 판정 (a)), 작업 영향 없음·승인 항목 아님 | 추가 행: `- 고지: 스펙 §2/§4의 파일 개수 라벨(curriculum 20 / remotion 34 / pdf-builder 29)은 Planner 산술 오류로 확인됨 — 실제 17/40/35 …` |

### Round 2 재검증 (2026-08-18 실행)

- `diff -rq --exclude='.DS_Store' 원본/.claude/skills 산출/skills` → **변경 24파일 + Only-in 1건(remotion-slide-builder/references/layout-library.md)** — 1차와 동일 집합, 제품 트리 무변동 확인.
- `diff 원본 ai-slop-checklist.md 산출` → IDENTICAL (변경 0).
- `wc -l skills/remotion-slide-builder/SKILL.md` → **488줄 (≤500)** — 카나리 유지.
- 게이트 문서 전재 매핑표 vs upgrade-notes 원문 → `diff` VERBATIM MATCH.

## Round 3 (audit_v2 반영)

위임 범위: audit_v2 Non-Blocking #1 — human-gate-diff-summary.md §1 통계표의 추가/삭제 줄 수 5행 정정. 그 외 편집 0건.

### 독립 재실측 (2026-08-18 실행)

원본 `/Users/uni4love/project/workspace/216-frentis/frentis-education/.claude/skills/` vs 산출 `skills/` 변경 24파일 전수에 대해 두 계수법으로 측정: ① `diff -u | awk '/^\+/ && !/^\+\+\+/'`(+)·`'/^-/ && !/^---/'`(-) ② `git diff --no-index --numstat`. **24/24 파일에서 두 방법 완전 일치.** 신규 layout-library.md(131줄)는 표 기존 관례대로 "+신규 131줄" 별도 표기 유지(합산 제외).

| 스킬 | 재실측 +/- | 표 기존값 | 판정 |
|------|-----------|----------|------|
| curriculum-builder | +10 / -10 | +10 / -9 | 정정 (-9→-10) |
| slide-builder | +2 / -2 | +2 / -2 | 일치 |
| remotion-slide-builder | +13 / -131 | +13 / -93 | 정정 (-93→-131; SKILL.md 단독 +5/-123, 606→488 순감 -118과 정합) |
| slide-reviewer | +7 / -7 | +7 / -4 | 정정 (-4→-7) |
| diagram-builder | +1 / -1 | +1 / -1 | 일치 |
| image-gen | +30 / -27 | +29 / -26 | 정정 (+29→+30, -26→-27) |
| pdf-builder | +1 / -2 | +1 / -2 | 일치 |
| doc-converter | +13 / -12 | +13 / -12 | 일치 |
| example-builder | +6 / -5 | +6 / -5 | 일치 |
| self-study-assistant | +2 / -2 | +2 / -1 | 정정 (-1→-2) |

재실측값은 audit_v2 P5의 실측값과 전 항목 일치. 변경 파일 수·백로그 근거 코드 열은 audit_v2가 정확 판정했으므로 무수정.

### 변경 셀 diff (human-gate-diff-summary.md §1)

```diff
-| curriculum-builder | … | +10 / -9 | …
+| curriculum-builder | … | +10 / -10 | …
-| remotion-slide-builder | … | +13 / -93 (+신규 131줄) | …
+| remotion-slide-builder | … | +13 / -131 (+신규 131줄) | …
-| slide-reviewer | … | +7 / -4 | …
+| slide-reviewer | … | +7 / -7 | …
-| image-gen | … | +29 / -26 | …
+| image-gen | … | +30 / -27 | …
-| self-study-assistant | … | +2 / -1 | …
+| self-study-assistant | … | +2 / -2 | …
```

표 직후에 정정 고지 1줄 추가: `(3회차 정정: 줄 수 재실측, audit_v2 반영)`.

### 무접촉 검증

- `find skills resources upgrade-notes.md skill-wizard-output -newer skill-wizard-output/human-gate-diff-summary.md -type f` → **0건** — 게이트 문서 편집 이후 다른 파일 무변동.
- `diff -rq` 원본 vs 산출 skills → 변경 **24파일 + Only-in 1건** 그대로.
- mtime: upgrade-notes.md 00:06:13, audit_v1.md 00:04:47, audit_v2.md 00:17:55, 제품 트리 최신 2026-08-17 23:32:10 — 전부 audit_v2 기록값과 동일(3회차 미접촉). generator_report.md(본 파일)·human-gate-diff-summary.md 2건만 3회차에 수정됨.
