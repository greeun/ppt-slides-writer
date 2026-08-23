// ============================================================
// 카탈로그 문서 스타일 템플릿
// ============================================================
// 용도: Q&A 형식 카탈로그 문서 (query-catalog 기반)
// 복사: cp -r templates/catalog docs/specs/{catalog}/typst
// ============================================================

// 색상 정의
#let accent-blue = rgb("#2563eb")
#let accent-green = rgb("#059669")
#let accent-red = rgb("#dc2626")
#let accent-purple = rgb("#7c3aed")
#let accent-orange = rgb("#ea580c")
#let accent-gray = rgb("#6b7280")
#let bg-light = rgb("#f8fafc")
#let bg-blue = rgb("#eff6ff")
#let bg-green = rgb("#f0fdf4")
#let bg-red = rgb("#fef2f2")
#let bg-purple = rgb("#faf5ff")
#let bg-orange = rgb("#fff7ed")

// ============================================================
// 질문 카드 컴포넌트
// ============================================================
// 사용법:
// #qcard(
//   "Q01",
//   "질문 내용",
//   "응답 블록 타입",
//   "응답 내용",
//   color: accent-blue,
//   bg: bg-blue,
// )
// ============================================================
#let qcard(number, question, blocks, response, color: accent-blue, bg: bg-blue) = {
  box(
    width: 100%,
    inset: 0pt,
    stroke: none,
  )[
    #box(
      width: 100%,
      fill: bg,
      inset: (x: 12pt, y: 10pt),
      radius: (top: 6pt),
    )[
      #grid(
        columns: (auto, 1fr, auto),
        gutter: 10pt,
        align: (left, left, right),
        box(fill: color, inset: (x: 8pt, y: 4pt), radius: 4pt)[
          #text(fill: white, weight: "bold", size: 9pt)[#number]
        ],
        text(weight: "bold", size: 10pt)[#question],
        text(size: 8pt, fill: rgb("#6b7280"))[#blocks],
      )
    ]
    #box(
      width: 100%,
      fill: white,
      inset: (x: 12pt, y: 10pt),
      radius: (bottom: 6pt),
      stroke: (bottom: 0.5pt + rgb("#e5e7eb"), left: 0.5pt + rgb("#e5e7eb"), right: 0.5pt + rgb("#e5e7eb")),
    )[
      #text(size: 9pt)[#response]
    ]
    #v(8pt)
  ]
}

// ============================================================
// 섹션 헤더
// ============================================================
#let section(title, icon, color) = {
  heading(level: 1)[#title]
  v(-0.5em)
  box(
    width: 100%,
    fill: color.lighten(90%),
    inset: 12pt,
    radius: 6pt,
  )[
    #text(size: 14pt, weight: "bold", fill: color)[#icon #title]
  ]
  v(0.5em)
}

// ============================================================
// 카테고리별 색상 프리셋
// ============================================================
// 라이선스 관련
#let license-color = accent-blue
#let license-bg = bg-blue

// 조직/사용자 관련
#let org-color = accent-green
#let org-bg = bg-green

// 모니터링/알림 관련
#let monitor-color = accent-orange
#let monitor-bg = bg-orange

// 자산 관련
#let asset-color = accent-purple
#let asset-bg = bg-purple

// 경고/위험 관련
#let warning-color = accent-red
#let warning-bg = bg-red

// ============================================================
// 응답 블록 타입 배지
// ============================================================
#let block-badge(block-type) = {
  let (color, label) = if block-type == "chart" {
    (accent-blue, "📊 Chart")
  } else if block-type == "table" {
    (accent-green, "📋 Table")
  } else if block-type == "summary" {
    (accent-purple, "📝 Summary")
  } else if block-type == "insight" {
    (accent-orange, "💡 Insight")
  } else if block-type == "alert" {
    (accent-red, "⚠️ Alert")
  } else {
    (accent-gray, block-type)
  }

  box(
    fill: color.lighten(85%),
    stroke: 0.5pt + color,
    inset: (x: 6pt, y: 2pt),
    radius: 3pt,
  )[
    #text(fill: color, weight: "medium", size: 7pt)[#label]
  ]
}
