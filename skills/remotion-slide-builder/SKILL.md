---
name: remotion-slide-builder
description: |
  소스 문서(CU/LO, 발표 원고, 제안서 등)를 기반으로 Remotion 영상 슬라이드 프로젝트를 생성하고 관리하는 스킬.
  프로젝트 초기화, 슬라이드 제작, 디자인 샘플링, PDF 출력을 포함한다.
  "Remotion 슬라이드 만들어", "영상 슬라이드", "CU를 Remotion으로", "슬라이드 프로젝트 생성",
  "발표자료 Remotion으로", "Remotion 프로젝트 초기화", "슬라이드 PDF", "Remotion 섹션 추가"뿐 아니라
  Remotion 프로젝트 구조, 컴포넌트 사용법, 슬라이드 추가/수정 관련 질문에도 이 스킬을 사용할 것.
version: 1.0.0
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, Agent, WebSearch, AskUserQuestion]
context: fork
---

# Remotion Slide Builder

소스 문서(CU/LO, 발표 원고, 제안서 등)를 Remotion 기반 영상 슬라이드 프로젝트로 변환하는 스킬.

> **참조 프로젝트** (패턴 복제 시 Read):
> - `<레이아웃 라이브러리 CU>/remotion/` — **레이아웃 컴포넌트 라이브러리** (15개 레이아웃, 30개 샘플, 데모 프레젠테이션)
> - `<실습 중심 CU>/remotion/` — (12개 섹션, 실습 중심, 표준 챕터 패턴 적용)
> - `CU-RAG 기반 생성형 AI 애플리케이션 구현/remotion/` — (8개 섹션, 78 슬라이드, CodeBlock 포함)
> - `CU-생성형 AI를 활용한 비즈니스 서비스 개발/remotion/` — 원본 (15개 LO, 200+ 슬라이드)
>
> **스킬 내부 리소스** (새 프로젝트 시 사용):
> - `templates/` — 프로젝트 스캐폴딩 (package.json, Root.tsx, render-pdf.mjs 등)
> - `samples/` — 슬라이드 패턴 샘플 (LOIndex, Divider, Content, Checkpoint)

## 핵심 원칙

```
소스 문서가 진실의 원천 → QMD 거치지 않음
1슬라이드 = 1React 컴포넌트
공통 컴포넌트 재사용 → 프로젝트별 커스텀은 최소화
격식체(합쇼체) — 교육/발표 자료는 공식 문서이므로 격식체 사용
코드로 먼저 레이아웃을 잡고, 필요 시 이미지로 전환
슬라이드 기본 5초 — 모든 슬라이드(Divider/콘텐츠/Checkpoint)는 5초를 기본으로 한다
```

> **룰 승격 절차**: 제작 중 새로 발견한 규칙은 즉시 이 스킬에 붙이지 않는다. 분류 → 중복 제거 → 일반화(고객명·Day·도메인·파일명 제거) → 예시 분리 → 보류(일회성·임시 우회는 제외) → 배치(전역 규칙은 SKILL.md, 세부 기준은 `references/`)의 순서를 거친 뒤 반영한다.

## 문체 상세

교육 및 발표 슬라이드는 **격식체(합쇼체)**를 기본으로 한다. 슬라이드 텍스트의 모든 문장에 적용한다.

### 허용 표현

- "~입니다", "~하였습니다", "~드리겠습니다"
- "확인하실 수 있습니다", "학습하겠습니다", "살펴보겠습니다"
- "~을 의미합니다", "~로 구성됩니다", "~가 필요합니다"

### 금지 표현

- 구어체/반말: "~거든요", "~해봐요", "~할게요", "~인데요"
- 감탄/추임: "놀랍게도!", "바로 이것입니다!", "정말 중요합니다!"
- 과장/마케팅: "혁명적인", "획기적인", "게임 체인저"
- 이모지를 제목이나 핵심 메시지에 사용 (ConceptCard의 icon prop은 허용)

### 한국어 톤 정리

- **영어 혼용 정리**: 불필요한 영어 단어는 한국어로 푼다 (trace는 추적 기록, fallback은 대체 경로, owner는 책임자). 단 API, PR, RAG처럼 정착된 표준 약어는 영어 원어를 유지한다
- **같은 표현 반복 회피**: "확인합니다" 같은 서술을 장표마다 반복하지 않고 내용에 맞게 다양하게 쓴다
- **구어·은유 회피**: 구어체와 은유(예: "판을 깔다")를 쓰지 않고 평이한 완결 문장으로 쓴다

### 타이틀 규칙

- 섹션/슬라이드 **타이틀은 포멀**하게 작성 — "확장 워크플로우와 검증 전략" 형식
- 도발적/자극적 문장("AI한테 속지 마십시오")은 타이틀이 아닌 **본문 인사이트**로 녹인다
- Q&A 응답은 본문 슬라이드에 섞지 않고 **별도 Q&A 섹션**으로 분리 — 맥락 없이 단독 슬라이드가 되면 이해 불가
- **제목은 주제명(키워드)**으로 짓는다. 나중에 다시 찾을 수 있는 주제 키워드여야 하며, 판단·주장은 제목이 아니라 부제나 본문으로 내린다. 파일명이나 "핵심 개념" 같은 범용어를 제목으로 단독 사용하지 않는다 (예: "권한 검증"은 가능, "권한 검증은 가장 중요하다"는 제목으로 부적합)
- **제작 의도를 문장 제목으로 쓰지 않는다**. "이 장표는 전환 장표입니다" 같은 메타 문장 대신 bridge 장표(방금 만든 것 / 이제 할 것 / 다음으로 넘길 것 3문장)로 처리한다
- 제목·부제·본문의 역할 분리 상세 기준은 `references/information-architecture.md`를 참고한다

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

## 프로젝트 위치

Remotion 프로젝트는 **슬라이드 소스 문서가 위치한 폴더** 안에 `remotion/`으로 배치한다.

```
{소스 폴더}/
├── *.md                      ← 슬라이드 원고, 발표자료 등
├── slides/                   ← 마크다운 슬라이드
└── remotion/                 ← Remotion 프로젝트
    ├── package.json
    ├── src/slides/
    ├── src/components/
    ├── scripts/render-pdf.mjs
    └── public/ (fonts, images)
```

소스 폴더는 도메인에 따라 다르다:
- 교육: `education/deliveries/CU-{주제}-{기관}/` 또는 `education/drafts/CU-{주제}/`
- 비즈니스: 해당 프로젝트의 산출물 폴더 (예: `04-발표/`)
- 기타: 슬라이드 원고가 있는 곳

> `remotion/`은 독립 git clone이 아니라 vault의 일부로 관리한다. `node_modules/`와 `out/`은 `.gitignore`에 포함.

## 듀얼 소스 워크플로우 (교육 프로젝트)

교육 CU에서는 마크다운 슬라이드(강사용 원고)와 Remotion 슬라이드(영상/PDF)를 **병렬 유지**한다.
비즈니스 발표 등 비교육 프로젝트에서는 마크다운 병렬이 필수가 아니며, 발표 원고가 소스 역할을 한다.

```
CU-{주제}/slides/<NN>-<topic>.md             ← 마크다운 (강사용, 세부 단계 포함)
CU-{주제}/remotion/src/slides/               ← Remotion (영상/PDF, 요약된 슬라이드)
```

| 항목 | 마크다운 | Remotion |
|------|---------|----------|
| 실습 번호 | 세부 단계 포함 가능 (1-1, 1-2...) | **실습 1, 실습 2만** (세부 없음) |
| 대상 | 강사 참고용 (LO 수준) | 수강생 화면 투사용 |
| 수정 흐름 | 마크다운 먼저 수정 → Remotion에 반영 |

### 동기화 규칙 (교육 프로젝트)

1. **마크다운이 소스**: 구조/내용 변경은 마크다운에서 먼저
2. **Remotion은 요약**: 마크다운의 세부 단계를 1~2장으로 압축
3. **병렬 작업 시**: 에이전트에게 마크다운 경로 + Remotion 경로 모두 전달

## 상세 레퍼런스

| 문서 | 내용 |
|------|------|
| `references/information-architecture.md` | 정보설계·콘텐츠 흐름 (시나리오 spine, 개념 micro-flow, 이론 밀도, bridge 장표, 제목·부제·본문 역할 분리) |
| `references/design-judgment.md` | 장표 타입 선택, 템플릿 반복 방지, 의미 라벨, 콘텐츠 유형별 시각 요소 매핑, 이미지 vs 코드 판단 |
| `references/review-rules.md` | 장표 단위 리뷰 절차 (P0/P1/P2 수정 순서, 6개 점검 항목) |
| `references/lo-as-slide-source.md` | LO를 발표자료 단일 원천으로 집필 (표준 절 구조, 분량 기준, 장표화 가능 밀도) |
| `references/chapter-pattern.md` | 표준 챕터 패턴, ChapterIntro/LabOverview 예시, 실습 번호 규칙, 이론 충실도, 명령어 검증 |
| `references/components.md` | 공통 컴포넌트 Props, 이미지 슬라이드 패턴, **이미지 소싱 워크플로우(image-gen/브라우저 자동화)**, 코드 라인 제한, sourceRef |
| `references/naming.md` | 파일명, Composition ID, 폴더명, LO index, 시간 배분, 전환/애니메이션, CU/LO 변환 |
| `references/layout-patterns.md` | 참고용 레이아웃 패턴 (흰색 패널, 2컬럼, 하단 배너, 바 차트, 플로우 카드) |
| `references/layout-library.md` | 레이아웃 컴포넌트 라이브러리 (사용 패턴·컴포넌트 구성·제작 우선순위·샘플 갤러리), 표준 레이아웃 패턴·카드 내부 공통 구조, 컴포넌트 업데이트 메모 |

> **정보설계와 리뷰는 별도 문서로 분리되어 있다.** 장표가 밋밋하거나 흐름이 끊긴다고 느끼면 디자인을 손대기 전에 `references/information-architecture.md`(콘텐츠 흐름)를 먼저 읽는다. 완성된 장표를 점검·수정할 때는 `references/review-rules.md`(장표 단위 리뷰 절차)를 따른다.

## 의도 파악

### 필수 확인 사항

| 항목 | 질문 | 이유 |
|------|------|------|
| 소스 문서 | 어떤 문서를 기반으로 하는지 (CU/LO, 발표 원고, 제안서 등) | 워크플로우 분기 결정 |
| 기존 프로젝트 | 복제할 기존 Remotion 프로젝트가 있는지 | 테마/컴포넌트 재사용 시 초기 비용 절감 |
| 대상 청중 | 수강생, 심사위원, 내부 발표 등 | 문체와 정보 밀도 결정 |
| 실습 코드 (교육) | 참조할 코드 저장소가 있는지 | CodeBlock 정합성 검증에 필요 |

### 바로 실행 (질문 불필요)

- 소스 문서가 명확히 지정된 경우
- "기존 프로젝트와 동일한 구조로" 라고 명시한 경우
- 기존 프로젝트에 섹션 추가하는 경우

## 워크플로우

### 제작 순서 (고정)

발표자료는 LO에서 파생되는 결과물이므로, 제작 순서를 다음으로 고정한다.

```
CU → LO 상세 원고 → 산출물/예제 패키지 → 발표자료(Remotion) → 리뷰
```

- **부족하면 LO를 먼저 보강한다**. 장표 내용이 빈약하면 장표를 꾸미지 말고 LO 원고를 먼저 채운 뒤 다시 장표화한다 (상세는 `references/lo-as-slide-source.md`).
- **구조 확정 전 대량 생성 금지**. 슬라이드 구조(Phase 2)가 승인되기 전에 Remotion 컴포넌트나 예제 코드를 대량으로 만들지 않는다.
- **대형 파일에 계속 붙이지 않는다**. 한 파일에 슬라이드를 무한정 추가하지 말고 LO·topic·phase 단위로 분해한다.
- **라이브 시연 실패 대비**. 라이브 시연이 포함된 강의는 시연이 실패할 경우를 대비해 사전 캡처 화면이나 샘플 산출물을 슬라이드에 미리 포함한다.

### Phase 1: 소스 분석

CU/LO를 읽고 슬라이드 구조를 설계한다.

```
1. CU 파일 Read → LO 매핑, 시간 배분, 전체 구조 파악
2. 각 LO 파일 Read → 핵심 개념, 실습 내용, 선수 지식
3. 실습 코드 저장소 탐색 (있으면) → CodeBlock에 사용할 코드 파악
4. 기존 Remotion 프로젝트 Read → 재사용할 컴포넌트/테마 확인
```

### Phase 2: 구조 설계 → 사용자 승인

슬라이드 구조를 표로 정리하여 제시. **승인 후 Phase 2.5 또는 Phase 3 진행.**

```markdown
| 섹션 | Composition ID | LO | 슬라이드 수 | 예상 시간 |
|------|---------------|-----|-----------|----------|
| 0 | 0-Course-Intro | 오프닝 | 6장 | 30초 |
| 1 | 1-Topic-Name | LO-xxx | 9장 | 40초 |
| ... | | | | |
```

슬라이드 수 산정 기준:
- CU의 시간 배분 참고, 개념당 1슬라이드
- 섹션당: SectionDivider(1) + 콘텐츠(N) + CheckpointSlide(1)
- 코드 많은 LO는 CodeBlock 슬라이드 추가

구조 설계 시 `references/design-judgment.md`를 참고하여 각 슬라이드에 적합한 시각 요소를 판단한다.
콘텐츠를 분해하고 시각 요소를 매핑하되, 매핑 테이블은 강제가 아니라 참고용이다.

### Phase 2.5: 디자인 샘플링 (선택)

레이아웃 선택이 중요한 슬라이드(로드맵, 비교 차트, 핵심 페이지 등)에 대해
**여러 안을 실제 Remotion 컴포넌트로 만들어 Studio에서 비교 선택**하는 단계.

#### 대상 식별

모든 슬라이드에 적용하지 않는다. 아래 조건에 해당하면 샘플링 후보:
- 복합 데이터를 담는 슬라이드 (타임라인 + 차트 + 텍스트 등)
- 레이아웃 배치에 따라 전달력이 크게 달라지는 슬라이드
- 발표에서 핵심인 슬라이드

#### 샘플 생성

기존 프로젝트의 `src/slides/_samples/` 폴더에 30개 레이아웃 샘플이 있다.
레이아웃 컴포넌트를 활용하여 빠르게 변형을 만든다.

1. `src/slides/_samples/` 폴더에서 적합한 레이아웃 패턴을 찾는다
2. 대상 슬라이드마다 2~3개 변형을 레이아웃 컴포넌트 조합으로 만든다:
   ```tsx
   // 옵션 A: TwoColumnSplit
   <SlideLayout title="로드맵">
     <TwoColumnSplit leftTitle="2025" items={[...]} />
   </SlideLayout>

   // 옵션 B: Timeline
   <SlideLayout title="로드맵">
     <Timeline events={[...]} />
   </SlideLayout>
   ```
3. `Root.tsx`에 샘플 전용 Folder로 등록한다
4. `references/layout-patterns.md`의 패턴을 참고하되, 자유롭게 변형한다

#### 선택 및 정리

```bash
npx remotion studio    # Studio에서 samples/ 폴더의 Composition을 비교
```

사용자가 선택하면:
1. 선택된 안을 본 슬라이드 폴더(`src/slides/<lo>/`)로 이동
2. `_samples/` 폴더와 Root.tsx의 샘플 Composition을 삭제
3. 본 슬라이드 제작 진행

### Phase 3: 프로젝트 생성

#### 3a. 초기화 (새 프로젝트)

**스킬 내부 templates/ 사용** (플레이스홀더 `{{...}}` 치환):
- `templates/package.json` → `{{PROJECT_NAME}}` 치환
- `templates/tsconfig.json` → 그대로 복사
- `templates/gitignore` → `.gitignore`로 복사
- `templates/src/index.ts`, `theme.ts`, `load-fonts.ts` → 그대로 복사
- `templates/src/Root.tsx`, `FullPresentation.tsx` → `{{SECTIONS}}` 주석을 실제 섹션으로 교체
- `templates/scripts/render-pdf.mjs` → `{{SECTIONS}}` 배열을 실제 섹션으로 교체

**기존 프로젝트에서 복사** (템플릿에 없는 것):
- `public/fonts/` (Pretendard woff2 5종)
- `src/components/` (전체 복사)
- `CLAUDE.md`, `SLIDE_GUIDELINES.md` (프로젝트에 맞게 수정)

```bash
# 컴포넌트/폰트 복사 원본 (레이아웃 라이브러리 포함)
education/deliveries/<레이아웃 라이브러리 CU>/remotion/
# src/components/ (원자 컴포넌트) + src/components/layouts/ (레이아웃 컴포넌트)
```

#### 3b. 슬라이드 제작

**병렬 에이전트** 활용 — 각 섹션을 독립 에이전트로 할당.

에이전트에게 전달할 정보:
1. LO 파일 경로 (핵심 개념/실습 추출)
2. 실습 코드 저장소 경로 (CodeBlock용)
3. 슬라이드 구조 (Phase 2에서 승인된)
4. **레이아웃 컴포넌트 목록** (`components/layouts/index.ts` 참조) + 기존 원자 컴포넌트 props
5. 네이밍 컨벤션 (아래 참조)
6. **`_samples/` 디렉토리 경로** — 30개 레이아웃 패턴 샘플 참조용
7. **슬라이드 제작 우선순위**: 레이아웃 컴포넌트 > 기존 원자 > 혼합 > 커스텀

#### 3c. 조합

- 각 LO 인덱스 파일 (TransitionSeries)
- `FullPresentation.tsx` (Series로 전체 연결)
- `Root.tsx` (Composition + Folder 등록)

### Phase 4: 검증 + 배포

```bash
pnpm install
npx tsc --noEmit --skipLibCheck   # 타입 체크
npx remotion compositions          # 컴포지션 목록 확인
pnpm pdf -- --section 0            # 첫 섹션 PDF 테스트
```

Remotion 프로젝트는 vault 커밋에 포함된다 (별도 GitHub 배포 불필요).

## Phase 5: Polish (퍼블리시 품질 검증)

Draft 단계(Phase 3)에서 콘텐츠와 구조를 잡았다면, Polish 단계에서는 **1장씩 렌더링하고 시각적으로 검증하여 퍼블리시 품질을 확보**한다.

### 언제 사용하는가

- Phase 3 완료 후 최종 점검 시
- 사용자가 "polish", "다듬어", "레이아웃 정리", "퍼블리시 준비" 등을 요청할 때
- 기존 슬라이드의 레이아웃 품질을 일괄 점검할 때

### 워크플로우

```
0. slide-lint 사전 검사
   node scripts/slide-lint.mjs
   → 기계적 이슈(missing source, flex:1 누락, 짧은 텍스트 등)를 먼저 일괄 수정
   → lint 카테고리: text count, content elements, description length, flex:1 usage, source prop
1. Studio 실행 확인 (또는 still 렌더링)
2. 대상 슬라이드의 스크린샷 캡처
   npx remotion still --comp <ID> --frame <완료프레임> --output out/review/<파일명>.png --scale 0.5
3. 스크린샷을 Read 도구로 읽어 시각적 평가
4. 레이아웃 체크리스트 대조
5. 문제 발견 시 수정 → 2로 돌아감 (re-render)
6. OK면 다음 슬라이드로
```

> **slide-lint 우선 원칙**: 렌더링 전에 반드시 lint를 먼저 돌린다. 렌더링은 시간이 걸리므로, 기계적으로 잡을 수 있는 문제를 먼저 해결하면 렌더링 횟수를 줄일 수 있다.

### 대상 지정

- **전체**: 모든 슬라이드 순회
- **LO 단위**: 특정 LO의 슬라이드만
- **개별**: 특정 슬라이드 1장

### 레이아웃 체크리스트

#### 필수 (위반 시 반드시 수정)

| 항목 | 기준 |
|------|------|
| 화면 채움 | 콘텐츠 영역이 flex:1로 가용 높이를 채워야 함. 하단에 큰 여백이 남으면 안 됨 |
| 최소 폰트 | 모든 텍스트 20px 이상. 18px 이하는 뒷자리에서 읽기 어려움 |
| 카드 프레임 | padding 32px, borderTop 5px, borderRadius 16px, gap 28px |
| 텍스트 잘림 | 긴 텍스트가 카드/뱃지 밖으로 넘치거나 잘리지 않아야 함 |
| 뱃지/라벨 폭 | 내용 길이에 비해 영역이 좁아 텍스트가 뭉치면 안 됨 |
| 출처 표기 | 모든 콘텐츠 슬라이드(Divider/Checkpoint 제외)에 `source` prop 필수. SlideLayout의 `source` prop(string, optional)을 사용. **좌측 하단**, 14px 회색 텍스트, 좌측 정렬. 페이지 번호는 **우측 하단**에 별도 배치. 출처는 의미 있는 인용 형식으로 작성 (예: "Anthropic, 'Building Effective Agents', 2024" — "Anthropic 2024"처럼 짧게 쓰지 않는다) |

#### 권장 (상황에 따라 판단)

| 항목 | 기준 |
|------|------|
| 콘텐츠 밀도 | 카드 내부가 텅 비어 보이면 설명이나 항목을 추가 |
| 시각적 균형 | N열 카드에서 한쪽만 내용이 많고 다른쪽이 비면 조정 |
| 색상 대비 | 배경색 위의 텍스트가 충분히 읽히는지 |
| 애니메이션 완료 상태 | still 캡처 시 모든 요소가 나타난 프레임을 사용 |

> **표준 레이아웃 패턴 / 카드 내부 공통 구조**: `references/layout-library.md` 참조.

### 리포트

Polish 완료 후 수정 내역을 요약한다:

```
## Polish 완료
- 전체: N장 검토
- 수정: M장 (목록)
- 스킵: K장 (이미지/Divider/Checkpoint)
- 잔여 이슈: (있으면)
```

## AI 모델명/가격 최신성 검증

슬라이드에 AI 모델명이나 가격이 등장할 때, 최종 확정 전에 반드시 최신 정보를 검증한다.

```bash
# OpenRouter API로 최신 모델/가격 조회 (인증 불필요)
curl -s "https://openrouter.ai/api/v1/models" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for m in data.get('data', []):
    p = m.get('pricing', {})
    inp = float(p.get('prompt','0')) * 1_000_000
    out = float(p.get('completion','0')) * 1_000_000
    if inp > 0: print(f'{m[\"id\"]:50s} \${inp:.3f} / \${out:.3f}')
"
```

- 구세대 모델을 그대로 사용하지 않고 현재 세대 모델로 업데이트한다
- 가격은 API 응답 기준으로 반영한다
- 적용 대상: 모든 슬라이드, 특히 비교표, 개요, 비용 산정 슬라이드

> **레이아웃 컴포넌트 라이브러리** (사용 패턴, 컴포넌트 구성, 원자 컴포넌트 혼합, 제작 우선순위, 샘플 갤러리): `references/layout-library.md` 참조.

> **컴포넌트 업데이트 메모** (CheckpointSlide, InstructorSlide, SlideLayout source prop): `references/layout-library.md` 참조.

## 과목 종속 정보 분리 원칙

스킬에는 범용 워크플로우만 포함한다. 아래 항목은 **CU 폴더의 CLAUDE.md**에 기록한다:

- 특정 도구의 버전별 커맨드 (예: OpenSpec 슬래시 커맨드 체계)
- 특정 모델명/가격 (검증 결과)
- CU의 독립/멀티데이 과정 구분
- 강사 프로필 데이터 소스 경로

## PDF 출력

`scripts/render-pdf.mjs`가 포함되어 있어야 함.

```bash
pnpm pdf                    # 전체 → out/presentation.pdf
pnpm pdf -- --section 4     # 섹션별 → out/section-4.pdf
```

원리: 각 섹션 Composition의 TransitionSeries 프레임 오프셋을 역산하여
애니메이션 완료 + 전환 직전 프레임을 캡처 → pdf-lib로 결합.

## 서브에이전트 활용

### 병렬 작업 패턴

여러 LO를 동시에 작업할 때 에이전트를 병렬로 할당한다.

**에이전트에게 전달할 정보:**
1. 마크다운 슬라이드 경로 (소스)
2. Remotion 슬라이드 폴더 경로 (출력)
3. 실습 코드 저장소 경로 (코드 검증용)
4. 표준 챕터 패턴 (위 참조)
5. 사용 가능한 컴포넌트 목록 + props
6. 실습 번호 규칙: 슬라이드에서는 "실습 1", "실습 2"만 (세부 번호 없음)
7. `samples/` 디렉토리 경로

**작업 단위:** 에이전트 1개 = LO 1개 (마크다운 수정 + Remotion 동기화)

| 도구 | 용도 |
|------|------|
| `general-purpose` 에이전트 (병렬) | LO당 1에이전트: 마크다운 + Remotion 동시 작업 |
| `web-researcher` | 통계/인용 자료 검색 |
| `remotion-best-practices` 스킬 | Remotion 코딩 참조 |

### 병렬 에이전트 후처리

병렬 에이전트 출력물은 서식 불일치가 불가피하다. 병합 후 반드시:
1. **P0 이슈 수정** — 타입 에러, import 누락, 컴포넌트 미존재 등
2. **패턴 통일** — 카드 프레임 규격, 폰트 크기, 색상 코드, 출처 형식 통일
3. **LOx.tsx import 확인** — 서브에이전트가 새 슬라이드를 만들었지만 LOx.tsx의 import와 TransitionSeries 배열에 반영하지 않는 경우가 빈번하므로, 각 LOx.tsx를 직접 열어 확인 필수

### 검증 체크리스트

각 LO 작업 완료 후:
1. `pnpm exec tsc --noEmit --skipLibCheck` — TypeScript 통과
2. `pnpm pdf -- --section N` — PDF 렌더링 성공
3. 마크다운과 Remotion 슬라이드 수 / 순서 일치 확인
4. 실습 코드가 저장소의 실제 코드와 일치 확인
5. **각 LOx.tsx의 import 문과 TransitionSeries 배열이 실제 슬라이드 파일과 일치하는지 확인**

## 문체

교육/발표 자료는 공식 문서이므로 격식체를 기본으로 한다.

- **격식체(합쇼체)** — "~입니다", "~하였습니다"
- 구어체/반말 금지

### 교육 프로젝트 추가 규칙

교육 슬라이드에서는 시연과 실습의 어조를 구분한다:
- 시연(Demo): 강사 단독 시연이므로 "따라오세요" 금지
- 실습(Practice): 수강생 직접 수행 → "실습합니다" 형태
- 실습 번호: 슬라이드에서는 "실습 1", "실습 2"만 (세부 번호 없음)
- 실습 명령어는 실제 소스코드(라우트, 포트, 파일명)와 반드시 대조 검증
