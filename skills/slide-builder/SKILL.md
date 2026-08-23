---
name: slide-builder
description: |
  마크다운 기반 발표 슬라이드 원고를 작성하는 스킬. CU/LO/README에서 콘텐츠를 추출하여 슬라이드를 생성한다.
  "슬라이드 만들어", "발표 자료", "PPT 작성", "섹션 추가", "CU를 슬라이드로",
  "마크다운 슬라이드", "강의 슬라이드" 등 마크다운 기반 슬라이드 원고가 필요할 때 사용할 것.
  Remotion 영상 슬라이드가 필요하면 remotion-slide-builder 스킬을 대신 사용한다.
version: 1.0.0
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch, AskUserQuestion]
context: fork
---

# Slide Builder Skill

마크다운 기반 슬라이드 원고를 작성하는 스킬. 원고는 Marp/Quarto에 직접 입력 가능한 형식.

> **상세 참조** (필요할 때 Read):
> - 마크다운 컨벤션 + 레이아웃: `workflows/schema.md`
> - 디자인 패턴 + 품질 체크: `workflows/patterns.md`
> - Hub 템플릿: `templates/hub-template.md`
> - 섹션 템플릿: `templates/section-template.md`

## 핵심 원칙

```
슬라이드 = 표준 마크다운 (--- 구분자)
메타 정보 = HTML 주석 (<!-- layout: -->, <!-- notes: -->)
1슬라이드 = 1메시지
실습 명령어는 실제 소스코드(라우트, 포트, 파일명)와 반드시 대조 검증
```

### 실습 슬라이드 필수 항목

실습 안내 슬라이드에 CLI 명령어를 쓸 때 다음을 확인:

- 작업 대상 파일 (어떤 파일을 수정/생성하는지)
- 사전 조건 (이미지 빌드, 기존 리소스 정리 등)
- API 엔드포인트, 포트, 이미지명은 실제 소스코드와 대조
- solutions 파일 = 해당 LO 완료 시점의 누적 스냅샷

## 의도 파악

### 질문이 필요한 경우

| 유형 | 질문 |
|------|------|
| 새 프로젝트 | 목적, CU 연결, 일시, 시간, 청중 |
| 섹션 추가 | 어떤 프로젝트에, 주제, 핵심 메시지 |

### 바로 실행 (질문 불필요)

- "슬라이드 현황 보여줘" / "hub.md 업데이트" / 이미 의도 파악된 경우
- CU가 이미 있고 "이걸로 슬라이드 만들어"
- 기존 섹션에 슬라이드 추가

## 폴더 구조

```
education/slides/
├── YYYY-MM-DD-제목/
│   ├── hub.md              ← 인덱스 (Obsidian 링크)
│   ├── 0-오프닝.md          ← 섹션별 마크다운
│   ├── 1-본론.md
│   ├── 2-실습.md
│   ├── 3-클로징.md
│   └── assets/             ← 이미지, 스크린샷
└── archive/
```

## 워크플로우

### Phase 1: 소스 수집

콘텐츠 소스를 파악하고 읽는다.

| 소스 | 추출 대상 |
|------|----------|
| **CU-** (납품/설계안) | LO 매핑, 시간표, 운영 메모, CU 활동 |
| **LO-** (학습목표) | 핵심 개념, 실습 내용, 선수 지식 |
| **README.md** (데모) | 시연 순서, 핵심 멘트, 코드 예시, 백업 플랜 |
| 기존 슬라이드 | 톤, 구조, 이미지 스타일 참고 |

**CU가 있으면 반드시 읽고 시작.** 없으면 의도 파악 질문.

### Phase 2: 구조 설계

1. 스토리 아크 정의 (오프닝 → 본론 → 클로징)
2. 섹션 분할 + 시간 배분
3. 섹션별 슬라이드 수 산정 (분당 ~2장 기준)
4. hub.md 생성 (`Read templates/hub-template.md`)
5. **사용자 승인** 후 Phase 3

### Phase 3: 섹션 작성

1. 섹션 파일 생성 (`Read templates/section-template.md`)
2. 각 슬라이드에 필수 요소:
   - `<!-- layout: type -->` — 레이아웃
   - `# 제목` + 본문 — 콘텐츠
   - `<!-- key-message: ... -->` — 핵심 메시지
   - `<!-- notes: ... -->` — 강사 노트
3. 이미지 필요 시 `<!-- image-prompt: ... -->` 추가
4. hub.md 업데이트

### Phase 4 (선택): 렌더링

원고 완성 후 렌더링이 필요하면:

```bash
# Marp CLI → PDF
npx @marp-team/marp-cli 1-오프닝.md -o 1-오프닝.pdf --theme-set theme.css

# Quarto → HTML (reveal.js)
quarto render 1-오프닝.md --to revealjs

# 전체 섹션 병합 후 렌더링
cat 0-*.md 1-*.md 2-*.md 3-*.md > _all.md
npx @marp-team/marp-cli _all.md -o slides.pdf
```

## 소스별 변환 패턴

### CU → 슬라이드 골격

```
CU의 LO 매핑 테이블
  → 섹션 = CU의 블록/파트
  → 슬라이드 수 = 시간(분) × 2장/분
  → 각 LO의 핵심 개념 → 슬라이드 본문
```

### 데모 README → 슬라이드

```
README 구조         → 슬라이드 매핑
─────────────────   ──────────────────
시연 목표           → section 슬라이드 (key-message)
사전 체크리스트     → (슬라이드 아님, 강사 준비용)
시연 순서 Step N    → 1-column 또는 code 슬라이드
핵심 멘트           → quote 슬라이드
백업 플랜           → notes에 포함
```

### 기존 슬라이드 참조

새 프로젝트 시 기존 슬라이드 톤 참고:
1. `Glob education/slides/*/hub.md` → 이미지 스타일, 색상 팔레트 확인
2. 유사한 발표의 섹션 파일 1~2개 Read → 분량, 레이아웃 빈도 파악
3. 필요시 `pattern-analyzer` 서브에이전트로 스타일 분석

## 분량 가이드라인

| 규칙 | 기준 |
|------|------|
| 슬라이드 속도 | 분당 ~2장 (30초/장) |
| 텍스트 | 슬라이드당 6줄 이내, 불릿 3~5개 |
| 코드 | 10줄 이내, 핵심만 |
| 표 | 5행 이내, 4열 이내 |
| 이미지 | 16:9, 텍스트 없는 일러스트 |
| key-message | 모든 슬라이드에 필수 (1줄) |

## 서브에이전트 & 연계

| 도구 | 용도 |
|------|------|
| `web-researcher` | 통계/인용 자료 검색 |
| `pattern-analyzer` | 기존 슬라이드 스타일 분석 |
| `image-gen` | 슬라이드 삽화 생성 (텍스트로 부족할 때) |
| `curriculum-builder` | CU 생성이 먼저 필요할 때 |
