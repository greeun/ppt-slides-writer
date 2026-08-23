// ============================================================
// 스펙 문서 메인 템플릿
// ============================================================
// 용도: 기능 요구사항 문서
// 빌드: typst compile main.typ output.pdf
// ============================================================

// ============================================================
// 프로젝트 설정 - 수정 필요
// ============================================================
#let project-name = "Project Name"
#let doc-title = "문서 제목"
#let doc-subtitle = "부제목"
#let doc-version = "v1.0"
#let doc-date = "2026-01-23"
#let doc-author = "작성자/팀"

// ============================================================
// 문서 메타데이터
// ============================================================
#set document(title: doc-title, author: doc-author)

// ============================================================
// 페이지 설정
// ============================================================
#set page(
  paper: "a4",
  margin: (x: 1.8cm, y: 2cm),
  header: context {
    if counter(page).get().first() > 1 [
      #grid(
        columns: (1fr, 1fr, 1fr),
        align: (left, center, right),
        text(size: 8pt, fill: rgb("#6b7280"))[#project-name],
        text(size: 8pt, fill: rgb("#6b7280"))[#doc-title],
        text(size: 8pt, fill: rgb("#6b7280"))[#counter(page).display("1 / 1", both: true)],
      )
    ]
  },
)

// ============================================================
// 텍스트 설정
// ============================================================
#set text(font: ("Pretendard", "Apple SD Gothic Neo"), size: 9.5pt)
#set par(leading: 0.7em, justify: true)
#set heading(numbering: "1.")

// ============================================================
// 스타일 import
// ============================================================
#import "_styles.typ": *

// ============================================================
// 헤딩 스타일 (Level 1 - 장 제목)
// ============================================================
#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  v(0.5em)
  box(
    fill: accent-blue.lighten(90%),
    inset: (x: 16pt, y: 12pt),
    radius: 6pt,
    width: 100%,
  )[
    #text(size: 16pt, weight: "bold", fill: accent-blue)[
      #counter(heading).display("1.") #it.body
    ]
  ]
  v(1em)
}

// ============================================================
// 헤딩 스타일 (Level 2 - 절 제목)
// ============================================================
#show heading.where(level: 2): it => {
  v(1em)
  box(
    inset: (left: 10pt, y: 4pt),
    stroke: (left: 3pt + accent-blue),
  )[
    #text(size: 12pt, weight: "bold", fill: rgb("#374151"))[
      #counter(heading).display("1.1") #it.body
    ]
  ]
  v(0.5em)
}

// ============================================================
// 문서 구조 - 섹션 include
// ============================================================

#include "_cover.typ"

#include "sections/00-template.typ"

// 추가 섹션은 아래에 include
// #include "sections/01-section.typ"
// #include "sections/02-section.typ"
