// ========================================
// 표지 페이지
// 프로젝트별로 내용 수정 필요
// ========================================
#page(
  margin: (top: 50mm, bottom: 30mm, left: 25mm, right: 25mm),
  header: none,
  footer: none,
  numbering: none,
)[
  #align(center)[
    // 로고 (있으면 활성화)
    // #image("logo.png", width: 30%)

    #v(3cm)

    // 메인 타이틀 (수정 필요)
    #text(size: 28pt, weight: "bold")[프로젝트 제목]

    #v(0.5cm)

    #text(size: 28pt, weight: "bold")[보고서 제목]

    #v(1cm)

    #text(size: 14pt)[부제목 또는 버전]

    #v(3cm)

    // 메타 정보 (수정 필요)
    #table(
      columns: (auto, auto),
      align: (right, left),
      stroke: none,
      inset: 6pt,
      [*프로젝트*], [프로젝트명],
      [*작성일*], [YYYY-MM-DD],
      [*버전*], [v1.0],
      [*작성*], [Frentis],
    )

    #v(1fr)

    #text(size: 10pt, fill: luma(120))[Confidential - Internal Use Only]
  ]
]

// ========================================
// 목차 페이지
// ========================================
#page(
  header: none,
  footer: none,
  numbering: none,
)[
  #outline(
    title: [목차],
    indent: 1.5em,
    depth: 3,
  )
]

#pagebreak()
