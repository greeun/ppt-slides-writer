// ========================================
// Frentis 보고서 전역 스타일 템플릿
// ========================================
// Quarto의 template-partials로 사용
// 표, 이미지, 코드 블록, 제목 스타일 정의
// ========================================

// ----------------------------------------
// 폰트 설정 (한글 우선)
// ----------------------------------------
#set text(
  font: ("Pretendard", "Apple SD Gothic Neo", "Noto Sans KR"),
  lang: "ko",
  region: "KR",
)

// ----------------------------------------
// 표 스타일 - 전폭 적용
// ----------------------------------------
#set table(
  inset: 10pt,
  stroke: 0.5pt + luma(150),
  fill: (x, y) => if y == 0 { luma(230) } else { none },
)

// 표 헤더 볼드
#show table.cell.where(y: 0): set text(weight: "bold")

// 표 전폭 상태 관리
#let wide-table-state = state("wide-table", false)

// 전폭 테이블 생성 함수
#let make-wide-table(it) = {
  let col-count = if type(it.columns) == array {
    it.columns.len()
  } else if type(it.columns) == int {
    it.columns
  } else {
    1
  }

  // 이미 1fr 컬럼이면 그대로 반환
  if type(it.columns) == array and it.columns.all(c => c == 1fr) {
    return it
  }

  // 필드 재구성
  let args = (:)
  for (key, val) in it.fields() {
    if key != "children" and key != "columns" {
      args.insert(key, val)
    }
  }

  wide-table-state.update(true)
  let result = table(
    columns: (1fr,) * col-count,
    ..args,
    ..it.children,
  )
  wide-table-state.update(false)
  result
}

// 표 전폭 show rule
#show table: it => context {
  if wide-table-state.get() {
    it
  } else {
    set align(center)
    block(width: 100%, make-wide-table(it))
  }
}

// figure 내 표도 동일 처리
#show figure.where(kind: table): it => {
  set align(center)
  block(width: 100%, breakable: true, it)
}

// ----------------------------------------
// 이미지/다이어그램 스타일
// ----------------------------------------
// 이미지가 페이지를 넘어가는 문제 해결:
// - width: 100%로 제한 (페이지 너비 초과 방지)
// - fit: "contain"으로 비율 유지하며 축소
// - 최대 높이를 페이지 여백 고려하여 제한
#show figure.where(kind: image): it => {
  set align(center)
  set image(width: 100%, fit: "contain")
  block(
    width: 100%,
    breakable: false,
    clip: true,  // 혹시 넘치면 잘라냄
  )[
    #box(
      width: 100%,
      // A4 기준: 297mm - 30mm(top) - 30mm(bottom) - 여유 = 약 200mm
      height: auto,
    )[#it]
  ]
}

// ----------------------------------------
// 코드 블록 스타일
// ----------------------------------------
#show raw.where(block: true): it => {
  set text(size: 9pt, font: "D2CodingLigature Nerd Font")
  block(
    width: 100%,
    fill: luma(245),
    inset: 10pt,
    radius: 4pt,
    it
  )
}

// ----------------------------------------
// 제목 스타일 (섹션 번호 포함)
// ----------------------------------------
#set heading(numbering: "1.1.1")

#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  v(1em)
  text(size: 18pt, weight: "bold")[
    #counter(heading).display("1.")
    #it.body
  ]
  v(0.5em)
}

#show heading.where(level: 2): it => {
  v(0.8em)
  text(size: 14pt, weight: "bold")[
    #counter(heading).display("1.1")
    #it.body
  ]
  v(0.4em)
}

#show heading.where(level: 3): it => {
  v(0.6em)
  text(size: 12pt, weight: "bold")[
    #counter(heading).display("1.1.1")
    #it.body
  ]
  v(0.3em)
}
