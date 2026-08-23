// ============================================================
// 핸드아웃 문서 표지 템플릿
// ============================================================
// 수정 대상 변수 (main.typ에서 정의):
// - workshop-title: 워크샵 제목
// - workshop-subtitle: 부제목
// - workshop-date: 일시
// - workshop-presenter: 발표자
// - workshop-target: 대상
// - workshop-location: 장소 (선택)
// ============================================================

// 표지 페이지
#page(
  margin: (top: 40mm, bottom: 30mm, left: 25mm, right: 25mm),
  header: none,
  footer: none,
  numbering: none,
)[
  #align(center)[
    #v(2cm)

    // 워크샵 타이틀
    #box(
      fill: accent-blue,
      inset: (x: 24pt, y: 16pt),
      radius: 8pt,
    )[
      #text(size: 28pt, weight: "bold", fill: white)[#workshop-title]
    ]

    #v(1cm)

    // 부제목
    #text(size: 16pt, fill: accent-gray)[#workshop-subtitle]

    #v(2cm)

    // 메타 정보 박스
    #box(
      fill: bg-light,
      inset: 20pt,
      radius: 8pt,
      width: 80%,
    )[
      #table(
        columns: (auto, 1fr),
        align: (right, left),
        stroke: none,
        inset: 8pt,
        [#text(weight: "bold", fill: accent-gray)[📅 일시]], [#workshop-date],
        [#text(weight: "bold", fill: accent-gray)[👤 발표]], [#workshop-presenter],
        [#text(weight: "bold", fill: accent-gray)[🎯 대상]], [#workshop-target],
      )
    ]

    #v(1fr)

    // 타임라인 요약 (선택)
    #if workshop-sessions.len() > 0 [
      #box(
        width: 90%,
        stroke: 0.5pt + rgb("#e5e7eb"),
        radius: 6pt,
      )[
        #box(
          width: 100%,
          fill: bg-blue,
          inset: 10pt,
          radius: (top: 5pt),
        )[
          #text(weight: "bold", size: 11pt, fill: accent-blue)[📋 세션 구성]
        ]
        #box(
          width: 100%,
          inset: 12pt,
          radius: (bottom: 5pt),
        )[
          #for session in workshop-sessions [
            #grid(
              columns: (auto, 1fr, auto),
              gutter: 8pt,
              align: (left, left, right),
              text(size: 9pt, fill: accent-gray)[#session.time],
              text(size: 9pt, weight: "medium")[#session.title],
              text(size: 8pt, fill: accent-gray)[#session.duration],
            )
            #v(4pt)
          ]
        ]
      ]
    ]

    #v(1cm)

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
