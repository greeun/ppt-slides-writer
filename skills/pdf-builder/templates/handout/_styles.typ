// ============================================================
// 핸드아웃 문서 스타일 템플릿
// ============================================================
// 용도: 워크샵/교육 핸드아웃 문서
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
// 세션 헤더 컴포넌트
// ============================================================
#let session-header(number, title, duration, subtitle: none) = {
  box(
    width: 100%,
    fill: accent-blue,
    inset: (x: 16pt, y: 14pt),
    radius: 8pt,
  )[
    #grid(
      columns: (auto, 1fr, auto),
      gutter: 12pt,
      align: (left, left, right),
      box(
        fill: white,
        inset: (x: 10pt, y: 6pt),
        radius: 6pt,
      )[
        #text(fill: accent-blue, weight: "bold", size: 14pt)[세션 #number]
      ],
      [
        #text(fill: white, weight: "bold", size: 16pt)[#title]
        #if subtitle != none [
          #linebreak()
          #text(fill: white.transparentize(30%), size: 10pt)[#subtitle]
        ]
      ],
      box(
        fill: white.transparentize(80%),
        inset: (x: 8pt, y: 4pt),
        radius: 4pt,
      )[
        #text(fill: white, size: 10pt)[#duration]
      ],
    )
  ]
  v(1em)
}

// ============================================================
// 아젠다 테이블 컴포넌트
// ============================================================
#let agenda-table(items) = {
  table(
    columns: (auto, 1fr, auto),
    align: (left, left, center),
    fill: (_, row) => if row == 0 { bg-blue } else { white },
    stroke: 0.5pt + rgb("#e5e7eb"),
    inset: 10pt,
    [*시간*], [*주제*], [*소요*],
    ..items.map(item => (item.time, item.topic, item.duration)).flatten()
  )
  v(1em)
}

// ============================================================
// 체크리스트 박스 컴포넌트
// ============================================================
#let checklist-box(title, items, color: accent-blue) = {
  box(
    width: 100%,
    stroke: 1pt + color.lighten(50%),
    radius: 6pt,
  )[
    #box(
      width: 100%,
      fill: color.lighten(90%),
      inset: (x: 12pt, y: 8pt),
      radius: (top: 5pt),
    )[
      #text(weight: "bold", fill: color, size: 10pt)[#title]
    ]
    #box(
      width: 100%,
      fill: white,
      inset: 12pt,
      radius: (bottom: 5pt),
    )[
      #for item in items [
        #text(size: 9pt)[☐ #item]
        #linebreak()
      ]
    ]
  ]
  v(0.8em)
}

// ============================================================
// 아스키 다이어그램 박스 컴포넌트
// ============================================================
#let ascii-diagram(content, title: none) = {
  box(
    width: 100%,
    fill: bg-light,
    stroke: 0.5pt + rgb("#e5e7eb"),
    inset: 0pt,
    radius: 6pt,
  )[
    #if title != none [
      #box(
        width: 100%,
        fill: rgb("#e5e7eb"),
        inset: (x: 12pt, y: 6pt),
        radius: (top: 5pt),
      )[
        #text(weight: "bold", size: 9pt, fill: accent-gray)[#title]
      ]
    ]
    #box(
      width: 100%,
      inset: 12pt,
      radius: if title == none { 6pt } else { (bottom: 5pt) },
    )[
      #set text(font: ("Fira Code", "Menlo", "Monaco", "monospace"), size: 8pt)
      #content
    ]
  ]
  v(0.8em)
}

// ============================================================
// 토론 포인트 박스 컴포넌트
// ============================================================
#let discussion-box(title, items) = {
  box(
    width: 100%,
    fill: bg-orange,
    stroke: 1pt + accent-orange.lighten(50%),
    inset: 12pt,
    radius: 6pt,
  )[
    #text(weight: "bold", fill: accent-orange, size: 10pt)[💬 #title]
    #v(6pt)
    #for item in items [
      #text(size: 9pt)[• #item]
      #linebreak()
    ]
  ]
  v(0.8em)
}

// ============================================================
// 정보 테이블 컴포넌트
// ============================================================
#let info-table(rows, header-color: bg-blue) = {
  table(
    columns: (auto, 1fr),
    align: (right, left),
    fill: (col, _) => if col == 0 { header-color } else { white },
    stroke: 0.5pt + rgb("#e5e7eb"),
    inset: 10pt,
    ..rows.map(row => (
      text(weight: "bold", size: 9pt)[#row.at(0)],
      text(size: 9pt)[#row.at(1)]
    )).flatten()
  )
  v(0.8em)
}

// ============================================================
// 타임라인 아이템 컴포넌트
// ============================================================
#let timeline-item(time, title, duration, highlight: false) = {
  let bg = if highlight { bg-blue } else { white }
  let border = if highlight { accent-blue } else { rgb("#e5e7eb") }

  box(
    width: 100%,
    fill: bg,
    stroke: (left: 3pt + border),
    inset: (x: 12pt, y: 8pt),
  )[
    #grid(
      columns: (auto, 1fr, auto),
      gutter: 8pt,
      align: (left, left, right),
      text(weight: "bold", size: 9pt, fill: accent-gray)[#time],
      text(weight: if highlight { "bold" } else { "regular" }, size: 9pt)[#title],
      text(size: 8pt, fill: accent-gray)[#duration],
    )
  ]
}

// ============================================================
// 핵심 포인트 박스 컴포넌트
// ============================================================
#let key-point-box(title, content) = {
  box(
    width: 100%,
    fill: bg-green,
    stroke: 1pt + accent-green.lighten(50%),
    inset: 12pt,
    radius: 6pt,
  )[
    #text(weight: "bold", fill: accent-green, size: 10pt)[💡 #title]
    #v(6pt)
    #text(size: 9pt)[#content]
  ]
  v(0.8em)
}

// ============================================================
// 경고 박스 컴포넌트
// ============================================================
#let warning-box(content) = {
  box(
    width: 100%,
    fill: bg-red,
    stroke: 1pt + accent-red.lighten(50%),
    inset: 12pt,
    radius: 6pt,
  )[
    #text(weight: "bold", fill: accent-red, size: 10pt)[⚠️ 주의]
    #v(4pt)
    #text(size: 9pt)[#content]
  ]
  v(0.8em)
}

// ============================================================
// 참조 문서 테이블 컴포넌트
// ============================================================
#let reference-table(items) = {
  table(
    columns: (1fr, 2fr),
    align: (left, left),
    fill: (_, row) => if row == 0 { bg-blue } else { white },
    stroke: 0.5pt + rgb("#e5e7eb"),
    inset: 10pt,
    [*문서*], [*설명*],
    ..items.map(item => (item.name, item.description)).flatten()
  )
  v(0.8em)
}

// ============================================================
// 코드 블록 스타일
// ============================================================
#let code-block(content, lang: none) = {
  box(
    width: 100%,
    fill: rgb("#1e293b"),
    inset: 12pt,
    radius: 6pt,
  )[
    #if lang != none [
      #text(fill: rgb("#94a3b8"), size: 7pt)[#lang]
      #v(4pt)
    ]
    #set text(font: ("Fira Code", "Menlo", "Monaco"), size: 8.5pt, fill: rgb("#e2e8f0"))
    #content
  ]
  v(0.8em)
}

// ============================================================
// 비교 테이블 컴포넌트
// ============================================================
#let comparison-table(headers, rows) = {
  let num-cols = headers.len()
  table(
    columns: (1fr,) * num-cols,
    align: center,
    fill: (_, row) => if row == 0 { bg-blue } else { white },
    stroke: 0.5pt + rgb("#e5e7eb"),
    inset: 10pt,
    ..headers.map(h => text(weight: "bold", size: 9pt)[#h]),
    ..rows.flatten().map(cell => text(size: 9pt)[#cell])
  )
  v(0.8em)
}
