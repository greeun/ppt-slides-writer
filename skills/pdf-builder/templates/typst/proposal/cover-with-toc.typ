// ============================================
// Frentis 제안서 표지 + 목차
// ============================================
// 수정 필요 항목:
//   - 영문 부제목 (line 15)
//   - 한글 제목 3줄 (line 19-25)
//   - 대상/범위 설명 (line 29)
//   - 표 내용: 발주처, 제안일, 사업규모, 버전 (line 35-40)
// ============================================

// ===== 표지 페이지 =====
#page(
  margin: (top: 50mm, bottom: 30mm, left: 25mm, right: 25mm),
  header: none,
  footer: none,
  numbering: none,
)[
  #align(center)[
    #v(2cm)

    // ▼▼▼ 영문 부제목 ▼▼▼
    #text(size: 16pt, fill: luma(80))[AI-Powered Platform Proposal]

    #v(0.5cm)

    // ▼▼▼ 한글 제목 (3줄) ▼▼▼
    #text(size: 28pt, weight: "bold")[프로젝트명]

    #v(0.3cm)

    #text(size: 28pt, weight: "bold")[시스템/서비스명]

    #v(0.3cm)

    #text(size: 28pt, weight: "bold")[구축 제안서]

    #v(1.5cm)

    // ▼▼▼ 대상/범위 설명 ▼▼▼
    #text(size: 14pt, fill: luma(100))[대상 기관 또는 범위 설명]

    #v(3cm)

    // ▼▼▼ 제안 정보 테이블 ▼▼▼
    #table(
      columns: (auto, auto),
      align: (right, left),
      stroke: none,
      inset: 8pt,
      [*발주처*], [발주 기관명],
      [*제안일*], [2026년 1월],
      [*사업규모*], [금액 / 기간],
      [*버전*], [v1.0],
    )

    #v(1fr)

    #text(size: 12pt, weight: "medium")[Frentis]

    #v(0.5cm)

    #text(size: 10pt, fill: luma(120))[Confidential]
  ]
]

// ===== 목차 페이지 =====
#page(
  header: none,
  footer: none,
  numbering: none,
)[
  #outline(
    title: [목차],
    indent: 1.5em,
    depth: 2,
  )
]

#pagebreak()
