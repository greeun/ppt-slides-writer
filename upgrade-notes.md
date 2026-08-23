# Upgrade Notes — frentis 10-스킬 원형 유지 고도화 (생성일: 2026-08-17)

## 검증 로그 (전역)

| # | 대상 | 조회 방법 | 조회일 | 출처 URL | 결과 요약 |
|---|------|----------|--------|----------|----------|
| 1 | Claude 모델 라인업 | WebFetch | 2026-08-17 | https://platform.claude.com/docs/en/about-claude/models/overview | 현행 라인업: Fable 5(`claude-fable-5`), Opus 5(`claude-opus-5`), Sonnet 5(`claude-sonnet-5`), Haiku 4.5(`claude-haiku-4-5`, 스냅샷 `claude-haiku-4-5-20251001`). `claude-sonnet-5`는 API ID이자 별칭으로 유효. `claude-sonnet-4-5-20250929`는 레거시 표에만 존재 |
| 2 | Gemini 이미지 모델 GA ID | WebFetch | 2026-08-17 | https://ai.google.dev/gemini-api/docs/image-generation | GA 4종 확인: `gemini-3.1-flash-image`(512px/1K/2K/4K), `gemini-3.1-flash-lite-image`(1K 전용), `gemini-3-pro-image`(1K/2K/4K), `gemini-2.5-flash-image`(레거시). 3.1 계열 지원 비율 10종(1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9). 극단 배너 비율(4:1/8:1/1:4/1:8)은 현행 문서에 미기재(2.5 레거시 전용) |
| 3 | Gemini GA 일자·Imagen 종료 | WebFetch | 2026-08-17 | https://ai.google.dev/gemini-api/docs/changelog | `gemini-3.1-flash-image`·`gemini-3-pro-image` GA 2026-05-28, `gemini-3.1-flash-lite-image` GA 2026-06-30. `imagen-4.0-generate-001`/`-ultra-`/`-fast-` 2026-08-17 서비스 종료 (2026-06-15 공지) |
| 4 | Gemini 이미지 가격 | WebFetch | 2026-08-17 | https://ai.google.dev/gemini-api/docs/pricing | `gemini-3.1-flash-image`: 512px $0.045 / 1K $0.067 / 2K $0.101 / 4K $0.151 (출력 $60/1M tokens). `gemini-3.1-flash-lite-image`: 1K $0.0336 ($30/1M). `gemini-3-pro-image`: 1K·2K $0.134 / 4K $0.24 ($120/1M). `gemini-2.5-flash-image`: 장당 $0.039 (1290 tokens/장) |
| 5 | OpenAI gpt-image-2 모델 카드 | WebFetch | 2026-08-17 | https://developers.openai.com/api/docs/models/gpt-image-2 | 페이지 유효. 현행 플래그십, 기본 스냅샷 `gpt-image-2-2026-04-21` |
| 6 | OpenAI 신형 mini 존재 여부 | WebFetch | 2026-08-17 | https://developers.openai.com/api/docs/models | `gpt-image-2-mini` 미존재 — gpt-image-1-mini가 현행 mini임을 확인 (매핑 변경 불요) |
| 7 | OpenAI 이미지 가격 | WebFetch | 2026-08-17 | https://developers.openai.com/api/docs/pricing (platform.openai.com/docs/pricing 301 리다이렉트) | 토큰 단가 체계: `gpt-image-2` 이미지 출력 $30/1M (텍스트 입력 $5, 이미지 입력 $8), `gpt-image-1.5` $32/1M, `gpt-image-1-mini` $8/1M, `gpt-image-1` $40/1M. quality×size 장당 정가 표는 페이지에 미게시(계산기 안내) — 장당 표기 셀은 "(생성 시점 검증 필요)" 마킹 대상 |
| 8 | OpenAI 모델 존재 교차 확인 | Bash `curl -s https://openrouter.ai/api/v1/models` | 2026-08-17 | https://openrouter.ai/api/v1/models | gpt-image-2 상당 모델(created 2026-04-21) 존재 확인. 장당 가격 필드는 null — 가격 교차 검증 불가 |
| 9 | npm 패키지 버전 | Bash `npm view <pkg> version` | 2026-08-17 | npm registry | remotion 4.0.512, @remotion/cli 4.0.512, @remotion/fonts 4.0.512, @remotion/transitions 4.0.512, react 19.2.8, @types/react 19.2.18, typescript 7.0.2(상위 메이저 — 갱신 제외), pdf-lib 1.17.1 |
| 10 | OpenAI 장당(per-image) 가격 | WebFetch | 2026-08-17 | https://developers.openai.com/api/docs/guides/image-generation | quality×size 장당 가격 표 존재 확인. gpt-image-2: low $0.006/$0.005/$0.005, medium $0.053/$0.041/$0.041, high $0.211/$0.165/$0.165 (1024²/1024×1536/1536×1024 순). gpt-image-1.5: $0.009/$0.013/$0.013, $0.034/$0.050/$0.050, $0.133/$0.200/$0.200. gpt-image-1-mini: $0.005/$0.006/$0.006, $0.011/$0.015/$0.015, $0.036/$0.052/$0.052. **원본 기재값과 전부 일치 — 수치 변경 불요, 날짜 표기만 갱신** |
| 11 | OpenAI cached input 단가 | WebFetch | 2026-08-17 | https://developers.openai.com/api/docs/pricing | cached text input: gpt-image-2 $1.25, gpt-image-1.5 $1.25, gpt-image-1-mini $0.20 — 원본 기재값과 일치. Batch 50% 할인 명시 확인 |

- Gemini Batch 장당 셀(openai.md 비교 표·generate.py 주석): 가격 페이지가 Batch=표준의 50%를 명시(로그 #4: 3.1 $30/1M, lite $15/1M, pro 장당 $0.067·$0.12). 원본의 Batch 셀($0.022/$0.034/$0.050/$0.076 등)은 검증된 표준가의 50% 반올림과 일치하므로 유지.

- `.DS_Store`는 복사에서 제외함 (OS 부산물, 스킬 구성 파일 아님).
- 원본 트리 변동 없음 확인: 원본 최신 mtime 2026-06-21 (스펙 작성일 2026-08-17 이전), 2026-08-16 이후 수정 파일 0건.

## 스킬별 변경 매핑

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

## 환경 의존 참조 (검증 제외 목록)

| 파일:행 | 참조 대상 | 사유 |
|---------|----------|------|
| skills/remotion-slide-builder/SKILL.md:456 · slide-builder/SKILL.md:165 · curriculum-builder/SKILL.md:283 · curriculum-builder/workflows/lo-enrichment.md:151 | `web-researcher` 서브에이전트명 | 배포 환경의 에이전트 정의에 의존 (경로 아님) |
| skills/slide-builder/SKILL.md:148,166 · curriculum-builder/SKILL.md:284 | `pattern-analyzer` 서브에이전트명 | 배포 환경의 에이전트 정의에 의존 |
| skills/remotion-slide-builder/SKILL.md:457 | `remotion-best-practices` 스킬명 | 외부 스킬 이름 참조 |
| skills/curriculum-builder/SKILL.md:285 · workflows/curriculum-create.md:243 | `duplicate-checker.py` / `duplicate-checker` | vault 스크립트 의존 |
| skills/example-builder/SKILL.md:4,6,53 · workflows/example-build.md:49 · curriculum-builder/workflows/lo-enrichment.md:73,224~248 | `course-materials` 레포 | 외부 저장소 참조 |
| skills/diagram-builder/SKILL.md:111 | `/Applications/draw.io.app/Contents/MacOS/draw.io` | 런타임 로컬 앱 경로 |
| resources/ai-slop-checklist.md:4,186,187 | gstack 경로 (`scripts/resolvers/constants.ts`, `design-review/SKILL.md`) | 원본 유지 대상 외부 참조 |
| resources/ai-slop-checklist.md:6,165 | `design-guide-builder`, `frontend-design` 외부 스킬명 | 원본 유지 대상 외부 참조 |
| skills/pdf-builder/references/render.md:34 | `uv run .claude/scripts/lit-to-bib.py` | 외부 스크립트 — `.claude/scripts/` 접두로 §3-8 `.claude/skills/` 치환 규칙 밖, 배포 환경 스크립트에 의존 |
| skills/remotion-slide-builder/SKILL.md:18~21,284~285 등 | `<레이아웃 라이브러리 CU>/remotion/`, `education/deliveries/...` 등 vault 경로 | 사용자 vault 구조에 의존 |
| 각 스킬 실행 명령 전반 | `python3 .claude/skills/<자기 스킬>/...`, typst `#import "/.claude/skills/pdf-builder/..."`, `cp -r .claude/skills/...` 런타임 경로 | §3-8: `.claude/` 배포 시점 유효 경로 — 원문 유지 |
| 전 스킬 문서 내 산출물·vault 파일명 예시 (curriculum-builder의 `CU-주제.md`·`los/LO-제목.md`·`templates/문헌.md`·`delivery-registry.md`, image-gen의 `tone-guide.md`·`CLAUDE.md`·`.prompt.md`, remotion의 `Root.tsx`·`SLIDE_GUIDELINES.md`, slide-builder 템플릿의 `0-오프닝.md` 류, pdf-builder의 `typst-show.typ`·`hub.md`·`PR-*` 류, doc-converter hwp.md의 `extract_hwp.py` 이름 언급 등) | 스킬이 사용자 프로젝트/vault에 생성·참조하는 파일의 이름 패턴 (스킬 내부 상호 참조 아님) | 환경·산출물 의존. 기계 추출 시 미해석으로 표시되나 원본과 완전 동일 집합임을 대조 확인(신규 파손 0건) — 원문 유지 |

## 개선 제안 (미적용)

| 스킬 | 제안 | 미적용 사유 |
|------|------|------------|
| remotion-slide-builder | templates/package.json `typescript: ^5.7.0` — npm 현행 7.0.2로 상위 메이저 존재. 메이저 업그레이드는 템플릿 코드(API 사용부) 영향 가능 | 원형 유지 규칙 (§3-4: 상위 메이저는 기존 메이저 유지) |
| image-gen | references/openai.md의 "Gemini 정확 가격 (비교용)" 표에 `gemini-3.1-flash-lite-image` 행 추가 여지 | 스펙 §4 openai.md 변경 범위(모델 ID 갱신·가격 갱신·날짜 갱신)에 lite 행 추가가 명시되지 않음 — 원형 유지 규칙 |
| image-gen | 해상도 지원의 모델별 구분(512px는 3.1 전용, lite는 1K 전용, pro/2.5는 1K~4K)을 SKILL.md "지원 비율 / 사이즈"에 명기 여지. generate.py도 모델별 해상도 제한을 검증하지 않음 | 스펙 §4 변경 항목 외 (로직·표 구조 불변 원칙) — 원형 유지 규칙 |
| doc-converter | Configuration 블록 `default_model: haiku`는 유지했으나, 장기적으로 Haiku 세대 표기(4.5) 명시 여지 | 스펙 §4 변경 항목 외 — 원형 유지 규칙 |

## 사람 게이트 승인 기록

- 2026-08-18 사용자 승인 (승인 항목: 변경 범위 전체 / 신규 파일 layout-library.md / doc-converter 청크 30페이지). 루프 3회(audit_v1~v3) 전 회차 PASS 후 승인.
