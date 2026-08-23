// ========================================
// 보고서 표지 + 목차 템플릿
// ========================================
// 수정 대상:
// - 메인 타이틀
// - 서브 타이틀
// - 문서 설명
// - 메타 정보 (프로젝트, 작성일, 작성자 등)
// ========================================

// ========================================
// 표지 페이지
// ========================================
#page(
  margin: (top: 50mm, bottom: 30mm, left: 25mm, right: 25mm),
  header: none,
  footer: none,
  numbering: none,
)[
  #align(center)[
    #v(3cm)

    // 메인 타이틀 - 수정 필요
    #text(size: 28pt, weight: "bold")[문서 제목]

    #v(0.5cm)

    // 서브 타이틀 - 수정 필요
    #text(size: 20pt, weight: "bold")[부제목을 입력하세요]

    #v(1cm)

    // 문서 설명 - 수정 필요
    #text(size: 14pt)[문서 설명]

    #v(3cm)

    // 메타 정보 - 수정 필요
    #table(
      columns: (auto, auto),
      align: (right, left),
      stroke: none,
      inset: 6pt,
      [*프로젝트*], [Project Name],
      [*작성일*], [2026-01-23],
      [*작성*], [팀/부서명],
      [*작성자*], [작성자명],
    )

    #v(1fr)

    #text(size: 10pt, fill: luma(120))[Internal Document]
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
