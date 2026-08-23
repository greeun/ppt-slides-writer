# 변환 규칙 — HTML → PPTX/PDF

`scripts/html2pptx.py`(네이티브 PPTX)와 `scripts/html2pdf.sh`(픽셀 동일 PDF)가 따르는
규칙. deck.html이 이 규칙을 지켜야 변환 충실도 검증(21~26)을 통과한다.

## 1. 변환 불가 CSS 금지 목록 (12항 — lint 체크 8, ERROR)

python-pptx의 도형·텍스트 모델로 재현할 수 없거나 PDF 인쇄에서 깨지는 속성은
**처음부터 쓰지 않는다**. "HTML에서만 예쁜" 장표는 납품물에서 깨진 장표다.

| # | 금지 항목 | 대체 |
|---|---|---|
| 1 | `linear-gradient`/`radial-gradient`/`conic-gradient` 전면 금지 (배경·도형 모두) | 단색. 층위가 필요하면 연한 단색 블록 2개 |
| 2 | `filter`, `backdrop-filter` | 사용하지 않음 |
| 3 | `box-shadow`, `text-shadow` | 구분이 필요하면 얇은 border 또는 배경색 대비 |
| 4 | `transform` — 단 `rotate(Ndeg)` **단독**만 허용 | rotate는 python-pptx `shape.rotation`으로 매핑됨. scale/translate/skew 금지 |
| 5 | `clip-path`, `mask` | 도형 조합으로 표현 |
| 6 | `::before`/`::after` 장식 콘텐츠 | 실제 요소(.el-shape/.el-text)로 배치 |
| 7 | `animation`, `transition` | 정적 산출물 범위 밖. 동영상·전환 효과 요청은 범위 밖 안내 |
| 8 | `writing-mode` 세로쓰기, `-webkit-background-clip: text` | 가로쓰기, 단색 텍스트 |
| 9 | `@import`·외부 웹폰트(`@font-face` 포함) | 시스템 폰트 스택만 — PPTX를 여는 기기에 폰트가 있어야 편집이 유지된다 |
| 10 | `.slide` 직계 배치의 flex/grid | 인라인 left/top/width/height 절대 배치 |
| 11 | `position: fixed/sticky`, 캔버스(1280×720) 이탈 좌표 | 절대 배치 + 경계 내 좌표 |
| 12 | `opacity` < 1, `rgba()/hsla()` 알파 < 1 (반투명) | 연한 단색으로 대체 (팔레트에 등재) |

## 2. 좌표·크기 매핑 (px → EMU)

- 슬라이드 크기: **12192000 × 6858000 EMU** (13.333in × 7.5in).
- **1px = 9525 EMU** (1280px × 9525 = 12192000). 변환식: `EMU = round(px × 9525)`.
- 폰트: `pt = px × 0.75`, **0.5pt 단위 반올림** (예: 48px→36pt, 20px→15pt, 12px→9pt).
- `font-family`는 **첫 번째 패밀리명**이 PPTX 폰트명으로 매핑된다.
- 인라인 style의 `var(--토큰)`은 변환기가 `:root` 값으로 해석한 뒤 매핑한다.

## 3. 요소별 변환 상세

### .el-text → 텍스트박스
- 블록(h1~h3/p/li)마다 문단 생성. `li`는 네이티브 불릿(buChar "•", 들여쓰기 0.25in).
- 인라인 `b/strong`→bold, `em/i`→italic, `span`의 color/font-weight/font-size→run 스타일.
- text-align→문단 정렬, line-height(배수 또는 px)→line_spacing.
- 텍스트박스 내부 여백 0, word_wrap 켬. 기본 크기(인라인 미지정 시):
  h1 40px / h2 32px / h3 24px / p·li 18px — 단, **인라인 명시가 원칙**이다.
- h1~h3는 기본 bold 처리된다.

### .el-image → picture
- `src` 로컬 상대 경로 파일을 동일 좌표에 삽입. 외부 URL·파일 부재는 변환 오류.
- 원본 해상도 ≥ 배치 px(하한, 검증 24 FAIL), 배치의 2배 미만은 WARN(인쇄 선명도).

### .el-shape → 도형
- `border-radius>0` → ROUNDED_RECTANGLE(반경은 min(w,h) 비율로 근사), 아니면 RECTANGLE.
- 단색 fill(`background-color`), `border: Npx solid #hex` → 외곽선. 그림자 없음 고정.
- 선·구분선도 얇은 사각형으로 만든다 (예: height 2px .el-shape).
- `rotate(Ndeg)` → `shape.rotation`. 텍스트가 있으면 도형 내 텍스트프레임으로 넣지만,
  좌표 정밀도가 필요한 텍스트는 `.el-text`로 분리하는 것이 원칙.

### .el-table → PPTX 표
- `tr`/`td·th` 격자 그대로. `thead th` = 헤더 행 bold.
- 셀 인라인 style: `background(-color)`→셀 채우기, `color`→글자색, `text-align`→정렬,
  `font-size`→크기(미지정 시 `.el-table` 인라인 값, 기본 14px).
- **colspan/rowspan 미지원** — 발견 시 변환 오류. 셀을 분해해 설계하라.
- 표 테두리는 PPTX 테마 기본값을 따른다(셀 CSS 테두리는 이관되지 않음 — 시각 잔차로
  사람 게이트 ④에서 확인).

### aside.notes → 발표자 노트
- `notes_slide` 텍스트 프레임으로 이관. `--image-slides` 모드에서도 이관된다.

### 섹션 배경
- 섹션 인라인 `background(-color)` 우선, 없으면 `<style>`의 `.slide` 규칙 값.

## 4. 오류 정책

파싱 집합(.el-text/.el-image/.el-shape/.el-table/aside.notes) 외 직계 요소, 좌표 누락,
외부 URL 이미지, colspan/rowspan 발견 시: **오류 목록을 전부 출력하고 exit 2, PPTX를
저장하지 않는다.** 부분 변환물은 검증을 오염시킨다.

## 5. `--image-slides` 옵션 (100% 비주얼 모드)

- headless Chrome `--screenshot`으로 장당 PNG(2x, 2560×1440)를 캡처해 full-bleed
  이미지 슬라이드를 구성한다. **파워포인트에서 텍스트 편집 불가.**
- 노트는 이 모드에서도 이관된다.
- 검증 22(텍스트)·23·24는 네이티브 PPTX 기준이다 — 이미지 버전은 사람 게이트 ④에서
  시각 확인만 한다. 기본 납품물은 항상 네이티브 PPTX다.

## 6. PDF 인쇄 (`scripts/html2pdf.sh`)

```bash
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="dist/deck.pdf" "file://<deck.html 절대경로>"
```
- 페이지 분할은 deck.html의 `@page { size: 1280px 720px; margin: 0 }` +
  `.slide { page-break-after: always }`가 담당 → 픽셀 동일 1280×720 페이지.
- `.slide:last-of-type { page-break-after: auto }`로 말미 빈 페이지를 방지한다.
- 크롬 탐색 순서: `$CHROME_BIN` → `/Applications/Google Chrome.app/Contents/MacOS/
  Google Chrome` → `google-chrome` → `chromium`. 부재 시 설치 안내 후 exit 2.

## 7. 알려진 시각 잔차 (기계 검증 밖 — 사람 게이트 ④ 확인 항목)

- 텍스트박스 줄바꿈 위치가 브라우저와 1~2자 다를 수 있다 (폰트 메트릭 차이).
- 표 테두리 스타일·불릿 마커 위치의 미세 차이.
- 이 잔차는 Evaluator가 채점하지 않고 critique.md "사람 게이트 확인 항목"으로 이관한다.
