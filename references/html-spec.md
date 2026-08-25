# HTML 중간 렌더 사양 (deck.html)

HTML은 최종 목표가 아니라 **중간 렌더 단계**다. 브라우저 시각 확인·범위 지정 수정 루프의
매체이며, 승인 후 `scripts/html2pptx.py`·`scripts/html2pdf.sh`의 입력이 된다.
이 사양을 지키지 않으면 lint(체크 1~20)와 변환기가 거부한다.
시작점은 `templates/slide-boilerplate.html`이다.

## 1. 문서 구조

- **단일 `deck.html`** — 모든 장표를 `<section class="slide">`로 포함한다.
- 16:9 고정, **캔버스 1280×720px** (변환 좌표 계산 기준, 1px = 9525 EMU).
- PDF 인쇄용 필수 CSS:
  ```css
  @page { size: 1280px 720px; margin: 0; }
  .slide { page-break-after: always; }
  .slide:last-of-type { page-break-after: auto; }  /* 말미 빈 페이지 방지 */
  * { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  ```
- 브라우저 확인용 스타일은 `@media screen` 블록에만 넣는다(인쇄 무영향).

## 2. 섹션 필수 속성

모든 `<section class="slide">`는 다음 속성을 가진다 (lint 체크 3 — ERROR):

- `data-role` — 아래 enum 중 하나:
  ```
  cover | agenda | section-divider | problem | insight | solution |
  concept | process | evidence | comparison | case | tactics | caveats |
  application | roadmap | team | financials | cta | appendix
  ```
  enum 확장은 storyline.md의 "역할 확장 정의"에 역할을 추가한 경우만 허용
  (lint는 enum 외 값을 WARN 처리).
- `data-key-message` — 이 장표의 키 메시지 1문장.
- `data-role="cover"`와 `data-role="cta"` 섹션은 반드시 존재한다 (체크 2 — ERROR).

## 3. 자기완결 (체크 5 — ERROR)

- 외부 CDN·웹폰트·원격 이미지 금지. `http(s)://` 참조(src/href/@import/CSS url()) 0건.
- 이미지는 `assets/` **로컬 상대 경로** — PPTX 변환 시 동일 파일을 재사용한다.
- CSS는 `<style>` 블록 인라인. 폰트는 시스템 폰트 스택만(`@font-face` 금지).

## 4. 디자인 토큰

- design-system.md의 토큰 표를 `:root` CSS 변수로 주입한다:
  `--color-*`, `--font-*`, `--radius-*`, `--space-*`.
- lint가 design-system.md의 HEX 목록을 파싱해 사용 색을 대조한다 (체크 6 — ERROR,
  무채색 계열 예외). design-system.md §6.1 "금지 색"에 적힌 HEX는 팔레트에서 제외되고
  사용 시 ERROR다. §6.1 "금지 표현"의 문구는 장표 텍스트에서 발견 시 체크 20 ERROR.
- **인라인 style 안에서 `var(--토큰)` 사용 가능** — lint와 변환기가 `:root` 값으로
  해석한다. 토큰에 없는 색을 raw HEX로 몰래 쓰는 것이 금지 대상이다.

## 5. 절대 배치 (체크 4 — ERROR)

- 변환 대상 요소(`.el-*`)는 **`.slide`의 직계 자식**이며, 인라인 `style`의
  `left/top/width/height`(px)로만 배치한다. 변환기는 cascade 해석 없이 이 값으로
  좌표를 확정한다.
- `.slide` 직계 수준에서 flex/grid 금지 (금지 CSS 10항). 경계:
  `left+width ≤ 1280`, `top+height ≤ 720`, 음수 좌표 금지.
- z-order는 DOM 순서다 (뒤에 쓴 요소가 위에 쌓인다 — 배경 도형을 먼저 쓴다).
- 렌더 오버플로: lint가 headless Chrome으로 `scrollHeight > clientHeight`를 측정한다.
  지정 높이 안에 콘텐츠가 실제로 들어가야 한다.

## 6. 변환 대상 요소 클래스 (파싱 집합 — 이외 직계 요소는 변환기 오류)

| 클래스 | 태그 | 변환 결과 | 규칙 |
|---|---|---|---|
| `.el-text` | div | 텍스트박스 | 내부 허용: `h1~h3`/`p`/`ul·ol·li`(**리스트 1단만 — 중첩 시 변환기 exit 2**), 인라인 `b/strong/em/span(color·font-weight·font-size)/a[href]`. 폰트 패밀리·크기·색·정렬은 인라인 style(또는 `.el-text` 인라인 상속). font-family 미지정 시 변환기가 `<style>`의 `.el-text`/`body` 규칙 값을 폴백으로 적용한다(conversion-rules §2) |
| `.el-image` | img | picture | `src`는 로컬 상대 경로. 원본 해상도 ≥ 배치 px(권장 2배) |
| `.el-shape` | div | 사각형 도형 | 단색 fill·border만. `border-radius>0`이면 라운드 사각형. `transform: rotate(Ndeg)` 단독 허용. 텍스트는 가급적 `.el-text`로 분리 |
| `.el-table` | table | PPTX 표 | `thead th` = 헤더 행(bold). 셀 인라인 style로 배경·색·정렬. colspan/rowspan 미지원 |
| `aside.notes` | aside | 발표자 노트 | `display:none`, 전 장표 필수·비어있으면 안 됨 (체크 17) |

**헤딩 크기 규칙(필수)**: 기본 스타일시트에
`.el-text h1, .el-text h2, .el-text h3 { font-size: inherit; font-weight: inherit; }`
를 유지한다. UA 기본 배율(h1=2em)이 걸리면 브라우저 렌더와 변환 좌표가 어긋난다.
크기·굵기는 `.el-text` 인라인 style에 명시한다.

**불릿 규칙**: `ul`은 `list-style-position: outside; padding-left: 28px`로 마커를
표시한다. `li::before` 장식은 금지 CSS 6항이다. PPTX에서는 네이티브 불릿(buChar)으로
변환된다. **리스트 중첩 금지(1단만)** — `li` 안의 `ul/ol`은 변환기가 오류(exit 2)로
거부한다. 하위 항목이 필요하면 문단 재구성 또는 장표 분할로 해소한다.

## 7. 분량·타이포 규칙

- 장당 본문 6줄 이내, 불릿 3~5개 (체크 19 — 6줄·5개 초과 시 ERROR. 불릿 하한 3개는
  권장치로 기계 검출하지 않으며 Evaluator가 판단한다).
- 최소 폰트: 본문 18px, 캡션·출처 12px (체크 14 — ERROR).
- 캡션·출처는 `.el-text source` 또는 `.el-text caption` 클래스를 붙인다 —
  lint가 12~17px를 허용하는 유일한 예외이자, 수치 출처 요구(체크 15)의 충족 요소다.
- 이모지 디자인 요소 금지 (체크 12 — ERROR). 장표 텍스트·노트는 격식체(합쇼체).

## 8. 병렬 생성 (fragments)

- 조각은 `fragments/NN.html` — 파일당 `<section class="slide">` 1개씩.
- 조립: 조각을 순서대로 deck.html의 `<body>`에 삽입한 뒤 **후처리 패턴 통일 패스**
  (팔레트·여백 리듬·라벨 표기·데이터 시각화 스타일·radius 계층)를 단일 패스로 수행한다.
  후처리 없이 lint·핸드오프 진행 금지 (workflows/04 참조).

## 9. 금지 CSS

12항 전체 목록과 근거는 `references/conversion-rules.md` 참조. 요약: 그라데이션·
filter·그림자·(rotate 외) transform·clip-path·의사요소 장식·애니메이션·세로쓰기·
웹폰트·`.slide` 직계 flex/grid·fixed/sticky·반투명.
