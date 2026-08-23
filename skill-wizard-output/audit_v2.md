# Audit — frentis 10-스킬 고도화 (v2)

감사일: 2026-08-18. 감사자: Evaluator 2회차 (신규 세션, 1회차와 별도). 라운드 2의 위임 범위는 "audit_v1 노트 반영을 위한 문서 전용 수정"이며, 본 감사는 ① 제품 트리 무접촉 입증 ② 노트 반영 정합 ③ 회귀 재검증 ④ 1회차가 보지 않은 각도의 신규 프로브를 수행했다. generator_report의 자기신고는 신뢰하지 않고 전 항목 명령 재실행으로 재현했다.

- 원본(read-only): `/Users/uni4love/project/workspace/216-frentis/frentis-education/.claude/skills/` + `.claude/resources/ai-slop-checklist.md`
- 산출: `/Users/uni4love/project/workspace/211-withwiz/claude-utils/claude-skills/ppt-slides-writer/{skills,resources,upgrade-notes.md}` + `skill-wizard-output/{generator_report.md,human-gate-diff-summary.md}`

## Verdict: PASS

판정 로직(스펙 §6-3, v1과 동일): 2× 축(원형 충실도 5, 최신성 5) ≥4, 1× 축(생태계 5, 저장소 5) ≥3, 재실행한 검증 항목 전부 통과, 라운드 2 제품 편집 0건 입증 → PASS. audit_v1 대비 회귀 없음(하단 Iteration Quality Note). 사람 게이트 제시 전 Non-Blocking #1(게이트 통계표 5행 수치)의 정정을 권고한다.

## 제품 트리 불변 검증

라운드 2 위임은 문서 전용이었으므로 `skills/`·`resources/`에 대한 어떤 편집도 FAIL 사유다. 세 갈래로 무접촉을 입증했다.

**(1) 원본 대비 diff 집합 = 1회차와 정확히 동일.** `diff -rq --exclude='.DS_Store' 원본 산출/skills` → 변경 **24파일** + Only-in **1건**(`remotion-slide-builder/references/layout-library.md`), EXIT 후 목록 전수 확인. 24파일 구성: curriculum-builder 8(SKILL.md, references/structure-rules.md, workflows 6), slide-builder 2, remotion-slide-builder 4(SKILL.md, package.json, references 2), slide-reviewer 1, diagram-builder 1, image-gen 3, pdf-builder 1, doc-converter 1, example-builder 2, self-study-assistant 1 — audit_v1의 Diff 화이트리스트 대조표와 파일 단위 완전 일치. `find` 목록 대조(검증 1)도 유일 diff `77a78 > ./remotion-slide-builder/references/layout-library.md`.

**(2) mtime 프로브(집합 동일 ≠ 내용 동일의 맹점 보강).** diff 집합이 같아도 이미 변경된 24파일을 라운드 2에서 재편집하면 집합은 그대로다. 이를 배제하기 위해 `find skills resources -type f -newermt "2026-08-18 00:00:00"` → **0건**. 제품 파일 최신 mtime은 2026-08-17 23:32:10(self-study SKILL.md). 반면 문서 3종은 라운드 2 시점 mtime: upgrade-notes.md 2026-08-18 00:06:13, human-gate-diff-summary.md 00:07:39, generator_report.md 00:08:28 — 전부 audit_v1.md(00:04:47) 이후. **문서만 수정되고 제품은 무접촉**임이 파일시스템 수준에서 입증됨.

**(3) 카나리.** `diff`+`cmp` ai-slop-checklist.md → **IDENTICAL(바이트 동일)**. `wc -l` remotion SKILL.md → **488줄(≤500)**, 1회차 기록값과 동일. 10개 SKILL.md 전부 100~488줄.

결론: 라운드 2 제품 편집 0건 — 위임 준수.

## 노트 반영 검증 (#1, #2, #3, #7 + #4, #5, #6 무접촉)

| Note | 판정 | 재현 증거 |
|------|------|----------|
| #1 (기록 정정) | **반영 확인** | generator_report.md:47 — `PASS(설명 필요 3건 — 2회차 정정)` 및 `③ information-architecture.md 1→0 (… 1차 보고에서 누락)` 명기, :55 — Known limitations 2에 `*(2회차 정정: 1차 보고의 "감소 2건"은 오기 — 실제 3건 …)*`. 1차 기록을 무언 삭제하지 않고 정정 표기로 남김 — audit_v1 #1의 "기록 정정" 지시와 정확히 부합. 감소 3건의 사실 자체는 산출물 무변경(위 불변 검증)이므로 1회차 판정 유지 |
| #2 (환경 의존 행) | **반영 확인** | upgrade-notes.md:153 — `\| skills/pdf-builder/references/render.md:34 \| \`uv run .claude/scripts/lit-to-bib.py\` \| 외부 스크립트 — \`.claude/scripts/\` 접두로 §3-8 \`.claude/skills/\` 치환 규칙 밖 …\|` 행 추가됨. **실물 대조**: render.md 34행 = `3. 참고문헌 동기화: \`uv run .claude/scripts/lit-to-bib.py\`` (sed로 직접 확인) — 파일:행·명령 문자열 모두 정확. 행 삽입 위치(표 중간 153행)는 audit_v1이 인용한 앞선 행번호(:50, :78, :79, :123)를 밀지 않음 — 인용 무결 유지 확인 |
| #3 (매핑표 전문 전재) | **반영 확인 (기계 대조)** | upgrade-notes.md `## 스킬별 변경 매핑` 섹션과 human-gate-diff-summary.md `## 2.` 섹션을 각각 awk 추출, 공백 행·전재 안내문 제외 후 `diff` → **차이 0, 양쪽 86행 완전 동일**. 전재 출처 1줄(human-gate:27 "(아래는 `../upgrade-notes.md` … verbatim 전재 …)") 명기 확인. 스펙 §7-2 "매핑표 전문" 충족. 전재본이 라운드 2 최종 upgrade-notes(#2 행 추가 후)와 대조된 것이므로 스냅샷 불일치 없음 |
| #7 (투명성 고지) | **반영 확인 + 수치 독립 재계수** | human-gate-diff-summary.md:23 — "고지: 스펙 §2/§4의 파일 개수 라벨(curriculum 20 / remotion 34 / pdf-builder 29)은 Planner 산술 오류로 확인됨 — 실제 17/40/35 … (승인 항목 아님, 투명성 고지)". `find` 재계수: curriculum **17** / remotion **40** / pdf-builder **35** (templates 31, 총 131) — 고지 수치 전부 실측과 일치 |
| #4 (무접촉) | 확인 | layout-library.md:1-4 스캐폴딩(제목 1행 + 안내 인용 2행) 원상 그대로 (head 재확인) — no action 판정대로 미개입 |
| #5 (무접촉) | 확인 | openai.md "나노바나나(네이티브 이미지 생성) 계열이 자연스러움 (Imagen 4 계열은 2026-08-17 서비스 종료)"·"(3.1 계열 10종, 2.5 레거시 14종)" 원상 그대로 (sed 재확인) |
| #6 (무접촉) | 확인 | image-gen SKILL.md:284-285 "(2.5 레거시 전용)" 부기 2행 원상 그대로 (grep 재확인) |

\#4~#6은 개별 스팟체크에 더해 위 mtime 프로브(제품 전체 무접촉)로 이중 확인됨.

## 회귀 재검증

| 항목 | 실행 명령 | 실제 결과 | 상태 |
|------|----------|----------|------|
| 검증 1 (트리 구조) | `diff <(find 원본) <(find 산출)` + resources cmp | 유일 diff layout-library.md(R7, upgrade-notes.md:50 기재 유지), ai-slop-checklist 바이트 동일 | PASS |
| 검증 2 (frontmatter 3필드) | awk로 첫 frontmatter 블록 추출, 원본 name·폴더명 3자 대조 | 10/10: name=폴더명=원본 name, description 존재, version = 1.0.0 ×8 / pdf 2.2.0 / slide-reviewer 0.2.0 (§3-5 정확 일치) | PASS |
| 검증 7 (≤500줄) | `wc -l` 10개 | 100~488줄 전부 ≤500 (최대 remotion 488) | PASS |
| 검증 8 (Python 문법) | `python3 -m py_compile` 4종 | generate.py / section-scanner.py / extract_pdf.py / extract_hwp.py 전부 exit 0. 컴파일이 생성한 `__pycache__` 3개는 본 감사가 제거, 잔존 0 (사전 비존재는 compile 이전 실행한 `diff -rq`에 Only-in 부재로 입증) | PASS |
| 무변경 파일 무작위 2개 | srand 무작위 추첨 → `cmp` | `self-study-assistant/templates/study-session.md`·`pdf-builder/templates/handout/sections/00-template.typ` 모두 **BYTE_IDENTICAL** (무변경 모집단 131-24-1=106개… 추첨 풀 107행 중 2개) | PASS |
| Task 잔존 | `grep -rnw 'Task' skills --include='*.md'` | 0건 (exit 1) | PASS |
| `-preview` 잔존 | `grep -rn -- '-preview' skills resources` | 0건 (exit 1) | PASS |

## Fresh-eyes Probes (1회차 미수행 각도)

**P1. 전 md frontmatter YAML 파싱 유효성** — skills/ 내 `---`로 시작하는 md 전수(27개: SKILL.md 10 + workflows 17)의 첫 frontmatter 블록을 `python3 yaml.safe_load`로 파싱 → **27/27 파싱 성공, 전부 dict**. Task→Agent 치환·version 삽입·model 줄 삭제가 YAML 구조를 깨지 않았음을 구문 수준에서 확인.

**P2. layout-library.md 포인터-헤딩 정합** — remotion SKILL.md의 포인터 4곳(156행 레퍼런스 표, 376·411·413행 인용 포인터)이 언급하는 절 제목 vs 파일 내 실제 헤딩 대조: `### 표준 레이아웃 패턴`(:6)·`### 카드 내부 공통 구조`(:20)·`## 레이아웃 컴포넌트 라이브러리`(:31, 하위 사용 패턴:36/컴포넌트 구성:53/원자 컴포넌트 혼합:82/제작 우선순위:95/샘플 갤러리:102)·`## 컴포넌트 업데이트 메모`(:110, CheckpointSlide:112/InstructorSlide:118/SlideLayout source prop:125) — **포인터가 열거한 절 전부 실재, 불일치 0건**.

**P3. R7 verbatim 독립 재검증** — layout-library.md에서 스캐폴드(1~4행) 제거 후 3구간을 분리, 각각 원본 SKILL.md의 substring인지 python으로 검사: 표준패턴+카드구조 1,425B / 레이아웃 컴포넌트 라이브러리 3,705B / 컴포넌트 업데이트 메모 804B — **3구간 모두 verbatim True** (audit_v1의 1,427/3,707/806B와 2B 차이는 구간 경계 개행 포함 여부 — 내용 동일).

**P4. upgrade-notes 검증 로그 참조 무결** — 본문 `검증 로그 #N`·`로그 #N` 참조 전수 추출(#1~#7, #9~#11) vs 로그 표 정의 행(#1~#11) → **참조 ⊆ 정의, 끊어진 # 참조 0건**. #8(OpenRouter 교차 확인)만 정의-무참조 — §3-3 보조 절차의 이행 기록 자체가 목적이므로 무결성 문제 아님(하단 INFO).

**P5. human-gate §1 통계표 실측 대조** — 변경 24파일 전수에 `diff -u` 기반 +/- 줄 계수(독립 교차: `git diff --no-index --numstat` per-file 동일값 확인) vs 게이트 표: **11행 중 5행 수치 불일치 발견** — curriculum 실측 +10/**-10**(표 -9), image-gen **+30/-27**(표 +29/-26), remotion +13/**-131**(표 -93), self-study +2/**-2**(표 -1), slide-reviewer +7/**-7**(표 -4). 산술 반증: remotion SKILL.md 606→488줄은 순감 -118이므로 삭제 -93은 성립 불가(실측 +5/-123). 변경 파일 수·백로그 코드 열·신규 131줄은 전부 정확. → Non-Blocking #1.

**P6. 부산물·잡파일 잔존** — `find skills resources`에서 `__pycache__`·`*.pyc`·`.DS_Store` **0건**; 트리 전체 `*.bak`/`*~`/`*.orig`/`*.tmp` **0건**. 산출 루트의 `.DS_Store` 1건은 제품 트리(skills/·resources/) 밖 Finder 부산물(mtime 08-17 23:35) — 스펙 §2 제외 규칙의 대상(복사 금지)과 무관한 위치로 무해(하단 INFO).

**P7. 검증 6 계수 불일치(9 vs 11) 규명** — audit_v1 "Marp 9→9" vs generator_report 2회차 "Marp 11→11"의 상호 모순처럼 보이는 수치를 직접 재계수: 매칭 **행 수**(`grep -ri`) 9→9, **발생 수**(`grep -rio`) 11→11 — 두 보고가 서로 다른 계수 단위를 쓴 것으로 **둘 다 각자 기준에서 정확**하고, 핵심 결론(Δ=0, 대체 스택 서술 신설 없음: reveal.js 2→2, "HTML 덱" 0→0 재확인)은 양쪽 일치. 모순 아님(하단 INFO).

**P8. audit_v1 보존** — `cmp audit.md audit_v1.md` → 바이트 동일. 1회차 감사 기록이 두 이름으로 보존되었고 라운드 2에서 덮어쓰이지 않음(mtime 00:04:47, 문서 수정 3건보다 이전).

## Iteration Quality Note

**회귀 없음 — 라운드 2는 순증(strict improvement).** audit_v1 시점 대비:

- 제품 트리: 무접촉 입증(3중 증거) — 1회차 PASS 상태 그대로 보존. 악화 지점 0.
- 문서: 지시된 4건(#1·#2·#3·#7)이 전부 정확히 반영됐고, 반영 과정에서 신규 오류 유입 없음 — 라운드 2가 추가한 서술의 사실 주장(diff 집합 동일, 488줄, VERBATIM MATCH, render.md:34, 17/40/35, Marp 11→11)을 전수 재현해 전부 사실로 확인. 특히 #3은 참조 링크 → 전문 전재로 스펙 §7-2 충족도가 실질 상승(1회차의 "첨부로 실질 충족" 우회가 불필요해짐), 축3도 anchor 결손("전부 목록화" 미달)이 해소됨.
- 1회차보다 나빠질 뻔한 유일 경로(제품 재편집·audit_v1 덮어쓰기·전재 스냅샷 불일치)는 전부 프로브로 배제됨.
- 단, P5의 게이트 통계표 부정확(5행)은 **라운드 2가 만든 회귀가 아니라 1회차부터 존재하던 미발견 결함**이다(해당 표는 1회차 산출이며 audit_v1은 §1 표의 줄 수를 실측 대조하지 않았음 — audit_v1 노트 #3은 §2만 다룸). 중간 회차 산출이 최종보다 나은 지점은 없다.

## 품질 축 채점 (§6-3 앵커, 판정 로직 동일)

| 축 | 가중 | 점수 | 근거 (재현 증거) |
|----|------|------|------------------|
| 원형 충실도 | 2× | **5** | 라운드 2 제품 편집 0건(mtime 0건 + diff 집합 24+1 동일 + 카나리) — 1회차 5점 상태 불변. R7 3구간 verbatim 독립 재확인(P3), 무작위 무변경 2파일 바이트 동일 |
| 최신성 정확도 | 2× | **5** | 제품 불변이므로 1회차 검증 상태 유지 + 직접 재확인: `-preview` 0건, `Task` 0건, openai.md GA ID·Imagen 종료 문구 원상(스팟), 게이트 고지 수치(17/40/35) 실측 일치 |
| 생태계 정합성 | 1× | **5** | 1회차 4점의 유일 결손(render.md:34 미목록)이 upgrade-notes.md:153 행 추가로 해소 — 실물(render.md:34) 대조 정확. 포인터-헤딩 정합 0건 불일치(P2), 검증 로그 # 참조 무결(P4), 신규 끊어진 참조 유발 요인 없음(제품 불변) |
| 저장소 규칙 준수 | 1× | **5** | 10/10 name/description/version 재확인(§3-5 정확 일치), SKILL.md 전부 ≤500(최대 488), frontmatter YAML 27/27 파싱 유효(P1), upgrade-notes §2 고정 스키마 4섹션 유지(행 추가가 스키마·기존 인용 행번호를 깨지 않음) |

판정: 2× 축 ≥4, 1× 축 ≥3, 재실행 검증 전부 통과 → **PASS**.

## Blocking Issues

없음.

## Non-Blocking Notes

1. **MED-LOW** — Where: human-gate-diff-summary.md:9,12,14,15,18 (§1 통계표). Actual: 추가/삭제 줄 수 5행이 실측과 불일치 — curriculum "-9"(실측 -10), slide-reviewer "-4"(실측 -7), image-gen "+29/-26"(실측 +30/-27), self-study "-1"(실측 -2), remotion "-93"(실측 -131; 606→488 순감 -118이므로 -93은 산술적으로 불가). Expected: 실측값. 성격: 1회차부터 존재한 요약 통계 오류(라운드 2 무관·라운드 2 범위 밖). 변경 파일 수·백로그 코드·신규 131줄·매핑표 전문(실질 승인 근거)은 전부 정확하므로 차단 아님. Fix direction: **사람 게이트 제시 전 5개 셀 정정 권고** — 사용자 승인 문서의 수치 정확성 문제이므로 다음 문서 수정 기회에 우선 반영.
2. **INFO** — audit_v1 "Marp 9→9" vs generator_report "Marp 11→11": 계수 단위 차이(행 수 vs 발생 수)로 양쪽 모두 각자 기준에서 정확(P7 재계수). 실질 결론(Δ=0) 동일 — 정정 불요, 기록 목적.
3. **INFO** — upgrade-notes 검증 로그 #8(OpenRouter 교차 확인)은 본문 매핑 행에서 참조되지 않는 정의-전용 행 — §3-3 보조 절차의 이행 증거로서 존재 자체가 목적이므로 무결성 문제 아님.
4. **INFO** — 산출 루트 `.DS_Store` 1건(제품 트리 밖, Finder 부산물). 제품 skills/·resources/ 내부는 0건. frentis 반영 시 복사 대상에서 자연 제외될 위치이나, 저장소 커밋 시 .gitignore 대상.
5. **INFO** — `audit.md`와 `audit_v1.md`가 바이트 동일 중복(1회차 산출의 이중 보존). 혼동 방지를 위해 최종 정리 시 하나로 정리해도 무방 — 본 감사는 지시대로 어느 쪽도 수정하지 않음.

## Recommended Next Focus (FAIL 시만)

해당 없음 (PASS). 게이트 제시 전 Non-Blocking #1의 5개 셀 정정만 권고.
