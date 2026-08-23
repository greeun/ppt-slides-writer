// ============================================================
// 카탈로그 섹션 템플릿
// ============================================================
// 용도: Q&A 형식 카탈로그 섹션 생성 시 복사하여 사용
// 파일명: 01-{section-name}.typ, 02-{section-name}.typ, ...
// ============================================================

#import "../_styles.typ": *

= 섹션 제목

섹션 설명을 여기에 작성합니다.

== 질문 카테고리

// 기본 질문 카드 예시
#qcard(
  "Q01",
  "예시 질문입니다",
  "Table + Summary",
  [
    응답 내용을 여기에 작성합니다.

    #table(
      columns: (1fr, 1fr, 1fr),
      align: (left, center, right),
      stroke: 0.5pt + rgb("#e5e7eb"),
      inset: 6pt,
      fill: (x, y) => if y == 0 { rgb("#f8fafc") } else { white },
      [*항목*], [*값*], [*비고*],
      [항목 1], [100], [설명],
      [항목 2], [200], [설명],
    )
  ],
)

// 색상 커스텀 질문 카드 예시
#qcard(
  "Q02",
  "라이선스 관련 질문",
  "Chart + Insight",
  [
    라이선스 현황에 대한 응답입니다.

    - 총 라이선스: 100개
    - 사용 중: 80개
    - 미사용: 20개
  ],
  color: license-color,
  bg: license-bg,
)

// 조직 관련 질문 카드
#qcard(
  "Q03",
  "조직/사용자 관련 질문",
  "Table",
  [
    조직 현황에 대한 응답입니다.
  ],
  color: org-color,
  bg: org-bg,
)

// 모니터링 관련 질문 카드
#qcard(
  "Q04",
  "모니터링/알림 관련 질문",
  "Alert + Summary",
  [
    모니터링 현황에 대한 응답입니다.
  ],
  color: monitor-color,
  bg: monitor-bg,
)

// 자산 관련 질문 카드
#qcard(
  "Q05",
  "자산 관련 질문",
  "Table + Chart",
  [
    자산 현황에 대한 응답입니다.
  ],
  color: asset-color,
  bg: asset-bg,
)

// 경고/위험 관련 질문 카드
#qcard(
  "Q06",
  "위험/경고 관련 질문",
  "Alert",
  [
    위험 상황에 대한 응답입니다.
  ],
  color: warning-color,
  bg: warning-bg,
)

#pagebreak()
