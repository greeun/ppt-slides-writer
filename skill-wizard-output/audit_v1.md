# Audit — frentis 10-스킬 고도화 (v1)

감사일: 2026-08-17. 감사자: Evaluator (Generator와 별도 세션, 산출물·원본·upgrade-notes만 근거).
모든 검증은 실제 명령 재실행으로 재현함 — generator_report 주장은 신뢰하지 않고 전부 독립 재검증.

- 원본(read-only): `/Users/uni4love/project/workspace/216-frentis/frentis-education/.claude/skills/` + `.claude/resources/ai-slop-checklist.md`
- 산출: `/Users/uni4love/project/workspace/211-withwiz/claude-utils/claude-skills/ppt-slides-writer/{skills,resources,upgrade-notes.md}`

## Verdict: PASS

판정 로직 적용: 2× 축(원형 충실도 5, 최신성 5) ≥4, 1× 축(생태계 4, 저장소 5) ≥3, 검증 1~9 전부 통과 → PASS.
사람 게이트(검증 10)는 자료 준비 완료 상태 — 승인은 사용자 몫 (스펙 §7).

## §6-1 검증 1~9 결과

| # | 검증 | 실행 명령 | 실제 결과 | 상태 |
|---|------|----------|----------|------|
| 1 | 트리 동일 구조 | `diff <(cd 원본 && find . -type f ! -name .DS_Store \| sort) <(cd 산출/skills && find …)` | 유일 diff `77a78 > ./remotion-slide-builder/references/layout-library.md` (R7, upgrade-notes.md:50 기재). `diff 원본 ai-slop-checklist.md 산출` → EXIT=0 (변경 0) | PASS |
| 2 | frontmatter 3필드 | awk로 첫 frontmatter 블록 name/description/version 추출, 원본 name과 대조 | 10/10 스킬: name=폴더명=원본 name, description 존재, version 존재 (1.0.0 ×8, pdf 2.2.0, slide-reviewer 0.2.0 — §3-5 확정값과 정확 일치) | PASS |
| 3 | diff→백로그 매핑 | `diff -rq --exclude='.DS_Store' 원본 산출` + 24개 파일 전수 `diff -u` | 변경 24파일 + 신규 1 — upgrade-notes 매핑표와 파일 단위 양방향 1:1 대응(매핑표에 없는 변경 파일 0건, diff 없는 매핑 행 0건). 전 hunk를 §6-2 허용 9유형으로 분류 완료(아래 표) | PASS |
| 4 | 검증 출처 기록 | upgrade-notes 매핑표 A1/A2/A3 행 검증 출처 열 검사 | A1 2행(로그 #1), A2 전행(로그 #2~#11), A3 1행(로그 #9) 전부 기재. 로그 URL은 §3 확정 출처와 부합(platform.claude.com overview / ai.google.dev / developers.openai.com / npm) | PASS |
| 5 | 참조 경로 무결성 | md 링크+인라인 코드 경로 추출·해석 스크립트(78건), 산출·원본 각각 실행 후 미해석 집합 대조 | C11 수정 경로 6곳 전부 실제 파일로 해석 OK(예: `skills/slide-reviewer/../../resources/ai-slop-checklist.md` 존재). 미해석 13건 = 원본 미해석 13건과 **집합 완전 동일**(스킬루트 상대 관행·vault 산출물 예시·brace 패턴) → 신규 파손 0건. 잔존 `.claude/` 16건은 전부 §3-8 런타임 경로(python3/typst import/cp/uv 명령·Configuration) — staging 치환 존재 확인 | PASS |
| 6 | Remotion 무손실 | 파일별 `grep -ci remotion` 원본 대비 전수 + 대체 어휘 diff 검사 | per-file 감소 **3건**(자기신고는 2건 — 아래 판정 (b)): ① lo-as-slide-source.md 2→1 ② SKILL.md 54→53 (layout-library.md 2 포함 시 55≥54) ③ **information-architecture.md 1→0 (자기신고 누락)**. 3건 모두 §4 명령 편집(C11 경로 문자열·R7 이동)의 필연 결과, 서술 손실 없음. 대체 스택: reveal.js 2→2, Marp 9→9, "HTML 덱" 0→0 — 치환 서술 신설 0건 | PASS (판정부) |
| 7 | SKILL.md ≤500줄 | `wc -l` 10개 | 100~488줄, 전부 ≤500 (최대 remotion 488) | PASS |
| 8 | Python 문법 | `python3 -m py_compile` 4종 | generate.py / section-scanner.py / extract_pdf.py / extract_hwp.py 전부 종료코드 0. 검증으로 생긴 `__pycache__`는 제거해 트리 원복 확인(잔존 0) | PASS |
| 9 | 도메인 어휘 보존 | 원본에서 CAT/CU/LO/vault/합쇼체/격식체/`los/` 등장 파일 전수 목록화 → 산출 동일 파일 grep | "VOCAB: no loss in any file" — 소실 0건 | PASS |

## Diff 화이트리스트 대조

| 스킬 | 변경 파일 | hunk 수 | 허용 유형 매핑 (§6-2) | 위반 |
|------|----------|---------|----------------------|------|
| curriculum-builder | SKILL.md | 3 | ④B5(model 삭제)+②B7(allowed-tools)+⑤C8, ⑥C11(132행) | 0 |
| curriculum-builder | references/structure-rules.md | 1 | ①A1(280행 팩트체크 예시 — 취지 유지, 현행 라인업 교체) | 0 |
| curriculum-builder | workflows 6개 | 각 1 | ②B7(frontmatter Task→Agent) | 0 |
| slide-builder | SKILL.md / workflows/schema.md | 1 / 1 | ④B5+⑤C8 / ①A1(161행 `claude-sonnet-5`) | 0 |
| diagram-builder | SKILL.md | 1 | ④B5+⑤C8 | 0 |
| slide-reviewer | SKILL.md | 4 | ⑤C8(0.1.0→0.2.0), ⑥C11 ×4(94·109·142·160행), ⑦C10 ×2(기존 문장 무삭제, 6줄·불릿 3~5·20px 수치는 원본 slide-builder/SKILL.md:155·remotion SKILL.md:359 실재 확인) | 0 |
| self-study-assistant | SKILL.md | 2 | ④B5+⑤C8, ⑦C10(원본 SKILL.md:58 "기본 탐구 깊이: Level 2…" 실재 확인) | 0 |
| doc-converter | SKILL.md | 6 | ⑤C8+②B7(allowed-tools), ③B6(청크 표 3행 + `--pages` 30단위 — 스펙 §4 값과 정확 일치), ②B7 ×4(본문 "Agent 도구 호출:") | 0 |
| example-builder | SKILL.md / workflows/example-build.md | 2 / 2 | ⑤C8+②B7, ②B7(73행) / ②B7(frontmatter, 119·124행) | 0 |
| pdf-builder | SKILL.md | 1 | ④B5+⑤C8(2.2.0, §3-5 위치 통일 — upgrade-notes.md:123 기재) | 0 |
| image-gen | SKILL.md | 6 | ⑤C8, ①A2(프로바이더 표 2셀), ⑨A2(lite 행)+①(날짜), ①A2(비율 세대 구분·배너 부기), ①A2(비용 날짜) | 0 |
| image-gen | generate.py | 3 | ①A2(MODELS GA ID)+⑨(lite 매핑·help·가격 주석 lite 줄) — 함수 로직·VALID_GEMINI_RATIOS 불변 확인 | 0 |
| image-gen | references/openai.md | 6 | ①A2(날짜 4곳·GA ID 6행·Imagen 3행 삭제+종료 안내 — §4 명시), ①A2(비교 표 2셀 — §3-2 전역 지시 소급, 하단 Notes 참조) | 0 |
| remotion-slide-builder | SKILL.md | 5 | ⑤C8, ⑧R7(레퍼런스 표 1행+이동 3구간+포인터 3개, 각 1줄) | 0 |
| remotion-slide-builder | references/layout-library.md (신규) | — | ⑧R7 — 하단 프로브 참조 (verbatim 재구성 PASS) | 0 |
| remotion-slide-builder | templates/package.json | 2 | ①A3(버전 문자열 6줄만 — 동일 메이저, 로그 #9 값과 일치. ts ^5.7.0·pdf-lib 유지) | 0 |
| remotion-slide-builder | references/{information-architecture,lo-as-slide-source}.md | 각 1 | ⑥C11(동일 폴더 상대형) | 0 |
| (그 외 106개 파일 + resources) | — | 0 | D — `diff -rq` 결과 바이트 동일 | 0 |

허용 유형 밖 hunk: **0건**. 매핑표 양방향 완전성: 확인(검증 3).

## Generator 자기신고 3건 판정

**(a) 스펙 파일 개수 라벨 불일치 → 동의 (ESCALATE 불요, 진행 타당)**
독립 재집계: curriculum 17 / remotion 40 / pdf-builder 35 (find 실행, 총 131파일) — 스펙 라벨 20/34/29와 불일치 재확인. 결정적 증거 2건: ① 스펙 §4 curriculum 파일 목록 자체가 17개를 열거하고 있어 라벨 "20개"는 스펙 내부 모순(열거된 17개 파일명은 실제 트리와 정확 일치 확인) ② 원본 무변동 — `find -newermt 2026-06-22` 0건, 최신 mtime 2026-06-21, `git log -1 -- .claude/skills` = 2026-06-21 15:52 (238c30e), 스펙 작성일 2026-08-17 이전. 따라서 §6-4-1의 전제(원본 드리프트)가 아니라 Planner 산술 오류. 전체 트리 verbatim 복사 방식이라 작업 결과에 비영향. pdf templates 실제 31개도 스펙 명시 유형(.typ 23, .yml 6, .qmd.template 1, README.md 1)에 전부 속함.

**(b) remotion 언급 per-file 감소 → 판정 동의, 단 열거 반박: 실제 3건 (자기신고 2건)**
독립 재실행 결과 감소 파일은 **3개**: lo-as-slide-source.md 2→1, SKILL.md 54→53에 더해 **information-architecture.md 1→0**이 자기신고에서 누락됨(generator_report.md:47). 누락 건의 원인도 동일 — §4 명시 C11 편집(information-architecture.md:14의 `.claude/skills/remotion-slide-builder/references/…` → `lo-as-slide-source.md`)이 경로 문자열 속 "remotion" 1회를 제거한 것으로, 서술 손실이 아님. 3건 모두 화이트리스트 편집의 필연 결과이고 대체 스택 서술 신설 0건(reveal.js 2→2, Marp 9→9, "HTML 덱" 0→0)이므로 검증 6의 취지(무손실·비치환)는 충족 — 기계 기준의 문자적 적용은 스펙 내부 모순이라는 판단에 동의. 산출물 수정 불요, 기록 정정만 권고(Non-Blocking #1).

**(c) session-plan.md:178 `.claude/skills` 경로 유지 → 동의**
맥락 확인: Phase 4 "CU 파일 생성/수정" 절차의 런타임 템플릿 지정(`템플릿: .claude/skills/curriculum-builder/templates/curriculum-delivery.md`) — 워크플로우 실행 중 Read 대상이므로 §3-8 "실행 명령 내 런타임 경로 원문 유지"에 해당. 결정적으로 §4 curriculum C11 화이트리스트(SKILL.md 132행 1건뿐)에 이 행이 없으므로, 수정했다면 오히려 §1-5 위반이 됨. staging 치환 검증: `skills/curriculum-builder/templates/curriculum-delivery.md` 존재 확인 OK. upgrade-notes.md:78에 기록됨.

## Adversarial Probes

**리라이팅 스캔** — `diff -rq` 전수(샘플 5개를 초과하는 강한 증거): 변경 24파일 외 **106개 파일 전부 바이트 동일**. 변경 파일 내부도 24개 전수 `diff -u`로 hunk 외 주변 문장 무변경 확인. 리라이팅 0건.

**R7 verbatim 재구성** — 원본 SKILL.md에서 3구간을 awk로 추출, layout-library.md 대응 구간과 diff: ① `## 레이아웃 컴포넌트 라이브러리`(3,707B) ② `## 컴포넌트 업데이트 메모`(806B) ③ `### 표준 레이아웃 패턴`+`### 카드 내부 공통 구조`(1,427B) — **3구간 모두 IDENTICAL(바이트 동일)**, 헤딩 레벨 원형 유지. 파일 내 스캐폴딩은 1행 제목 + 2행 안내 인용문(layout-library.md:1-4)뿐으로 신규 실질 내용 0 — 신규 파일 성립을 위한 최소 구성으로 판정(§4 포인터 스캐폴딩의 자연 연장, 하단 Notes #4). 산출 SKILL.md 488줄 ≤500 (`wc -l`).

**Version sweep** — 10/10: 값 §3-5 정확 일치(위 검증 2), 따옴표 없음, 전부 name/description 다음 줄(frontmatter 내 행번호 5~13, 각 description 직후) 확인. pdf-builder 위치 이동(말미→description 다음)은 §3-5 표기 규칙 준수 조치로 upgrade-notes.md:123에 기재.

**도구명 잔존** — `grep -rnw 'Task' skills --include='*.md'` → **0건** (grep 종료코드 1). 비도구 용례 포함 잔존 없음.

**날짜 통일** — image-gen 3개 파일 모두 2026-08 (표·주석·라인업), 출처 확인일만 원본과 동일 형식의 전체 날짜(2026-08-17). `2026-05` 잔존 grep 결과 2건은 curriculum-builder/SKILL.md:36·references/structure-rules.md:51의 "2026-05-09" — 가격/모델 스냅샷이 아닌 정책 개정 이력 날짜로 통일 대상 아님(upgrade-notes.md:79 기재와 일치, 원본 그대로).

**개선 제안 누출 (4건)** — 전부 미적용 확인: ① package.json `typescript: ^5.7.0` 유지(diff 증거) ② openai.md Gemini 가격 표에 lite 행 없음(diff 증거) ③ SKILL.md 지원 비율 절에 모델별 해상도 제한 명기 없음 + generate.py 해상도 검증 로직 추가 없음(diff에 로직 hunk 부재) ④ doc-converter Configuration `default_model: summary/full/extract: haiku` 원문 그대로(SKILL.md:281-284). 누출 0건.

**웹 스팟체크 (스펙 §3 확정값 재검증)** —
- `ai.google.dev/gemini-api/docs/image-generation`: GA 4종 `gemini-3.1-flash-image`(512px/1K/2K/4K)·`gemini-3.1-flash-lite-image`(1K 전용)·`gemini-3-pro-image`·`gemini-2.5-flash-image` 확인, 3.1 비율 10종 정확 일치, `-preview` ID 부재 → 로그 #2·산출 표기와 일치.
- `ai.google.dev/gemini-api/docs/pricing`: 3.1 $0.045/$0.067/$0.101/$0.151, lite $0.0336, pro $0.134/$0.24, 2.5 $0.039, Batch=표준 50% 명시 → 로그 #4·가격 셀·Batch 유지 근거와 전부 일치.
- `developers.openai.com/api/docs/guides/image-generation`: gpt-image-2 high $0.211/$0.165/$0.165, mini $0.036/$0.052 등 quality×size 표 → 로그 #10·산출 표와 전부 일치. 비용 예시 재계산 6건 산술 검산 일치(예: 2×$0.165+8×$0.052=$0.746→$0.75).
- Claude 라인업(로그 #1): Fable 5/Opus 5/Sonnet 5(`claude-sonnet-5`)+Haiku 4.5 — 현행 공식 라인업과 일치, schema.md:161·structure-rules.md:280 표기 정확. 구 ID·추측 모델명·미검증 수치 잔존 0건.

## 품질 축 채점

| 축 | 가중 | 점수 | 근거 (파일:행 인용) |
|----|------|------|---------------------|
| 원형 충실도 | 2× | **5** | 전 diff hunk가 허용 9유형에 매핑(위 대조표, 위반 0). 106개 무변경 파일 바이트 동일. R7 3구간 바이트 동일(layout-library.md:6-131 = 원본 SKILL.md 추출본). C10 3건 모두 기존 문장 무삭제 + 실재 수치 기준 연결(slide-reviewer/SKILL.md:100-101, self-study/SKILL.md:92) |
| 최신성 정확도 | 2× | **5** | `-preview` 잔존 0건(grep), GA ID 전부 §3-2 확정값(generate.py:16-19, openai.md:139-144), `claude-sonnet-5`(schema.md:161), 가격 셀 전부 검증 로그 #4·#10·#11 대응 + 라이브 페이지 재확인 일치, 마킹 필요 셀 0건(전 수치 검증됨), 날짜 2026-08 통일 |
| 생태계 정합성 | 1× | **4** | 신규 끊어진 참조 0건(미해석 집합 원본과 완전 동일 13=13), C11 6경로 staging 해석 OK, 환경 의존 표 광범위 — 단 pdf-builder/references/render.md:34 `uv run .claude/scripts/lit-to-bib.py`가 개별 항목 없이 "각 스킬 실행 명령 전반" 범주 행으로만 커버됨(Non-Blocking #2) |
| 저장소 규칙 준수 | 1× | **5** | 10/10 name/description/version, 값 §3-5 정확 일치, SKILL.md 전부 ≤500(최대 488), upgrade-notes가 §2 고정 스키마 4섹션·열 구성 그대로(upgrade-notes.md:3,24,141,157) |

## Blocking Issues

없음.

## Non-Blocking Notes

1. **LOW** — Where: generator_report.md:47 (및 Known limitations 2). Actual: 검증 6 감소 "2건" 자기신고. Expected: 실제 3건 — information-architecture.md 1→0 누락. Fix direction: 기록 정정(산출물 자체는 무결 — 누락 건도 C11 화이트리스트 편집의 필연 결과임을 본 감사가 확인). 사람 게이트 문서에는 해당 주장 없어 게이트 영향 없음.
2. **LOW** — Where: upgrade-notes.md:141-155 환경 의존 표. Actual: pdf-builder/references/render.md:34 `uv run .claude/scripts/lit-to-bib.py`(`.claude/scripts/` 접두 — `.claude/skills/` 치환 규칙 밖 외부 스크립트)가 개별 항목으로 미기재. Expected: duplicate-checker.py처럼 개별 행 기재가 §6-3 축3 anchor 5("전부 목록화")에 더 부합. Fix direction: 표에 1행 추가 고려(범주 행 "각 스킬 실행 명령 전반"이 간접 커버하므로 차단 사유 아님).
3. **LOW** — Where: human-gate-diff-summary.md:26. Actual: 스펙 §7-2 "매핑표 전문" 대신 upgrade-notes 참조 링크로 대체. Fix direction: 게이트 제시 시 upgrade-notes.md를 함께 첨부하면 실질 충족 — 별도 재작업 불요.
4. **INFO** — layout-library.md:1-4 스캐폴딩(제목+안내 인용 2행)은 §4에 문자로 명시되지 않았으나, 신규 독립 문서 성립의 최소 필요 구성이고 실질 내용 추가가 없어 R7 포인터 스캐폴딩의 허용 범위로 판정.
5. **INFO** — openai.md:132·135("Imagen 4 기반" 교정, "14종" 세대 구분)는 §4 openai.md 행에 문구 단위로 명시되지 않았으나 §3-2 전역 지시("'Imagen 4 기반' 같은 근거 문구는 삭제·교정 대상 (A2)")로 소급 가능하고 매핑표(upgrade-notes.md:37)에 기재됨 — 허용 판정. 미교정 시 오히려 축2 위반이 되는 사실 교정.
6. **INFO** — 극단 배너 비율 "(2.5 레거시 전용)" 표기: 현행 Gemini 문서는 어떤 모델에도 해당 비율을 기재하지 않음(스팟체크 확인) — 모순이 아닌 부재이므로 §6-4-2 미해당, 스펙 §3-2 확정값 준수 확인.
7. **INFO** — 스펙 개수 라벨 오류(20/34/29 → 실제 17/40/35)는 Planner 산술 오류로 확정(판정 (a)). 사람 게이트에서 사용자에게 1줄 고지 권장(투명성 목적, 승인 항목 아님).

## Recommended Next Focus (FAIL 시만)

해당 없음 (PASS).
