# Convert Workflow

마크다운(md) 파일을 Quarto(qmd) 형식으로 변환하는 워크플로우입니다.

## 핵심 원칙

```
❌ 여러 md를 하나의 qmd로 합치지 않는다
✅ 기존 문서 구조를 유지한다 (1 md → 1 qmd)
✅ 출판에 적합한 형태로 변환한다
```

---

## Phase 1: 분석 (Analyze)

### 1.1 대상 문서 파악

```
프로젝트 폴더에서:
- hub.md (목차/인덱스) 확인
- PR-*.md, REP-*.md 등 콘텐츠 파일 목록화
- 문서 간 의존성/순서 파악
```

### 1.2 문서 구조 매핑

| 원본 (Obsidian) | 변환 (Quarto) | 역할 |
|-----------------|---------------|------|
| `hub.md` | `index.qmd` (선택) | 프로젝트 소개 |
| `PR-프로젝트-제안서.md` | `01-제안서.qmd` | 챕터 1 |
| `PR-프로젝트-모듈상세.md` | `02-모듈상세.qmd` | 챕터 2 |
| `PR-프로젝트-추진계획.md` | `03-추진계획.qmd` | 챕터 3 |

### 1.3 _quarto.yml 챕터 순서 결정

```yaml
book:
  chapters:
    - index.qmd       # 선택: hub.md 기반
    - 01-제안서.qmd
    - 02-모듈상세.qmd
    - 03-추진계획.qmd
```

---

## Phase 2: 변환 (Transform)

### 2.1 Frontmatter 변환

**Obsidian frontmatter:**
```yaml
---
created: 2026-01-16
updated: 2026-01-17
tags: [proposal, overseas]
status: 작성중
---
```

**Quarto frontmatter:**
```yaml
---
# Quarto는 frontmatter 최소화 (메타데이터는 _quarto.yml에)
---
```

> 대부분의 메타데이터는 `_quarto.yml`에서 관리하므로 qmd frontmatter는 비워두거나 최소화

### 2.2 제목 계층 조정

**원본 (md):**
```markdown
# 문서 제목

## 1. 첫번째 섹션
### 1.1 세부 항목
```

**변환 (qmd):**
```markdown
# 첫번째 섹션 {#sec-overview}

## 세부 항목 {#sec-overview-detail}
```

**규칙:**
1. 문서 제목(`#`)은 제거 → `_quarto.yml`의 `title`이 대체
2. `##`가 최상위 섹션이 됨
3. 수동 번호(`1.`, `1.1`) 제거 → Quarto가 자동 번호 부여
4. 필요 시 `{#sec-label}` 추가하여 교차 참조 지원

### 2.3 이미지 경로 처리

**Obsidian:**
```markdown
![[assets/diagrams/시스템-아키텍처.png]]
```

**Quarto:**
```markdown
![시스템 아키텍처](assets/diagrams/시스템-아키텍처.png){#fig-architecture}
```

**또는 figure 블록:**
```markdown
::: {#fig-architecture}
![](assets/diagrams/시스템-아키텍처.png)

시스템 아키텍처
:::
```

### 2.4 내부 링크 처리

**Obsidian wikilink:**
```markdown
[[PR-인도네시아-검찰청-모듈상세#3.1 채널관리 모듈]]
```

**Quarto cross-reference:**
```markdown
@sec-channel-management (섹션 참조)
@fig-architecture (그림 참조)
@tbl-modules (표 참조)
```

> 문서 간 링크는 Quarto book에서 자동 처리

### 2.5 표 형식 정리

**필수 레이블 추가:**
```markdown
| 항목 | 내용 |
|------|------|
| ... | ... |

: 표 제목 {#tbl-summary}
```

### 2.6 콜아웃 변환

**Obsidian:**
```markdown
> [!NOTE]
> 참고 사항
```

**Quarto:**
```markdown
:::{.callout-note}
참고 사항
:::
```

---

## Phase 3: 검증 (Validate)

### 3.1 체크리스트

- [ ] 모든 md 파일이 qmd로 변환됨
- [ ] `_quarto.yml` chapters에 모든 qmd 등록
- [ ] 이미지 경로가 올바름
- [ ] 깨진 링크 없음
- [ ] 제목 계층이 적절함

### 3.2 미리보기

```bash
quarto preview
```

### 3.3 최종 렌더

```bash
quarto render --to pdf
```

---

## 변환 예시

### Before: PR-인도네시아-검찰청-제안서.md

```markdown
---
created: 2026-01-16
tags: [proposal]
---

# 인도네시아 검찰청 AI 플랫폼 제안서

## 1. 사업 개요

### 1.1 배경
인도네시아 검찰청은...

### 1.2 목표
![[assets/diagrams/시스템-아키텍처.png]]

자세한 내용은 [[PR-인도네시아-검찰청-모듈상세]]를 참조하세요.
```

### After: 01-제안서.qmd

```markdown
---
---

# 사업 개요 {#sec-overview}

## 배경 {#sec-background}

인도네시아 검찰청은...

## 목표 {#sec-objectives}

![시스템 아키텍처](assets/diagrams/시스템-아키텍처.png){#fig-architecture}

자세한 내용은 @sec-modules를 참조하세요.
```

---

## 자동화 규칙

### 파일명 변환

```
접두사 제거 + 순번 부여 + .qmd 확장자

PR-프로젝트-제안서.md     → 01-제안서.qmd
PR-프로젝트-모듈상세.md   → 02-모듈상세.qmd
PR-프로젝트-추진계획.md   → 03-추진계획.qmd
REP-분석보고서.md        → 01-분석보고서.qmd
```

### 처리하지 않는 파일

| 파일 | 이유 |
|------|------|
| `hub.md` | 관리용 (index.qmd로 선택 변환) |
| `assets/research/*.md` | 리서치 자료 (출판 대상 아님) |
| `old/*.md` | 이전 버전 |

---

## 변환 모드

### A. 복사 변환 (권장)

```
원본 md 유지 + 별도 qmd 생성
- hub.md, PR-*.md 그대로 유지
- 01-*.qmd 별도 생성
```

장점: Obsidian에서 계속 편집 가능, 양쪽 동기화

### B. 제자리 변환

```
md → qmd 확장자만 변경
- PR-*.md를 PR-*.qmd로 변경
- _quarto.yml에서 PR-*.qmd 참조
```

장점: 파일 수 적음
단점: Obsidian 링크 깨짐

---

## 빠른 참조

### 변환 명령 흐름

```
1. 분석: 대상 md 파일 목록화
2. 순서: hub.md 기반으로 챕터 순서 결정
3. 변환: md → qmd (제목 계층, 이미지, 링크)
4. 설정: _quarto.yml 업데이트
5. 검증: quarto preview
```

### Quarto 교차 참조 문법

| 유형 | 정의 | 참조 |
|------|------|------|
| 섹션 | `## 제목 {#sec-name}` | `@sec-name` |
| 그림 | `{#fig-name}` | `@fig-name` |
| 표 | `: 캡션 {#tbl-name}` | `@tbl-name` |
| 코드 | `#| label: lst-name` | `@lst-name` |
