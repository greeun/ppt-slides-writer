# Audit — frentis 10-스킬 고도화 (v3, 최종)

감사일: 2026-08-18. 감사자: Evaluator 3회차 (신규 세션, 1·2회차와 별도). 라운드 3의 위임 범위는 "audit_v2 Non-Blocking #1(게이트 통계표 5행 수치) 정정 — human-gate-diff-summary.md·generator_report.md 2개 문서만"이며, 본 감사는 ① 통계표 정정의 셀 단위 독립 재실측 ② 3회차 범위 봉쇄(그 외 파일 무접촉) 입증 ③ 최종 회귀 샘플 ④ v1→v3 발견 전수 추적(루프 종결) ⑤ 사람 게이트 준비 상태 최종 판정을 수행했다. generator_report의 자기신고는 신뢰하지 않고 전 수치를 명령 재실행으로 재현했다.

- 원본(read-only): `/Users/uni4love/project/workspace/216-frentis/frentis-education/.claude/skills/` + `.claude/resources/ai-slop-checklist.md`
- 산출: `/Users/uni4love/project/workspace/211-withwiz/claude-utils/claude-skills/ppt-slides-writer/{skills,resources,upgrade-notes.md}` + `skill-wizard-output/{generator_report.md,human-gate-diff-summary.md}`
- 기준선(미수정 보존): `skill-wizard-output/audit_v1.md`(mtime 2026-08-18 00:04:47), `audit_v2.md`(00:17:55)

## Verdict: PASS

판정 로직(스펙 §6-3): 2× 축(원형 충실도 5, 최신성 5) ≥4, 1× 축(생태계 5, 저장소 5) ≥3, 재실행 검증 전부 통과, 3회차 위임 범위 준수 입증, v2의 유일 정정 대상(통계표 5행)이 셀 단위 실측 일치로 해소 → **PASS**. v1→v3 전 발견이 종결 상태(해결 9 / 허용판정 6 / 잔존 허용 2 — 잔존 2건 모두 INFO·비차단)이며 회차 간 회귀 0건. **남은 단계는 사용자 승인(검증 10) 하나뿐이다.**

## 통계표 정정 검증

변경 24파일 전수를 두 계수법으로 독립 재실측했다: ① `diff -u | awk '/^\+/ && !/^\+\+\+/'`(+) · `'/^-/ && !/^---/'`(-) ② `git diff --no-index --numstat`. **24/24 파일에서 두 방법 완전 일치** (per-file 출력 전수 확인, MISMATCH 0건).

### per-skill 합산 (per-file 실측치의 수기 합산) vs 게이트 §1 표

| 스킬 | 본 감사 실측 | 게이트 표 (정정 후) | 셀 판정 | per-file 내역 |
|------|-------------|--------------------|--------|---------------|
| curriculum-builder | +10 / -10 | +10 / -10 | 일치 | SKILL 3/3, structure-rules 1/1, workflows 6×(1/1) |
| slide-builder | +2 / -2 | +2 / -2 | 일치 | SKILL 1/1, schema.md 1/1 |
| remotion-slide-builder | +13 / -131 | +13 / -131 (+신규 131줄) | 일치 | SKILL **5/123**, package.json 6/6, references 2×(1/1). 신규 layout-library.md `wc -l` = **131줄** 실측 일치 |
| slide-reviewer | +7 / -7 | +7 / -7 | 일치 | SKILL 7/7 |
| diagram-builder | +1 / -1 | +1 / -1 | 일치 | SKILL 1/1 |
| image-gen | +30 / -27 | +30 / -27 | 일치 | SKILL 9/7, generate.py 7/5, openai.md 14/15 |
| pdf-builder | +1 / -2 | +1 / -2 | 일치 | SKILL 1/2 |
| doc-converter | +13 / -12 | +13 / -12 | 일치 | SKILL 13/12 |
| example-builder | +6 / -5 | +6 / -5 | 일치 | SKILL 3/2, example-build.md 3/3 |
| self-study-assistant | +2 / -2 | +2 / -2 | 일치 | SKILL 2/2 |
| resources/ai-slop-checklist.md | 0 / 0 | 0 / 0 | 일치 | `cmp` IDENTICAL |

**11/11행 전 셀 일치.** 산술 정합 재확인: remotion SKILL.md 원본 `wc -l` **606줄** → 산출 **488줄** = 순감 -118 = +5-123 — v2가 반증했던 "-93" 불가 논리와 정확히 정합. audit_v2 P5 실측값·generator Round 3 재실측표와도 전 항목 일치(3자 독립 측정 수렴).

- **정정 고지 존재**: human-gate-diff-summary.md:21 `(3회차 정정: 줄 수 재실측, audit_v2 반영)` — 표 직후 배치 확인.
- **구 수치 소거**: 정정 대상 5행(curriculum -9, remotion -93, slide-reviewer -4, image-gen +29/-26, self-study -1) 전부 신값으로 교체됨 — 표 본문 직접 판독으로 확인(human-gate-diff-summary.md:9,11,12,14,18).
- **변경 파일 수 열 무손상**: `diff -rq --exclude='.DS_Store'` 재실행 → 변경 24파일 + Only-in 1건. 스킬별 분해(8/2/4+1/1/1/3/1/1/2/1)가 표와 완전 일치.
- **백로그 근거 코드 열 무손상**: 10행 전부 audit_v1 Diff 화이트리스트 대조표와 동일(B5·B7·C8·C11·A1 / B5·C8·A1 / C8·R7·A3·C11 / C8·C11·C10 / B5·C8 / C8·A2 / B5·C8 / B7·C8·B6 / B7·C8 / B5·C8·C10) — 3회차 편집이 이 열을 건드리지 않음.

## 3회차 범위 봉쇄 검증

3회차 위임은 "게이트 문서 §1 정정 + generator_report Round 3 절 추가"뿐이므로 그 외 어떤 파일의 변경도 FAIL 사유다. 네 갈래로 봉쇄를 입증했다.

**(1) mtime 프로브.** `find skills resources upgrade-notes.md -type f -newer skill-wizard-output/audit_v2.md` → **0건**. 제품 트리 최신 mtime 2026-08-17 23:32:10(self-study SKILL.md) — v2 기록값과 동일. skill-wizard-output 전 파일 mtime: audit_v1.md 00:04:47, audit_v2.md 00:17:55(둘 다 3회차 편집 이전 — 미변조), **human-gate-diff-summary.md 00:19:44·generator_report.md 00:20:25 두 건만 audit_v2 이후** — 3회차 수정 파일이 정확히 위임된 2개 문서뿐임이 파일시스템 수준에서 입증됨.

**(2) diff -rq 카나리.** 원본 vs 산출 skills → 변경 **24파일 + Only-in 1건**(layout-library.md) — v1·v2와 동일 집합(파일 목록 전수 대조).

**(3) 콘텐츠 카나리.** `cmp` ai-slop-checklist.md → **IDENTICAL(바이트 동일)**. `wc -l` remotion SKILL.md → **488줄(≤500)**. 무변경 파일 스팟체크 2건 `cmp` → `diagram-builder/templates/system-architecture.drawio`·`pdf-builder/references/typst-build.md` 모두 **BYTE_IDENTICAL**.

**(4) 기준선 보존.** `cmp audit.md audit_v1.md` → 바이트 동일(v2 P8 상태 유지). audit_v1·audit_v2 mtime이 3회차 편집(00:19:44)보다 앞서므로 미변조. 게이트 문서 내 간접 증거: v2가 인용한 행번호(:23 고지, :27 전재 안내)가 현재 :25·:29로 정확히 +2 이동 — §1에 정정 고지 1행+공행 1행만 삽입됐음을 방증하며, §2~§4는 무접촉.

추가로 **원본 read-only 준수 재확인**: 원본 트리에서 2026-08-17 이후 mtime 파일 10건은 **전부 `.DS_Store`**(Finder 열람 부산물, 콘텐츠 아님 — 스펙 §2 제외 대상). `.DS_Store` 제외 시 2026-06-22 이후 수정 콘텐츠 파일 **0건**, ai-slop-checklist.md mtime 2026-06-21 — v1의 git log 판정(최종 커밋 2026-06-21)과 정합. 원본 콘텐츠 무접촉(하단 INFO #2).

결론: 3회차 편집 = 위임된 2개 문서뿐. 범위 봉쇄 **PASS**.

## 최종 회귀 샘플

| 항목 | 실행 명령 | 실제 결과 | 상태 |
|------|----------|----------|------|
| 검증 2 (frontmatter 3필드) | awk로 첫 frontmatter 블록 추출, name=폴더명=원본 name 3자 대조 + description·version 존재 | 10/10 전부 OK — version = 1.0.0 ×8 / pdf-builder 2.2.0 / slide-reviewer 0.2.0 (§3-5 정확 일치) | PASS |
| 검증 7 (≤500줄) | `wc -l` 10개 SKILL.md | 100~488줄, 전부 ≤500 (최대 remotion 488) | PASS |
| 검증 8 (Python 문법) | `python3 -m py_compile` 4종 | generate.py / section-scanner.py / extract_pdf.py / extract_hwp.py 전부 EXIT=0. 감사가 생성한 `__pycache__` 제거 후 잔존 0 확인 | PASS |
| Task 잔존 | `grep -rnw 'Task' skills --include='*.md'` | **0건** (EXIT=1) | PASS |
| `-preview` 잔존 | `grep -rn -- '-preview' skills resources` | **0건** (EXIT=1) | PASS |
| 무변경 스팟체크 2건 | `cmp` (v2와 다른 파일 선정) | system-architecture.drawio·typst-build.md **BYTE_IDENTICAL** | PASS |
| 부산물 | `find` .DS_Store/`*.pyc`/`__pycache__`/`*.bak`/`*.orig`/`*~` in skills·resources | **0건** | PASS |

## 루프 종결 평가 (v1→v3 발견 전수 추적표)

| # | 발견 (회차) | 심각도 | 조치 회차 | 종결 상태 · 본 감사 확인 |
|---|------------|--------|----------|--------------------------|
| 1 | 검증 6 감소 "2건" 자기신고 오기 — 실제 3건 (v1 NB#1) | LOW | R2 | **해결** — generator_report.md:47·55 "(2회차 정정)" 표기, v2 검증 완료. 제품 무변경이므로 v3에서 사실관계 불변 |
| 2 | render.md:34 `uv run` 환경 의존 미기재 (v1 NB#2) | LOW | R2 | **해결** — upgrade-notes.md:153 행 존재, v2 실물 대조 완료. v3 mtime 프로브로 upgrade-notes 3회차 무접촉 확인 — 상태 유지 |
| 3 | 게이트 매핑표가 참조 링크 (v1 NB#3) | LOW | R2 | **해결** — v3 기계 재대조: upgrade-notes "스킬별 변경 매핑" vs 게이트 §2 awk 추출·공행 제외 `diff` → **86행 VERBATIM MATCH** (3회차 편집 후에도 전재 정합 유지) |
| 4 | layout-library.md 스캐폴딩 제목+안내 2행 (v1 NB#4) | INFO | — | **허용판정 종결** — R7 포인터 스캐폴딩 허용 범위 확정(v1), v2 무접촉 확인, v3 제품 봉쇄로 상태 불변 |
| 5 | openai.md "Imagen 4 기반" 교정·"14종" 세대 구분 (v1 NB#5) | INFO | — | **허용판정 종결** — §3-2 전역 지시 소급 확정(v1) |
| 6 | 극단 배너 비율 "(2.5 레거시 전용)" (v1 NB#6) | INFO | — | **허용판정 종결** — 모순 아닌 부재, §6-4-2 미해당 확정(v1) |
| 7 | 스펙 파일 개수 라벨 오류 17/40/35 (v1 NB#7·판정 (a)) | INFO | R2 | **해결** — 투명성 고지 게이트 문서 :25 잔존 확인(v3), 수치는 v2 실측 일치 |
| 8 | 자기신고 (b) 감소 열거 누락 (v1) | 판정 | R2 | **해결** — #1과 동일 건, 기록 정정으로 종결 |
| 9 | 자기신고 (c) session-plan.md:178 런타임 경로 유지 (v1) | 판정 | — | **동의 종결** — §3-8 예외 + 화이트리스트 우선(v1 확정) |
| 10 | 게이트 §1 통계표 5행 수치 불일치 (v2 NB#1) | MED-LOW | R3 | **해결** — 본 감사 24파일 재실측(2계수법 교차)으로 11행 전 셀 일치 확인 (위 정정 검증 절) |
| 11 | Marp 9 vs 11 계수 단위 차이 (v2 NB#2) | INFO | — | **허용판정 종결** — 행 수 vs 발생 수, 양쪽 각자 기준 정확(v2 P7) |
| 12 | 검증 로그 #8 정의-전용 행 (v2 NB#3) | INFO | — | **허용판정 종결** — §3-3 보조 절차 이행 증거로 존재 자체가 목적(v2 P4) |
| 13 | 산출 루트 `.DS_Store` 1건 (v2 NB#4) | INFO | — | **잔존 허용** — v3 재확인: 여전히 존재하나 제품 트리(skills/·resources/) 밖, 내부 0건. 커밋 시 .gitignore 권고 유지 |
| 14 | audit.md ↔ audit_v1.md 바이트 동일 중복 (v2 NB#5) | INFO | — | **잔존 허용** — v3 `cmp` 재확인 바이트 동일. 기록 보존 목적, 본 감사도 지시대로 미수정. 최종 정리 시 하나로 정리 무방 |

**미해결(open) 항목: 0건.** 잔존 2건(#13·#14)은 모두 명시적 허용판정을 받은 INFO로, 산출물 품질·게이트 승인에 영향 없음.

**Iteration Quality Note — 회차 간 회귀 0건.** 제품 트리는 R1 완료 시점(2026-08-17 23:32:10)에 동결된 채 3개 회차의 감사를 통과했고(v1 검증 1~9 전수 → v2 3중 무접촉 입증 → v3 4중 봉쇄), 문서는 회차마다 순증만 했다(R2: 기록 정정·환경 의존 행·전재·고지 / R3: 통계표 5셀 정정). 각 회차의 정정이 새 오류를 유입한 사례 없음 — R3가 추가한 사실 주장(재실측표 10행·SKILL.md 단독 +5/-123·정정 diff 5쌍)을 전수 재현해 전부 사실로 확인. 중간 회차 산출이 최종보다 나은 지점 없음. 유일한 발견 지연은 통계표 오류가 v1에서 미발견된 것(v2가 이미 "v1의 미실측 각도"로 규명)이며, 3회차 루프 안에서 발견→정정→독립 재검증까지 완결됐다.

## 사람 게이트 준비 상태

스펙 §7-2 요구 5요소를 게이트 문서(human-gate-diff-summary.md)에서 전수 확인:

| §7-2 요소 | 위치 | 본 감사 판정 |
|-----------|------|-------------|
| 1. 스킬별 diff 통계 표 (변경 파일 수/추가·삭제 줄/백로그 코드) | §1 (:7-19) | **충족** — 11행 전 셀이 본 감사 독립 실측과 일치 (v2의 유일 결손 해소) |
| 2. 매핑표 전문 | §2 (:27-144) | **충족** — upgrade-notes 원문과 86행 VERBATIM MATCH (v3 재대조) |
| 3. 대표 diff 발췌 3건 | §3 — ① image-gen(:148) ② remotion 이동(:160) ③ Task→Agent+B6(:173) | **충족** — 발췌 내용을 실제 diff와 대조: doc-converter 청크 표 3행·`--pages` 예시, image-gen 날짜·lite 행 전부 실제 diff 출력과 일치(충실성 스팟체크) |
| 4. 명시 승인 3항목 (a)(b)(c) | §4 (:193-195) | **충족** — 변경 범위 전체 / 신규 파일 1건 / 청크 30페이지 완화 |
| 5. 투명성 고지 | :25 (개수 라벨) + :21 (3회차 정정 고지) | **충족** — 수치 17/40/35는 v2 실측 일치 확인분 |

**게이트 문서는 스펙 §7-2를 결손 없이 충족한다. 본 감사 PASS로 남은 단계는 사용자 승인(검증 10) 하나다.** 부분 반려 시 해당 항목만 재작업 후 게이트 재실행(스펙 §7).

## 품질 축 최종 채점

| 축 | 가중 | 점수 | 근거 (재현 증거) |
|----|------|------|------------------|
| 원형 충실도 | 2× | **5** | 3회차 제품 편집 0건(mtime 0건 + diff -rq 24+1 동일 + 카나리 3종 + 스팟체크 2파일 바이트 동일) — v1의 5점 상태(전 hunk 허용 9유형, 106파일 바이트 동일, R7 verbatim)가 3개 회차 동안 동결 보존. 원본 read-only 준수 재확인(콘텐츠 파일 무변동) |
| 최신성 정확도 | 2× | **5** | `-preview` 0건·`Task` 0건 재현, 검증 2/7/8 전부 PASS, 게이트 통계·고지 수치가 전부 실측 일치 — 제품 불변이므로 v1 웹 스팟체크(GA ID·가격·라인업) 결과 유효 유지 |
| 생태계 정합성 | 1× | **5** | 제품·upgrade-notes 무변동으로 v2의 5점 상태(render.md:34 행 추가·포인터-헤딩 정합·로그 # 무결) 유지. 전재본 86행 재대조 일치로 문서 간 정합도 최종 확인 |
| 저장소 규칙 준수 | 1× | **5** | 10/10 name/description/version(§3-5 정확 일치) 재확인, SKILL.md 전부 ≤500(최대 488), 게이트 문서가 §7-2 스키마 결손 0, 부산물 0건 |

판정: 2× 축 ≥4, 1× 축 ≥3, 재실행 검증 전부 통과 → **PASS**.

## Blocking Issues

없음.

## Non-Blocking Notes

1. **INFO** — Where: generator_report.md:130. Actual: 3회차 무접촉 검증 자기신고 `find … -newer human-gate-diff-summary.md → 0건`은 최종 상태 기준으로는 부정확 — generator_report.md 자체(mtime 00:20:25)가 게이트 문서(00:19:44)보다 늦게 저장되어 1건이 매치됨. 자기 참조적 아티팩트(보고서 최종 저장 전에 실행된 명령)로, 제품·문서 봉쇄 결론 자체는 본 감사의 독립 프로브(audit_v2 기준 `-newer` 0건)로 별도 입증됨 — 영향 없음, 기록 목적.
2. **INFO** — 원본 트리 내 `.DS_Store` 10건의 mtime이 2026-08-17로 갱신되어 있음(Finder 열람 부산물 — 콘텐츠 파일은 `.DS_Store` 제외 시 2026-06-21 이후 변동 0건). 스펙 §1-4 read-only 규칙은 콘텐츠 기준으로 준수됨. 향후 감사에서 mtime 프로브 사용 시 `.DS_Store` 제외 필요(본 감사는 제외 후 판정).
3. **INFO** — 잔존 허용 2건 상태 유지: ① 산출 루트 `.DS_Store` 1건(제품 트리 밖 — 커밋 시 .gitignore) ② `audit.md`↔`audit_v1.md` 바이트 동일 중복(기록 보존 — 최종 정리 시 하나로 정리 무방). 둘 다 v2 판정 그대로, 게이트 승인에 무관.

## Recommended Next Focus (FAIL 시만)

해당 없음 (PASS). 루프 종결 — 사용자 승인(검증 10)으로 진행.
