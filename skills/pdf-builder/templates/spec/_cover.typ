// ============================================================
// 스펙 문서 표지 템플릿
// ============================================================
// 수정 대상 변수:
// - project-name: 프로젝트명
// - doc-title: 문서 제목
// - doc-subtitle: 문서 부제목
// - doc-version: 문서 버전
// - doc-date: 작성일
// - doc-author: 작성자/팀
// - summary-stats: 상태 요약 통계 (implemented, partial, not-implemented)
// ============================================================

// 표지 페이지
#page(
  margin: (top: 50mm, bottom: 30mm, left: 25mm, right: 25mm),
  header: none,
  footer: none,
  numbering: none,
)[
  #align(center)[
    #v(3cm)

    // 메인 타이틀
    #text(size: 28pt, weight: "bold")[{{PROJECT_NAME}}]

    #v(0.5cm)

    #text(size: 20pt, weight: "bold")[{{DOC_TITLE}}]

    #v(0.3cm)

    #text(size: 14pt, fill: luma(100))[{{DOC_SUBTITLE}}]

    #v(3cm)

    // 메타 정보
    #table(
      columns: (auto, auto),
      align: (right, left),
      stroke: none,
      inset: 6pt,
      [*프로젝트*], [{{PROJECT_NAME}}],
      [*문서 버전*], [{{DOC_VERSION}}],
      [*작성일*], [{{DOC_DATE}}],
      [*작성*], [{{DOC_AUTHOR}}],
    )

    #v(1.5cm)

    // 상태 요약 (선택적 - 필요 시 사용)
    // implemented, partial, not-implemented 숫자를 수정하세요
    #box(
      fill: rgb("#f8fafc"),
      inset: 16pt,
      radius: 8pt,
    )[
      #grid(
        columns: (1fr, 1fr, 1fr),
        gutter: 20pt,
        align: center,
        [
          #text(size: 24pt, weight: "bold", fill: rgb("#059669"))[0]
          #linebreak()
          #text(size: 10pt, fill: luma(100))[구현 완료]
        ],
        [
          #text(size: 24pt, weight: "bold", fill: rgb("#ea580c"))[0]
          #linebreak()
          #text(size: 10pt, fill: luma(100))[부분 구현]
        ],
        [
          #text(size: 24pt, weight: "bold", fill: rgb("#6b7280"))[0]
          #linebreak()
          #text(size: 10pt, fill: luma(100))[미구현]
        ],
      )
    ]

    #v(1fr)

    #text(size: 10pt, fill: luma(120))[Internal Document]
  ]
]

// 목차 페이지
#page(
  header: none,
  footer: none,
  numbering: none,
)[
  #text(size: 18pt, weight: "bold")[목차]
  #v(1em)

  #show outline.entry.where(level: 1): it => {
    v(0.5em)
    strong(it)
  }

  #outline(
    title: none,
    indent: 1.5em,
    depth: 2,
  )
]

#pagebreak()
