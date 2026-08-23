# 레이아웃 패턴

`components/layouts/` 컴포넌트를 활용한 슬라이드 구성 패턴.
레이아웃 컴포넌트가 있으면 우선 사용하고, 없는 경우에만 인라인 스타일로 커스텀 작성한다.

> 30개 샘플이 `src/slides/_samples/`에 있다. Remotion Studio에서 미리보기 가능.

## 레이아웃 선택 가이드

| 콘텐츠 유형 | 레이아웃 컴포넌트 | 예시 |
|-----------|----------------|------|
| 핵심 개념 + 근거 리스트 | `TwoColumnSplit` | SDD 원칙, 도구 특징 |
| 전후 비교, 장단점 | `ComparisonPanels` | Before/After, Do/Don't |
| 기능 목록, 원칙 나열 | `CardGrid` | 8가지 핵심 기능, 6원칙 |
| 프로세스, 워크플로우 | `FlowDiagram` | OpenSpec 5단계 |
| 절차, 설치 가이드 | `NumberedSteps` | 프로젝트 시작 4단계 |
| 도구/성능 비교 데이터 | `BarChart` | AI 도구 효율 비교 |
| 다항목 기능 비교 | `ComparisonMatrix` | 도구별 기능 체크표 |
| 용어집, 개념 정의 | `DefinitionList` | SDD 핵심 용어 4개 |
| 주의사항, 실습 준비 | `CalloutStack` | TIP/WARNING/INFO |
| FAQ, 오해 교정 | `QnAList` | 자주 묻는 질문 |
| 전문가 인용 | `Quote` | CEO 발언, 연구 결과 |
| 섹션 마무리, 핵심 정리 | `KeyTakeaways` | 4가지 핵심 원칙 |
| 연혁, 발전사 | `Timeline` | AI 코딩 도구 진화 |
| 과정 표지 | `CoverSlide` | 교육과정 첫 장 |
| 섹션 구분 | `DividerSlide` | LO 시작 간지 |

## 혼합 레이아웃

레이아웃 컴포넌트와 기존 원자 컴포넌트를 flex로 조합한다.

### 코드 + 설명 (2컬럼)

```tsx
<SlideLayout title="Constitution 파일 작성법" source="...">
  <div style={{ display: "flex", gap: 32, flex: 1 }}>
    <div style={{ flex: 1 }}>
      <CodeBlock title="constitution.md" code={`...`} />
    </div>
    <div style={{ flex: 1 }}>
      <NumberedSteps steps={[...]} />
    </div>
  </div>
</SlideLayout>
```

### 통계 + 테이블 (세로 분할)

```tsx
<SlideLayout title="SDD 도입 효과" source="...">
  <div style={{ display: "flex", flexDirection: "column", gap: 24, flex: 1 }}>
    <StatCard items={[...]} columns={3} />
    <DataTable headers={[...]} rows={[...]} compact />
  </div>
</SlideLayout>
```

### 카드 + 콜아웃 (세로 분할)

```tsx
<SlideLayout title="실습 준비" source="...">
  <div style={{ display: "flex", flexDirection: "column", gap: 20, flex: 1 }}>
    <ConceptCard items={[...]} columns={3} />
    <CalloutStack items={[
      { type: "info", title: "필수 설치", content: "..." },
      { type: "tip", title: "실습 팁", content: "..." },
    ]} />
  </div>
</SlideLayout>
```

## 커스텀 레이아웃 (컴포넌트 없는 경우)

레이아웃 컴포넌트로 커버되지 않는 패턴은 인라인으로 직접 작성한다.

### 흰색 패널 컨테이너

```tsx
<div style={{
  background: "#FFFFFF",
  borderRadius: 16,
  padding: 24,
  boxShadow: "0 2px 12px rgba(30,58,95,0.08)",
  flex: 1,
}}>
  {/* 콘텐츠 */}
</div>
```

### 하단 배너

```tsx
<div style={{
  background: "linear-gradient(135deg, #1E3A5F, #2C5282)",
  borderRadius: 12,
  padding: "16px 32px",
  marginTop: 16,
}}>
  <div style={{ color: "#FFFFFF", fontSize: 20, fontWeight: 600, textAlign: "center" }}>
    핵심 메시지
  </div>
</div>
```

### 조합 프레임

```
┌─ SlideLayout (title, sectionLabel) ──────────────────────────┐
│                                                               │
│  ┌─ 레이아웃 컴포넌트 또는 flex 조합 ──────────────────────┐ │
│  │ TwoColumnSplit / ComparisonPanels / CardGrid / ...       │ │
│  │ 또는: CodeBlock + NumberedSteps (flex 조합)              │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                               │
│  ┌─ 하단 배너 (선택) ──────────────────────────────────────┐ │
│  │ KeyTakeaways의 banner prop 또는 커스텀 div              │ │
│  └──────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────┘
```
