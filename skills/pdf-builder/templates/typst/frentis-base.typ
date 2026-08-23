// ============================================
// Frentis Base Design System v2.1
// ============================================
// 옵션 조합 방식 — 프리셋 없음
//
// #import "/.claude/skills/pdf-builder/templates/typst/frentis-base.typ": *
// #show: frentis-doc.with(
//   title: "문서 제목",
//   cover: true,           // 표지 페이지
//   logo: "/path/to/company_logo.png",
//   toc: true,             // 목차
//   header-footer: true,   // 헤더/푸터
//   numbering: "1.1.1",    // 섹션 번호 (none이면 없음)
// )
//
// 빌드: typst compile --root <vault-root> input.typ output.pdf
// ============================================

// ===== 디자인 토큰 =====

#let frentis-colors = (
  primary: rgb("#1a365d"),       // 진한 네이비
  primary-light: rgb("#2b6cb0"), // 밝은 파란
  secondary: rgb("#2d3748"),     // 진한 회색
  muted: rgb("#718096"),         // 연한 텍스트
  text: rgb("#1a202c"),          // 본문
  accent: rgb("#3182ce"),        // 강조 파란
  // 표
  table-header-bg: rgb("#2b6cb0"),   // 파란 헤더 배경
  table-header-text: white,          // 헤더 텍스트
  table-border: rgb("#cbd5e0"),      // 테두리
  // 코드
  code-bg: rgb("#f7fafc"),
  code-border: rgb("#e2e8f0"),
  // 링크
  link: rgb("#2b6cb0"),
)

#let frentis-fonts = (
  main: ("Pretendard", "Apple SD Gothic Neo"),
  // code 폰트 fallback에 한글 폰트 포함 — 인라인 코드 안에 한글이 들어가는 경우 깨짐 방지
  code: ("Monoplex KR Nerd", "Menlo", "Apple SD Gothic Neo", "Pretendard"),
)

// ===== 표지 페이지 =====

#let frentis-cover(
  title: none,
  subtitle: none,
  author: none,
  date: none,
  logo: none,
  cover-style: "gradient",  // "gradient" or "simple"
) = {
  if cover-style == "gradient" {
    page(margin: 0cm, numbering: none)[
      #set text(font: frentis-fonts.main, lang: "ko", region: "KR")
      #box(
        width: 100%,
        height: 100%,
        fill: gradient.linear(
          frentis-colors.primary,
          frentis-colors.primary-light,
          angle: 135deg,
        ),
      )[
        #place(center + horizon)[
          #block(width: 75%)[
            #set text(fill: white)

            #if logo != none {
              align(left)[#image(logo, width: 25%)]
              v(2em)
            }

            #text(size: 32pt, weight: "bold")[#title]

            #if subtitle != none {
              v(0.5em)
              text(size: 18pt, weight: "light")[#subtitle]
            }

            #v(2em)
            #line(length: 100%, stroke: 2pt + white.transparentize(50%))
            #v(2em)

            #if author != none {
              text(size: 14pt)[#author]
              v(0.5em)
            }

            #if date != none {
              text(size: 12pt, fill: white.transparentize(30%))[#date]
            }
          ]
        ]
      ]
    ]
  } else {
    // simple cover
    page(
      margin: (top: 50mm, bottom: 30mm, left: 25mm, right: 25mm),
      header: none,
      footer: none,
      numbering: none,
    )[
      #set text(font: frentis-fonts.main, lang: "ko", region: "KR")

      #if logo != none {
        image(logo, width: 25%)
        v(2cm)
      }

      #align(center)[
        #v(3cm)
        #text(size: 28pt, weight: "bold", fill: frentis-colors.primary)[#title]

        #if subtitle != none {
          v(0.5cm)
          text(size: 16pt, fill: frentis-colors.muted)[#subtitle]
        }

        #v(3cm)

        #if author != none or date != none {
          set text(size: 11pt)
          table(
            columns: (auto, auto),
            align: (right, left),
            stroke: none,
            fill: none,
            inset: 8pt,
            ..if author != none { ([*작성*], [#author]) } else { () },
            ..if date != none { ([*일자*], [#date]) } else { () },
          )
        }

        #v(1fr)
        // 로고가 있으면 로고, 없으면 텍스트
        #if logo != none {
          image(logo, width: 20%)
        } else {
          text(size: 12pt, weight: "medium", fill: frentis-colors.primary)[Frentis]
        }
      ]
    ]
  }
}

// ===== 타이틀 블록 (표지 없을 때 문서 상단용) =====

#let title-block(title, subtitle: none, author: none, logo: none) = {
  if logo != none {
    grid(
      columns: (1fr, auto),
      align: (left + horizon, right + horizon),
      [
        #text(16pt, weight: "bold", fill: frentis-colors.primary)[#title]
        #if subtitle != none {
          v(0.1em)
          text(9pt, fill: frentis-colors.muted)[#subtitle]
        }
      ],
      // 로고에 명시적 크기 (글로벌 set image 무시)
      box(width: 80pt)[#image(logo)],
    )
  } else {
    align(center)[
      #text(16pt, weight: "bold", fill: frentis-colors.primary)[#title]
      #if subtitle != none {
        v(0.15em)
        text(9pt, fill: frentis-colors.muted)[#subtitle]
      }
    ]
  }
  if author != none {
    align(center)[
      #v(0.1em)
      #text(9pt, fill: frentis-colors.muted)[#author]
    ]
  }
  v(0.3em)
  line(length: 100%, stroke: 1pt + frentis-colors.primary-light)
  v(0.3em)
}

// ===== 메인 함수 =====

#let frentis-doc(
  // 콘텐츠 메타
  title: none,
  subtitle: none,
  author: none,
  date: none,
  // 옵션
  cover: false,                  // 표지 페이지
  cover-style: "gradient",       // "gradient" or "simple"
  logo: none,                    // 로고 경로 (none = 없음)
  toc: false,                    // 목차
  header-footer: true,           // 헤더/푸터
  header-text: "Frentis",        // 헤더 우측 텍스트
  numbering: "1.1.1",           // 섹션 번호 (none = 없음)
  // 레이아웃 세부 조정
  fontsize: 11pt,
  margin: (top: 25mm, bottom: 25mm, left: 25mm, right: 25mm),
  leading: 0.8em,
  doc,
) = {
  // --- 표지 ---
  if cover and title != none {
    frentis-cover(
      title: title,
      subtitle: subtitle,
      author: author,
      date: date,
      logo: logo,
      cover-style: cover-style,
    )
  }

  // --- 목차 ---
  if toc {
    page(
      paper: "a4",
      margin: margin,
      header: none,
      footer: none,
      numbering: none,
    )[
      #set text(font: frentis-fonts.main, lang: "ko", region: "KR")
      #heading(outlined: false, numbering: none)[목차]
      #outline(title: none, indent: 1.5em, depth: 3)
    ]
  }

  // --- 본문 페이지 설정 ---
  let header-start = if cover { 1 } else { 2 }

  set page(
    paper: "a4",
    margin: margin,
    numbering: if header-footer { "1" } else { none },
    ..if header-footer {(
      header: context {
        let pg = counter(page).get().first()
        if pg >= header-start {
          grid(
            columns: (1fr, 1fr),
            align: (left, right),
            text(size: 9pt, fill: frentis-colors.muted)[],
            text(size: 9pt, fill: frentis-colors.muted)[#header-text],
          )
          v(2pt)
          line(length: 100%, stroke: 0.5pt + frentis-colors.table-border)
        }
      },
      footer: context {
        let pg = counter(page).get().first()
        if pg >= header-start {
          align(center)[
            #text(size: 9pt, fill: frentis-colors.muted)[#counter(page).display()]
          ]
        }
      },
    )} else {(:)}
  )

  // --- 텍스트 기본 ---
  set text(
    font: frentis-fonts.main,
    size: fontsize,
    lang: "ko",
    region: "KR",
    fill: frentis-colors.text,
  )

  // --- 단락 ---
  set par(leading: leading, spacing: 1.2em, justify: true)

  // --- 제목 ---
  set heading(numbering: numbering)

  show heading.where(level: 1): it => {
    v(1.2em)
    text(size: 18pt, weight: "bold", fill: frentis-colors.primary, it)
    v(0.6em)
  }

  show heading.where(level: 2): it => {
    v(1em)
    text(size: 14pt, weight: "bold", fill: frentis-colors.secondary, it)
    v(0.4em)
  }

  show heading.where(level: 3): it => {
    v(0.8em)
    text(size: 12pt, weight: "bold", fill: frentis-colors.secondary, it)
    v(0.3em)
  }

  show heading.where(level: 4): it => {
    v(0.6em)
    text(size: 11pt, weight: "bold", it)
    v(0.2em)
  }

  // --- 표 (파란 헤더 — fill 함수 방식) ---
  show table: it => block(width: 100%, it)
  set table(
    inset: (x: 10pt, y: 8pt),
    stroke: 0.5pt + frentis-colors.table-border,
    align: left,
    fill: (_, row) => if row == 0 { frentis-colors.table-header-bg } else { none },
  )

  // 헤더 행 텍스트 스타일
  show table.cell.where(y: 0): set text(weight: "bold", fill: frentis-colors.table-header-text)

  // --- 리스트 ---
  set list(marker: ([•], [◦], [▪]), indent: 1.5em, body-indent: 0.5em)
  set enum(indent: 1.5em, body-indent: 0.5em)

  // --- 코드 블록 ---
  show raw.where(block: true): it => {
    set text(font: frentis-fonts.code, size: 9pt)
    block(
      fill: frentis-colors.code-bg,
      stroke: 0.5pt + frentis-colors.code-border,
      inset: 12pt,
      radius: 4pt,
      width: 100%,
      it,
    )
  }

  show raw.where(block: false): it => {
    set text(font: frentis-fonts.code, size: 0.9em)
    box(fill: rgb("#edf2f7"), inset: (x: 3pt, y: 1pt), radius: 2pt, it)
  }

  // --- 링크 ---
  show link: it => { text(fill: frentis-colors.link, it) }

  // --- 인용 블록 ---
  show quote: it => {
    block(
      fill: frentis-colors.code-bg,
      inset: (left: 12pt, rest: 10pt),
      stroke: (left: 3pt + frentis-colors.accent),
      it,
    )
  }

  // --- Figure ---
  set figure(gap: 1em)
  show figure.caption: it => {
    set text(size: 10pt, fill: frentis-colors.muted)
    it
  }

  // --- 이미지 기본: max-width 100% (넘침 방지) ---
  set image(width: 100%)

  // --- 수평선 ---
  show line: it => {
    v(0.3em)
    it
    v(0.3em)
  }

  // --- 타이틀 블록 (표지 없을 때) ---
  if not cover and title != none {
    title-block(title, subtitle: subtitle, author: author, logo: logo)
  }

  doc
}

// ===== 유틸리티: 정보 박스 =====

#let info-box(title: none, body) = {
  block(
    fill: rgb("#ebf8ff"),
    stroke: (left: 3pt + frentis-colors.accent),
    inset: 12pt,
    radius: (right: 4pt),
    width: 100%,
  )[
    #if title != none {
      text(weight: "bold", fill: frentis-colors.accent)[#title]
      v(0.3em)
    }
    #body
  ]
}

#let warning-box(title: none, body) = {
  block(
    fill: rgb("#fffbeb"),
    stroke: (left: 3pt + rgb("#d69e2e")),
    inset: 12pt,
    radius: (right: 4pt),
    width: 100%,
  )[
    #if title != none {
      text(weight: "bold", fill: rgb("#d69e2e"))[#title]
      v(0.3em)
    }
    #body
  ]
}
