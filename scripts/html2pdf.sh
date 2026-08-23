#!/usr/bin/env bash
# html2pdf.sh — deck.html → 픽셀 동일 PDF (headless Chrome 인쇄).
#
# 사용법: html2pdf.sh <deck.html> [출력.pdf]
#   출력 기본값: <deck.html 폴더>/dist/deck.pdf
#
# 페이지 분할은 deck.html의 @page { size: 1280px 720px; margin: 0 } +
# .slide { page-break-after: always } 가 담당한다 → 1280x720 픽셀 동일 페이지.
#
# 크롬 바이너리 탐색 순서: $CHROME_BIN → macOS Chrome → google-chrome → chromium
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "사용법: html2pdf.sh <deck.html> [출력.pdf]" >&2
  exit 1
fi

DECK="$1"
if [ ! -f "$DECK" ]; then
  echo "오류: 입력 파일이 없다 — $DECK" >&2
  exit 1
fi

# 절대 경로화 (상대 경로 assets/ 해석을 위해 file:// URL 사용)
DECK_ABS="$(cd "$(dirname "$DECK")" && pwd)/$(basename "$DECK")"
DECK_DIR="$(dirname "$DECK_ABS")"
OUT="${2:-$DECK_DIR/dist/deck.pdf}"

# 크롬 탐색
CHROME=""
if [ -n "${CHROME_BIN:-}" ] && [ -x "${CHROME_BIN}" ]; then
  CHROME="$CHROME_BIN"
elif [ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
  CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
elif command -v google-chrome >/dev/null 2>&1; then
  CHROME="$(command -v google-chrome)"
elif command -v chromium >/dev/null 2>&1; then
  CHROME="$(command -v chromium)"
else
  cat >&2 <<'EOF'
오류: headless Chrome을 찾지 못했다.
해결 방법 중 하나를 수행할 것:
  1) Google Chrome 설치: https://www.google.com/chrome/
  2) chromium 설치: brew install chromium (macOS) / apt install chromium (Linux)
  3) 커스텀 경로 지정: CHROME_BIN=/path/to/chrome ./html2pdf.sh deck.html
EOF
  exit 2
fi

mkdir -p "$(dirname "$OUT")"

"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$OUT" "file://$DECK_ABS"

if [ ! -s "$OUT" ]; then
  echo "오류: PDF가 생성되지 않았다 — $OUT" >&2
  exit 3
fi

echo "PDF 저장 완료: $OUT"
