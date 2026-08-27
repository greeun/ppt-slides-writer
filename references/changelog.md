# 변경 이력 — ppt-slides-writer

SemVer. 버그 수정 = patch, 기능 추가 = minor, 호환성 파괴 = major.
출처 표기: 실전 테스트 백로그(`skill-wizard-output/live-test-notes.md`)는 (#N), 감사 후 REFINE은
(audit #N), salesclue 원문(`salesclue.io/blog/claude-design-ppt`) 대조 미준수분은 (SC-N),
렌더 게이트 실물 확인에서 나온 시각 결함은 (V-N), 2차 검증 덱 런(ai-automation-guide,
validation_report)의 pattern-spec 템플릿 갭은 (G-N), 스킬 결함·마찰은 (F-N).

**템플릿 동기화 체크(릴리스 관례)**: scripts/·boilerplate의 계약을 바꾸는 릴리스는 같은 계약을
서술하는 `templates/`·`references/`·`workflows/` 문구를 **같은 릴리스에서** 갱신하고, 이 파일의
해당 항목에 동기화한 파일을 명시한다(§8 룰 승격의 역방향 — v1.2.0 표 계약이 templates/
pattern-spec.md에 미반영된 채 두 릴리스가 지나간 재발 방지). 진행 중 작업 폴더는 첫 lint 전에
최신 항목의 호환성 파괴 여부를 확인해 덱을 마이그레이션한다.

## 1.3.1 (2026-08-28)

2차 검증 덱 런(ai-automation-guide — 리드마그넷형·신규 도메인)에서 드러난 P0
"templates/pattern-spec.md의 v1.2.0 표 계약 미반영"을 닫고, pattern-spec 슬롯 갭과
운영 마찰을 문서·템플릿 수준에서 흡수했다.

### P0 — pattern-spec 템플릿 표 계약 동기화 (G-1·G-7, F-1)

- **`templates/pattern-spec.md` §0 표 행 재작성**: "PPTX 열 폭 균등·셀 padding·테두리는
  PPTX 기본값, th/td에 height 인라인" 서술을 v1.2.0+ 계약(colgroup 필수·`<tr>` 행 높이·
  boilerplate CSS가 셀 padding 12×16·middle·구분선의 정본)으로 교체. 이전 서술을 따르는
  병렬 조각 Generator는 전원 lint 체크 4 ERROR를 냈다.
- **§6.4 판단표 재작성**: "열 폭 균등 — `<col>`·셀 width 금지" 지시 제거 →
  colgroup(합=표 width)·`<tr height>`(합=표 height) 필수로 교정하고, **lint 체크 4를 실제로
  통과하는 HTML 예시**를 수록. 행 높이 산식도 셀 padding 상하 24px 반영값으로 갱신
  (1줄 48 → 56 / 2줄 64 → 80 / 3줄 88 → 104, 줄 수 한계 열 폭 −20 → −32).
- §8 조립 체크리스트 6항을 같은 계약으로 교정(셀 height 인라인 → `<tr>`·`<col>` 치수).
- references/design-rules.md §9 판단표 행의 "열 폭 균등·행 높이 균등"도 colgroup·tr 계약으로 교정.
- 재발 방지: 이 파일 상단에 "템플릿 동기화 체크(릴리스 관례)" 명문화 (F-1·F-7).

### pattern-spec 슬롯 갭 반영 (G-2~G-10)

- G-2: §1 머리에 "덱 기본 프레임 선택" 지침 — 제목 px×자수 추정으로 1줄/2줄 기본 프레임을
  덱 단위로 먼저 고른다(읽는 덱은 대부분 1줄). §1.1의 "(기본)" 표기 제거.
- G-3: §1.1 상단 밴드 슬롯에 "특수 프레임 전용 가능" 주석.
- G-4: §1.3에 자유 분할 행(실측 x 범위 기입식) 추가 — 비정형 분할의 즉석 발명 방지.
- G-5: §6.14 CTA 버튼 규격 신설(도형+링크 텍스트 겹침, `a[href]`+UTM·`&amp;` 이스케이프,
  링크 기본 스타일 근거) + §1.4 cta에서 §6.14 참조. workflows/01 리드마그넷 특화 규칙에도 연결.
- G-6: §6 머리에 "§6 색 표기는 예시 — §4 design-system 의미 라벨이 항상 우선" 명문화.
- G-8: §6.8 우측 슬롯을 "금액·태그(색은 의미 라벨)"로 일반화, design-rules §9에
  "실행 지침·체크리스트 나열 → 6.8" 행 추가(§8 승격 절차 이행).
- G-9: §6.9 스케일 문구 확정 — "행별 정규화가 기본, 단위 환산은 같은 행 안에서만"
  (design-rules §9의 "단위 환산 필수"도 동일 교정).
- G-10: §6.5에 비지표 변형(병렬 항목 소개) 내부 규격 추가, design-rules §9에
  "병렬 항목 소개 → 6.5 비지표 변형" 행 추가.

### 스킬 결함·마찰 반영 (F-2~F-10)

- F-2: **lint 체크 16 리드마그넷 인식** — storyline `발표 시간: 해당 없음(사유)` 명시 시
  WARN 대신 INFO("시간 검산 생략"). 실제 필드 줄만 인식(줄 앵커) — 템플릿 지침 문구가 잔존한
  발표덱의 검산이 조용히 생략되는 오탐 방지. `0분` 우회(total > 0 가드)도 파싱 계약에 문서화.
  templates/storyline.md 파싱 계약·개요·시간 검산 절, workflows/01에 표기 규칙 정식화.
- F-3: 체크 10 slide-bottom 맹점(푸터·캡션 포함 측정이라 푸터 있는 덱은 무발화) —
  design-rules §4에 문서화, 게이트 ③ 캡처 열람으로 보완. 측정 로직 보강은 이월.
- F-4: workflows/01·templates/storyline.md에 읽는 덱의 발표자 노트 용도(읽는 이 보충 설명) 명시.
- F-5: workflows/01 질문 3·storyline 템플릿에 읽는 덱 장수 산정 기준(완독 목표 시간·내용 단위) 추가.
- F-9: shot_slides.py docstring에 Chrome stderr 노이즈 안내(성공 판정은 exit code·완료 메시지) 1줄.
- F-10: §6.8에 "첫 블록 룰은 프레임 구분선과 겸용 가능" 노트(S6 이중선 인상).

### 이월 (다음 릴리스 백로그)

- F-3 구현부: 체크 10 slide-bottom을 캡션·푸터 제외 본문 기준으로 측정 — 기존 통과 덱에
  새 WARN을 만들므로 픽스처 재보정과 함께 별도 릴리스로.
- F-6 일부: concept용 사분면/2×2 시각 유형 신설 — 실측 사례 없이 좌표 규격을 발명하지
  않는다(§8 승격 절차: 2개 덱 이상 반복 신고 시 등재). 6.8·6.5 비지표는 이번에 등재 완료.
- F-9 구현부: shot_slides.py stderr 필터링(동작 변경) — docstring 안내로 대체, 필요 시 다음에.

## 1.3.0 (2026-08-28)

기계 검증이 형식·수량만 보고 레이아웃 품질을 보지 못하던 사각지대를 메웠다.
"lint 통과 = 볼 만하다"가 아니라는 것을 절차로 못박는다.

- **lint 체크 10 확장(여백 균형)**: Chrome 렌더 측정에 3종 추가 — `.el-text` 박스
  점유율 50% 미만(여유 48px 초과), 장표 마지막 요소 아래 160px 초과 공백, 카드
  (`.el-shape`, 높이 120px 이상·장표 폭 0.95배 미만) 안 콘텐츠 아래 80px 초과 공백.
  배경 띠·전면 배경 도형은 제외한다. (V-6)
- **`scripts/shot_slides.py` 신설**: deck.html 장별 PNG 캡처(`--slides 2,5-7`,
  `--scale`). 상대 경로 자산이 살도록 deck.html과 같은 폴더에서 렌더한다. (V-7)
- **시각 확인 절차 의무화**: 렌더 게이트 ③에 오케스트레이터 선행 확인 단계(0번) 추가 —
  사용자에게 보여주기 전에 캡처본을 직접 본다. Evaluator 프로브 5도 PNG 캡처·열람을
  요구하고, 캡처 불가 시 사실을 critique.md에 명시하도록 했다. (V-8)

## 1.2.0 (2026-08-28)

시각 산출물 실물 확인(렌더 게이트 ③)에서 드러난 표·링크 기본 스타일 부재를 닫았다.
기존 덱은 `colgroup` 추가가 필요하다(체크 4 ERROR).

- **표 기본 스타일 신설**: boilerplate에 셀 패딩(12px 16px)·수직 정렬(middle)·구분선
  (헤더 하단 2px, 행 하단 1px, 세로선 없음)을 넣었다. 이전에는 `border: 1px` 격자만 있어
  텍스트가 선에 붙고 행 안에서 위로 몰렸다. (V-1)
- **열 너비 계약**: `<colgroup><col style="width:Npx">` 필수 + `table-layout: fixed`.
  브라우저 auto layout과 PPTX 균등 분할이 어긋나던 문제를 단일 원천으로 해소했다.
  lint 체크 4에 열 너비 누락·합 불일치 ERROR, 행 높이 합 불일치 WARN 추가. (V-2)
- **변환기 표 이관 확장**: colgroup 열 너비·`<tr>` 행 높이·CSS padding→셀 여백·
  vertical-align→앵커·CSS 지정 변만 그리는 테두리(`a:lnT/B/L/R`)를 이관하고,
  PPTX 테마 기본 격자·첫 행 강조·줄무늬를 끈다. (V-3)
- **링크 기본 스타일**: `.el-text a { color: inherit; text-decoration: none; }` 추가.
  1.1.0에서 `<a href>` 지원을 넣으면서 UA 기본 파란 글자+밑줄이 그대로 렌더되던 문제. (V-4)
- lint 체크 18 보고 예시가 캡처 그룹 때문에 튜플로 출력되던 버그 수정
  (`findall` → `finditer` + `group(0)`). (V-5)

## 1.1.0 (2026-08-26)

두 작업 흐름(실전 테스트 백로그 + salesclue 원문 대조)을 하나의 minor 릴리스로 통합했다.
체크 번호(1~20, 21~26)·게이트 ①~④·프로브 9종·verdict logic은 바뀌지 않았다.

### 실전 테스트 백로그 8건

- `scripts/verify_conversion.py` 체크 22가 HTML 주석(bs4 `Comment`)을 손실 텍스트로 오탐하던
  버그 수정. `scripts/html2pptx.py`도 `<p>` 안 주석이 run으로 새지 않게 차단. (#1)
- `scripts/lint_slides.py --partial [--wrap-head deck.html]`: 조각 단독 lint — 체크 1·2·16
  생략, 보고서 머리에 "PARTIAL 모드 — 체크 1·2·16 생략". `--wrap-head` 생략 시 상위 deck.html
  자동 적용, 없으면 렌더 검사 SKIP. 조립 마커 `<!-- APPEND: … -->`를 boilerplate에 추가. (#2)
- `templates/pattern-spec.md` 신설 + File Handoff Contract에 `pattern-spec.md` 추가.
  S2 종료 시 Generator 작성 → Evaluator "병렬 파견 판정" → 조각 Generator 입력. (#3)
- `references/design-rules.md` §9 콘텐츠→시각 유형 매핑 사전(네이티브 한정 12유형),
  workflows/05에서 모호한 시각화 피드백의 제안 카탈로그로 사용. (#4)
- 네이티브 우선 전략 명시(SKILL.md 생태계 연계, workflows/04, design-rules §7,
  generator-prompt): 차트·도식은 `.el-*` 기본, image-gen은 삽화 한정, API 키 부재 폴백 =
  기본 경로. (#5)
- 제목 줄 수 안전장치: lint 렌더 검사에 "h1 마지막 줄 실측 폭 > 박스 폭 × 0.92이고 박스에
  여유 줄 없음 → PPTX N+1줄 위험" WARN(체크 4, Chrome 부재 시 SKIP). 변환기 기하는 불변.
  conversion-rules §7에 해소 절차. (#6)
- Evaluator·Generator 프롬프트에 절 단위 부분 저장 규칙 + workflows/04 연결 끊김 복구. (#7)
- 오케스트레이터 파견 프롬프트의 토큰 의미 재정의·확장 금지(SKILL.md, workflows/05). (#8)

### 감사 후 REFINE 4건

- `--partial`에서 `--wrap-head` 생략 시 `fragments/` 상위 `deck.html`을 자동 적용하고, 그것도
  없으면 렌더 검사를 SKIP한다(절대 배치 CSS 없는 측정은 오탐이므로). 보고서 모드 줄에
  "자동 탐지" 표기. (audit #2)
- 제목 폭 WARN 조건을 "마지막 줄 실측 폭 > 박스 폭 × 0.92 AND 박스 높이 < (줄 수+1) ×
  line-height"로 확정 — 2줄 프레임에서 상시 발화하던 최대 폭 기준을 대체하고, 여유 줄을
  확보하면 면제된다. (audit #3)
- 조립 마커를 `<!-- APPEND: … -->` 하나로 통일(boilerplate·html-spec §8·pattern-spec §8·
  workflows/04·generator-prompt 3.c가 같은 마커를 가리킴). (audit #4)
- README.md Version 1.1.0 + changelog 참조, 저장소 구조 표에 changelog·pattern-spec·
  `--partial`·제목 폭 WARN·design-rules §9·conversion-rules 시각 잔차 반영. (audit #7)

### salesclue 원문 대조 미준수 4건

- 배포 후 측정: workflows/07에 지표 6종(열람·체류·다운로드·CTA 클릭·폼 제출·완독률) 확보
  방법, 링크 배포 권고, CTA 링크 UTM 부여, 측정 결과의 재작업 환류. `scripts/html2pptx.py`가
  `.el-text` 안 `<a href>`를 PPTX run 하이퍼링크(`run.hyperlink.address`)로 이관 —
  PPTX·PDF 양쪽에서 클릭 가능(클릭 추적의 유일한 경로). html-spec/conversion-rules/
  generator-prompt에 `a[href]` 허용·사용 규칙 명시. (SC-1)
- 역할 enum 확장 14 → 19종: `concept` / `process` / `tactics` / `caveats` / `application`
  추가(information-architecture §2, lint `ROLE_ENUM`, html-spec, storyline·boilerplate·
  pattern-spec 템플릿). information-architecture §2-1 기본 10장 골격 신설(고정 템플릿이
  아닌 출발점). 10장 이상 덱은 caveats(한계) 장표 기본 포함, 미포함 시 사유 명시(rubric C1,
  planner-prompt). (SC-2)
- 입력 자산 수집 확장: workflows/02에 입력 자산 6종 표(기존 덱·웹사이트·로고·폰트·샘플
  카피·금지 목록) 신설, 네거티브 리스트는 경로 A/B 모두에서 확보. `templates/design-system.md`
  §6.1 네거티브 리스트 서식 고정. lint가 §6.1을 파싱해 금지 색은 팔레트에서 제외 후 사용 시
  체크 6 ERROR, 금지 표현은 체크 20 ERROR. 미기입 플레이스홀더·구버전 파일은 무시. (SC-3)
- 사람 검수 체크리스트: workflows/07 게이트 ④에 사실 검수 6항목 표(메시지·수치·실명·브랜드·
  보안·흐름) — 수치 정확성과 고객사 실명은 사람 확인 없이 통과 불가. evaluator-prompt가
  대조 필요 수치·실명 사용처 목록을 critique.md에 상시 이관. SKILL.md 안전 게이트에 "사실
  검수는 사람 몫" 추가. lint 체크 18·Evaluator 프로브 3에 미공개(내부 전용) 로드맵·전략
  패턴 추가. (SC-4)

## 1.0.0 (2026-08-19)

- 최초 릴리스: Planner–Generator–Evaluator Full tier, 사람 게이트 4개, lint 체크 1~20,
  변환 검증 21~26, 네이티브 PPTX + PDF 납품.
