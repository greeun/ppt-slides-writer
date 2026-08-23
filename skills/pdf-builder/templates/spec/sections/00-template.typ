// ============================================================
// 섹션 템플릿
// ============================================================
// 용도: 새 섹션 파일 생성 시 복사하여 사용
// 파일명: 01-{section-name}.typ, 02-{section-name}.typ, ...
// ============================================================

#import "../_styles.typ": *

= 섹션 제목

== 개요

이 섹션은 템플릿 예시입니다. 실제 내용으로 교체하세요.

== 기능 목록

// 기능 카드 예시
#feature-card(
  "REQ-01-01",
  "기능명",
  "기능에 대한 간단한 설명을 작성합니다.",
  "not_implemented",  // implemented, partial, not_implemented
  "v1.0",
  (
    purpose: "이 기능의 목적을 설명합니다.",
  ),
)

// 상세 기능 카드 예시
#feature-card-detailed(
  "REQ-01-02",
  "상세 기능명",
  "상세 기능에 대한 설명을 작성합니다.",
  "partial",
  "v1.0",
  (
    purpose: "이 기능의 목적",
    key_functions: (
      "핵심 기능 1",
      "핵심 기능 2",
      "핵심 기능 3",
    ),
    expected_benefits: "기대 효과 설명",
    current_implementation: "현재 구현 상태 설명",
  ),
  components: ("Component1", "Component2"),
)

== 요약 테이블

#table(
  columns: (auto, 1fr, auto, auto),
  align: (left, left, center, center),
  stroke: 0.5pt + rgb("#e5e7eb"),
  inset: 6pt,
  fill: (x, y) => if y == 0 { rgb("#eff6ff") } else { white },
  [*ID*], [*기능명*], [*상태*], [*버전*],
  [REQ-01-01], [기능명 1], [#status-badge("not_implemented")], [#version-badge("v1.0")],
  [REQ-01-02], [기능명 2], [#status-badge("partial")], [#version-badge("v1.0")],
  [REQ-01-03], [기능명 3], [#status-badge("implemented")], [#version-badge("v1.0")],
)

== 진행률

#progress-bar(1, 1, 3, label: "전체 진행률")

#pagebreak()
