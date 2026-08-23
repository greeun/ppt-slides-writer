---
name: curriculum-builder
description: |
  교육 자료의 3계층 구조(카탈로그, 커리큘럼, LO) 및 연구/문헌 관리를 대화형으로 설계하고 생성하는 스킬.
  "LO 생성", "LO 확장", "커리큘럼 만들어", "납품 커리큘럼", "연구 프로젝트", "논문 정리",
  "카탈로그 만들어", "CAT-", "과정 묶음", "교육 프로그램 설계", "과정 패키지",
  LO/CU/CAT/RE/LIT 파일 생성이 필요할 때 사용할 것.
version: 1.0.0
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion, WebSearch, WebFetch, Agent]
disable-model-invocation: false
---

# Curriculum Builder Skill

교육 자료의 3계층 구조(CAT, CU, LO)와 연구/문헌 관리를 대화형으로 지원하는 스킬.

## 핵심 원칙

- **대화형 설계**: 커리큘럼/LO 생성 시 각 단계마다 사용자와 합의 후 진행
- **조사 후 제안**: vault 검색 + 웹 리서치 결과를 근거로 제시
- **LO 시간 자율**: 개념 중심, 프로젝트 독립적, 재사용 극대화. 분량 과도 시 A/B로 분할
- **CU 활동 분리**: 프로젝트 실습, 오프닝, 클로징은 LO가 아닌 CU에 직접 기술
- **중복 최소화**: 기존 LO 재사용, 양방향 링크 유지

## 3계층 교육 구조

```
catalogs/        ← CAT-{주제}-{연도}/ 폴더 (카탈로그 — 여러 CU를 묶는 교육 프로그램)
    ↓ CU 조합
deliveries/      ← CU-{주제}/ 폴더 (납품 건). 내부에 los/ 보유
drafts/          ← CU-{주제}/ 폴더 (미납품 설계안). 내부에 los/ 보유
                    └── los/ ← LO-*.md (CU 전용 학습 단위, 재사용 금지)
los/             ← (아카이브) 과거 재사용 LO 보관소. 신규 생성 금지
```

> **LO 위치 정책 (2026-05-09 이후)**: LO는 더 이상 vault 루트 `los/`에 두지 않습니다. 사용하는 CU 폴더 안 `los/`에 둡니다. 다른 CU에서 같은 주제가 필요하면 **복사 후 해당 CU에 맞게 수정**하며, wikilink로 공유하지 않습니다. 이유: 기관·시나리오마다 톤·예시·길이가 달라 재사용 wikilink가 강의 흐름을 깨는 사례 누적.

### CAT (카탈로그)

여러 CU를 하나의 교육 프로그램으로 묶는 상위 단위. 영업/제안/운영에 필요한 정보를 집약한다.

- **위치**: `education/catalogs/`
- **역할**: 과정 목록, 선택 가이드, 학습 경로, 일정 템플릿, 납품 이력, 가격 가이드, 커스터마이징 옵션
- **핵심 규칙**: CU wikilink만 포함, 콘텐츠 직접 작성 금지 (CU와 같은 원칙)

### CAT 명명 규칙

| 유형 | 명명 | 용도 | 예시 |
|------|------|------|------|
| **범용 CAT** | `CAT-{주제}-{연도}` | 제품 카탈로그, 범용 영업용 | `CAT-AI 실무 마스터-2026` |
| **기관 CAT** | `CAT-{주제}-{기관}-{연도}` | 특정 기관 맞춤 프로그램 | `CAT-DS College-KTDS-2026` |

**구분 기준**: 기관명이 있으면 기관 맞춤, 없으면 범용(재사용)

### CAT 폴더 구조

CAT는 항상 폴더로 생성한다 (CU와 동일한 폴더 승격 정책).

```
CAT-{주제}-{연도}/
├── CAT-{주제}-{연도}.md    ← 본문 (Obsidian hub, wikilink 중심)
├── roadmap/                ← 로드맵 이미지, 프롬프트
├── typst/                  ← Typst 소스 + PDF 렌더링 (제안용)
└── archive/                ← 이전 버전
```

### CU 폴더 구조

자료가 있는 CU는 폴더로 승격. CU frontmatter에 `slug` 필드(영문 kebab-case) 필수.

```
CU-{주제}/
├── CU-{주제}.md          ← 본문
├── los/                  ← LO-*.md (CU 전용 학습 단위, 필수)
├── slides/               ← 슬라이드 (YAML/MD/Quarto)
├── slides-slidev/        ← Slidev 프로젝트 (해당 시)
├── {slug}-guide.md       ← 강사가이드 (해당 시)
├── labs/                 ← 실습 레포 (독립 git clone, gitignore)
└── archive/              ← 아카이브 자료 (해당 시)
```

CU 본문에서 LO를 참조할 때는 모호 방지를 위해 상대 경로 명시:

```markdown
**사용 LO**: [[los/LO-주제]]
```

### CU 두 가지 유형

| 유형 | 명명 규칙 | 역할 |
|------|----------|------|
| **표준 CU** | `CU-주제.md` | LO 목록, 의존성, 운영 가이드 (재사용 템플릿). 납품 이력을 내부 테이블로 누적 관리 |
| **커스텀 CU** | `CU-주제-기관-YYMMDD.md` | 표준과 다른 구성이 필요한 일회성 맞춤 설계서. 상세 시간표, CU 활동, 환경 설정 포함 |

**구분 기준**: 날짜가 있으면 커스텀(일회성), 없으면 표준(재사용)
**단독 커스텀 CU**: 표준 CU 없이 커스텀 CU만 단독으로 생성 가능 (세미나, 브리핑 등 재사용성이 낮은 경우)
**반복 납품**: 표준과 동일한 구성으로 반복 납품하면 커스텀 CU를 만들지 않고, 표준 CU의 "납품 이력" 테이블에 날짜/기관/비고를 기록

### 계층별 담는 것

| 계층 | 담는 것 | 안 담는 것 |
|------|---------|-----------|
| LO | 학습 목표, 핵심 개념, 이론/코드 콘텐츠, 체크포인트 | 시간 배분, 프로젝트 실습 |
| 표준 CU | LO 목록, 순서, 의존성, 대상, 운영 가이드, 납품 이력 | 상세 시간표, 프로젝트 실습 |
| 커스텀 CU | 상세 시간표, CU 활동(실습), 환경 설정, 피드백 | LO 콘텐츠 (링크 참조) |

### CU 활동 (커스텀 CU에 직접 기술)

LO로 만들지 않는 과정 종속 활동:
- **오프닝**: 자기소개, 과정 안내, 프로젝트 소개
- **프로젝트 실습**: 진행 방법, 체크포인트, 주의사항 포함
- **클로징**: 핵심 정리, Q&A, 실무 도입 팁
- **Q&A 섹션**: 강의 중 나온 Q&A 응답은 본문 슬라이드에 섞지 않고 별도 Q&A 섹션으로 분리 — 맥락 없이 단독 슬라이드가 되면 이해 불가

### LO 설계 패턴

| 학습 유형 | 설계 패턴 | 예시 |
|----------|----------|------|
| 도구/워크플로우 학습 | **패턴별 케이스 실습** 구조 | Case 1: Quick Feature, Case 2: Exploratory, Case 3: Bug Fix |
| 개념 학습 | 이론 슬라이드 + 비교표 | ConceptCard, DataTable |
| 실습 중심 | 표준 챕터 패턴 (remotion-slide-builder 참조) | Lab Overview, Step, Result |

### LO는 발표자료의 단일 원천

발표자료(Remotion 장표)는 LO를 시각으로 옮기는 계층이다. 따라서 LO를 단일 원천 문서로 충실히 집필해야 장표가 빈약해지지 않는다.

- **단일 원천 문서**: LO 하나에 강의 원고, 산출물 작성 기준, 예제 해설, 시연 런북, 실습 검증 기준을 모두 담는다.
- **장표화 가능한 밀도**: LO 본문은 그대로 학생에게 보여도 자연스러운 밀도로 쓴다. 강사용 메모나 장표화 시 삭제할 메타 문장("여기서는 ~를 설명할 예정")은 넣지 않는다.
- **표준 절 구조**: 위치/목표/핵심 메시지/이론 원고/산출물 기준/예제 해설/시연 런북/실습·토론/검증 체크리스트/발표 전환 메모/참고의 절을 두고, 각 절이 발표자료 블록 1개에 대응하게 한다.
- **분량 기준**: 시간대별로 분량 하한을 명시한다(예: 30~60분 LO는 원고 2,000자 이상, 핵심 LO는 5,000자 이상). 분량이 부족하면 장표가 아니라 LO를 먼저 보강하고, 줄여야 할 때도 발표자료가 아니라 LO·운영(시간 배분) 단계에서 줄인다.

> 상세 절 구조와 분량 표는 remotion-slide-builder 스킬의 [`references/lo-as-slide-source.md`](../remotion-slide-builder/references/lo-as-slide-source.md)를 참조한다.

### 난이도 램프업

전문용어가 연속으로 등장하는 단원은 초반에 "쉬운 표현과 강의 용어를 매핑하는" 장표나 절을 둔다.

- 예: "대체 경로(폴백)", "추적 기록(트레이스)"처럼 쉬운 표현을 먼저 제시하고 강의 용어를 연결한다.
- 근거: 낯선 용어가 예고 없이 쏟아지면 수강생이 흐름에서 이탈한다. 쉬운 표현으로 한 번 풀어 주면 이후 용어 사용이 자연스러워진다.

### 실습은 모든 LO에 강제하지 않음

LO 성격에 맞춰 구성하며, 이론 LO에 억지로 실습을 끼워 넣지 않는다.

| LO 유형 | 강화 방향 |
|---------|----------|
| 이론 LO | 리서치, 표준, 판단 기준, 토론을 강화 (실습 대신 능동성 확보) |
| 실습 LO | 폴더·입력·필드·금지·완료 기준을 step-by-step으로 |

- 근거: 이론 LO에 억지 실습을 넣으면 내용이 얕아진다. 유형에 맞는 충실도가 학습 효과를 높인다.

### 시간표 설계 규칙

**60분 블록** 단위로 편성:

```
[50분 강의] + [10분 휴식] = 60분 블록
```

- 09:00-18:00 (8시간), 점심 12:00-13:00 (60분)
- 오전 3블록 + 오후 5블록 = 8블록 (400분 강의)
- LO, CU 활동, 실습을 자유롭게 배치
- 모든 휴식은 10분 고정

## 파일 접두사

| 접두사 | 폴더 | 예시 |
|--------|------|------|
| `LO-` | `{CU 폴더}/los/` | `drafts/CU-바이브코딩/los/LO-바이브코딩 개념.md` |
| `CAT-` (범용) | `catalogs/` | `CAT-AI 실무 마스터-2026/` |
| `CAT-` (기관) | `catalogs/` | `CAT-DS College-KTDS-2026/` |
| `CU-` (표준) | `curriculums/` | `CU-바이브코딩 with Claude Code.md` |
| `CU-` (커스텀) | `curriculums/` | `CU-바이브코딩-KOSTA-260322.md` |
| `RE-` | `Research/` | `RE-LLM Agent 평가체계.md` |
| `LIT-` | `literature/` | `LIT-Attention Is All You Need.md` |

> SS- 접두사는 더 이상 사용하지 않음. 기존 SS 파일은 sessions/Archive/에 보관.

## LO 필수 규칙

### LO-블록 매핑

LO와 시간표 블록(50분)은 N:M 관계입니다:
- 1 LO가 여러 블록에 걸칠 수 있음 (예: 실습 LO가 블록 4-7 점유)
- 1 블록에 여러 LO를 축약 배치할 수 있음 (예: 블록 1에 이론 LO 2개)

```
블록 1 ── LO-A 축약 + LO-B 축약 ── 이론 소개
블록 2 ── LO-C 전체 ───────────── 설치+실습
블록 3 ── LO-D 축약 + LO-E 시작 ── 전환
블록 4-7  LO-E 계속 + LO-F ────── 핵심 실습
블록 8 ── CU 활동 ─────────────── 자유 확장+회고
```

### 분할 기준
- **4블록 이상** 점유하는 LO는 A/B로 분할 검토
- 분할 기준은 내용의 자연스러운 구분점 (시간이나 줄 수 기준 아님)
- 분할된 LO는 독립 파일로 관리 (예: `LO-주제 A.md`, `LO-주제 B.md`)

### level 필드
- `beginner`, `intermediate`, `advanced` 세 값만 사용
- 다른 값(예: basic, expert 등)은 허용하지 않음

### prerequisites 필드
- LO frontmatter에 `prerequisites: []` 필수 (빈 배열이라도 명시)
- 선행 LO가 있으면 `prerequisites: [LO-선행학습]` 형태로 기재

### LO 분할 시 CU 동기화
- LO를 분할하면 해당 LO를 참조하는 모든 CU의 `lo_sequence`를 업데이트해야 함
- 분할 전 반드시 `grep -rl "LO-원래이름" education/curriculums/` 로 영향받는 CU 확인
- 분할 후 각 CU의 시간 합계가 달라지므로 CU의 `total_duration`도 재계산
- 분할된 LO들의 순서와 의존성을 CU 내에서 재배치

## 워크플로우 라우터

사용자 요청을 분석하여 적절한 워크플로우를 자동 실행.

| 키워드 | 워크플로우 | 파일 |
|--------|-----------|------|
| 카탈로그/CAT-/과정 묶음/프로그램 설계/패키지 | **Catalog Create** (대화형) | [workflows/catalog-create.md](workflows/catalog-create.md) |
| LO 확장/작성/학습목표 | **LO Enrichment** (대화형) | [workflows/lo-enrichment.md](workflows/lo-enrichment.md) |
| 커리큘럼 생성/CU- | **Curriculum Create** (대화형) | [workflows/curriculum-create.md](workflows/curriculum-create.md) |
| 커스텀/납품/강의/YYMMDD | **Session Plan** (커스텀 CU 생성) | [workflows/session-plan.md](workflows/session-plan.md) |
| 연구/특허/RE- | **Research Project** | [workflows/research-project.md](workflows/research-project.md) |
| 논문/문헌/리뷰/LIT- | **Literature Review** | [workflows/literature-review.md](workflows/literature-review.md) |

### 대화형 워크플로우 (Curriculum Create + LO Enrichment)

**Curriculum Create** — 4 Phase 공동 설계:
1. **방향 설정** (꼼꼼): 대상/주제/목표를 옵션 비교표로 토론
2. **뼈대 설계** (꼼꼼): LO 구성 + 의존성 정의를 옵션으로 제안
3. **세부 설계** (토픽 확인): 각 LO별 토픽을 초안+질문으로 제안
4. **콘텐츠 생성** (자율): 확정된 구조대로 LO/CU 파일 생성

**LO Enrichment** — 대화형 토픽 설계:
1. 커리큘럼 맥락 확인 → 2. 토픽/깊이 토론 → 3. 콘텐츠 작성(자율) → 4. 피드백

> 각 Phase 합의 없이 다음으로 넘어가지 않는다.

### 에이전트 팀 워크플로우 (대규모 제작)

LO 다수 + CU 동시 제작 시 에이전트 팀 활용:
1. **작성자(creator)**: WebSearch, context7(resolve-library-id, query-docs) 등으로 최신 정보 및 공식 문서 조사 후 LO/CU 생성 (과정별 병렬)
2. **검수자(reviewer)**: 시간 검증, 일관성, 기술 정확성, 문체 규칙 검토
3. **학생(student)**: 수강생 관점에서 이해도, 실습 실행 가능성, 시간 현실성 리뷰
4. **수정자(fixer)**: 리뷰 피드백 반영

### 실행 원칙

1. 해당 워크플로우 `.md` 파일을 로드하고 Phase 지침을 따름
2. Phase 1부터 순차 실행, AskUserQuestion으로 중간 검증
3. 완료 후 연관 파일 링크 업데이트

### 조회 요청 (바로 실행)

- "LO-xxx 보여줘" → 조회
- "커리큘럼 목록" → 조회
- 이전 대화에서 이미 의도가 파악된 경우

## 리소스 참조

### Reference Files

상세 규칙과 체크리스트:
- **[references/structure-rules.md](references/structure-rules.md)** — 구조 규칙, 양방향 링크, Quality Checklist, 웹 리서치 규칙
- **[reference.md](reference.md)** — LO 콘텐츠 작성 가이드라인, 출처 명시, Mermaid 규칙

### Templates

- **[templates/catalog.md](templates/catalog.md)** — 카탈로그 템플릿 (CAT)
- **[templates/curriculum-standard.md](templates/curriculum-standard.md)** — 표준 커리큘럼 템플릿
- **[templates/curriculum-delivery.md](templates/curriculum-delivery.md)** — 커스텀 커리큘럼 템플릿
- **[templates/lo.md](templates/lo.md)** — LO 템플릿

### Examples

- **[examples.md](examples.md)** — 사용 예시 및 에러 처리

## 서브에이전트 & 스크립트

| 도구 | 용도 |
|------|------|
| `web-researcher` | 최신 기술 트렌드 조사, LO 정보 보강 |
| `pattern-analyzer` | 기존 LO/CU 스타일 분석 |
| `duplicate-checker.py` | LO 중복 검사 |

## LO-Remotion 동기화 규칙

Remotion 슬라이드가 이미 제작된 CU의 LO를 수정할 때는 반드시 해당 Remotion TSX 슬라이드도 함께 수정한다.

### 판단 기준

- CU 폴더 내 `remotion/` 디렉토리가 존재하면 Remotion 슬라이드가 제작된 것으로 판단
- 또는 `외부 코드 저장소`에 해당 CU의 Remotion 프로젝트 저장소가 있는 경우

### 매핑 방식

- LO의 `slug` 필드를 기준으로 `remotion/src/slides/{slug}/` 디렉토리와 매칭
- slug가 없으면 LO 폴더명 또는 파일명에서 유추

### 수정 절차

1. LO 수정 내용을 확정
2. 해당 LO의 slug로 Remotion 슬라이드 디렉토리를 탐색
3. LO 변경 사항(개념 추가/삭제, 순서 변경, 실습 수정 등)을 Remotion TSX에 반영
4. TypeScript 컴파일 확인 (`pnpm exec tsc --noEmit --skipLibCheck`)

### 주의

- LO만 수정하고 Remotion을 수정하지 않으면 콘텐츠 불일치가 발생한다
- 항상 LO와 Remotion TSX를 쌍으로 수정할 것

## 개념 노트와의 협력

개념 노트(notes/) 생성이 필요하면 노트 생성 도구로 만들고, 생성된 노트를 LO에 링크합니다.

## 태그

| 계층 | 기본 태그 | 예시 |
|------|----------|------|
| Research | `#research` | `#research/ai` |
| Literature | `#literature` | `#literature/paper` |
| Catalog | `#catalog` | `#catalog/ai` |
| Curriculum | `#curriculum` | `#curriculum/ai` |
| LO | `#lo` | `#lo/beginner` |
