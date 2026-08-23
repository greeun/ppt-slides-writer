# 레이아웃 라이브러리

> remotion-slide-builder `SKILL.md`에서 원문 그대로 이동한 섹션 모음 (SKILL.md 500줄 제한 준수 목적).
> Phase 5 Polish의 표준 레이아웃 패턴·카드 내부 공통 구조, 레이아웃 컴포넌트 라이브러리, 컴포넌트 업데이트 메모.

### 표준 레이아웃 패턴

Polish 시 아래 패턴에 맞는지 확인한다. 내부 콘텐츠는 자유롭되, 외형 프레임은 통일한다.

| 패턴 | 프레임 규격 | 용도 |
|------|-----------|------|
| N열 카드 (2-4열) | padding 32, borderTop 5px color, borderRadius 16, gap 28, flex:1 | 개념 비교, 프로세스, 역할 비교 |
| 비대칭 카드 | 프레임 동일, 내부 구조 다름 허용 | 좌우 성격이 다른 2개 영역 |
| 수평 행 카드 | flex:1로 행 높이 균등, borderLeft 5px, padding 20-28px | 성숙도 모델, 계층 비교 |
| 하단 요약 박스 | padding 16px 이상, borderRadius 16, borderLeft 5px, font 22px 이상 | 인용, 공식, 핵심 메시지 |
| DataTable | 컴포넌트 자체 규격 사용 | 비교표, 체크리스트 |
| 이미지 풀스크린 | flex:1, objectFit contain, borderRadius 12 | 다이어그램, 스크린샷 |
| CodeBlock | fontSize 20px 이상, 컴포넌트 자체 규격 | 코드 예시 |

### 카드 내부 공통 구조

```
제목 (h3, fontWeight 700, 컬러)
subtitle (body-4, textLight, italic)          ← 선택
───────────────────────────────────          ← 구분선 (border 색상)
본문 설명 (body-4, textLight, lineHeight 1.7)
뱃지/태그 (배경 컬러 10%, border 컬러 25%)   ← 선택
항목 리스트 (flex:1로 남은 공간 채움)
```

## 레이아웃 컴포넌트 라이브러리

슬라이드 제작의 기본 방식은 **레이아웃 컴포넌트 + props 조립**이다.
하드코딩된 스타일 대신, `components/layouts/`의 재사용 컴포넌트에 데이터를 전달하여 슬라이드를 구성한다.

### 사용 패턴

```tsx
import { SlideLayout } from "../components/SlideLayout";
import { ComparisonPanels } from "../components/layouts";

// 데이터만 전달 — 레이아웃/애니메이션은 컴포넌트가 담당
export const S03_Comparison: React.FC = () => (
  <SlideLayout title="개발 패러다임의 전환" source="GitHub, 2024">
    <ComparisonPanels
      left={{ label: "BEFORE", title: "전통적 개발", items: [...], color: "#EF4444", bgColor: "#FEF2F2" }}
      right={{ label: "AFTER", title: "AI 시대 개발", items: [...], color: "#10B981", bgColor: "#F0FDF4" }}
    />
  </SlideLayout>
);
```

### 컴포넌트 구성

**래퍼**: `SlideLayout` (기존, 제목/출처/페이지번호 담당)

**콘텐츠 레이아웃** (`components/layouts/`, SlideLayout 내부에서 사용):

| 컴포넌트 | 용도 | 주요 Props |
|---------|------|-----------|
| `TwoColumnSplit` | 좌측 강조 패널 + 우측 리스트 | `leftTitle, leftDesc, items[]` |
| `ComparisonPanels` | 2열 비교 (Before/After, Do/Don't) | `left{}, right{}, centerBadge` |
| `CardGrid` | 유연한 카드 그리드 | `items[], columns, variant("icon"/"mini"/"accent-top")` |
| `FlowDiagram` | 수평 순차 플로우 | `steps[], banner?` |
| `NumberedSteps` | 세로 번호 스텝 | `steps[{title, desc, tags?}]` |
| `BarChart` | 수평 바 차트 + 인사이트 | `bars[], insight?` |
| `ComparisonMatrix` | 체크마크 비교 테이블 | `columns[], rows[], showTotals` |
| `DefinitionList` | 용어 + 정의 + 예시 | `items[{term, category?, definition, example?}]` |
| `CalloutStack` | TIP/WARNING/INFO 콜아웃 | `items[{type, title, content, extra?}]` |
| `QnAList` | Q&A 쌍 | `items[{question, answer}]` |
| `Quote` | 큰 인용 + 저자 + 맥락 | `text, author, role?, context?` |
| `KeyTakeaways` | 2x2 요약 그리드 + 배너 | `items[], banner?, columns` |
| `Timeline` | 수평 타임라인 | `events[{year, title, desc}]` |

**독립 슬라이드** (SlideLayout 없이 단독 사용):

| 컴포넌트 | 용도 | 주요 Props |
|---------|------|-----------|
| `CoverSlide` | 과정 표지 | `title, subtitle, date, meta, variant("center"/"left")` |
| `DividerSlide` | 섹션 간지 | `number, title, items[], variant("left"/"center")` |

### 기존 원자 컴포넌트와 혼합

레이아웃 컴포넌트와 기존 원자 컴포넌트(`ConceptCard`, `StatCard`, `DataTable`, `CodeBlock` 등)를 자유롭게 조합할 수 있다.

```tsx
<SlideLayout title="Constitution 파일 작성법" source="교육팀, 2025">
  <div style={{ display: "flex", gap: 32, flex: 1 }}>
    <CodeBlock title="constitution.md" code={`...`} />    {/* 기존 원자 */}
    <NumberedSteps steps={[...]} />                        {/* 레이아웃 */}
  </div>
</SlideLayout>
```

### 슬라이드 제작 우선순위

1. **레이아웃 컴포넌트 먼저** — 매칭되는 레이아웃이 있으면 사용
2. **기존 원자 컴포넌트** — ConceptCard, StatCard, DataTable 등 단독 사용
3. **혼합 조합** — 레이아웃 + 원자를 flex로 배치
4. **커스텀** — 위 3가지로 불가능한 경우에만 인라인 스타일 작성

### 샘플 갤러리

`src/slides/_samples/` 폴더에 30개 샘플이 있다. 19개는 레이아웃 컴포넌트로 전환 완료. 새 슬라이드 제작 시 참고용으로 활용한다.

```bash
npx remotion studio  # samples 폴더에서 30개 패턴 미리보기
```

## 컴포넌트 업데이트 메모

### CheckpointSlide

- `subtitle` prop 지원 (string, optional)
- 기본값: "다음 섹션으로 넘어가기 전에 확인합니다"
- 커스텀 자막이 필요한 경우 override 가능

### InstructorSlide 디자인 패턴

권장 레이아웃 (Layout A):
- **상단**: 3-4열 임팩트 숫자 (경력 연수, 교육 실적, 전문 분야 등)
- **하단**: 2열 구성 (좌: 경력 타임라인 | 우: 주요 고객사/성과)
- 데이터 소스: 해당 CU의 강사 프로필 문서를 참조

### SlideLayout source prop

- `source` prop (string, optional) 추가됨
- 위치: **좌측 하단**, 14px 회색 텍스트, 좌측 정렬
- 페이지 번호는 **우측 하단**에 별도 배치
- 모든 콘텐츠 슬라이드(Divider/Checkpoint 제외)에 사용

