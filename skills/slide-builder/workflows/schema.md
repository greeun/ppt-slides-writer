# 마크다운 슬라이드 컨벤션

## 섹션 파일 구조

```markdown
---
section: 1
title: 도입
duration: 15분
---

<!-- layout: title -->
# 발표 제목

## 부제목

<!-- key-message: 핵심 메시지 한 줄 -->
<!-- notes: 강사 노트. 실제 발화 내용. -->

---

<!-- layout: 1-column -->
# 두 번째 슬라이드

- 항목 1
- 항목 2

<!-- key-message: 이 슬라이드의 핵심 -->
<!-- notes: 설명 멘트 -->

---

# 세 번째 슬라이드

내용...
```

## 필수 규칙

| 요소 | 문법 | 비고 |
|------|------|------|
| 슬라이드 구분 | `---` | Marp/Quarto/Slidev 공통 |
| frontmatter | 첫 `---` 블록 | section, title, duration |
| 레이아웃 힌트 | `<!-- layout: type -->` | 슬라이드 시작 직후 |
| 핵심 메시지 | `<!-- key-message: ... -->` | **모든 슬라이드 필수** |
| 강사 노트 | `<!-- notes: ... -->` | 실제 발화 내용 |
| 이미지 프롬프트 | `<!-- image-prompt: ... -->` | 생성 이미지 필요 시 |

## 레이아웃 타입

### title — 타이틀

```markdown
<!-- layout: title -->
# 발표 제목

## 부제목 또는 발표자 정보

<!-- key-message: 이 발표의 핵심 주제 -->
<!-- notes: 인사, 자기소개, 발표 개요 안내 -->
```

### section — 섹션 구분 (간지)

```markdown
<!-- layout: section -->
# 섹션 제목

> 섹션 요약 한 줄

<!-- key-message: 이 섹션에서 다룰 핵심 -->
<!-- notes: 섹션 전환 멘트 -->
```

### 1-column — 단일 컬럼

```markdown
<!-- layout: 1-column -->
# 슬라이드 제목

### 소제목
- 항목 1
- 항목 2
- **강조 항목**

<!-- key-message: 핵심 메시지 -->
<!-- notes: 각 항목 설명 멘트 -->
```

### 2-column — 2단 비교

```markdown
<!-- layout: 2-column -->
# Before vs After

:::::: columns
::: left
### Before
- 수동 처리
- 높은 오류율
:::

::: right
### After
- 자동화
- 99.9% 정확도
:::
::::::

<!-- key-message: 변화의 핵심 -->
<!-- notes: 좌우 비교하며 설명 -->
```

### image-text — 이미지 + 텍스트

```markdown
<!-- layout: image-text -->
# AI Agent 아키텍처

![AI Agent 구조](assets/ai-agent.png)

- **Planner**: 계획 수립
- **Executor**: 실행
- **Evaluator**: 품질 평가

<!-- image-prompt:
  concept: AI Agent 구성 요소 간 연결 구조
  composition: horizontal flow diagram, left to right
  details: blue accent color, clean lines
  style: Corporate tech illustration, 16:9, no text
-->

<!-- key-message: Agent는 계획-실행-평가 루프 -->
<!-- notes: 다이어그램 요소 하나씩 설명 -->
```

### table — 표 중심

```markdown
<!-- layout: table -->
# 도구 비교

| 도구 | 장점 | 단점 |
|------|------|------|
| Marp | 간단, 빠름 | 레이아웃 제한 |
| Quarto | 유연, 강력 | 설정 복잡 |

<!-- key-message: 상황에 맞는 도구 선택 -->
<!-- notes: 각 행별로 설명 -->
```

### code — 코드 강조

```markdown
<!-- layout: code -->
# API 호출 예시

\`\`\`python
client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-sonnet-5",
    messages=[{"role": "user", "content": "Hello!"}]
)
\`\`\`

<!-- key-message: 3줄이면 AI 호출 완료 -->
<!-- notes: 라이브 코딩으로 보여주기 -->
```

### quote — 인용문

```markdown
<!-- layout: quote -->
# AI 시대의 교육

> "AI를 활용하는 교사가 그렇지 않은 교사를 대체한다."
>
> — 교육공학 저널, 2025

<!-- key-message: AI 활용 능력이 핵심 역량 -->
<!-- notes: 인용문 출처 설명 후 의미 해석 -->
```

### step-by-step — 단계별 안내

```markdown
<!-- layout: step-by-step -->
# OAuth 설정하기

### Step 1. Credential 생성
Gmail 노드에서 'Create New Credential' 클릭

### Step 2. Google 로그인
계정 로그인 → 권한 허용

### Step 3. 저장
Save 클릭

<!-- key-message: 3단계로 연동 완료 -->
<!-- notes: 각 단계별 화면 보여주며 진행 -->
```

## 이미지 프롬프트 형식

```markdown
<!-- image-prompt:
  concept: "핵심 컨셉 (1줄)"
  composition: "구도, 요소 배치"
  details: "색상, 분위기, 스타일 디테일"
  style: "Corporate tech illustration, 16:9, no text"
-->
```

- hub.md의 이미지 가이드와 스타일 일치 필수
- 실제 이미지 있으면 `![alt](path)` 사용, 프롬프트 생략 가능

## 렌더러별 주의사항

### Marp CLI

- frontmatter에 `marp: true` 추가
- `<!-- layout: -->` 은 Marp가 무시 (렌더링에 영향 없음)
- `---`가 슬라이드 구분자
- 2-column은 HTML `<div>` 필요할 수 있음

### Quarto Reveal.js

- frontmatter에 `format: revealjs`, `slide-level: 2`
- `<!-- layout: -->` 은 Quarto가 무시
- `##`이 슬라이드 구분 (`slide-level: 2`)
- 2-column은 `:::: {.columns}` + `::: {.column width="50%"}`
