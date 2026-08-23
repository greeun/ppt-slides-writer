# 사람 게이트 자료 — frentis 10-스킬 원형 유지 고도화 (2026-08-17)

승인 대상 산출: `ppt-slides-writer/skills/` 10개 스킬 + `resources/ai-slop-checklist.md` + `upgrade-notes.md`

## 1. 스킬별 diff 통계

| 스킬 | 변경 파일 수 | 추가/삭제 줄 | 백로그 근거 코드 |
|------|------------|-------------|-----------------|
| curriculum-builder | 8 (SKILL.md, structure-rules.md, workflows 6) | +10 / -10 | B5, B7, C8, C11, A1 |
| slide-builder | 2 (SKILL.md, workflows/schema.md) | +2 / -2 | B5, C8, A1 |
| remotion-slide-builder | 4 변경 + 신규 1 (references/layout-library.md, 131줄) | +13 / -131 (+신규 131줄) | C8, R7, A3, C11 |
| slide-reviewer | 1 (SKILL.md) | +7 / -7 | C8, C11, C10 |
| diagram-builder | 1 (SKILL.md) | +1 / -1 | B5, C8 |
| image-gen | 3 (SKILL.md, generate.py, references/openai.md) | +30 / -27 | C8, A2 (A4 확인 0건) |
| pdf-builder | 1 (SKILL.md) | +1 / -2 | B5, C8 |
| doc-converter | 1 (SKILL.md) | +13 / -12 | B7, C8, B6 (B5: haiku 핀 유지) |
| example-builder | 2 (SKILL.md, workflows/example-build.md) | +6 / -5 | B7, C8 |
| self-study-assistant | 1 (SKILL.md) | +2 / -2 | B5, C8, C10 |
| resources/ai-slop-checklist.md | 0 (verbatim 복사) | 0 / 0 | D |

(3회차 정정: 줄 수 재실측, audit_v2 반영)

- 전체: 변경 24개 파일 + 신규 1개(layout-library.md). 파일 삭제 0건.
- 검증 1~9 자체 점검 전부 PASS (상세: generator_report.md).
- 고지: 스펙 §2/§4의 파일 개수 라벨(curriculum 20 / remotion 34 / pdf-builder 29)은 Planner 산술 오류로 확인됨 — 실제 17/40/35 (audit_v1 판정 (a)). 트리 전체 verbatim 복사 방식이라 작업 결과에 영향 없음 (승인 항목 아님, 투명성 고지).

## 2. 스킬별 변경 매핑표 전문

(아래는 `../upgrade-notes.md` "스킬별 변경 매핑" 섹션의 verbatim 전재 — 전 변경 행이 백로그 코드·검증 출처와 함께 기재됨. A1/A2/A3 행은 검증 로그 # 대응.)

### image-gen (v1.0.0)

| 파일 | 변경 내용 | 백로그 근거 | 검증 출처 |
|------|----------|------------|----------|
| SKILL.md | frontmatter `version: 1.0.0` 추가 | C8 | — |
| SKILL.md | 프로바이더 선택 표: "Imagen 4 기반이 자연스러움" → 나노바나나 계열 근거로 교정 + Imagen 4 종료(2026-08-17) 명기; "14종 비율 네이티브 지원" → 세대 구분(3.1 계열 10종/2.5 레거시 14종) 명기 | A2 | 검증 로그 #2, #3 |
| SKILL.md | 모델 선택 표: `lite`(나노바나나 2 Lite, $0.0336/1K) 행 추가, 날짜 "2026-05" → "2026-08" | A2 | 검증 로그 #2, #4 |
| SKILL.md | 지원 비율: 3.1 계열 10종/2.5 레거시 14종 세대 구분 명기, 배너·세로 극단 행에 "(2.5 레거시 전용)" 부기. 21:9 슬라이드 권장 문구 유지 | A2 | 검증 로그 #2 |
| SKILL.md | 비용 예시 날짜 "2026-05" → "2026-08" (수치는 재검증 결과 원본과 동일 — 재계산 확인: 10×$0.039=$0.39, 10×$0.067=$0.67, 10×$0.052=$0.52, 10×$0.165=$1.65, 2×$0.165+8×$0.052=$0.746→$0.75, 2×$0.165+8×$0.067=$0.866→$0.87) | A2 | 검증 로그 #4, #10 |
| generate.py | `MODELS`: `"3.1"` → `gemini-3.1-flash-image`, `"pro"` → `gemini-3-pro-image`(GA ID), `"lite": ("gemini", "gemini-3.1-flash-lite-image")` 추가; `--model` help에 lite 반영; 가격 주석 날짜 2026-05→2026-08 + lite 가격 줄 추가($0.0336/Batch $0.0168). 함수 로직·인자 체계 불변 | A2 | 검증 로그 #2, #4 |
| references/openai.md | 날짜 표기 3곳(2026-05-01 확인→2026-08-17, 라인업 2026-05→2026-08, per-image 2026-05→2026-08) 갱신. 가격 수치는 재검증 결과 원본과 전부 일치(변경 0) | A2 | 검증 로그 #7, #10, #11 |
| references/openai.md | Gemini 비교 표: "Imagen 4 기반" → 나노바나나 계열 근거 교정 + 종료 명기, "14종" → 세대 구분 명기 | A2 | 검증 로그 #2, #3 |
| references/openai.md | Gemini 정확 가격 표: `-preview` ID 6행 → GA ID, Imagen 4 행 3개 삭제 + 종료 안내 1줄 추가, 날짜 2026-05→2026-08 | A2 | 검증 로그 #2, #3, #4 |

- `VALID_GEMINI_RATIOS` 14종 리스트 유지 근거: 2.5 레거시 슈퍼셋 검증용 (3.1 계열 10종은 이 리스트의 부분집합이므로 유효 입력을 차단하지 않음). 로직 불변 원칙(§4)에 따라 유지.
- gpt-image-2-mini 존재 확인 결과: 미존재 — gpt-image-1-mini가 현행 mini임을 확인, `gpt2-mini` 매핑 유지 (검증 로그 #6).
- description(C9): 트리거 "나노바나나로"·"gpt-image-2" 현행 확인(검증 로그 #2, #5) — 변경 불요.
- A4 관련: OpenAI 장당 가격이 원본 값과 전부 일치하여 가격 "수치" 변경은 0건, 날짜 표기와 모델 ID만 갱신됨.

### remotion-slide-builder (v1.0.0)

| 파일 | 변경 내용 | 백로그 근거 | 검증 출처 |
|------|----------|------------|----------|
| SKILL.md | frontmatter `version: 1.0.0` 추가 | C8 | — |
| SKILL.md → references/layout-library.md | 3개 섹션 verbatim 이동(바이트 동일 확인): ① `## 레이아웃 컴포넌트 라이브러리` 전체(2,761자) ② `## 컴포넌트 업데이트 메모` 전체(482자) ③ Phase 5 내부 `### 표준 레이아웃 패턴`+`### 카드 내부 공통 구조`(895자). 각 원위치에 1~2줄 포인터, "상세 레퍼런스" 표에 layout-library.md 행 1개 추가. 이동 후 SKILL.md 488줄(≤500) | R7 | 이동 전후 substring 대조 PASS |
| templates/package.json | caret 하한 갱신(동일 메이저 내, 버전 문자열만): @remotion/cli·fonts·transitions·remotion `^4.0.0`→`^4.0.512`, react `^19.0.0`→`^19.2.8`, @types/react `^19.0.0`→`^19.2.18`. pdf-lib `^1.17.1` 유지(현행 1.17.1), typescript `^5.7.0` 유지(현행 7.0.2 상위 메이저 — 개선 제안 기록) | A3 | 검증 로그 #9 |
| references/information-architecture.md | 14행 `.claude/skills/remotion-slide-builder/references/lo-as-slide-source.md` → `lo-as-slide-source.md` (동일 폴더 상대형) | C11 | — |
| references/lo-as-slide-source.md | 7행 `.claude/skills/remotion-slide-builder/references/information-architecture.md` → `information-architecture.md` | C11 | — |

- A4: "AI 모델명/가격 최신성 검증" 섹션의 OpenRouter 스니펫은 원문 유지 — 갱신할 예시 출력이 원본에 없어 변경 0건.
- allowed-tools는 이미 `Agent` 표기 — B7 변경 불요.

### slide-reviewer (v0.2.0)

| 파일 | 변경 내용 | 백로그 근거 | 검증 출처 |
|------|----------|------------|----------|
| SKILL.md | frontmatter `version: 0.1.0` → `0.2.0` | C8 | — |
| SKILL.md | 94행 `(.claude/skills/remotion-slide-builder/references/review-rules.md)` → `(../remotion-slide-builder/references/review-rules.md)` | C11 | — |
| SKILL.md | 109·142·160행 `.claude/resources/ai-slop-checklist.md` 3곳 → `../../resources/ai-slop-checklist.md` | C11 | — |
| SKILL.md | 디자인 체크리스트 2개 항목 옆에 기존 수치 기준 연결 구절 추가(기존 문장 유지): "텍스트가 충분한가" ← slide-builder 분량 가이드라인(6줄 이내·불릿 3~5개), "정보가 넘치지 않는가" ← 동일 기준 초과 + remotion 최소 폰트 20px | C10 | — |

### curriculum-builder (v1.0.0)

| 파일 | 변경 내용 | 백로그 근거 | 검증 출처 |
|------|----------|------------|----------|
| SKILL.md | frontmatter `model: sonnet` 줄 삭제 | B5 | — |
| SKILL.md | allowed-tools `Task` → `Agent` | B7 | — |
| SKILL.md | `version: 1.0.0` 추가 | C8 | — |
| SKILL.md | 132행 `(.claude/skills/remotion-slide-builder/references/lo-as-slide-source.md)` → `(../remotion-slide-builder/references/lo-as-slide-source.md)` | C11 | — |
| references/structure-rules.md | 280행 팩트체크 예시 갱신: 역전된 구 예시("Sonnet 5 → 실제 Sonnet 4.6") 대신 "세대 명칭을 추측 기재하지 않고 작성 시점 공식 라인업 확인" 취지 유지 + 2026-08 현행 라인업(Claude 5 패밀리: Fable/Opus/Sonnet 5, Haiku 4.5) 예시로 교체 | A1 | 검증 로그 #1 |
| workflows/ 6개 파일 | frontmatter allowed-tools `Task` → `Agent` (각 1곳: catalog-create, curriculum-create, literature-review, lo-enrichment, research-project, session-plan) | B7 | — |

- workflows/session-plan.md:178의 `` `.claude/skills/curriculum-builder/templates/curriculum-delivery.md` ``는 워크플로우 실행 시 프로젝트 루트 기준으로 Read되는 런타임 템플릿 경로로 판단, §3-8 런타임 경로 유지 규칙에 따라 원문 유지 (§4 C11 목록에도 미포함). staging 치환 검증 시 대상 파일 존재 확인됨.
- SKILL.md:36 및 references/structure-rules.md:51의 "2026-05-09"는 가격·모델 스냅샷 날짜가 아닌 정책 개정 이력 날짜 — 날짜 통일(S7 규칙 2) 대상 아님, 원문 유지.

### slide-builder (v1.0.0)

| 파일 | 변경 내용 | 백로그 근거 | 검증 출처 |
|------|----------|------------|----------|
| SKILL.md | frontmatter `model: sonnet` 줄 삭제 | B5 | — |
| SKILL.md | `version: 1.0.0` 추가 | C8 | — |
| workflows/schema.md | 161행 코드 예시 `model="claude-sonnet-4-5-20250929"` → `model="claude-sonnet-5"` | A1 | 검증 로그 #1 |

### diagram-builder (v1.0.0)

| 파일 | 변경 내용 | 백로그 근거 | 검증 출처 |
|------|----------|------------|----------|
| SKILL.md | frontmatter `model: sonnet` 줄 삭제 | B5 | — |
| SKILL.md | `version: 1.0.0` 추가 | C8 | — |

- description의 "나노바나나" 통칭은 §3-2 확인 결과 현행 마케팅 명칭 — 변경 불요 (검증 로그 #2).

### doc-converter (v1.0.0)

| 파일 | 변경 내용 | 백로그 근거 | 검증 출처 |
|------|----------|------------|----------|
| SKILL.md | allowed-tools `Task` → `Agent` | B7 | — |
| SKILL.md | 본문 "Task tool 호출:" 4곳(요약/전체/추출/비전 폴백) → "Agent 도구 호출:" | B7 | — |
| SKILL.md | `version: 1.0.0` 추가 | C8 | — |
| SKILL.md | 청크 분할 기준 표 3행 수치 완화(표 구조·열 구성 유지): ~10페이지(chars<10,000)→~30페이지(chars<90,000), 11~30→31~90(30페이지씩), 31+→91+(30페이지씩, 병렬 서브에이전트 권장). 청크 추출 예시 `--pages` 나열을 30페이지 단위(0~29, 30~59)로 동기화. 근거: Haiku 4.5 200K 컨텍스트 기준 30페이지 ≈ 90K chars ≈ 30K 토큰은 단일 패스 안전 범위 | B6 | 검증 로그 #1 (Haiku 4.5 200K) |

- `model: haiku` 핀 및 서브에이전트 블록 내 `model: "haiku"` 4곳 유지 (B5 결정: 기계적 대량 처리형).

### example-builder (v1.0.0)

| 파일 | 변경 내용 | 백로그 근거 | 검증 출처 |
|------|----------|------------|----------|
| SKILL.md | allowed-tools `Task` → `Agent` | B7 | — |
| SKILL.md | 73행 "Task 서브에이전트로 Reviewer를 호출하여 검증." → "Agent 도구로 실행하는 서브에이전트로 Reviewer를 호출하여 검증." | B7 | — |
| SKILL.md | `version: 1.0.0` 추가 | C8 | — |
| workflows/example-build.md | frontmatter allowed-tools `Task` → `Agent`; 119행 "**Task 서브에이전트**로" → "**Agent 도구로 실행하는 서브에이전트**로"; 124행 `Task (subagent_type: general-purpose)` → `Agent (subagent_type: general-purpose)` | B7 | — |

### pdf-builder (v2.2.0)

| 파일 | 변경 내용 | 백로그 근거 | 검증 출처 |
|------|----------|------------|----------|
| SKILL.md | frontmatter `model: sonnet` 줄 삭제 | B5 | — |
| SKILL.md | `version: 2.1.0` → `2.2.0` (위치도 §3-5 규칙에 따라 name/description 다음 줄로 통일 — 원본은 frontmatter 말미) | C8 | — |

### self-study-assistant (v1.0.0)

| 파일 | 변경 내용 | 백로그 근거 | 검증 출처 |
|------|----------|------------|----------|
| SKILL.md | frontmatter `model: sonnet` 줄 삭제 | B5 | — |
| SKILL.md | `version: 1.0.0` 추가 | C8 | — |
| SKILL.md | 체크리스트 "적절한 깊이에서 멈추기" 항목 옆에 기존 수치 기준 연결 구절만 추가(문장 교체 없음): 공통 원칙 "기본 탐구 깊이: Level 2, 요청 시 Level 4까지" 괄호 참조 | C10 | — |

### 공유 리소스: resources/ai-slop-checklist.md

- 변경 0건 — 원본 verbatim 복사 (D). diff 대조 0건 확인.

### 공통 (C9)

- C9 점검 수행: 10개 전 스킬 description 검토 — 기능+트리거 병기 원칙 충족, description 내 모델명("나노바나나", "gpt-image-2")도 현행 확인(검증 로그 #2, #5). 변경 불요.

## 3. 대표 diff 발췌 3건

### ① image-gen 모델·가격 표 (A2 — Gemini GA ID·lite 행 추가·날짜 갱신)

```diff
-### 모델 선택 (2026-05 공식 가격, 정확값)
+### 모델 선택 (2026-08 공식 가격, 정확값)

 | `3.1` | Gemini | $0.067 (1K) | $0.067 (1K, 모든 비율) | 기본 품질, 사진/일러스트 |
+| `lite` | Gemini | $0.0336 (1K) | $0.0336 (1K, 모든 비율) | 나노바나나 2 Lite — 최저가, 1K 전용 |
```

generate.py `MODELS`: `gemini-3.1-flash-image-preview` → `gemini-3.1-flash-image`, `gemini-3-pro-image-preview` → `gemini-3-pro-image`, `lite` 매핑 추가. 가격 수치는 2026-08-17 재검증 결과 원본 값과 전부 일치하여 수치 변경 0건(날짜 표기·ID만 갱신), "(생성 시점 검증 필요)" 마킹 필요 셀 0건.

### ② remotion 500줄 이동 (R7 — 606줄 → 488줄)

```diff
-### 표준 레이아웃 패턴
-
-Polish 시 아래 패턴에 맞는지 확인한다. ... (표 7행)
-### 카드 내부 공통 구조
-... (코드 블록)
+> **표준 레이아웃 패턴 / 카드 내부 공통 구조**: `references/layout-library.md` 참조.
```

`## 레이아웃 컴포넌트 라이브러리`(2,761자)·`## 컴포넌트 업데이트 메모`(482자)·Phase 5 내부 2개 절(895자)을 `references/layout-library.md`로 **바이트 동일 이동**(substring 대조 PASS). 원위치 3곳에 포인터, "상세 레퍼런스" 표에 1행 추가.

### ③ Task→Agent 치환 예 (B7) + 청크 완화 (B6, doc-converter)

```diff
-allowed-tools: [Read, Write, Bash, Task, AskUserQuestion]
+version: 1.0.0
+allowed-tools: [Read, Write, Bash, Agent, AskUserQuestion]
 model: haiku          ← 유지 (B5 결정)

-| ~10페이지 (chars < 10,000) | 한번에 추출 → 서브에이전트 1회 |
-| 11~30페이지 | 10페이지씩 청크 분할 → 서브에이전트 N회 → 결과 합치기 |
-| 31페이지+ | 10페이지씩 청크 분할 → 서브에이전트 N회 → 결과 합치기 |
+| ~30페이지 (chars < 90,000) | 한번에 추출 → 서브에이전트 1회 |
+| 31~90페이지 | 30페이지씩 청크 분할 → 서브에이전트 N회 → 결과 합치기 |
+| 91페이지+ | 30페이지씩 청크 분할 → 서브에이전트 N회 → 결과 합치기 (병렬 서브에이전트 권장) |
```

본문 "Task tool 호출:" 4곳 → "Agent 도구 호출:", example-builder "Task 서브에이전트" 3곳 → Agent 도구 기준 표현. 잔존 `Task`(단어 단위) 전 스킬 0건.

## 4. 명시 승인 요청 항목

- (a) **변경 범위 전체** — 위 매핑표(upgrade-notes.md)의 전 변경 건
- (b) **신규 파일 1건** — `remotion-slide-builder/references/layout-library.md` (R7, verbatim 이동)
- (c) **doc-converter 청크 기준 30페이지 완화 수치** — chars<90,000 / 31~90 / 91+ (Haiku 4.5 200K 전제)

## 별첨: 개선 제안 (미적용)

`../upgrade-notes.md`의 "개선 제안 (미적용)" 표 참조 — typescript 상위 메이저(7.x), openai.md lite 행, 모델별 해상도 구분 명기 등 4건. 채택되더라도 본 산출물 반영이 아닌 후속 작업으로 분리.
