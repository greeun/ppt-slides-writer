# Skill Specification: frentis 10-스킬 원형 유지 고도화

## 1. 목적 & 절대 규칙

frentis-education의 강의 PT 제작 스킬 10종(`/Users/uni4love/project/workspace/216-frentis/frentis-education/.claude/skills/`)과 공유 리소스 `ai-slop-checklist.md`를 **도메인·구조·이름·워크플로우 무변형**으로 복제한 뒤, intake 백로그(A1~A4, B5~B7, C8~C11)에 해당하는 현대화 변경만 적용한 사본을 `ppt-slides-writer/` 아래에 생성한다. 이것은 신규 스킬 설계가 아니라 **기존 스킬의 제자리 고도화**이며, Generator의 모든 편집은 이 스펙 §4의 변경 항목 표에 열거된 것으로 한정된다.

### 절대 규칙 (위반 = 즉시 FAIL)

1. **변형 금지** — 교육 도메인 어휘(CAT/CU/LO/RE/LIT, vault, 합쇼체·격식체), 스킬 이름 10개, 폴더 구조, 워크플로우 Phase 구성·순서, 템플릿 구조, 컴포넌트 라이브러리 설계, 디자인 토큰 수치, 페르소나 구성, AI slop 블랙리스트 항목을 변경하지 않는다. 의미가 같아도 한국어 문장을 다시 쓰는 것(리라이팅)은 변형이다.
2. **Remotion 유지** — HTML 덱, reveal.js, Marp 등 다른 렌더 스택으로의 치환·제안 금지. Remotion 언급은 무손실 보존.
3. **병합 금지** — 10개 스킬 각각 독립 폴더 유지. 스킬 간 내용 이동 금지.
4. **원본 read-only** — frentis 원본 트리는 절대 수정하지 않는다. 검증 후 frentis 반영 여부는 사용자가 별도 결정한다.
5. **허용 diff 화이트리스트 원칙** — 원본 대비 모든 diff hunk는 §4 변경 항목 표의 행 하나와 대응해야 하며, 각 행은 아래 매핑 코드 중 하나를 근거로 가진다.

### 매핑 코드 정의

| 코드 | 의미 |
|------|------|
| A1 | 구세대 Claude 모델명 예시 갱신 |
| A2 | 이미지 프로바이더·모델·가격 재검증 및 매핑 갱신 |
| A3 | remotion templates/package.json 의존성 버전 확인·갱신 |
| A4 | 가격 조회 스니펫 등 검증 절차 유지 + 예시 출력 갱신 |
| B5 | frontmatter `model:` 핀 재조정 |
| B6 | doc-converter 청크 기준 완화 (대형 컨텍스트 전제) |
| B7 | allowed-tools·본문 도구명 현행화 (Task→Agent) |
| C8 | frontmatter `version:` 부여 (SemVer) |
| C9 | description 트리거 재점검 (구조 유지) |
| C10 | 모호 서술 옆 기존 수치 기준 연결 (이진 판정화) |
| C11 | 스킬 간·리소스 상호 참조 경로 상대화 |
| R7 | intake 검증 7·품질 축 4에서 직접 도출된 저장소 규칙 준수 조치 (SKILL.md ≤500줄) — remotion-slide-builder 1건에만 적용 |
| D | 유지 (변경 없음) |

R7은 intake 검증 10종 중 7번("SKILL.md 500줄 이하 전 스킬")과 품질 축 4("저장소 규칙 준수")가 백로그 A~C에 개별 항목으로 없어 별도 코드로 명문화한 것이다. 적용 대상은 remotion-slide-builder의 섹션 verbatim 이동 1건뿐이며, 그 외 어떤 변경도 R7을 근거로 삼을 수 없다.

## 2. 산출 디렉터리 레이아웃

산출 루트: `/Users/uni4love/project/workspace/211-withwiz/claude-utils/claude-skills/ppt-slides-writer/`

```
ppt-slides-writer/
├── skills/
│   ├── curriculum-builder/        ← 원본 트리 동일 (파일 20개)
│   ├── slide-builder/             ← 원본 트리 동일 (파일 6개)
│   ├── remotion-slide-builder/    ← 원본 트리 + references/layout-library.md 1개 추가 (근거 R7)
│   ├── slide-reviewer/            ← 원본 트리 동일 (파일 2개)
│   ├── diagram-builder/           ← 원본 트리 동일 (파일 9개)
│   ├── image-gen/                 ← 원본 트리 동일 (파일 6개)
│   ├── pdf-builder/               ← 원본 트리 동일 (파일 29개)
│   ├── doc-converter/             ← 원본 트리 동일 (파일 4개)
│   ├── example-builder/           ← 원본 트리 동일 (파일 2개)
│   └── self-study-assistant/      ← 원본 트리 동일 (파일 10개)
├── resources/
│   └── ai-slop-checklist.md       ← 원본 verbatim 복사 (변경 0)
└── upgrade-notes.md               ← 변경→백로그 매핑표 + 검증 로그
```

- `.DS_Store`는 복사하지 않는다 (OS 부산물, 스킬 구성 파일 아님 — upgrade-notes에 제외 근거 1줄 기록).
- 파일 추가는 `remotion-slide-builder/references/layout-library.md` 1건뿐. 파일 삭제는 0건.
- 이 레이아웃에서 스킬 폴더 기준 상대 경로 관계(`../<다른 스킬>/`, `../../resources/`)는 frentis 배포 레이아웃(`.claude/skills/<스킬>/`, `.claude/resources/`)과 동일하게 성립한다. C11 경로 상대화가 두 배치 모두에서 유효한 이유이다.

### upgrade-notes.md 형식 (고정 스키마)

```markdown
# Upgrade Notes — frentis 10-스킬 원형 유지 고도화 (생성일: YYYY-MM-DD)

## 검증 로그 (전역)
| # | 대상 | 조회 방법 | 조회일 | 출처 URL | 결과 요약 |

## 스킬별 변경 매핑
### <스킬명> (v<X.Y.Z>)
| 파일 | 변경 내용 | 백로그 근거 | 검증 출처 |

## 환경 의존 참조 (검증 제외 목록)
| 파일:행 | 참조 대상 | 사유 |

## 개선 제안 (미적용)
| 스킬 | 제안 | 미적용 사유 |
```

- "스킬별 변경 매핑"의 백로그 근거 열은 §1 매핑 코드만 사용한다.
- A1/A2/A3 근거 행은 검증 출처 열(URL 또는 검증 로그 # 참조)이 필수다.
- 변경이 없는 파일은 매핑표에 적지 않는다 (D는 §4에 스킬 단위로만 명시).

## 3. 전역 결정

### 3-1. Claude 모델 라인업 표기 기준 (웹 검증 완료, 2026-08-17)

- 현행 라인업: **Claude 5 패밀리 — Fable 5 (`claude-fable-5`), Opus 5 (`claude-opus-5`), Sonnet 5 (`claude-sonnet-5`) + Haiku 4.5 (`claude-haiku-4-5`)**.
- 코드 예시에는 `claude-sonnet-5`를 사용한다 (슬라이드 예시 코드 목적상 별칭 형태로 충분. 날짜 스냅샷 ID를 임의 추측해 적는 것 금지).
- 출처 (upgrade-notes 검증 로그에 기록):
  - https://platform.claude.com/docs/en/about-claude/models/overview
  - https://www.anthropic.com/news/claude-sonnet-5
- Generator는 생성 시점에 위 overview 페이지를 WebFetch로 재확인하고 조회일을 검증 로그에 기록한다.

### 3-2. 이미지 모델 표기 기준 (웹 검증 완료, 2026-08-17)

**Gemini (나노바나나 계열) — GA 전환이 핵심 변경.** 원본의 `-preview` 접미사 ID는 구식이다.

| 통칭 | 공식 모델 ID (현행) | 원본 표기 (구식) | 비고 |
|------|--------------------|-----------------|------|
| 나노바나나 2 | `gemini-3.1-flash-image` | `gemini-3.1-flash-image-preview` | GA (2026-05-28 출시). 512px/1K/2K/4K |
| 나노바나나 2 Lite | `gemini-3.1-flash-lite-image` | (원본에 없음 — 신규 추가) | GA. 최저가·1K 전용 |
| 나노바나나 Pro | `gemini-3-pro-image` | `gemini-3-pro-image-preview` | GA. 1K/2K/4K |
| 나노바나나 (레거시) | `gemini-2.5-flash-image` | 동일 | 유지 (레거시 명기) |

- 지원 비율: 3.1 계열은 10종(1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9)이며 극단 배너 비율(4:1, 8:1, 1:4, 1:8)은 2.5 전용이다. image-gen SKILL.md 비율 표에 이 세대 구분을 명기한다 (A2).
- Imagen 4 계열(imagen-4.0-*)은 2026-08-17 서비스 종료 — "Imagen 4 기반" 같은 근거 문구는 삭제·교정 대상 (A2).
- 출처: https://ai.google.dev/gemini-api/docs/image-generation , https://blog.google/innovation-and-ai/technology/developers-tools/build-with-nano-banana-2/ , https://ai.google.dev/gemini-api/docs/changelog

**OpenAI gpt-image 계열 — 원본 표기가 현행과 일치함을 확인.**

| 단축키 | 모델 ID | 상태 |
|--------|---------|------|
| `gpt2` | `gpt-image-2` | 현행 플래그십 (2026-04-21 출시) — 유지 |
| `gpt2-mini` | `gpt-image-1-mini` | 현행 mini — 유지 |
| `gpt1.5` | `gpt-image-1.5` | 직전 플래그십 — 유지 |
| `dalle3` | `dall-e-3` | deprecated 명기 유지 |

- 출처: https://openrouter.ai/openai/gpt-image-2 (모델 존재·현행성), 모델 카드 https://developers.openai.com/api/docs/models/gpt-image-2 (원본 기재 URL — Generator가 생성 시점 유효성 재확인)
- Generator 추가 확인 절차: 생성 시점에 `gpt-image-2-mini` 등 신형 mini 존재 여부를 OpenAI 모델 문서에서 확인하고, 존재하면 매핑 갱신 + 검증 로그 기록, 없으면 "gpt-image-1-mini가 현행 mini임을 확인" 1줄 기록.

### 3-3. 가격 검증 절차 (수치 동결 금지 — Generator가 생성 시점 실행)

가격 수치는 이 스펙에서 동결하지 않는다. Generator는 image-gen 스프린트에서 다음 절차를 실행한다:

1. **Gemini 가격**: `https://ai.google.dev/gemini-api/docs/pricing` WebFetch → 이미지 모델별 장당 가격 확보.
2. **OpenAI 가격**: `https://platform.openai.com/docs/pricing` WebFetch (실패 시 developers.openai.com 가격 문서) → gpt-image 계열 quality×size별 장당 가격 확보. 보조 교차 확인: `curl -s "https://openrouter.ai/api/v1/models"` (remotion-slide-builder에 이미 있는 스니펫과 동일 원리).
3. 확보한 수치로 image-gen SKILL.md 가격 표·비용 예시·generate.py 가격 주석·references/openai.md 가격 표를 갱신하고, 각 표의 날짜 표기를 "2026-05" → 생성 시점(YYYY-MM)으로 바꾼다.
4. 모든 수치는 upgrade-notes 검증 로그에 [조회일, URL, 값] 기록. **확인 불가 수치는 갱신하지 말고 해당 셀에 "(생성 시점 검증 필요)"를 마킹**한다. 추측 기재 절대 금지.

### 3-4. Remotion·의존성 버전 검증 절차 (A3)

1. `npm view remotion version && npm view @remotion/cli version && npm view react version && npm view typescript version && npm view pdf-lib version` 실행, 결과를 검증 로그에 기록.
2. **동일 메이저 내에서만** caret 하한 갱신 (예: `^4.0.0` → `^4.0.x` 최신 확인값). 현행이 상위 메이저(예: Remotion 5.x)면 **템플릿은 기존 메이저 유지**하고 upgrade-notes '개선 제안 (미적용)'에 기록만 한다 — 템플릿 코드(API 사용부)를 손대는 순간 변형이기 때문.
3. package.json 변경은 버전 문자열만 허용. scripts/의존성 목록 구조 불변.

### 3-5. version frontmatter 부여 규칙 (C8)

- 원본에 `version:` 없는 8개 스킬: **`1.0.0`** 부여 (최초 버전 스탬프).
- 원본에 있는 스킬: 이번 고도화는 기능 추가 성격이므로 **minor 상향** — pdf-builder `2.1.0` → `2.2.0`, slide-reviewer `0.1.0` → `0.2.0`.
- 표기: 따옴표 없는 SemVer(`version: 1.0.0`), name/description 다음 줄에 배치.

### 3-6. model: 핀 정책 (B5)

기준: **판단·설계형 스킬은 핀 제거(세션 강모델 상속), 기계적 대량 처리형만 하위 모델 유지.** 스킬별 확정은 §4. 요약:

| 스킬 | 원본 | 결정 |
|------|------|------|
| curriculum-builder | `model: sonnet` | 핀 제거 |
| slide-builder | `model: sonnet` | 핀 제거 |
| diagram-builder | `model: sonnet` | 핀 제거 |
| pdf-builder | `model: sonnet` | 핀 제거 |
| self-study-assistant | `model: sonnet` | 핀 제거 |
| doc-converter | `model: haiku` | **유지** (기계적 대량 처리 + 서브에이전트 haiku 위임 유지) |
| remotion-slide-builder, slide-reviewer, image-gen, example-builder | 핀 없음 | 유지 (변경 없음) |

`context: fork`는 전 스킬 유지 (B7 점검 결과 현행 유효 문법).

### 3-7. allowed-tools 정합화 규칙 (B7)

| 구식 표기 | 현행 표기 | 적용 위치 |
|-----------|-----------|----------|
| `Task` (frontmatter allowed-tools) | `Agent` | doc-converter, curriculum-builder(+workflows 6개), example-builder(+workflows 1개) |
| "Task tool 호출" / "Task 서브에이전트" / `Task (subagent_type: ...)` (본문) | "Agent 도구 호출" / "Agent 도구로 실행하는 서브에이전트" / `Agent (subagent_type: ...)` | doc-converter SKILL.md 4곳, example-builder SKILL.md 1곳 + workflows/example-build.md 2곳 |
| 그 외 도구명 (Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch, AskUserQuestion) | 변경 없음 | — |

서브에이전트 호출 블록 내부의 `model: "haiku"` 지정은 B5 결정에 따라 유지한다.

### 3-8. 경로 표기 규칙 (C11)

- **마크다운 상호 참조** (다른 스킬·resources를 가리키는 링크/안내): 스킬 폴더 기준 상대 경로로 교체 — `../<스킬명>/...`, `../../resources/...`. 같은 스킬 내부인데 `.claude/skills/` 절대형으로 쓴 참조는 동일 폴더 상대형으로 정리.
- **실행 명령 내 런타임 경로** (`python3 .claude/skills/<자기 스킬>/...`, typst `#import "/.claude/skills/..."`, `cp -r .claude/skills/...`): **원문 유지**. 이는 `.claude/` 배포 시점에 유효한 경로이며 변경 시 배포 호환성이 깨진다. Evaluator는 staging 검증 시 `.claude/skills/` 접두를 `ppt-slides-writer/skills/`로 치환해 대상 파일 존재만 확인한다.
- 스킬·서브에이전트·외부 자산 **이름 참조**(경로 아님: `web-researcher`, `pattern-analyzer`, `remotion-best-practices`, `duplicate-checker.py`, `course-materials`, vault 경로 `education/…`, `/Applications/draw.io.app` 등)는 원문 유지, 검증 제외 목록에 기록.

## 4. 스킬별 업그레이드 결정 (10개 각각 + 공유 리소스)

공통 (전 스킬, 이하 표에서 생략): SKILL.md frontmatter에 C8 규칙대로 `version:` 추가/상향. C9 재점검 결과 **10개 전 스킬 description 변경 0건으로 확정** — 기능+트리거 병기 원칙을 이미 충족하며, description 내 모델명(`gpt-image-2`, "나노바나나")도 §3-2 검증 결과 현행이다. upgrade-notes에 "C9 점검 수행, 변경 불요" 1줄 기록.

### curriculum-builder

- 파일 목록 (20개, 추가/삭제 없음): `SKILL.md`, `TODO.md`, `examples.md`, `reference.md`, `references/structure-rules.md`, `templates/{catalog.md, curriculum-delivery.md, curriculum-standard.md, curriculum.md, lo.md, session.md}`, `workflows/{catalog-create.md, curriculum-create.md, literature-review.md, lo-enrichment.md, research-project.md, session-plan.md}`
- 변경 항목 표:

| 파일 | 변경 내용 | 백로그 근거 |
|------|----------|------------|
| SKILL.md | frontmatter `model: sonnet` 줄 삭제 | B5 |
| SKILL.md | allowed-tools `Task` → `Agent` | B7 |
| SKILL.md | `version: 1.0.0` 추가 | C8 |
| SKILL.md 132행 | `(.claude/skills/remotion-slide-builder/references/lo-as-slide-source.md)` → `(../remotion-slide-builder/references/lo-as-slide-source.md)` | C11 |
| references/structure-rules.md 280행 | 팩트체크 예시 갱신: 원본 예시("Claude Sonnet 5"가 실제는 "Claude Sonnet 4.6")는 현행 사실과 역전되어 오도함. "세대 명칭을 추측으로 기재하지 않고 작성 시점 공식 라인업을 웹 검색으로 확인한다"는 취지를 유지하며 2026-08 기준 현행 라인업(Claude 5 패밀리: Fable/Opus/Sonnet 5, Haiku 4.5)을 예시로 교체 | A1 |
| workflows/ 6개 파일 | frontmatter allowed-tools `Task` → `Agent` (각 1곳) | B7 |

- model: 핀 결정 — **핀 제거**. 커리큘럼·LO 설계는 대화형 판단·설계 작업으로 세션 강모델 상속이 품질 우선.
- 유지 (D): 3계층 구조·명명 규칙·LO 규칙·시간표 규칙 전체, 워크플로우 6종 본문, 템플릿 6종, reference.md·examples.md·TODO.md, `disable-model-invocation: false`, LO 분량 수치 기준(2,000자/5,000자 — 이미 이진 판정 가능하므로 C10 불요), 서브에이전트 이름(web-researcher 등).

### slide-builder

- 파일 목록 (6개, 추가/삭제 없음): `SKILL.md`, `scripts/section-scanner.py`, `templates/{hub-template.md, section-template.md}`, `workflows/{patterns.md, schema.md}`
- 변경 항목 표:

| 파일 | 변경 내용 | 백로그 근거 |
|------|----------|------------|
| SKILL.md | frontmatter `model: sonnet` 줄 삭제 | B5 |
| SKILL.md | `version: 1.0.0` 추가 | C8 |
| workflows/schema.md 161행 | 코드 예시 `model="claude-sonnet-4-5-20250929"` → `model="claude-sonnet-5"` | A1 |

- model: 핀 결정 — **핀 제거**. 슬라이드 원고 구조 설계·콘텐츠 변환은 판단형.
- 유지 (D): 워크플로우 Phase 1~4, 분량 가이드라인 수치(분당 2장, 6줄, 불릿 3~5개 — 이미 수치화), 마크다운 컨벤션·레이아웃 타입 전체, 템플릿 2종, section-scanner.py 로직, `context: fork`, Marp/Quarto 렌더링 명령.

### remotion-slide-builder

- 파일 목록: 원본 34개 파일 전체 + **신규 `references/layout-library.md` 1개 추가** (근거 R7 — SKILL.md 606줄 > 500줄. 내용 삭제 없이 verbatim 이동으로만 해결).
- 변경 항목 표:

| 파일 | 변경 내용 | 백로그 근거 |
|------|----------|------------|
| SKILL.md | `version: 1.0.0` 추가 | C8 |
| SKILL.md → references/layout-library.md | 다음 3개 섹션을 **원문 그대로(verbatim, 리라이팅 금지)** 신규 파일로 이동: ① `## 레이아웃 컴포넌트 라이브러리` 전체(하위 절 포함) ② `## 컴포넌트 업데이트 메모` 전체 ③ Phase 5 내부 `### 표준 레이아웃 패턴` + `### 카드 내부 공통 구조` 2개 절. 각 원위치에 1~2줄 참조 포인터(`references/layout-library.md` 안내)를 남기고, "상세 레퍼런스" 표에 layout-library.md 행 1개 추가. 이동 후 SKILL.md ≤500줄 확인 | R7 |
| templates/package.json | §3-4 절차로 의존성 caret 하한 갱신 (동일 메이저 내) | A3 |
| references/information-architecture.md 14행 | `.claude/skills/remotion-slide-builder/references/lo-as-slide-source.md` → `lo-as-slide-source.md` (동일 폴더 상대형) | C11 |
| references/lo-as-slide-source.md 7행 | `.claude/skills/remotion-slide-builder/references/information-architecture.md` → `information-architecture.md` | C11 |

- model: 핀 결정 — **핀 없음 유지**. 원본이 이미 세션 상속 구조.
- A4 확인 사항: "AI 모델명/가격 최신성 검증" 섹션의 OpenRouter 스니펫은 원문 유지(갱신할 예시 출력이 원본에 없음 — 변경 0건임을 upgrade-notes에 명시).
- 유지 (D): 핵심 원칙(5초 룰, 격식체, 룰 승격 절차), 문체 상세·타이틀 규칙, LO-Remotion 동기화 규칙, 듀얼 소스 워크플로우, Phase 1~5 구성(이동 대상 3개 절 제외 본문), slide-lint 절차, 레이아웃 체크리스트 수치(20px, padding 32px 등 디자인 토큰), references 8종 본문(경로 2건 외), samples 11종, templates/src TSX·render-pdf.mjs·tsconfig·gitignore 전체, allowed-tools(이미 `Agent` 표기 — 현행).

### slide-reviewer

- 파일 목록 (2개, 추가/삭제 없음): `SKILL.md`, `references/personas.md`
- 변경 항목 표:

| 파일 | 변경 내용 | 백로그 근거 |
|------|----------|------------|
| SKILL.md | `version: 0.1.0` → `0.2.0` | C8 |
| SKILL.md 94행 | `(.claude/skills/remotion-slide-builder/references/review-rules.md)` → `(../remotion-slide-builder/references/review-rules.md)` | C11 |
| SKILL.md 109·142·160행 | `.claude/resources/ai-slop-checklist.md` (3곳) → `../../resources/ai-slop-checklist.md` | C11 |
| SKILL.md 디자인 체크리스트 | "텍스트가 충분한가 (빈 공간 과다 아닌지)" / "정보가 넘치지 않는가 (과밀 아닌지)" 두 항목 옆에 **기존 수치 기준 연결 구절만 추가** (문장 삭제·교체 금지): slide-builder 분량 가이드라인(슬라이드당 6줄 이내·불릿 3~5개) 및 remotion 최소 폰트 20px 기준을 괄호 참조로 연결 | C10 |

- model: 핀 결정 — **핀 없음 유지**. 리뷰는 판단형이며 원본이 이미 세션 상속.
- 유지 (D): 5개 페르소나 구성·평가 기준, P0~P3 우선순위 체계, 장표 단위 리뷰 절차, AI Slop 체크 항목, 스토리 아크·기술 과장 감지, 출력 형식, personas.md 전체, description(영문 위주 트리거 포함 — 원형).

### diagram-builder

- 파일 목록 (9개, 추가/삭제 없음): `SKILL.md`, `templates/{component-diagram, data-flow, deployment-diagram, system-architecture}.drawio`, `workflows/{arrows.md, layout.md, styles.md, tokens.md}`
- 변경 항목 표:

| 파일 | 변경 내용 | 백로그 근거 |
|------|----------|------------|
| SKILL.md | frontmatter `model: sonnet` 줄 삭제 | B5 |
| SKILL.md | `version: 1.0.0` 추가 | C8 |

- model: 핀 결정 — **핀 제거**. Draw.io XML 좌표·레이아웃 설계는 공간 판단형이며 대량 처리가 아님.
- 유지 (D): 도구 선택·자동 분기 규칙("나노바나나" 통칭 포함 — §3-2 확인 결과 현행 마케팅 명칭), Draw.io/Mermaid 워크플로우 전체, 디자인 토큰·색상 팔레트 수치, Quality Checklist, Anti-patterns, 출력 경로 표, .drawio 템플릿 4종, workflows 4종, `/Applications/draw.io.app` 경로(런타임 환경 의존 — 검증 제외 목록 기록).

### image-gen

- 파일 목록 (6개, 추가/삭제 없음): `SKILL.md`, `generate.py`, `references/{openai.md, prompt-guide.md, proposal-templates.md, visual-blocks.md}`
- 변경 항목 표:

| 파일 | 변경 내용 | 백로그 근거 |
|------|----------|------------|
| SKILL.md | `version: 1.0.0` 추가 | C8 |
| SKILL.md | 프로바이더 선택 표·모델 선택 표: Gemini ID를 §3-2 GA 표기 기준으로 갱신, `lite`(나노바나나 2 Lite) 행 추가, "Imagen 4 기반이 자연스러움" 근거 문구를 현행 사실로 교정(Imagen 계열 2026-08-17 종료), "2026-05 공식 가격" 날짜 표기를 생성 시점으로 갱신 | A2 |
| SKILL.md | 가격 표·비용 예시(10장 세트 계산 포함)를 §3-3 검증 절차 결과값으로 재계산·갱신. 검증 불가 셀은 "(생성 시점 검증 필요)" 마킹 | A2 |
| SKILL.md | 지원 비율 표: 3.1 계열 10종 / 2.5 레거시 14종(극단 배너 비율은 2.5 전용) 세대 구분 명기. 21:9 슬라이드 권장 문구는 유지 | A2 |
| generate.py | `MODELS` 매핑 갱신: `"3.1"` → `gemini-3.1-flash-image`, `"pro"` → `gemini-3-pro-image`, `"lite": ("gemini", "gemini-3.1-flash-lite-image")` 추가, `--model` help 문자열 동기화. 가격 주석 블록을 §3-3 결과로 갱신, "2026-05 기준" 주석 날짜 갱신. **함수 로직·인자 체계·VALID_GEMINI_RATIOS는 불변** (14종 리스트는 2.5 레거시 슈퍼셋 검증용으로 유지 — 근거를 upgrade-notes에 기록) | A2 |
| references/openai.md | 모델 표 현행성 재확인(§3-2 절차), 가격 표를 §3-3 결과로 갱신, Gemini 비교 표의 모델 ID를 GA 표기로 갱신, 모델 카드 URL 유효성 확인, 날짜 표기 갱신 | A2 |

- model: 핀 결정 — **핀 없음 유지**. 원본이 이미 세션 상속.
- 유지 (D): 톤 가이드 1~6단계 워크플로우 구조, guided/freestyle 모드 판단 표, 프롬프트 작성 원칙, web 모드, 사이드카 규약, references/{prompt-guide, proposal-templates, visual-blocks}.md 전체, allowed-tools, `context: fork`, description(트리거 "나노바나나로"·"gpt-image-2" — 현행 확인).

### pdf-builder

- 파일 목록 (29개, 추가/삭제 없음): `SKILL.md`, `references/{convert.md, render.md, typst-build.md}`, `templates/` 이하 25개 (.typ/.yml/.qmd.template/README.md)
- 변경 항목 표:

| 파일 | 변경 내용 | 백로그 근거 |
|------|----------|------------|
| SKILL.md | frontmatter `model: sonnet` 줄 삭제 | B5 |
| SKILL.md | `version: 2.1.0` → `2.2.0` | C8 |

- model: 핀 결정 — **핀 제거**. 빌드 실패 진단(Typst 오류·폰트·경로)은 판단형이고 단발 호출이라 하위 모델 비용 이득이 미미. intake 기준상 "기계적 대량 처리형"이 아님.
- 유지 (D): 렌더링 스택 이원 체계(Typst 단독/Quarto), frentis-base.typ 파라미터·옵션 조합 표, 절대 금지 사항, 에러 처리 표, references 3종, 템플릿 25종 전체, typst `#import "/.claude/skills/pdf-builder/..."` 런타임 경로(§3-8 규칙 — 유지), diagram-builder 연계 언급.

### doc-converter

- 파일 목록 (4개, 추가/삭제 없음): `SKILL.md`, `scripts/{extract_hwp.py, extract_pdf.py}`, `workflows/hwp.md`
- 변경 항목 표:

| 파일 | 변경 내용 | 백로그 근거 |
|------|----------|------------|
| SKILL.md | allowed-tools `Task` → `Agent` | B7 |
| SKILL.md | 본문 "Task tool 호출:" 4곳(요약/전체/추출/비전 폴백 블록) → "Agent 도구 호출:" | B7 |
| SKILL.md | `version: 1.0.0` 추가 | C8 |
| SKILL.md | 청크 분할 기준 표(3행) 수치 완화 — 표 구조·열 구성 유지, 값만 교체: ① `~30페이지 (chars < 90,000)` → 한번에 추출·서브에이전트 1회 ② `31~90페이지` → 30페이지씩 청크 ③ `91페이지+` → 30페이지씩 청크(병렬 서브에이전트 권장). 청크 추출 예시 명령의 `--pages` 나열도 30페이지 단위로 동기화. 근거: 대형 컨텍스트(Haiku 4.5 200K) 기준 30페이지(≈90K chars ≈ 30K 토큰)는 단일 패스 안전 범위 | B6 |

- model: 핀 결정 — **`model: haiku` 유지**. intake가 명시한 기계적 대량 처리형의 대표 사례. 서브에이전트 블록 내 `model: "haiku"` 지정 4곳도 유지. 서브에이전트 위임 아키텍처(컨텍스트 위생) 자체는 불변.
- 유지 (D): AI-Readable 재구성 철학, 아키텍처 다이어그램, 모드 3종, 서브에이전트 프롬프트 본문(도구명 표기 외), 파일 유형 표, 에러 처리, Configuration 블록(`default_model: haiku`, `extract_script` 런타임 경로 포함), Do/Don't, 스크립트 2종 로직, workflows/hwp.md(런타임 경로 포함).

### example-builder

- 파일 목록 (2개, 추가/삭제 없음): `SKILL.md`, `workflows/example-build.md`
- 변경 항목 표:

| 파일 | 변경 내용 | 백로그 근거 |
|------|----------|------------|
| SKILL.md | allowed-tools `Task` → `Agent` | B7 |
| SKILL.md 73행 | "Task 서브에이전트로 Reviewer를 호출하여 검증." → Agent 도구 기준 표현 | B7 |
| SKILL.md | `version: 1.0.0` 추가 | C8 |
| workflows/example-build.md | frontmatter allowed-tools `Task` → `Agent`; 119행 "**Task 서브에이전트**로 Reviewer를 호출한다" 및 124행 `Task (subagent_type: general-purpose)` → `Agent (subagent_type: general-purpose)` | B7 |

- model: 핀 결정 — **핀 없음 유지**. 원본이 이미 세션 상속 (코드 생성은 판단형).
- 유지 (D): labs/ 산출 구조, 시나리오 합의 우선·Maker-Reviewer 패턴, Phase 1~5, 검증 통과 기준 수치(키워드 80%, 6개월 이내 릴리즈 — 이미 이진 판정 가능), 금지 사항, argument-hint, `context: fork`.

### self-study-assistant

- 파일 목록 (10개, 추가/삭제 없음): `SKILL.md`, `templates/{code-analysis.md, concept-note.md, context-extraction.md, study-session.md}`, `workflows/{code-dissector.md, concept-explorer.md, context-extractor.md, examples.md, study-session.md}`
- 변경 항목 표:

| 파일 | 변경 내용 | 백로그 근거 |
|------|----------|------------|
| SKILL.md | frontmatter `model: sonnet` 줄 삭제 | B5 |
| SKILL.md | `version: 1.0.0` 추가 | C8 |
| SKILL.md 체크리스트 | "적절한 깊이에서 멈추기" 항목 옆에 기존 수치 기준 연결 구절만 추가(문장 교체 금지): 공통 원칙의 "기본 Level 2, 요청 시 Level 4까지" 기준을 괄호 참조로 연결 | C10 |

- model: 핀 결정 — **핀 제거**. 개념 분해·설명은 판단형.
- 유지 (D): Top-Down 철학·인용, 4대 기능 라우팅 표, Phase 1~3, 템플릿 4종·워크플로우 5종, 학습 기록 위치, DO/DON'T, 위키링크 참조.

### 공유 리소스: resources/ai-slop-checklist.md

- **변경 0건 — 원본 verbatim 복사** (근거 D). intake D가 "AI slop 블랙리스트 항목" 유지를 명시. 내부의 gstack 경로·외부 스킬명(design-guide-builder, frontend-design)은 원문 유지하고 검증 제외 목록에 기록.
- slide-reviewer가 `../../resources/ai-slop-checklist.md`로 도달 가능해야 함 (검증 5에서 확인).

## 5. 스프린트 계획 (Full tier)

**기본 방식: "verbatim 복사 후 편집".** Sprint 0에서 원본 트리를 그대로 복사해 두고, 이후 스프린트는 §4 표의 편집만 수행한다. 이 방식이 원형 충실도를 구조적으로 보장하고 diff 대조를 깨끗하게 만든다.

| 스프린트 | 범위 | 관찰 가능한 완료 체크 |
|----------|------|----------------------|
| S0 스캐폴드+전역 검증 | `rsync -a --exclude='.DS_Store'`로 10개 스킬 트리 + resources 복사, upgrade-notes.md 골격 생성, §3-1~3-4 검증 절차 실행·기록 | `diff -r 원본 산출` 결과 .DS_Store 외 0건; 검증 로그 표에 Claude/Gemini/OpenAI/npm 조회 행 존재 |
| S1 image-gen | §4 image-gen 표 전체 (A2 최대 작업) | 매핑표 작성 완료; `python3 -m py_compile generate.py` 통과; grep으로 `-preview` 접미사 0건; 가격 셀마다 출처 또는 마킹 존재 |
| S2 remotion-slide-builder | §4 표 전체 (R7 이동, A3, C11 2건) | `wc -l SKILL.md` ≤500; layout-library.md 내용 = 이동 전 원문과 diff 0(공백 제외); package.json 버전만 diff |
| S3 slide-reviewer + curriculum-builder | §4 두 스킬 표 (C11 상호 참조 집중, A1) | 상대 경로 4+1곳 해석 성공; structure-rules.md 팩트체크 예시에 현행 라인업 반영 |
| S4 slide-builder + diagram-builder | §4 두 스킬 표 (A1, B5) | schema.md에 `claude-sonnet-5`; 두 SKILL.md에서 `model:` 줄 부재 + `version:` 존재 |
| S5 doc-converter + example-builder | §4 두 스킬 표 (B6·B7 집중) | `grep -rn '\bTask\b'` 두 스킬 md에서 0건; 청크 표 신규 수치 반영 |
| S6 pdf-builder + self-study-assistant | §4 두 스킬 표 | version 2.2.0/1.0.0 확인; `model:` 줄 부재 확인 |
| S7 후처리+최종 검증 | 병렬 산출 서식 통일 + §6 검증 1~9 전체 재실행 + 사람 게이트 자료 생성 | 검증 1~9 전부 PASS; diff 요약 문서 생성 |

- 순서·의존성: S0이 전 스프린트의 전제(검증 로그를 S1~S6이 인용). S2를 S3보다 먼저 수행 권장(경로 검증 대상인 remotion 파일 상태 확정). S1~S6은 상호 독립이라 병렬 배정 가능하되, 병렬 시 S7 후처리는 생략 불가.
- 각 스프린트 종료 시 Evaluator가 해당 스킬 범위의 §6 검증을 수행하고 PASS 후 다음 스프린트로 진행.
- **병렬 생성 시 후처리 규칙 (S7)**: ① version 표기 형식 통일(따옴표 없음, name/description 다음 줄) ② 날짜 표기 통일(생성 시점 YYYY-MM 단일 표기) ③ upgrade-notes 매핑표 열 순서·용어 통일 ④ 도구명 잔존 최종 grep(`grep -rnw 'Task' skills --include='*.md'` → 0건) ⑤ 스킬 간 참조 grep 전체 재실행.

## 6. Evaluator 설계 (이 업그레이드 프로젝트의 QA)

Evaluator는 Generator와 별도 세션으로 실행하며, 산출물·원본·upgrade-notes 파일만 근거로 판정한다(대화 맥락 인용 금지 — 증거 기반 평가). 모든 지적에 파일:행 인용 필수.

### 6-1. 검증 체크 (intake 10종의 실행 절차)

| # | 검증 | 실행 절차 |
|---|------|----------|
| 1 | 트리 동일 구조 | `diff <(cd 원본/.claude/skills && find . -type f ! -name .DS_Store \| sort) <(cd 산출/skills && find . -type f ! -name .DS_Store \| sort)` — 허용 diff는 `remotion-slide-builder/references/layout-library.md` 1건뿐이며 upgrade-notes에 R7 근거 기록 확인. resources는 `diff 원본/.claude/resources/ai-slop-checklist.md 산출/resources/ai-slop-checklist.md` → 변경 0 |
| 2 | frontmatter 3필드 | 각 SKILL.md 첫 frontmatter 블록에서 `name:`/`description`/`version:` grep; name 값 = 폴더명 = 원본 name 동일 확인 (10/10) |
| 3 | diff→백로그 매핑 | 파일별 `diff -u 원본 산출` 전수 실행. 모든 hunk가 upgrade-notes 매핑표 행과 대응하는지 대조. 보조: `diff -rq` 변경 파일 목록 vs 매핑표 파일 열 — 매핑표에 없는 변경 파일 0건, 매핑표에 있는데 diff 없는 행 0건 |
| 4 | 검증 출처 기록 | 매핑표에서 근거가 A1/A2/A3인 모든 행의 검증 출처 열 비어 있지 않음 + 검증 로그의 URL이 §3 확정 출처와 부합 |
| 5 | 참조 경로 무결성 | md 파일에서 `grep -rnoE '\((\.\./\|\./)?[^() ]+\.(md\|py\|typ\|tsx\|json\|drawio)\)'` 및 인라인 코드 경로 추출 → 각 경로를 파일 위치 기준 해석해 존재 확인. `.claude/skills/` 접두 경로는 `산출/skills/` 치환 후 존재 확인. upgrade-notes '환경 의존 참조' 목록(vault 경로, 외부 스킬·서브에이전트명, /Applications 경로, gstack 경로, course-materials)은 제외. 끊어진 참조 0건 |
| 6 | Remotion 무손실 | 파일별 `grep -ci remotion` 산출 ≥ 원본 (전 파일); "HTML 덱"·"reveal.js"·"Marp" 로의 대체 서술 신설 0건 (`diff`에서 해당 어휘 추가 hunk 검사) |
| 7 | SKILL.md ≤500줄 | `for f in 산출/skills/*/SKILL.md; do wc -l "$f"; done` — 10개 전부 ≤500 |
| 8 | Python 문법 | `python3 -m py_compile` 4종: image-gen/generate.py, slide-builder/scripts/section-scanner.py, doc-converter/scripts/extract_pdf.py, doc-converter/scripts/extract_hwp.py — 모두 종료코드 0 |
| 9 | 도메인 어휘 보존 | 원본에서 `CAT`/`CU`/`LO`/`vault`/`합쇼체\|격식체`/`los/`가 등장하는 파일 목록을 만들고, 동일 파일의 산출본에서 동일 어휘 잔존 grep — 소실 0건 |
| 10 | 사람 게이트 | §7 절차 수행 (Evaluator는 자료 준비까지, 승인은 사용자) |

### 6-2. 원형 충실도 판정 규칙 (현대화 vs 변형)

**현대화(허용)로 판정하는 diff — 아래 9유형에 한정:**

1. §3·§4에 명시된 모델 ID·버전·가격·날짜 문자열 교체 (A1~A4)
2. Task→Agent 도구명 치환 (B7, §3-7 매핑표 범위)
3. doc-converter 청크 표 3행 수치 및 `--pages` 예시 동기화 (B6)
4. §3-6 대상 스킬의 frontmatter `model:` 줄 삭제 (B5)
5. `version:` 줄 추가/상향 (C8, §3-5 값과 일치할 때만)
6. §4에 명시된 상호 참조 경로 문자열 교체 (C11)
7. §4에 명시된 위치에 기존 수치 기준 연결 구절 **추가** (C10 — 기존 문장 삭제·교체가 동반되면 위반)
8. remotion 3개 섹션 verbatim 이동 + 포인터 + 레퍼런스 표 1행 (R7)
9. image-gen `lite` 단축키 행/매핑 추가 (A2)

**변형(위반)으로 판정하는 diff — 예시:**

- 워크플로우 Phase·Step의 추가/삭제/순서 변경, 표의 열 구성 변경
- 스킬명·파일명·컴포넌트명·Composition 규칙 변경, 스킬 병합·분리
- 문체 규칙(합쇼체)·디자인 토큰 수치·페르소나·AI slop 항목 변경
- Remotion 관련 서술 삭제 또는 타 스택 치환
- 허용 유형에 속하지 않는 한국어 문장 리라이팅 (의미가 같아도 위반)
- Python/TSX 코드 로직 변경 (모델명·주석 상수 외)
- §4에 없는 파일 추가·삭제

### 6-3. few-shot 앵커 (품질 축 4개 × score 1/3/5)

**축 1: 원형 충실도 (2×)**
- 5: 전 diff hunk가 §6-2 허용 9유형에 매핑됨. 예: schema.md는 모델 문자열 1곳만 diff, remotion SKILL.md는 이동·포인터·version만 diff.
- 3: 내용 손실은 없으나 허용 유형 밖 diff 존재. 예: doc-converter 철학 절의 문장 두 개가 동의어로 다시 쓰임 — 의미 동일하지만 백로그로 설명 불가.
- 1: 구조 훼손. 예: slide-builder Phase 4가 삭제되거나, remotion SKILL.md가 "HTML 렌더 대안" 절을 신설, 두 스킬이 한 폴더로 합쳐짐.

**축 2: 최신성 정확도 (2×)**
- 5: 모든 모델 ID가 §3 확정값과 일치(`gemini-3.1-flash-image`, `claude-sonnet-5` 등), 가격 셀마다 검증 로그 URL 대응 또는 "(생성 시점 검증 필요)" 마킹, 날짜 표기가 생성 시점으로 통일.
- 3: 모델 ID는 전부 정확하나 가격 일부가 출처 기록 없이 갱신됨, 또는 비용 예시 재계산이 표의 단가와 불일치.
- 1: `gemini-3.1-flash-image-preview` 등 구 ID 잔존, 존재하지 않는 추측 모델명(예: `gpt-image-3`) 기재, 팩트체크 예시가 여전히 "Sonnet 4.6이 최신" 취지.

**축 3: 생태계 정합성 (1×)**
- 5: 검증 5 grep 결과 끊어진 참조 0건. slide-reviewer→remotion·resources, curriculum→remotion 경로가 staging에서 실제 파일로 해석되고, 환경 의존 참조가 전부 목록화됨.
- 3: 경로 상대화는 수행됐으나 1건이 오타(`../remotion-slide-buider/`)로 미해석, 또는 외부 참조 1건이 목록 누락.
- 1: `.claude/resources/...` 구식 경로가 그대로 남아 staging에서 전부 끊김, layout-library.md 포인터가 잘못된 파일명을 가리킴.

**축 4: 저장소 규칙 준수 (1×)**
- 5: 10개 스킬 모두 name/description/version 존재, version 값이 §3-5 표와 정확히 일치, SKILL.md 10개 전부 ≤500줄, upgrade-notes가 §2 스키마 그대로.
- 3: version은 전부 있으나 pdf-builder가 2.1.0 그대로(상향 누락), 또는 SKILL.md 1개가 501~510줄.
- 1: version 미부여 스킬 3개 이상, remotion SKILL.md 600줄대 방치, upgrade-notes 매핑표 부재.

**판정 로직**: 2× 축(1·2) 어느 하나 <4 → FAIL. 1× 축(3·4) 어느 하나 <3 → FAIL. 검증 1~9 중 하나라도 미통과 → 점수와 무관하게 FAIL. FAIL 시 파일:행 인용 + 수정 지시를 담은 critique를 Generator에 반환.

### 6-4. ESCALATE 조건 (사용자 개입 요청)

1. 원본 파일이 §4 파일 목록과 불일치 (누락·신규 발견 — 원본이 스펙 작성 시점 이후 변동)
2. 생성 시점 웹 검증 결과가 §3 확정값과 모순 (예: gpt-image-2 문서 소멸, Gemini ID 재변경)
3. R7 지정 이동만으로 SKILL.md 500줄 충족 불가 (추가 이동·압축은 임의 결정 금지)
4. 동일 축 FAIL이 2회 반복 (Generator-Evaluator 루프 교착)
5. 변형 없이는 intake 검증을 통과할 수 없는 신규 케이스 발견

## 7. 사람 게이트

- **시점**: 단 1회 — S7 후처리 완료 + Evaluator 최종 PASS 직후, 작업 완료 선언 전.
- **형식**: 다음을 한 문서로 제시하고 사용자 승인을 받는다.
  1. 스킬별 diff 통계 표 (변경 파일 수 / 추가·삭제 줄 수 / 백로그 근거 코드 목록)
  2. upgrade-notes.md의 스킬별 변경 매핑표 전문
  3. 대표 diff 발췌 3건 — ① image-gen 모델·가격 표 ② remotion 500줄 이동(이동 전후 대비) ③ Task→Agent 치환 예
  4. 명시 승인 요청 항목: (a) 변경 범위 전체 (b) 신규 파일 layout-library.md 1건 (c) doc-converter 청크 기준 30페이지 완화 수치
- **처리**: 승인 → 완료 선언. 부분 반려 → 해당 항목만 재작업 후 게이트 재실행. frentis 원본 반영은 이 게이트와 별개의 사용자 결정이며 이 프로젝트 범위 밖.

## 8. 테스트 시나리오

### 정상 경로
S0~S7 순차(또는 S1~S6 병렬+S7) 실행 → 스프린트별 Evaluator PASS → 최종 검증 1~9 PASS → 사람 게이트 승인 → 완료. 산출: skills/ 10개 + resources/ 1개 + upgrade-notes.md.

### 엣지 1: 원본 파일 누락·변동 발견
Generator가 §4 파일 목록에 없는 원본 파일을 발견하거나 목록의 파일이 부재한 경우 — 해당 스킬 작업을 중단하고 ESCALATE(§6-4 조건 1). 임의로 목록을 보정해 진행하지 않는다. 다른 스킬 스프린트는 계속 진행 가능.

### 엣지 2: 원본에 이미 존재하는 끊어진 참조
외부 환경 의존 참조(vault 경로, course-materials, web-researcher/pattern-analyzer 서브에이전트, remotion-best-practices 스킬, duplicate-checker.py, gstack 경로 등)는 **수정하지 않고 원문 유지** + upgrade-notes '환경 의존 참조' 표에 기록. 이 범주 밖에서 원본 자체의 깨진 상호 참조가 발견되면(§4 C11 목록 외) 수정하지 말고 ESCALATE.

### 범위 외: 변형 요구 발견 시 처리
Generator가 작업 중 구조 개선 아이디어(스킬 통합, 워크플로우 재설계, 문장 개선, 상위 메이저 의존성 도입 등)를 발견하면 — **적용 금지**. upgrade-notes '개선 제안 (미적용)' 표에 [스킬, 제안, 미적용 사유="원형 유지 규칙"]으로 기록만 하고, 사람 게이트 문서에 별첨한다. 사용자가 게이트에서 채택하더라도 본 프로젝트 산출물에는 반영하지 않으며 후속 작업으로 분리한다.
