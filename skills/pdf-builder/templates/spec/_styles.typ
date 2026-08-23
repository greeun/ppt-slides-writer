// ============================================================
// 스펙 문서 스타일 템플릿
// ============================================================
// 용도: 기능 요구사항 문서 (core-features 기반)
// 복사: cp -r templates/spec docs/specs/{feature}/typst
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

// 상태 색상
#let status-implemented = rgb("#059669")
#let status-partial = rgb("#ea580c")
#let status-not-implemented = rgb("#6b7280")

// ============================================================
// 상태 배지 컴포넌트
// ============================================================
#let status-badge(status) = {
  let (color, text-label) = if status == "implemented" {
    (status-implemented, "구현됨")
  } else if status == "partial" {
    (status-partial, "부분 구현")
  } else {
    (status-not-implemented, "미구현")
  }

  box(
    fill: color.lighten(85%),
    stroke: 0.5pt + color,
    inset: (x: 8pt, y: 3pt),
    radius: 4pt,
  )[
    #text(fill: color, weight: "bold", size: 8pt)[#text-label]
  ]
}

// ============================================================
// 버전 배지 컴포넌트
// ============================================================
#let version-badge(version) = {
  box(
    fill: accent-purple.lighten(90%),
    stroke: 0.5pt + accent-purple,
    inset: (x: 6pt, y: 2pt),
    radius: 3pt,
  )[
    #text(fill: accent-purple, size: 7pt)[#version]
  ]
}

// ============================================================
// 기능 카드 컴포넌트 (기본)
// ============================================================
#let feature-card(id, name, description, status, target-version, details) = {
  box(
    width: 100%,
    inset: 0pt,
    stroke: none,
  )[
    // 헤더
    #box(
      width: 100%,
      fill: bg-blue,
      inset: (x: 12pt, y: 10pt),
      radius: (top: 6pt),
    )[
      #grid(
        columns: (auto, 1fr, auto, auto),
        gutter: 10pt,
        align: (left, left, right, right),
        box(fill: accent-blue, inset: (x: 8pt, y: 4pt), radius: 4pt)[
          #text(fill: white, weight: "bold", size: 9pt)[#id]
        ],
        text(weight: "bold", size: 10pt)[#name],
        status-badge(status),
        version-badge(target-version),
      )
    ]
    // 본문
    #box(
      width: 100%,
      fill: white,
      inset: (x: 12pt, y: 10pt),
      radius: (bottom: 6pt),
      stroke: (bottom: 0.5pt + rgb("#e5e7eb"), left: 0.5pt + rgb("#e5e7eb"), right: 0.5pt + rgb("#e5e7eb")),
    )[
      #text(size: 9pt)[#description]

      #if details != none [
        #v(6pt)
        #text(size: 8pt, fill: accent-gray)[
          *목적:* #details.at("purpose", default: "-")
        ]
      ]
    ]
    #v(8pt)
  ]
}

// ============================================================
// 상세 기능 카드 (확장형) - 상태별 색상 차별화
// ============================================================
#let feature-card-detailed(id, name, description, status, target-version, details, components: ()) = {
  // 상태별 색상 정의
  let (header-bg, header-accent, border-color) = if status == "implemented" {
    (bg-green, status-implemented, status-implemented)
  } else if status == "partial" {
    (bg-orange, status-partial, status-partial)
  } else {
    (bg-light, accent-gray, accent-gray)
  }

  box(
    width: 100%,
    inset: 0pt,
    stroke: 1pt + border-color.lighten(50%),
    radius: 6pt,
  )[
    // 헤더
    #box(
      width: 100%,
      fill: header-bg,
      inset: (x: 12pt, y: 10pt),
      radius: (top: 5pt),
    )[
      #grid(
        columns: (auto, 1fr, auto, auto),
        gutter: 10pt,
        align: (left, left, right, right),
        box(fill: header-accent, inset: (x: 8pt, y: 4pt), radius: 4pt)[
          #text(fill: white, weight: "bold", size: 9pt)[#id]
        ],
        text(weight: "bold", size: 10pt)[#name],
        status-badge(status),
        version-badge(target-version),
      )
    ]
    // 본문
    #box(
      width: 100%,
      fill: white,
      inset: (x: 12pt, y: 10pt),
      radius: (bottom: 5pt),
    )[
      #text(size: 9pt, weight: "medium")[#description]

      #v(8pt)

      #if details != none [
        // 목적
        #if details.at("purpose", default: none) != none [
          #text(size: 8pt, fill: accent-gray)[*목적:* #details.purpose]
          #v(4pt)
        ]

        // 핵심 기능
        #if details.at("key_functions", default: none) != none [
          #text(size: 8pt, weight: "bold")[핵심 기능:]
          #for func in details.key_functions [
            #text(size: 8pt)[• #func]
            #linebreak()
          ]
          #v(4pt)
        ]

        // 기대 효과
        #if details.at("expected_benefits", default: none) != none [
          #text(size: 8pt, fill: status-implemented)[*기대 효과:* #details.expected_benefits]
        ]

        // 현재 구현 상태
        #if details.at("current_implementation", default: none) != none [
          #v(4pt)
          #box(
            fill: bg-green,
            inset: 6pt,
            radius: 4pt,
            width: 100%,
          )[
            #text(size: 8pt, fill: status-implemented)[*현재 구현:* #details.current_implementation]
          ]
        ]
      ]

      // 관련 컴포넌트
      #if components.len() > 0 [
        #v(4pt)
        #text(size: 7pt, fill: accent-gray)[
          관련 컴포넌트: #components.join(", ")
        ]
      ]
    ]
    #v(10pt)
  ]
}

// ============================================================
// 카테고리 헤더
// ============================================================
#let category-header(number, title, count, icon: "📦") = {
  box(
    width: 100%,
    fill: accent-blue.lighten(90%),
    inset: (x: 16pt, y: 12pt),
    radius: 6pt,
  )[
    #grid(
      columns: (auto, 1fr, auto),
      align: (left, left, right),
      text(size: 18pt)[#icon],
      text(size: 14pt, weight: "bold", fill: accent-blue)[
        #number. #title
      ],
      text(size: 10pt, fill: accent-gray)[#count개 기능],
    )
  ]
  v(1em)
}

// ============================================================
// 요약 테이블 행
// ============================================================
#let summary-row(id, name, status, version) = {
  (
    text(weight: "medium")[#id],
    text[#name],
    status-badge(status),
    version-badge(version),
  )
}

// ============================================================
// 진행률 바 컴포넌트
// ============================================================
#let progress-bar(implemented, partial, total, label: "") = {
  let impl-pct = implemented / total * 100
  let partial-pct = partial / total * 100
  let not-impl-pct = 100 - impl-pct - partial-pct

  box(
    width: 100%,
    inset: 0pt,
  )[
    #if label != "" [
      #text(size: 9pt, weight: "medium")[#label]
      #h(1fr)
      #text(size: 9pt, fill: accent-gray)[#implemented + #partial / #total]
      #v(4pt)
    ]
    #box(
      width: 100%,
      height: 12pt,
      radius: 6pt,
      fill: bg-light,
      clip: true,
    )[
      #stack(
        dir: ltr,
        box(width: impl-pct * 1%, height: 100%, fill: status-implemented),
        box(width: partial-pct * 1%, height: 100%, fill: status-partial),
        box(width: not-impl-pct * 1%, height: 100%, fill: rgb("#e5e7eb")),
      )
    ]
  ]
}

// ============================================================
// 카테고리 미니 진행률
// ============================================================
#let category-progress(icon, name, implemented, partial, total) = {
  let completed = implemented + partial
  box(
    width: 100%,
    fill: bg-light,
    inset: 10pt,
    radius: 6pt,
  )[
    #grid(
      columns: (auto, 1fr, auto),
      gutter: 8pt,
      align: (left, left, right),
      text(size: 14pt)[#icon],
      [
        #text(size: 9pt, weight: "medium")[#name]
        #v(2pt)
        #box(
          width: 100%,
          height: 6pt,
          radius: 3pt,
          fill: rgb("#e5e7eb"),
          clip: true,
        )[
          #stack(
            dir: ltr,
            box(width: (implemented / total * 100) * 1%, height: 100%, fill: status-implemented),
            box(width: (partial / total * 100) * 1%, height: 100%, fill: status-partial),
          )
        ]
      ],
      text(size: 8pt, fill: accent-gray)[#implemented + #partial / #total],
    )
  ]
}
