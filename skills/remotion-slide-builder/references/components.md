# 컴포넌트 레퍼런스

## 공통 컴포넌트 (`src/components/`)

| 컴포넌트 | Props | 용도 |
|----------|-------|------|
| `SlideLayout` | `title, subtitle, sectionLabel, pageNumber, totalPages, source, dark, children` | 기본 레이아웃 (source: 좌측 하단, pageNumber: 우측 하단) |
| `AnimatedList` | `items[], staggerDelay, startFrom, icon, itemFontSize, color?` | 순차 등장 리스트 (`color`로 불릿/강조색 지정) |
| `SectionDivider` | `sectionNumber, title, objectives[], duration, pageNumber?, totalPages?` | LO 시작 간지 (다크) |
| `ConceptCard` | `items[{icon, title, description, color}], startFrom, columns` | 카드형 개념 (icon은 빈 문자열 `""` 권장) |
| `DataTable` | `headers[], rows[][], startFrom, compact, columnWidths?` | 데이터 테이블 (`columnWidths={["20%","80%"]}` 등) |
| `StatCard` | `items[{value, label, sub}], startFrom, columns` | 통계 카드 |
| `PromptDemo` | `messages[{role, content}], startFrom` | AI 대화창 |
| `CheckpointSlide` | `title, points[], sectionLabel, subtitle?, pageNumber?, totalPages?` | LO 마무리 |
| `CodeBlock` | `code, language, title, startFrom, fontSize, sourceRef` | 코드 블록 (구문 강조) |
| `AnnotatedCode` | `fileName, lines[{code, note?}], callout?{label?, text}, codeFontSize?, noteFontSize?, animate?, staggerDelay?` | 코드를 한 줄씩 우측 주석과 격자로 읽는 블록 (코드 뜯어보기 슬라이드) |
| `Pipeline` | `nodes[{label, sub?, color?}], startFrom?, dark?, arrowLabel?` | 가로 흐름 아키텍처 (단계를 화살표로 연결, 노드 많으면 자동 줄바꿈) |
| `HandsOnSlide` | `sectionLabel, blockNumber, title, instruction, command?, expectation, storyNote, pageNumber?, totalPages?` | 실습 안내 독립 다크 슬라이드 (SlideLayout 불필요, 화면 전체 차지) |
| `PageNumber` | `pageNumber?, totalPages?, dark?` | 우측 하단 페이지 번호 (독립 슬라이드에서 직접 배치할 때 사용) |
| `IllustrationSlide` | `title, subtitle?, sectionLabel, image, source?, pageNumber?, totalPages?` | 단일 삽화를 중앙에 크게 배치하는 슬라이드 (`image`는 `staticFile` 상대 경로) |

## 레이아웃 선택 가이드

콘텐츠 개수와 유형에 따라 최적의 레이아웃을 동적으로 선택한다.
"항상 1열" 또는 "항상 가로 나열"은 피하고, 아래 기준에 따라 판단한다.

### 카드형 컴포넌트 (ConceptCard, StatCard)

| 아이템 수 | columns 값 | 레이아웃 | 이유 |
|-----------|-----------|---------|------|
| 2개 | `columns={2}` | 1x2 가로 | 대비/비교에 최적 |
| 3개 | `columns={3}` | 1x3 가로 | 황금 비율, 가장 일반적 |
| 4개 | `columns={2}` | **2x2 그리드** | 가로 4열은 카드가 너무 좁음 |
| 5개 | `columns={3}` | 2행 (3+2) | 첫 행 3개, 둘째 행 2개 |
| 6개 | `columns={3}` | 2x3 그리드 | 균형 잡힌 배치 |

> **핵심 원칙**: 카드 내 텍스트가 3줄 이상이면 columns를 줄여 가독성을 확보한다.
> 예: 설명이 긴 4개 카드는 `columns={2}`(2x2)가 `columns={4}`(1x4)보다 읽기 편하다.

### 리스트형 컴포넌트 (AnimatedList)

| 아이템 수 | 레이아웃 | 방법 |
|-----------|---------|------|
| 3~5개 | 1열 전체 너비 | AnimatedList 단독 |
| 6~8개 | 2열 분할 | 좌우 div에 AnimatedList 2개 배치 |
| 8개+ | 1열 + 작은 폰트 | `itemFontSize={fontSize.caption}` 축소 |

### 혼합 레이아웃 (텍스트 + 카드/이미지)

| 구성 | 권장 레이아웃 |
|------|------------|
| 정의 + 목록 | 좌측 정의 박스(flex: 0.4) + 우측 AnimatedList(flex: 0.6) |
| 텍스트 + 이미지 | 좌측 텍스트(flex: 1) + 우측 이미지(flex: 1) |
| 개념 + 비교 | 상단 개념 설명 + 하단 DataTable 또는 ConceptCard |
| Before/After | 좌측 카드(경고색 테두리) + 우측 카드(성공색 테두리) |

### 콘텐츠 영역 높이 계산

SlideLayout의 콘텐츠 영역은 약 711px이다. 레이아웃이 이를 초과하지 않도록 주의한다.

| 요소 | 높이 기준 |
|------|----------|
| ConceptCard 1행 (설명 2줄) | 약 140px |
| ConceptCard 1행 (설명 4줄) | 약 200px |
| AnimatedList 1아이템 | 약 50px (body) / 35px (caption) |
| DataTable 1행 | 약 55px (body) / 40px (caption) |
| 여백 (gap) | spacing.element = 24px |

> 2x2 ConceptCard(설명 3줄)는 약 140*2 + 24 = 304px로 여유가 충분하다.
> AnimatedList 8개(body)는 약 50*8 + 24*7 = 568px로 여유가 있지만, 10개 이상이면 caption 폰트를 사용한다.

## 레이아웃 컴포넌트 (`src/components/layouts/`)

재사용 가능한 레이아웃 컴포넌트. SlideLayout children으로 사용하거나 독립 슬라이드로 사용한다.
모든 컴포넌트에 fade + translate 애니메이션이 내장되어 있으며, `startFrom` prop으로 시작 시점을 조절한다.

### 콘텐츠 레이아웃 (SlideLayout 내부)

| 컴포넌트 | Props | 용도 |
|---------|-------|------|
| `TwoColumnSplit` | `leftTitle, leftSubtitle?, leftDesc?, leftGradient?, items[{label, desc}], ratio?, startFrom?` | 좌측 강조 패널 + 우측 번호 리스트 |
| `ComparisonPanels` | `left{label, title, items[], color, bgColor, icon?}, right{...}, centerBadge?` | 2열 비교 (Before/After, Do/Don't) |
| `CardGrid` | `items[{icon?, title, desc, accentColor?}], columns?(2/3/4), variant?("icon"/"mini"/"accent-top")` | 유연한 카드 그리드 |
| `FlowDiagram` | `steps[{icon, title, desc, highlight?}], banner?{icon?, text}` | 수평 순차 플로우 |
| `NumberedSteps` | `steps[{title, desc, tags?[]}]` | 세로 번호 스텝 |
| `BarChart` | `bars[{label, sublabel?, value, display, color?}], insight?{title, text}, maxValue?` | 수평 바 차트 + 인사이트 박스 |
| `ComparisonMatrix` | `columns[{name, color?}], rows[{feature, desc?, checks[]}], showTotals?` | 체크마크 비교 테이블 |
| `DefinitionList` | `items[{term, category?, categoryColor?, definition, example?}]` | 용어 + 정의 + 예시 |
| `CalloutStack` | `items[{type("tip"/"warning"/"info"/"error"), title, content, extra?}]` | TIP/WARNING/INFO 콜아웃 |
| `QnAList` | `items[{question, answer}]` | Q&A 쌍 |
| `Quote` | `text, author, role?, context?` | 큰 인용 + 저자 + 맥락 |
| `KeyTakeaways` | `items[{title, detail, accentColor?}], banner?{icon?, text}, columns?(2/3)` | 요약 그리드 + 배너 |
| `Timeline` | `events[{year, title, desc, color?}]` | 수평 타임라인 |
| `LayeredArchitecture` | `layers[{title, desc, tone?}], caption?, startFrom?` | 계층 구조를 아래에서 위로 쌓아 표현 (layers는 아래 계층부터 입력, 3~5개 권장) |
| `HubSpokeMap` | `hubTitle, hubDesc, spokes[{title, desc}], startFrom?` | 중심 개념과 주변 요소를 방사형으로 배치 (spokes는 최대 6개 표시) |
| `SwimlaneFlow` | `steps[{lane, title, desc}], startFrom?` | 주체(레인)별 단계 흐름을 가로로 펼침 (lane은 최대 4개, 같은 lane끼리 화살표 연결) |
| `SpectrumScale` | `items[{title, desc}], leftLabel?, rightLabel?, caption?, startFrom?` | 단순에서 복합으로 이어지는 스펙트럼 위에 항목을 번호로 배치 |
| `ModuleConstellation` | `centerTitle, centerDesc, nodes[{title, desc}], caption?, startFrom?` | 중심 모듈과 주변 모듈을 별자리형으로 배치 (nodes는 최대 6개 표시) |

### 독립 슬라이드 (SlideLayout 없이)

| 컴포넌트 | Props | 용도 |
|---------|-------|------|
| `CoverSlide` | `topLabel?, title, subtitle?, date?, meta?, variant?("center"/"left")` | 과정 표지 |
| `DividerSlide` | `number, title, subtitle?, items?[], duration?, variant?("left"/"center")` | 섹션 간지 |

### import 방법

```tsx
// barrel export로 한 줄 import
import { TwoColumnSplit, ComparisonPanels, CardGrid } from "../../components/layouts";

// 신규 레이아웃도 같은 barrel에서 import
import { LayeredArchitecture, HubSpokeMap, SwimlaneFlow, SpectrumScale, ModuleConstellation } from "../../components/layouts";

// 독립 슬라이드
import { CoverSlide, DividerSlide } from "../../components/layouts";
```

> `LayeredArchitecture`, `SpectrumScale`, `ModuleConstellation`은 `colors.amber`, `colors.white`, `colors.clay`를 사용합니다.
> 템플릿 `theme.ts`에 이 색상이 포함되어 있으므로 별도 작업 없이 바로 사용할 수 있습니다.

## theme 확장

`theme.ts`는 슬라이드 전반의 색상, 폰트, 간격을 정의합니다.

- **`fonts.mono`** — 코드/명령어 표기에 쓰는 고정폭 글꼴 스택입니다. `AnnotatedCode`, `HandsOnSlide` 등 코드 표기가 있는 컴포넌트에서 사용할 수 있습니다.
- **조밀 spacing 변형** — 콘텐츠가 많아 한 화면에 넣기 어려울 때 `spacing` 값을 줄인 변형을 쓸 수 있습니다. 적용 판단 기준은 `design-judgment.md`를 참조하십시오.

## 이미지 슬라이드 패턴

## 이미지 슬라이드 패턴

image-gen 스킬로 생성한 삽화를 슬라이드에 배치하는 패턴.

### SlideLayout 콘텐츠 영역 계산

```
전체: 1920 x 1080
padding: 80px (spacing.page) 상하좌우 → 가용: 1760 x 920

헤더 (sectionLabel + title + subtitle):
  sectionLabel: 22px + marginBottom 12 = ~34px
  title h1: 56px * 1.3 = ~73px
  subtitle: marginTop 12 + 28px * 1.5 = ~54px
  합계: ~161px

children marginTop: 48px (spacing.section)

콘텐츠 영역: 1760 x 711px (비율 약 2.48:1)
```

### 권장 이미지 비율

Gemini API는 고정 비율만 지원. 콘텐츠 영역(2.48:1)에 가장 가까운 것은 **21:9 (2.33:1)**.

```bash
# image-gen 스킬로 슬라이드 삽화 생성 시
--aspect-ratio 21:9 --resolution 2K
```

### 컴포넌트 코드

```tsx
import { staticFile, Img } from "remotion";
import { SlideLayout } from "../../components/SlideLayout";

export const S03_Example: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(
    frame, [0.2 * fps, 0.6 * fps], [0, 1],
    { extrapolateRight: "clamp", extrapolateLeft: "clamp" },
  );
  const scale = interpolate(
    frame, [0.2 * fps, 0.6 * fps], [0.95, 1],
    { extrapolateRight: "clamp", extrapolateLeft: "clamp" },
  );

  return (
    <SlideLayout title="제목" subtitle="설명" sectionLabel="SECTION">
      <div style={{
        flex: 1,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        overflow: "hidden",
        opacity,
        transform: `scale(${scale})`,
      }}>
        <Img
          src={staticFile("images/example.png")}
          style={{ width: "95%", objectFit: "contain", borderRadius: 12 }}
        />
      </div>
    </SlideLayout>
  );
};
```

**핵심 포인트:**
- `width: "95%"` — 페이지 번호와 겹침 방지 (100%면 하단 잘림)
- `overflow: "hidden"` — 만약의 넘침 방지
- `objectFit: "contain"` — 비율 유지
- 이미지 파일은 `public/images/`에 저장
- Img 컴포넌트에 `maxHeight: "100%"` 추가 권장 (오버플로우 방지)

### 이미지 소싱 워크플로우

슬라이드에 필요한 이미지는 유형에 따라 도구를 선택한다.

#### 도구 선택 기준

| 이미지 유형 | 도구 | 설정 | 예시 |
|------------|------|------|------|
| 개념 다이어그램, 아키텍처, 비유 삽화 | `image-gen` 스킬 | `--model 3.1 --aspect-ratio 21:9 --resolution 2K` | Agent 구조도, RAG 파이프라인, OAuth 흐름 |
| 실제 UI 스크린샷 | 브라우저 자동화 도구 | viewport `1920x800` | n8n 캔버스, 노드 설정 화면, 실행 결과 |
| 코드/터미널 출력 | `CodeBlock` 컴포넌트 | — | 꼭 필요한 경우만 (스크린샷 우선) |

#### image-gen 삽화 생성

프로젝트별 `tone-guide.md`를 `public/` 또는 프로젝트 루트에 배치한다. tone-guide가 없으면 첫 이미지 생성 시 자동 생성한다.

```bash
# 삽화 생성 (Gemini 3.1, 21:9 2K)
# image-gen 스킬 호출 시 자동으로 tone-guide.md 참조
```

생성된 이미지는 `public/images/`에 저장하고, 프롬프트는 `public/images/<파일명>.prompt.md`로 함께 보관한다.

#### 브라우저 자동화 스크린샷 캡처

실제 서비스 UI를 고화질로 캡처한다. 브라우저 자동화 도구로 뷰포트를 1920x800으로 맞춘 뒤 캡처한다.

```bash
# 브라우저 세션 시작 후
set viewport 1920 800          # 슬라이드 비율에 맞는 와이드 뷰포트 (세션 유지)

# CSS zoom이 필요한 경우 (UI가 작게 보일 때)
eval "document.body.style.zoom='1.5'"   # 페이지 이동 시 매번 재설정 필요
```

**주의사항:**
- `set viewport`는 세션 동안 유지, CSS zoom은 페이지별 재적용
- 기본 viewport 1280x720은 슬라이드(1920x1080)보다 작아 흐림 — 반드시 1920x800 설정
- 캡처 결과 비율: 1920x800 = 2.4:1 (슬라이드 콘텐츠 영역 2.48:1과 거의 동일)
- AI 생성 삽화(3168x1344 = 2.36:1)와도 비율 호환

#### 이미지 파일 관리

```
public/images/
├── lo1-interface.png              ← 스크린샷 (브라우저 자동화)
├── lo3-agent-architecture.png     ← 삽화 (image-gen)
├── lo3-agent-architecture.prompt.md  ← 프롬프트 보관
└── tone-guide.md                  ← 프로젝트 스타일 가이드
```

## 코드 슬라이드 라인 제한

CodeBlock이 SlideLayout 콘텐츠 영역(711px)을 넘지 않도록 라인 수를 제한한다.

### 최대 라인 수 (title bar 포함 기준)

| fontSize | 행 높이 | 최대 라인 |
|----------|---------|----------|
| 20 | 32px | **19줄** |
| 18 | 28.8px | **21줄** |
| 17 | 27.2px | **23줄** |
| 16 | 25.6px | **24줄** |

> 2컬럼 레이아웃이면 높이가 더 제한될 수 있으므로 여유 2~3줄 확보.

### 넘칠 때 대응: 중략 패턴

반복 구조는 한 줄로 압축하거나 `// ... (동일 패턴)` 주석으로 생략한다.

```groovy
// Before (39줄 — 넘침)
stage('Install') {
    steps {
        dir('apps/backend') {
            sh 'npm install'
        }
    }
}

// After (한 줄 압축)
stage('Install') {
    steps { dir('apps/backend') { sh 'npm install' } }
}
```

### sourceRef — 파일명 표시

`sourceRef` prop으로 코드블록 우측 하단에 원본 파일명을 표시한다.
풀 URL은 변경될 수 있으므로 상대 파일명만 사용.

```tsx
<CodeBlock
  code={code}
  language="groovy"
  title="Jenkinsfile"
  sourceRef="Jenkinsfile (backend)"
/>
```
