// Frentis Proposal 스타일 (Quarto template-partial)
// 디자인 토큰: frentis-base.typ과 동일

// ===== 디자인 토큰 =====
#let c = (
  primary: rgb("#1a365d"),
  secondary: rgb("#2d3748"),
  muted: rgb("#718096"),
  text: rgb("#1a202c"),
  table-header: rgb("#e2e8f0"),
  table-border: rgb("#cbd5e0"),
  code-bg: rgb("#f7fafc"),
  code-border: rgb("#e2e8f0"),
  link: rgb("#2b6cb0"),
)

// ===== 페이지 설정 =====
#set page(
  paper: "a4",
  margin: (top: 25mm, bottom: 25mm, left: 20mm, right: 20mm),
)

// ===== 폰트 설정 =====
#set text(
  font: ("Pretendard", "Apple SD Gothic Neo"),
  size: 11pt,
  lang: "ko",
  fill: c.text,
)

// ===== 단락 설정 =====
#set par(leading: 1.3em, spacing: 1.2em, justify: true)

// ===== 제목 =====
#set heading(numbering: "1.1.1")

#show heading.where(level: 1): it => {
  v(1.5em)
  text(size: 16pt, weight: "bold", fill: c.primary, it)
  v(0.8em)
}

#show heading.where(level: 2): it => {
  v(1.2em)
  text(size: 13pt, weight: "bold", fill: c.secondary, it)
  v(0.5em)
}

#show heading.where(level: 3): it => {
  v(1em)
  text(size: 11pt, weight: "bold", fill: c.secondary, it)
  v(0.3em)
}

// ===== 표 (파란 헤더) =====
#show table: it => block(width: 100%, it)
#set table(
  inset: (x: 10pt, y: 8pt),
  stroke: 0.5pt + c.table-border,
  align: left,
  fill: (_, row) => if row == 0 { rgb("#2b6cb0") } else { none },
)
#show table.cell.where(y: 0): set text(weight: "bold", fill: white)

// ===== 리스트 =====
#set list(marker: ([•], [◦], [▪]), indent: 1.5em, body-indent: 0.5em)
#set enum(indent: 1.5em, body-indent: 0.5em)

// ===== 코드 블록 =====
#show raw.where(block: true): it => {
  set text(font: ("Monoplex KR Nerd", "Menlo"), size: 9pt)
  block(fill: c.code-bg, stroke: 0.5pt + c.code-border, inset: 12pt, radius: 4pt, width: 100%, it)
}

#show raw.where(block: false): it => {
  set text(font: ("Monoplex KR Nerd", "Menlo"), size: 0.9em)
  box(fill: rgb("#edf2f7"), inset: (x: 3pt, y: 1pt), radius: 2pt, it)
}

// ===== 링크 =====
#show link: it => { text(fill: c.link, it) }

// ===== 인용 블록 =====
#show quote: it => {
  block(fill: c.code-bg, inset: (left: 12pt, rest: 10pt), stroke: (left: 3pt + c.link), it)
}

// ===== Figure 캡션 =====
#set figure(gap: 1em)
#show figure.caption: it => { set text(size: 10pt, fill: c.muted); it }

// ===== 헤더/푸터 (3p부터) =====
#set page(
  header: context {
    if counter(page).get().first() > 2 {
      grid(
        columns: (1fr, 1fr),
        align: (left, right),
        text(size: 9pt, fill: c.muted)[],
        text(size: 9pt, fill: c.muted)[Frentis],
      )
      v(2pt)
      line(length: 100%, stroke: 0.5pt + c.table-border)
    }
  },
  footer: context {
    if counter(page).get().first() > 2 {
      align(center)[
        #text(size: 9pt, fill: c.muted)[#counter(page).display()]
      ]
    }
  },
)
