// Frentis Catalog 템플릿 (Quarto template-partial)
// 디자인 토큰: frentis-base.typ과 동일

#let c = (
  primary: rgb("#1a365d"),
  secondary: rgb("#2d3748"),
  muted: rgb("#718096"),
  table-header: rgb("#e2e8f0"),
  table-border: rgb("#cbd5e0"),
  code-bg: rgb("#f7fafc"),
  code-border: rgb("#e2e8f0"),
  link: rgb("#2b6cb0"),
)

#let project(
  title: none,
  subtitle: none,
  authors: (),
  date: none,
  abstract: none,
  cols: 1,
  margin: (x: 2.5cm, y: 2.5cm),
  paper: "a4",
  lang: "ko",
  region: "KR",
  font: "Pretendard",
  fontsize: 10pt,
  sectionnumbering: none,
  toc: false,
  toc_title: "목차",
  toc_depth: 2,
  toc_indent: 1.5em,
  doc,
) = {
  set document(title: title)
  set page(
    paper: paper,
    margin: margin,
    numbering: "1",
    header: context {
      if counter(page).get().first() > 1 [
        #set text(9pt, fill: c.muted)
        #title
        #h(1fr)
        Frentis Education Catalog
      ]
    },
    footer: context {
      set text(9pt, fill: c.muted)
      h(1fr)
      counter(page).display("1")
      h(1fr)
    }
  )

  set text(font: ("Pretendard", "Apple SD Gothic Neo"), size: fontsize, lang: lang, region: region)
  set heading(numbering: sectionnumbering)
  set par(leading: 0.8em, spacing: 1.2em, justify: true)

  show heading.where(level: 1): it => {
    set text(18pt, weight: "bold", fill: c.primary)
    block(above: 2em, below: 1em)[#it]
  }
  show heading.where(level: 2): it => {
    set text(14pt, weight: "bold", fill: c.secondary)
    block(above: 1.5em, below: 0.8em)[#it]
  }
  show heading.where(level: 3): it => {
    set text(12pt, weight: "bold", fill: c.secondary)
    block(above: 1.2em, below: 0.6em)[#it]
  }

  set table(
    fill: (_, row) => if row == 0 { rgb("#2b6cb0") } else { none },
    stroke: 0.5pt + c.table-border,
    inset: 8pt,
  )

  show raw.where(block: true): it => {
    block(fill: c.code-bg, stroke: 0.5pt + c.code-border, inset: 10pt, radius: 4pt, width: 100%)[#it]
  }

  show raw.where(block: false): it => {
    box(fill: rgb("#edf2f7"), inset: (x: 4pt, y: 2pt), radius: 2pt)[#it]
  }

  show link: it => {
    set text(fill: c.link)
    underline(it)
  }

  set list(marker: ([•], [◦], [▪]), indent: 1.5em, body-indent: 0.5em)
  set enum(indent: 1.5em, body-indent: 0.5em)

  // 커버 페이지
  page(margin: 0cm, numbering: none)[
    #box(
      width: 100%,
      height: 100%,
      fill: gradient.linear(c.primary, c.link, angle: 135deg)
    )[
      #place(center + horizon)[
        #block(width: 80%)[
          #set text(fill: white)
          #v(2em)
          #text(size: 36pt, weight: "bold")[#title]
          #v(0.5em)
          #text(size: 24pt, weight: "light")[#subtitle]
          #v(3em)
          #line(length: 100%, stroke: 2pt + white.transparentize(50%))
          #v(3em)
          #text(size: 14pt)[
            #for author in authors [
              #author.name #h(1em)
            ]
          ]
          #v(1em)
          #text(size: 12pt)[#date]
        ]
      ]
    ]
  ]

  // 목차
  if toc {
    page(numbering: none)[
      #heading(outlined: false, numbering: none)[#toc_title]
      #outline(title: none, depth: toc_depth, indent: toc_indent)
    ]
  }

  if cols == 1 { doc } else { columns(cols, doc) }
}
