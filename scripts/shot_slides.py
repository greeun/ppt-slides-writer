#!/usr/bin/env python3
"""shot_slides.py — deck.html 장별 PNG 캡처 (렌더 게이트 ③·Evaluator 시각 확인용).

사용법:
    python3 shot_slides.py <deck.html> [--out-dir shots] [--slides 2,5-7] [--scale 1]

용도: lint(형식)와 변환 검증(수량)이 잡지 못하는 것 — 여백 균형, 대비, 시각적 위계 —
를 사람과 Evaluator가 실제 픽셀로 확인한다. Evaluator는 마크업만 읽으면 "박스는 있는데
그 안이 비어 보인다"를 절대 볼 수 없다 (references/evaluator-prompt.md 시각 확인 절).

출력: <out-dir>/S01.png … 장표당 1장 (1280x720 × scale).
의존성: headless Chrome (탐색 순서는 lint_slides.py와 동일: $CHROME_BIN → macOS 앱 →
google-chrome → chromium). Chrome 부재 시 안내 후 exit 1.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

CANVAS_W, CANVAS_H = 1280, 720


def find_chrome():
    env = os.environ.get("CHROME_BIN")
    if env and os.path.exists(env):
        return env
    mac = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if os.path.exists(mac):
        return mac
    for name in ("google-chrome", "chromium", "chromium-browser"):
        found = shutil.which(name)
        if found:
            return found
    return None


def parse_range(spec, total):
    """'2,5-7' → [2,5,6,7]. None이면 전체."""
    if not spec:
        return list(range(1, total + 1))
    out = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return [n for n in out if 1 <= n <= total]


def split_sections(html):
    """head(문서 상단) + 각 <section class="slide"> 조각으로 분리."""
    parts = re.split(r'(?=<section class="slide")', html)
    head = parts[0]
    sections = []
    for chunk in parts[1:]:
        end = chunk.find("</section>")
        if end == -1:
            continue
        sections.append(chunk[:end] + "</section>")
    return head, sections


def main():
    ap = argparse.ArgumentParser(description="deck.html 장별 PNG 캡처")
    ap.add_argument("deck")
    ap.add_argument("--out-dir", default="shots")
    ap.add_argument("--slides", default=None, help="예: 2,5-7 (미지정 시 전체)")
    ap.add_argument("--scale", type=float, default=1.0, help="배율 (기본 1 — 1280x720)")
    args = ap.parse_args()

    chrome = find_chrome()
    if not chrome:
        print("headless Chrome 미탐지 — 설치 후 재시도하거나 $CHROME_BIN을 지정한다.\n"
              "  https://www.google.com/chrome/", file=sys.stderr)
        return 1

    deck_path = os.path.abspath(args.deck)
    with open(deck_path, encoding="utf-8") as f:
        html = f.read()
    head, sections = split_sections(html)
    if not sections:
        print("section.slide 를 찾지 못했다.", file=sys.stderr)
        return 1

    targets = parse_range(args.slides, len(sections))
    os.makedirs(args.out_dir, exist_ok=True)
    # 상대 경로 자산(assets/)을 살리려면 deck.html과 같은 폴더에서 렌더해야 한다
    tmp_dir = tempfile.mkdtemp(prefix=".shots-", dir=os.path.dirname(deck_path))
    written = []
    try:
        for n in targets:
            one = os.path.join(tmp_dir, f"s{n}.html")
            with open(one, "w", encoding="utf-8") as f:
                f.write(head + sections[n - 1] + "\n</body>\n</html>")
            out = os.path.abspath(os.path.join(args.out_dir, f"S{n:02d}.png"))
            subprocess.run(
                [chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                 f"--screenshot={out}",
                 f"--window-size={int(CANVAS_W * args.scale)},{int(CANVAS_H * args.scale)}",
                 f"--force-device-scale-factor={args.scale}",
                 "--virtual-time-budget=3000", "file://" + one],
                capture_output=True, timeout=90,
            )
            if os.path.exists(out):
                written.append(out)
            else:
                print(f"S{n:02d} 캡처 실패", file=sys.stderr)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    print(f"캡처 완료 {len(written)}장 → {os.path.abspath(args.out_dir)}")
    for w in written:
        print(f"  {w}")
    return 0 if written else 1


if __name__ == "__main__":
    sys.exit(main())
