// 책 표지 + 목차
// 사용: include-before-body에서 호출

// ===== 표지 =====
#page(
  margin: 0pt,
  header: none,
  footer: none,
)[
  #box(
    width: 100%,
    height: 100%,
    fill: gradient.linear(
      rgb("#1a365d"),
      rgb("#2c5282"),
      angle: 135deg,
    ),
  )[
    #place(
      center + horizon,
      dx: 0pt,
      dy: -50pt,
    )[
      #block(
        width: 80%,
        [
          // 제목 (수정 필요)
          #align(center)[
            #text(
              size: 36pt,
              weight: "bold",
              fill: white,
            )[책 제목]
          ]

          #v(1em)

          // 부제목 (수정 필요)
          #align(center)[
            #text(
              size: 18pt,
              fill: rgb("#a0aec0"),
            )[부제목]
          ]

          #v(4em)

          // 저자 (수정 필요)
          #align(center)[
            #text(
              size: 14pt,
              fill: white,
            )[저자명]
          ]

          #v(2em)

          // 날짜
          #align(center)[
            #text(
              size: 12pt,
              fill: rgb("#a0aec0"),
            )[#datetime.today().display("[year]년 [month]월")]
          ]
        ]
      )
    ]

    // 하단 로고/회사명
    #place(
      bottom + center,
      dy: -40pt,
    )[
      #text(
        size: 14pt,
        fill: rgb("#718096"),
      )[Frentis]
    ]
  ]
]

// ===== 목차 =====
#page(
  header: none,
  footer: none,
)[
  #v(2em)
  #align(center)[
    #text(size: 24pt, weight: "bold", fill: rgb("#1a365d"))[목차]
  ]
  #v(2em)

  #outline(
    title: none,
    indent: 2em,
    depth: 2,
  )
]

// 본문 시작 전 페이지 브레이크
#pagebreak()
