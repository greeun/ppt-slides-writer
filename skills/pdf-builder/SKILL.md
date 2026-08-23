---
name: pdf-builder
description: |
  This skill should be used when the user asks to "PDF 만들어", "PDF 빌드", "렌더링 해줘",
  "문서 출력", "typst 컴파일", "보고서 PDF로", ".typ 파일 빌드", "Quarto 렌더",
  "md를 qmd로 변환", or mentions PDF rendering, document compilation, or Typst builds.
  Handles Typst standalone compilation (default) and Quarto+Typst rendering (exception).
version: 2.2.0
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion]
context: fork
---

# PDF Builder

문서를 PDF로 렌더링하는 스킬. Typst 단독 빌드를 기본으로, Quarto+Typst를 예외로 지원한다.

## 렌더링 스택

| 방식 | 용도 | 명령 |
|------|------|------|
| **Typst 단독** (기본) | 보고서, 제안서, 가이드 | `typst compile --root <vault-root>` |
| **Quarto + Typst** (예외) | 기존 .qmd 변환, 참고문헌 | `quarto render --to typst` |

## 디자인 시스템: frentis-base.typ

모든 Typst 문서의 공용 디자인 토큰과 옵션 조합을 제공하는 기반 파일.

**위치**: `templates/typst/frentis-base.typ`

```typst
#import "/.claude/skills/pdf-builder/templates/typst/frentis-base.typ": *

#show: frentis-doc.with(
  title: "문서 제목",
  cover: true,
  logo: "/path/to/company_logo.png",
  toc: true,
  header-footer: true,
  numbering: "1.1.1",
)
```

### 파라미터

| 파라미터 | 기본값 | 설명 |
|----------|--------|------|
| `title` / `subtitle` | `none` | 제목 / 부제 |
| `author` / `date` | `none` | 작성자 / 날짜 |
| `cover` | `false` | 표지 표시 |
| `cover-style` | `"gradient"` | `"gradient"` 또는 `"simple"` |
| `logo` | `none` | 로고 경로 |
| `toc` | `false` | 목차 표시 |
| `header-footer` | `true` | 헤더/푸터 표시 |
| `header-text` | `"Your Company"` | 헤더 우측 텍스트 |
| `numbering` | `"1.1.1"` | 섹션 번호 (`none`이면 없음) |
| `fontsize` | `11pt` | 본문 크기 |
| `margin` | 25mm | 여백 |
| `leading` | `0.8em` | 줄간격 |

### 옵션 조합 예시

| 문서 유형 | 핵심 옵션 |
|-----------|-----------|
| 1페이지 주간보고 | `cover: false, header-footer: false, numbering: none, fontsize: 9pt, margin: 1.2cm` |
| 기술 보고서 | `cover: false, logo: "...", header-footer: true, numbering: "1.1.1"` |
| 정식 제안서 | `cover: true, cover-style: "gradient", logo: "...", toc: true` |
| 간결 제안서 | `cover: true, cover-style: "simple", logo: "...", toc: true` |

### 유틸리티 함수

- `info-box(title: "제목")[내용]` — 파란색 정보 박스
- `warning-box(title: "제목")[내용]` — 노란색 경고 박스

## 빌드 방법

### Typst 단독 (기본)

```bash
typst compile --root <vault-root> input.typ output.pdf
```

> frentis-base.typ의 절대경로 import 사용 시 `--root` 플래그 필수.

### Quarto + Typst (예외)

```bash
quarto render --to typst
```

> `_quarto.yml`의 `mainfont` 제거 필수. 폰트는 `typst-show.typ`에서만 정의한다.

## 절대 금지 사항

- **ASCII 아트 다이어그램 금지** — 아키텍처, 흐름도 등을 ASCII 문자로 표현하지 않는다. 다이어그램은 **diagram-builder 스킬**로 Draw.io PNG 생성 후 이미지로 삽입한다.
- **`$` 기호 주의** — Typst에서 `$`는 수식 구분자. 금액 등에서 `\$` 또는 텍스트로 대체한다.

## 에러 처리

| 오류 | 원인 | 해결 |
|------|------|------|
| cannot read file outside of project root | 절대경로 import | `--root <vault-root>` 추가 |
| 폰트 없음 | Pretendard 미설치 | `brew install --cask font-pretendard` |
| 한글 깨짐 (Quarto) | `_quarto.yml`의 mainfont | mainfont 제거, typst-show.typ에서 정의 |

## 연계 스킬

- **diagram-builder** — 다이어그램 PNG 생성 (Draw.io/Mermaid)
- 장문 문서·보고서 작성 워크플로우 — 렌더링 시 pdf-builder를 호출합니다

## 의존성

```bash
brew install --cask quarto && brew install typst
```

## 추가 리소스

### 참조 자료

상세 워크플로우는 필요 시 참조:

- **`references/typst-build.md`** — Typst 빌드 상세 절차, 옵션 조합 예제, 일괄 빌드, 감시 모드
- **`references/render.md`** — Quarto 렌더링 상세 (방식 판별, Phase 1~3, 출력 경로)
- **`references/convert.md`** — md → qmd 변환 절차 (제목 계층, 이미지, 링크, 콜아웃)

### 템플릿

문서 생성 시 선택할 수 있는 Typst 템플릿:

- **`templates/typst/frentis-base.typ`** — 모든 .typ 문서가 import하는 기본 디자인 시스템
- **`templates/typst/{report,book,proposal}/typst-show.typ`** — Quarto 렌더링용 template-partials (타입별 스타일)
- **`templates/typst/catalog/typst-template.typ`** — Quarto 카탈로그 템플릿 (커버 포함)
- **`templates/{spec,catalog,handout}/`** — 독립 Typst 멀티섹션 문서 (선택적)
