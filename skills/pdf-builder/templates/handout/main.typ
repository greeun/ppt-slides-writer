// ============================================================
// 핸드아웃 문서 메인 템플릿
// ============================================================
// 용도: 워크샵/교육 핸드아웃 문서
// 빌드: typst compile main.typ output.pdf
// ============================================================

// ============================================================
// 워크샵 설정 - 수정 필요
// ============================================================
#let workshop-title = "워크샵 제목"
#let workshop-subtitle = "부제목"
#let workshop-date = "2026-01-30 (목) 09:00-13:30"
#let workshop-presenter = "발표자"
#let workshop-target = "PM + 개발자"

// 세션 구성 (표지에 표시)
#let workshop-sessions = (
  (time: "09:00-10:00", title: "세션 1: 제목", duration: "60분"),
  (time: "10:10-11:10", title: "세션 2: 제목", duration: "60분"),
  (time: "11:20-12:00", title: "세션 3: 제목", duration: "40분"),
  (time: "12:30-13:30", title: "세션 4: 제목", duration: "60분"),
)

// ============================================================
// 문서 메타데이터
// ============================================================
#set document(title: workshop-title, author: workshop-presenter)

// ============================================================
// 페이지 설정
// ============================================================
#set page(
  paper: "a4",
  margin: (x: 2cm, y: 2.2cm),
  header: context {
    if counter(page).get().first() > 1 [
      #grid(
        columns: (1fr, 1fr, 1fr),
        align: (left, center, right),
        text(size: 8pt, fill: rgb("#6b7280"))[#workshop-title],
        text(size: 8pt, fill: rgb("#6b7280"))[워크샵 핸드아웃],
        text(size: 8pt, fill: rgb("#6b7280"))[#counter(page).display("1 / 1", both: true)],
      )
    ]
  },
  footer: context {
    if counter(page).get().first() > 1 [
      #align(center)[
        #text(size: 8pt, fill: rgb("#9ca3af"))[#workshop-date]
      ]
    ]
  },
)

// ============================================================
// 텍스트 설정
// ============================================================
#set text(font: ("Pretendard", "Apple SD Gothic Neo", "Noto Sans KR"), size: 10pt)
#set par(leading: 0.75em, justify: true)
#set heading(numbering: none)

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
    #text(size: 16pt, weight: "bold", fill: accent-blue)[#it.body]
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
    #text(size: 12pt, weight: "bold", fill: rgb("#374151"))[#it.body]
  ]
  v(0.5em)
}

// ============================================================
// 헤딩 스타일 (Level 3 - 소제목)
// ============================================================
#show heading.where(level: 3): it => {
  v(0.8em)
  text(size: 10.5pt, weight: "bold", fill: rgb("#4b5563"))[#it.body]
  v(0.4em)
}

// ============================================================
// 테이블 기본 스타일
// ============================================================
#set table(
  fill: (_, row) => if row == 0 { rgb("#eff6ff") } else { white },
  stroke: 0.5pt + rgb("#e5e7eb"),
  inset: 8pt,
)

// ============================================================
// 코드 블록 스타일
// ============================================================
#show raw.where(block: true): it => {
  block(
    fill: rgb("#1e293b"),
    inset: 12pt,
    radius: 6pt,
    width: 100%,
  )[
    #set text(font: ("Fira Code", "Menlo", "Monaco"), size: 8.5pt, fill: rgb("#e2e8f0"))
    #it
  ]
}

// ============================================================
// 인라인 코드 스타일
// ============================================================
#show raw.where(block: false): it => {
  box(
    fill: rgb("#f1f5f9"),
    inset: (x: 4pt, y: 2pt),
    radius: 3pt,
  )[
    #set text(font: ("Fira Code", "Menlo"), size: 9pt)
    #it
  ]
}

// ============================================================
// 문서 구조 - 섹션 include
// ============================================================

#include "_cover.typ"

#include "sections/00-template.typ"

// 추가 섹션은 아래에 include
// #include "sections/01-session.typ"
// #include "sections/02-session.typ"
