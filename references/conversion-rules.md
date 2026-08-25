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
- `font-family`는 **첫 번째 패밀리명**이 PPTX 폰트명으로 매핑된다. 해석은 폴백
  체인을 따른다: **블록 인라인 → `.el-*` 인라인 → `<style>`의 `.el-text`/`body` 규칙**
  — boilerplate 기본 경로에서 모든 텍스트 run에 폰트명이 반드시 도달한다
  (미도달 시 PPTX 테마 기본 폰트로 무음 대체되는 것을 막는 규칙).
- 인라인 style의 `var(--토큰)`은 변환기가 `:root` 값으로 해석한 뒤 매핑한다.

## 3. 요소별 변환 상세

### .el-text → 텍스트박스
- 블록(h1~h3/p/li)마다 문단 생성. `li`는 네이티브 불릿(buChar "•", 들여쓰기 0.25in).
- **리스트는 1단만 허용** — `li` 안의 `ul/ol` 중첩은 변환 오류(exit 2, §4 오류 정책).
  하위 항목은 문단 재구성 또는 장표 분할로 해소한다.
- 인라인 `b/strong`→bold, `em/i`→italic, `span`의 color/font-weight/font-size→run 스타일.
- `a[href]`→run 하이퍼링크(`run.hyperlink.address`). PPTX·PDF 양쪽에서 클릭된다 —
  CTA·부록 URL은 텍스트로 적지 말고 `<a>`로 감싼다 (배포 후 클릭 추적의 유일한 경로,
  workflows/07). 링크 색·밑줄은 PPTX 테마 기본값을 따른다(시각 잔차).
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
  `font-size`→크기(미지정 시 `.el-table` 인라인 값, 기본 18px). 표 셀도 본문
  최소 크기 규칙(18px — html-spec §7, lint 체크 14 ERROR)을 그대로 따른다.
- **colspan/rowspan 미지원** — 발견 시 변환 오류. 셀을 분해해 설계하라.
- 표 테두리는 PPTX 테마 기본값을 따른다(셀 CSS 테두리는 이관되지 않음 — 시각 잔차로
  사람 게이트 ④에서 확인).

### aside.notes → 발표자 노트
- `notes_slide` 텍스트 프레임으로 이관. `--image-slides` 모드에서도 이관된다.

### 섹션 배경
- 섹션 인라인 `background(-color)` 우선, 없으면 `<style>`의 `.slide` 규칙 값.

## 4. 오류 정책

파싱 집합(.el-text/.el-image/.el-shape/.el-table/aside.notes) 외 직계 요소, 좌표 누락,
외부 URL 이미지, colspan/rowspan, 중첩 리스트(li 안의 ul/ol) 발견 시: **오류 목록을
전부 출력하고 exit 2, PPTX를 저장하지 않는다.** 부분 변환물은 검증을 오염시킨다.
해석 불가 구조의 무음 통과·근사 변환 금지 — 무음 오염이 조기 실패보다 나쁘다.

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
- **제목 줄 수 안전장치 (h1 폭 안전 계수 0.92)**: 같은 메트릭 차이로 브라우저에서 1줄인
  제목이 PPTX에서 한 줄 더 넘어갈 수 있다. 안전장치는 변환기 기하 변경이 아니라 **lint 렌더
  검사의 WARN**이다 — `.el-text h1`의 **마지막 줄** 실측 폭이 박스 폭 × 0.92를 넘고, 박스
  높이에 여유 줄((줄 수 + 1) × line-height)이 없을 때만 체크 4 WARN "제목 폭 안전 계수 …
  PPTX N+1줄 위험"을 낸다(Chrome 부재 시 SKIP). 최대 폭이 아니라 마지막 줄을 보는 이유:
  줄바꿈된 제목은 첫 줄이 항상 박스에 꽉 차므로 2줄 프레임(pattern-spec §1.1)에서 상시
  발화하게 된다 — 한 줄이 더 생길지는 마지막 줄이 얼마나 찼는지가 결정한다. 해소 순서:
  ① 제목 박스 폭을 실측 폭 ÷ 0.92 이상으로 넓힌다(안전 여백 64px 안에서) ② 제목을
  축약한다 ③ 둘 다 불가하면 박스 높이를 (줄 수 + 1) × font-size × line-height로 확보한다
  (확보하면 WARN 자체가 면제된다) — html2pptx는 word_wrap을 켠 채 박스 폭 안에서
  줄바꿈하므로 높이만 확보되면 줄 수 차이는 아래 요소와 겹치지 않고 흡수된다. 변환기
  좌표·크기 매핑(§2)은 이 잔차 때문에 바꾸지 않는다.
- 표 테두리 스타일·불릿 마커 위치의 미세 차이.
- `.el-image` 비율 불일치: 브라우저는 `object-fit: contain`으로 레터박스 처리하지만
  PPTX는 지정 좌표(w×h)로 스트레치한다 — 원본 비율 = 배치 비율을 맞추는 것이 원칙.
- 폰트 패밀리는 폴백 체인(§2)으로 run까지 이관되지만, PPTX를 여는 기기에 해당
  폰트가 없으면 대체 폰트로 렌더된다 (시스템 폰트 스택만 허용하는 이유 — 금지 9항).
- 이 잔차는 Evaluator가 채점하지 않고 critique.md "사람 게이트 확인 항목"으로 이관한다.
