#!/usr/bin/env python3
"""lint_slides.py — deck.html 기계 lint (ppt-slides-writer 체크 1~20).

사용법:
    python3 lint_slides.py <deck.html> <design-system.md> <storyline.md> \
        [--report lint_report.md] [--no-render] \
        [--partial [--wrap-head deck.html]]

2단계 검사:
  1) 정적 파싱(BeautifulSoup) — 체크 1~20 중 기계 검증분
  2) 렌더 검사(headless Chrome) — 요소 scrollHeight>clientHeight 오버플로 (체크 4 보강)
     + 제목(h1) 폭 안전 계수 WARN (체크 4, 폰트 메트릭 잔차): 마지막 줄 실측 폭 > 박스 폭 × 0.92
       이면서 박스 높이에 여유 줄(줄 수+1)이 없을 때만 "PPTX N+1줄 위험". 줄바꿈된 제목의
       첫 줄은 항상 박스에 꽉 차므로 최대 폭이 아니라 마지막 줄 폭을 본다.
     Chrome 부재 시 SKIP 기록 후 경고.

--partial: 조각(fragments/NN.html) 단독 lint. 조립 전에는 성립하지 않는 체크 1(장수)·
  2(cover/cta)·16(시간 합)을 생략하고 보고서 머리에 "PARTIAL 모드"를 명시한다.
  조각에 <head>(:root 토큰·기본 스타일)가 없으면 --wrap-head <deck.html> 의 <head>를 씌워
  검사한다 — 토큰 해석(체크 6·14)과 렌더 검사가 :root·기본 CSS에 의존한다. --wrap-head를
  생략하면 조각 폴더의 상위 deck.html(fragments/ 규약)을 자동 적용하고, 그것도 없으면
  렌더 검사를 SKIP한다(절대 배치 CSS 없이는 오버플로 측정이 오탐이므로).

출력: lint_report.md + exit code (ERROR 존재 시 1, 아니면 0).
의존성: beautifulsoup4
"""

import argparse
import html as html_mod
import json
import os
import re
import shutil
import subprocess
import sys

from bs4 import BeautifulSoup, Tag

ROLE_ENUM = {
    "cover", "agenda", "section-divider", "problem", "insight", "solution",
    "concept", "process", "evidence", "comparison", "case", "tactics",
    "caveats", "application", "roadmap", "team", "financials",
    "cta", "appendix",
}

CANVAS_W, CANVAS_H = 1280, 720

GENERIC_TITLES = [
    "핵심 기능", "왜 우리인가", "혁신적인", "차세대", "게임 체인저",
    "미래를 선도", "최고의 선택", "Our Solution", "Why Us", "Why Choose Us",
    "Key Features", "About Us", "Solution Overview", "Next Generation",
]

# 이모지 블록 (화살표 2190-21FF 는 제외 — 정당한 기호)
EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF"
    "\U00002B00-\U00002BFF\U0000FE0F\U0001F900-\U0001F9FF]"
)

INFORMAL_RE = re.compile(
    r"(해요|이에요|예요|네요|세요|어요|아요|드려요|거야|잖아"
    r"|[가-힣]야[.!?]|[가-힣]임[.!?]|[가-힣]함[.!?])"
)

SENSITIVE_PATTERNS = [
    ("주민등록번호", re.compile(r"\b\d{6}\s*[-–]\s*[1-4]\d{6}\b")),
    ("전화번호", re.compile(r"\b01[016789][-\s.]?\d{3,4}[-\s.]?\d{4}\b")),
    ("이메일", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    ("계좌번호 추정", re.compile(r"\b\d{3,6}-\d{2,6}-\d{4,8}\b")),
    ("민감 키워드", re.compile(r"(대외비|사외비|Confidential|급여|연봉|임금|견적\s*단가|단가표)", re.I)),
    # 미공개 전략·로드맵 (기밀 전략 문서 유출 방지 — 단어 '로드맵' 단독은 오탐이므로 수식어와 결합)
    ("미공개 전략·로드맵", re.compile(
        r"((미공개|비공개|내부\s*전용|공개\s*예정|출시\s*전|unreleased|internal[\s-]*only)"
        r"[^\n]{0,12}(로드맵|전략|계획|기능|출시|roadmap|strateg\w*|plan\w*|feature\w*)"
        r"|(로드맵|전략)[^\n]{0,6}(미공개|비공개|내부\s*전용))", re.I)),
]

NUMERIC_CLAIM_RE = re.compile(r"\d[\d,\.]*\s*(%|원|억|조|만|배|건|명|개사|달러|\$|₩)")

HEX_RE = re.compile(r"#[0-9A-Fa-f]{6}\b|#[0-9A-Fa-f]{3}\b")


def norm_hex(h):
    h = h.lstrip("#").lower()
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return "#" + h


def parse_negative_list(ds_src):
    """design-system.md 6.1 네거티브 리스트에서 금지 색 HEX·금지 표현을 뽑는다.

    서식(templates/design-system.md 고정): `- 금지 색: #RRGGBB, #RRGGBB | 없음`
                                          `- 금지 표현: 문구1, 문구2 | 없음`
    절이 없으면 빈 값 — 구버전 design-system.md와 호환된다."""
    colors, phrases = set(), []
    for m in re.finditer(r"^\s*[-*]?\s*금지\s*색\s*[:\uff1a]\s*(.+)$", ds_src, re.M):
        colors |= {norm_hex(h) for h in HEX_RE.findall(m.group(1))}
    for m in re.finditer(r"^\s*[-*]?\s*금지\s*표현\s*[:\uff1a]\s*(.+)$", ds_src, re.M):
        raw = m.group(1).strip()
        if raw in ("없음", "-", "N/A"):
            continue
        if raw.startswith("{") and raw.endswith("}"):
            continue  # 미기입 템플릿 플레이스홀더
        for part in re.split(r"[,\u00b7/]", raw):
            part = part.strip().strip("`'\"{}")
            if part and part not in ("없음", "-"):
                phrases.append(part)
    return colors, phrases


def hex_rgb(h):
    h = norm_hex(h).lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def is_grayscale(h):
    r, g, b = hex_rgb(h)
    return max(r, g, b) - min(r, g, b) <= 10


def rgb_to_hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    mx, mn = max(r, g, b), min(r, g, b)
    d = mx - mn
    if d == 0:
        h = 0.0
    elif mx == r:
        h = 60 * (((g - b) / d) % 6)
    elif mx == g:
        h = 60 * (((b - r) / d) + 2)
    else:
        h = 60 * (((r - g) / d) + 4)
    s = 0.0 if mx == 0 else d / mx
    return h, s, mx


def parse_style(style_str):
    """인라인 style 문자열 → dict (소문자 속성명)."""
    out = {}
    if not style_str:
        return out
    for part in style_str.split(";"):
        if ":" not in part:
            continue
        k, v = part.split(":", 1)
        out[k.strip().lower()] = v.strip()
    return out


def parse_root_vars(style_text):
    """<style>의 :root 블록에서 CSS 변수 추출."""
    out = {}
    m = re.search(r":root\s*\{([^}]*)\}", style_text, re.S)
    if not m:
        return out
    for name, val in re.findall(r"(--[\w-]+)\s*:\s*([^;]+);?", m.group(1)):
        out[name.strip()] = val.strip()
    return out


def resolve_vars(value, root_vars):
    """var(--x) / var(--x, fallback) 치환 (중첩 2단계까지)."""
    if value is None:
        return value
    for _ in range(3):
        def rep(m):
            name = m.group(1).strip()
            fb = m.group(2)
            return root_vars.get(name, fb.strip() if fb else m.group(0))
        new = re.sub(r"var\(\s*(--[\w-]+)\s*(?:,([^)]*))?\)", rep, value)
        if new == value:
            break
        value = new
    return value


def px(value):
    if value is None:
        return None
    m = re.match(r"^(-?\d+(?:\.\d+)?)px$", value.strip())
    return float(m.group(1)) if m else None


def find_chrome():
    """§7.5 탐색 순서: $CHROME_BIN → macOS Chrome → google-chrome → chromium."""
    cands = []
    if os.environ.get("CHROME_BIN"):
        cands.append(os.environ["CHROME_BIN"])
    cands.append("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    cands += ["google-chrome", "chromium"]
    for c in cands:
        if os.path.sep in c:
            if os.path.isfile(c) and os.access(c, os.X_OK):
                return c
        else:
            p = shutil.which(c)
            if p:
                return p
    return None


class Linter:
    def __init__(self):
        self.findings = []  # (check_no, level, message)
        self.safety_flags = []

    def add(self, no, level, msg):
        self.findings.append((no, level, msg))

    def errors(self):
        return [f for f in self.findings if f[1] == "ERROR"]


def collect_el_elements(section):
    """섹션 직계의 변환 대상 요소(.el-*)를 수집."""
    els = []
    for child in section.children:
        if not isinstance(child, Tag):
            continue
        classes = child.get("class") or []
        if any(c.startswith("el-") for c in classes):
            els.append(child)
    return els


def el_kind(el):
    for c in (el.get("class") or []):
        if c.startswith("el-"):
            return c
    return ""


def has_class_up(el, names, stop):
    """el 및 stop까지의 조상에 names 중 하나의 클래스가 있는가."""
    cur = el
    while cur is not None and cur is not stop:
        if isinstance(cur, Tag):
            cls = cur.get("class") or []
            if any(n in cls for n in names):
                return True
        cur = cur.parent
    return False


TITLE_WIDTH_SAFETY = 0.92  # 제목 폭 안전 계수 — conversion-rules §7 (PPTX 폰트 메트릭 잔차)


def wrap_with_head(fragment_src, head_deck_path):
    """조각(섹션만 있는 HTML)에 deck.html의 <head>를 씌운다 (--wrap-head)."""
    with open(head_deck_path, encoding="utf-8") as f:
        head_doc = f.read()
    m = re.search(r"<head>.*?</head>", head_doc, re.S | re.I)
    head = m.group(0) if m else "<head></head>"
    return f'<!DOCTYPE html>\n<html lang="ko">\n{head}\n<body>\n{fragment_src}\n</body>\n</html>\n'


def run_render_check(deck_path, chrome, lint, src=None):
    """headless Chrome --dump-dom 으로 오버플로·제목 폭 측정. src가 있으면 파일 대신 그 문자열을 렌더."""
    if src is None:
        with open(deck_path, encoding="utf-8") as f:
            src = f.read()
    probe = """
<script>
window.addEventListener('load', function () {
  var out = [], titles = [];
  var SAFETY = %s;
  var slides = document.querySelectorAll('section.slide');
  slides.forEach(function (s, i) {
    if (s.scrollHeight > s.clientHeight + 1 || s.scrollWidth > s.clientWidth + 1)
      out.push({slide: i + 1, el: 'section.slide', sh: s.scrollHeight, ch: s.clientHeight,
                sw: s.scrollWidth, cw: s.clientWidth});
    s.querySelectorAll('[class*="el-"]').forEach(function (el) {
      if (el.scrollHeight > el.clientHeight + 2 || el.scrollWidth > el.clientWidth + 2)
        out.push({slide: i + 1, el: el.className, sh: el.scrollHeight, ch: el.clientHeight,
                  sw: el.scrollWidth, cw: el.clientWidth});
    });
    s.querySelectorAll('.el-text h1').forEach(function (h) {
      var box = h.closest('.el-text');
      var bw = box ? box.clientWidth : h.clientWidth;
      var bh = box ? box.clientHeight : h.clientHeight;
      var cs = getComputedStyle(h);
      var lh = parseFloat(cs.lineHeight);
      if (!(lh > 0)) lh = parseFloat(cs.fontSize) * 1.2;
      var range = document.createRange();
      range.selectNodeContents(h);
      var rects = range.getClientRects();
      if (!rects.length) return;
      // 줄바꿈된 제목은 첫 줄이 항상 박스에 꽉 차므로, 한 줄이 더 생길지는 마지막 줄 폭이 결정한다
      var lastTop = -Infinity, k;
      for (k = 0; k < rects.length; k++) if (rects[k].top > lastTop) lastTop = rects[k].top;
      var l = Infinity, r = -Infinity;
      for (k = 0; k < rects.length; k++) {
        if (Math.abs(rects[k].top - lastTop) < 2) {
          if (rects[k].left < l) l = rects[k].left;
          if (rects[k].right > r) r = rects[k].right;
        }
      }
      var lw = r - l;
      var lines = Math.max(1, Math.round(h.getBoundingClientRect().height / lh));
      var spare = bh >= (lines + 1) * lh - 1;
      if (bw > 0 && lw > bw * SAFETY && !spare)
        titles.push({slide: i + 1, text: (h.textContent || '').trim().slice(0, 40),
                     lw: Math.round(lw), bw: bw, lines: lines, bh: bh, lh: Math.round(lh)});
    });
  });
  var pre = document.createElement('pre');
  pre.id = '__lint_overflow__';
  pre.textContent = JSON.stringify({overflow: out, titles: titles});
  document.body.appendChild(pre);
});
</script>
""" % TITLE_WIDTH_SAFETY
    if "</body>" in src:
        injected = src.replace("</body>", probe + "</body>", 1)
    else:
        injected = src + probe
    tmp = os.path.join(os.path.dirname(os.path.abspath(deck_path)), ".lint_render_tmp.html")
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(injected)
        proc = subprocess.run(
            [chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
             "--virtual-time-budget=3000", "--dump-dom", "file://" + tmp],
            capture_output=True, text=True, timeout=90,
        )
        m = re.search(r'<pre id="__lint_overflow__">(.*?)</pre>', proc.stdout, re.S)
        if not m:
            lint.add(4, "WARN", "렌더 검사 결과를 파싱하지 못했다 (Chrome dump-dom 출력 이상). 정적 검사만 반영됨.")
            return
        data = json.loads(html_mod.unescape(m.group(1)) or "{}")
        for item in data.get("overflow", []):
            lint.add(4, "ERROR",
                     f"렌더 오버플로 — S{item['slide']} `{item['el']}`: "
                     f"scroll {item.get('sw','?')}x{item.get('sh','?')} > client {item.get('cw','?')}x{item.get('ch','?')}")
        if not data.get("overflow"):
            lint.add(4, "INFO", "렌더 오버플로 검사 통과 (Chrome 측정).")
        for item in data.get("titles", []):
            limit = item["bw"] * TITLE_WIDTH_SAFETY
            n = item["lines"]
            lint.add(4, "WARN",
                     f"제목 폭 안전 계수 — S{item['slide']} h1 \"{item['text']}\"({n}줄): 마지막 줄 실측 폭 {item['lw']}px > "
                     f"박스 폭 {item['bw']}px × {TITLE_WIDTH_SAFETY} = {limit:.0f}px, 박스 높이 {item['bh']}px < "
                     f"{n + 1}줄분({(n + 1) * item['lh']}px) → PPTX {n + 1}줄 위험(폰트 메트릭 차이). "
                     "박스 폭 확장·제목 축약 또는 박스 높이 +1줄 확보 (conversion-rules §7).")
    except Exception as e:  # noqa: BLE001 — lint는 진단 도구, 렌더 실패는 WARN으로 강등
        lint.add(4, "WARN", f"렌더 검사 실행 실패({e}). 정적 검사만 반영됨.")
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def main():
    ap = argparse.ArgumentParser(description="deck.html 기계 lint (체크 1~20)")
    ap.add_argument("deck")
    ap.add_argument("design_system")
    ap.add_argument("storyline")
    ap.add_argument("--report", default=None)
    ap.add_argument("--no-render", action="store_true", help="렌더 검사(headless Chrome) 생략")
    ap.add_argument("--partial", action="store_true",
                    help="조각(fragments/NN.html) 단독 lint — 체크 1·2·16 생략, 보고서에 PARTIAL 모드 명시")
    ap.add_argument("--wrap-head", default=None, metavar="DECK_HTML",
                    help="--partial 시 조각에 <head>가 없으면 이 deck.html의 <head>(:root·기본 CSS)를 씌워 검사")
    args = ap.parse_args()

    deck_dir = os.path.dirname(os.path.abspath(args.deck))
    report_path = args.report or os.path.join(deck_dir, "lint_report.md")

    with open(args.deck, encoding="utf-8") as f:
        html_src = f.read()
    with open(args.design_system, encoding="utf-8") as f:
        ds_src = f.read()
    with open(args.storyline, encoding="utf-8") as f:
        story_src = f.read()

    lint = Linter()
    wrapped = False
    wrap_source = None
    render_skip_reason = None
    if args.partial and not re.search(r"<head>", html_src, re.I):
        head_src = args.wrap_head
        if not head_src:
            # fragments/NN.html 규약 → 상위 폴더의 deck.html을 자동 적용
            cand = os.path.normpath(os.path.join(deck_dir, os.pardir, "deck.html"))
            if os.path.isfile(cand):
                head_src = cand
        if head_src:
            html_src = wrap_with_head(html_src, head_src)
            wrapped, wrap_source = True, head_src
        else:
            render_skip_reason = "PARTIAL — 조각에 <head> 없음·deck.html 미탐지"
            lint.add(4, "WARN", "PARTIAL: 조각에 <head>(:root 토큰·기본 CSS)가 없고 --wrap-head 미지정·상위 폴더 "
                                "deck.html 미탐지 — 토큰 해석(체크 6·14) 불완전, 렌더 검사 SKIP(절대 배치 CSS 없이는 "
                                "오버플로 측정이 오탐). --wrap-head <deck.html> 지정 권장.")

    soup = BeautifulSoup(html_src, "html.parser")
    sections = soup.select("section.slide")
    style_text = "\n".join(s.get_text() for s in soup.find_all("style"))
    root_vars = parse_root_vars(style_text)

    if not sections:
        lint.add(1, "ERROR", "deck.html에 section.slide가 없다.")

    if not args.partial:
        # ---------- 체크 1: 장수 일치 ----------
        story_slides = re.findall(r"^##\s+S(\d+)\.", story_src, re.M)
        if len(story_slides) != len(sections):
            lint.add(1, "ERROR",
                     f"장수 불일치 — storyline.md {len(story_slides)}장 vs deck.html {len(sections)}섹션.")

        # ---------- 체크 2: 표지·CTA ----------
        roles = [s.get("data-role", "") for s in sections]
        if "cover" not in roles:
            lint.add(2, "ERROR", 'data-role="cover" 섹션이 없다.')
        if "cta" not in roles:
            lint.add(2, "ERROR", 'data-role="cta" 섹션이 없다.')

    # ---------- 체크 3: data 속성 ----------
    for i, s in enumerate(sections, 1):
        role = s.get("data-role")
        km = s.get("data-key-message")
        if not role:
            lint.add(3, "ERROR", f"S{i}: data-role 누락.")
        elif role not in ROLE_ENUM:
            lint.add(3, "WARN", f"S{i}: data-role='{role}' 는 enum 외 값 — storyline.md 역할 확장 정의 필요.")
        if not km or not km.strip():
            lint.add(3, "ERROR", f"S{i}: data-key-message 누락 또는 빈 값.")

    # ---------- 체크 4(정적): 좌표 경계 + 절대 배치 ----------
    for i, s in enumerate(sections, 1):
        for el in collect_el_elements(s):
            st = {k: resolve_vars(v, root_vars) for k, v in parse_style(el.get("style", "")).items()}
            l, t = px(st.get("left")), px(st.get("top"))
            w, h = px(st.get("width")), px(st.get("height"))
            if None in (l, t, w, h):
                lint.add(4, "ERROR",
                         f"S{i} `{el_kind(el)}`: 인라인 left/top/width/height(px) 절대 배치 누락 — html-spec §배치 위반.")
                continue
            if l < 0 or t < 0 or l + w > CANVAS_W + 0.5 or t + h > CANVAS_H + 0.5:
                lint.add(4, "ERROR",
                         f"S{i} `{el_kind(el)}`: 캔버스(1280x720) 이탈 — left+width={l + w:.0f}, top+height={t + h:.0f}.")

    # ---------- 체크 4(표): 열 너비·행 높이 계약 ----------
    # 브라우저는 auto layout, PPTX는 균등 분할 — colgroup 없이는 둘이 어긋난다.
    for i, s in enumerate(sections, 1):
        for tbl in s.find_all("table", class_="el-table"):
            tst = {k: resolve_vars(v, root_vars) for k, v in parse_style(tbl.get("style", "")).items()}
            tw, th = px(tst.get("width")), px(tst.get("height"))
            rows = tbl.find_all("tr")
            ncols = max((len(r.find_all(["td", "th"])) for r in rows), default=0)
            cols = tbl.find_all("col")
            widths = [px({k: resolve_vars(v, root_vars)
                          for k, v in parse_style(c.get("style", "")).items()}.get("width")) for c in cols]
            if len(widths) != ncols or not all(widths):
                lint.add(4, "ERROR",
                         f"S{i} .el-table: colgroup 열 너비 누락 — <col style=\"width:Npx\"> {ncols}개 필요 "
                         "(브라우저 auto layout과 PPTX 균등 분할이 어긋난다, html-spec §6).")
            elif tw and abs(sum(widths) - tw) > 1:
                lint.add(4, "ERROR",
                         f"S{i} .el-table: 열 너비 합 {sum(widths):.0f}px != 표 width {tw:.0f}px.")
            heights = [px({k: resolve_vars(v, root_vars)
                           for k, v in parse_style(r.get("style", "")).items()}.get("height")) for r in rows]
            if all(heights) and th and abs(sum(heights) - th) > 1:
                lint.add(4, "WARN",
                         f"S{i} .el-table: 행 높이 합 {sum(heights):.0f}px != 표 height {th:.0f}px — "
                         "PPTX가 비율 보정하므로 의도한 행 높이와 달라질 수 있다.")

    # ---------- 체크 5: 자기완결 ----------
    for tag in soup.find_all(src=True):
        if re.match(r"^https?://", tag["src"], re.I):
            lint.add(5, "ERROR", f"외부 src 참조: {tag['src']}")
    for tag in soup.find_all(href=True):
        if tag.name == "link" and re.match(r"^https?://", tag["href"], re.I):
            lint.add(5, "ERROR", f"외부 link href 참조: {tag['href']}")
    if re.search(r"@import", style_text):
        lint.add(5, "ERROR", "CSS @import 사용 — 자기완결 위반.")
    for m in re.finditer(r"url\(\s*['\"]?(https?://[^)'\"]+)", style_text, re.I):
        lint.add(5, "ERROR", f"CSS 외부 url() 참조: {m.group(1)}")

    # ---------- 네거티브 리스트 파싱 (design-system.md §6.1) ----------
    banned_colors, banned_phrases = parse_negative_list(ds_src)

    # ---------- 색 수집 (체크 6·9용) ----------
    # 금지 색 HEX는 design-system.md 본문에 등장하므로 팔레트에서 명시적으로 뺀다
    # (빼지 않으면 금지 색이 "등재된 색"으로 통과한다).
    palette = {norm_hex(h) for h in HEX_RE.findall(ds_src)} - banned_colors
    used_colors = set()
    all_inline_styles = []
    for s in sections:
        for el in s.find_all(True):
            st_raw = el.get("style")
            if st_raw:
                all_inline_styles.append(resolve_vars(st_raw, root_vars))
    resolved_style_text = resolve_vars(style_text, root_vars)
    color_sources = all_inline_styles + [resolved_style_text]
    for src_text in color_sources:
        for h in HEX_RE.findall(src_text or ""):
            used_colors.add(norm_hex(h))
        for m in re.finditer(r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", src_text or ""):
            r, g, b = (int(x) for x in m.groups())
            used_colors.add("#{:02x}{:02x}{:02x}".format(r, g, b))

    # ---------- 체크 6: HEX 준수 + 브랜드 금지 색 ----------
    for c in sorted(used_colors):
        if c in banned_colors:
            lint.add(6, "ERROR", f"브랜드 금지 색 사용: {c} (design-system.md §6.1 네거티브 리스트).")
        elif c not in palette and not is_grayscale(c):
            lint.add(6, "ERROR", f"팔레트 외 색 사용: {c} (design-system.md 미등재, 무채색 아님).")

    # ---------- 체크 7: 폰트 ≤3 ----------
    families = set()
    for src_text in color_sources:
        for m in re.finditer(r"font-family\s*:\s*([^;}]+)", src_text or "", re.I):
            first = m.group(1).split(",")[0].strip().strip("'\"")
            if first and not first.startswith("var("):
                families.add(first)
    if len(families) > 3:
        lint.add(7, "ERROR", f"폰트 패밀리 {len(families)}종 사용(3 초과): {sorted(families)}")

    # ---------- 체크 8: 금지 CSS 12항 ----------
    combined = "\n".join(color_sources)
    forbidden = [
        (r"(linear|radial|conic)-gradient", "그라데이션 (금지 1항)"),
        (r"backdrop-filter\s*:", "backdrop-filter (금지 2항)"),
        (r"(?<!backdrop-)\bfilter\s*:", "filter (금지 2항)"),
        (r"box-shadow\s*:|text-shadow\s*:", "그림자 (금지 3항)"),
        (r"clip-path\s*:|\bmask\s*:|-webkit-mask", "clip-path/mask (금지 5항)"),
        (r"::?before\b|::?after\b", "::before/::after 장식 (금지 6항)"),
        (r"\banimation(-[\w]+)?\s*:|\btransition(-[\w]+)?\s*:", "animation/transition (금지 7항)"),
        (r"writing-mode\s*:\s*vertical|background-clip\s*:\s*text", "세로쓰기/텍스트 클립 (금지 8항)"),
        (r"@font-face", "웹폰트 @font-face (금지 9항 — 시스템 폰트 스택만)"),
        (r"position\s*:\s*(fixed|sticky)", "position fixed/sticky (금지 11항)"),
    ]
    for pat, label in forbidden:
        for m in re.finditer(pat, combined, re.I):
            lint.add(8, "ERROR", f"금지 CSS — {label}: `{m.group(0)}`")
            break  # 항목당 1회 보고
    # transform: rotate(Ndeg) 단독만 허용 (금지 4항)
    for m in re.finditer(r"transform\s*:\s*([^;}]+)", combined, re.I):
        val = m.group(1).strip()
        if not re.match(r"^rotate\(\s*-?\d+(\.\d+)?deg\s*\)$", val):
            lint.add(8, "ERROR", f"금지 CSS — transform은 rotate(Ndeg) 단독만 허용 (금지 4항): `{val}`")
    # opacity < 1 / rgba·hsla 알파 (금지 12항)
    for m in re.finditer(r"opacity\s*:\s*(0?\.\d+|0)\b", combined):
        lint.add(8, "ERROR", f"금지 CSS — 반투명 opacity:{m.group(1)} (금지 12항, 연한 단색으로 대체).")
    for m in re.finditer(r"(rgba|hsla)\([^)]*,\s*(0?\.\d+|0)\s*\)", combined):
        lint.add(8, "ERROR", f"금지 CSS — {m.group(1)} 알파 {m.group(2)} 반투명 (금지 12항).")
    # .slide 직계 flex/grid (금지 10항): .slide 셀렉터 규칙 + 섹션 인라인
    for m in re.finditer(r"([^{}]+)\{([^}]*)\}", style_text):
        sel, body = m.group(1), m.group(2)
        if ".slide" in sel and re.search(r"display\s*:\s*(flex|grid)", body):
            lint.add(8, "ERROR", "금지 CSS — .slide 직계 배치에 flex/grid (금지 10항).")
    for s in sections:
        st = parse_style(s.get("style", ""))
        if re.match(r"^(flex|grid)$", st.get("display", "")):
            lint.add(8, "ERROR", "금지 CSS — section.slide 인라인 display:flex/grid (금지 10항).")

    # ---------- 체크 9: 보라/인디고 단색 대역 ----------
    for c in sorted(used_colors):
        h, s_, v = rgb_to_hsv(*hex_rgb(c))
        if 235 <= h <= 275 and s_ >= 0.45 and v >= 0.45:
            lint.add(9, "WARN", f"인디고/바이올렛 대역 단색 {c} — AI slop 시그니처 색상. 팔레트 재고 권장.")

    # ---------- 체크 10: 가운데 정렬 비율 ----------
    text_els, centered = 0, 0
    for s in sections:
        for el in collect_el_elements(s):
            if el_kind(el) != "el-text":
                continue
            text_els += 1
            st = parse_style(el.get("style", ""))
            if st.get("text-align", "").strip() == "center":
                centered += 1
    if text_els and centered / text_els > 0.6:
        lint.add(10, "WARN", f"가운데 정렬 비율 {centered}/{text_els} ({centered / text_els:.0%}) — 60% 초과.")

    # ---------- 체크 11: radius 균일 ----------
    radii = []
    for src_text in color_sources:
        for m in re.finditer(r"border-radius\s*:\s*(\d+(?:\.\d+)?)px", src_text or ""):
            radii.append(float(m.group(1)))
    big = [r for r in radii if r >= 16]
    if len(radii) >= 5 and big:
        from collections import Counter
        top_val, top_cnt = Counter(big).most_common(1)[0]
        if top_cnt / len(radii) > 0.8:
            lint.add(11, "WARN", f"border-radius {top_val:.0f}px가 전체의 {top_cnt}/{len(radii)} — 80% 초과 균일. radius 계층 규칙 적용 필요.")

    # ---------- 체크 12: 이모지 ----------
    for i, s in enumerate(sections, 1):
        hits = EMOJI_RE.findall(s.get_text())
        if hits:
            lint.add(12, "ERROR", f"S{i}: 이모지 디자인 요소 검출: {' '.join(hits[:5])}")

    # ---------- 체크 13: 제네릭 제목 ----------
    for i, s in enumerate(sections, 1):
        head = s.find(["h1", "h2"])
        title = head.get_text(strip=True) if head else ""
        for pat in GENERIC_TITLES:
            if pat.lower() in title.lower():
                lint.add(13, "WARN", f"S{i}: 제네릭 제목 패턴 '{pat}' — 제목은 주장이어야 한다: \"{title}\"")

    # ---------- 체크 14: 최소 폰트 ----------
    for i, s in enumerate(sections, 1):
        for el in s.find_all(True):
            if el.name == "aside":
                continue
            st = {k: resolve_vars(v, root_vars) for k, v in parse_style(el.get("style", "")).items()}
            fs = px(st.get("font-size"))
            if fs is None:
                continue
            is_caption = has_class_up(el, ("source", "caption"), s)
            if fs < 12:
                lint.add(14, "ERROR", f"S{i}: font-size {fs:.0f}px < 12px (최소 하한).")
            elif fs < 18 and not is_caption:
                lint.add(14, "ERROR", f"S{i}: 본문 font-size {fs:.0f}px < 18px (캡션·출처는 .source/.caption 클래스 필요).")

    # ---------- 체크 15: 출처 ----------
    for i, s in enumerate(sections, 1):
        body_text = " ".join(
            el.get_text(" ", strip=True) for el in collect_el_elements(s) if el_kind(el) != "el-image"
        )
        if NUMERIC_CLAIM_RE.search(body_text):
            has_source = any(
                "source" in (el.get("class") or []) for el in s.find_all(True)
            )
            if not has_source:
                lint.add(15, "WARN", f"S{i}: 수치가 있으나 .source(출처) 요소 없음.")

    # ---------- 체크 16: 시간 배분 (PARTIAL 모드는 생략 — 조각에는 전체 합이 없다) ----------
    if not args.partial:
        m_total = re.search(r"발표\s*시간\s*[:：]\s*(\d+(?:\.\d+)?)\s*분", story_src)
        slide_times = [float(x) for x in re.findall(r"예상\s*시간\s*[:：]\s*(\d+(?:\.\d+)?)\s*분", story_src)]
        if not m_total:
            lint.add(16, "WARN", "storyline.md에 '발표 시간: N분' 필드가 없다.")
        elif not slide_times:
            lint.add(16, "WARN", "storyline.md에 장별 '예상 시간' 필드가 없다.")
        else:
            total = float(m_total.group(1))
            ssum = sum(slide_times)
            if total > 0 and abs(ssum - total) > total * 0.10:
                lint.add(16, "WARN", f"시간 정합 이탈 — 장별 합 {ssum:.1f}분 vs 발표 시간 {total:.0f}분 (±10% 초과).")

    # ---------- 체크 17: 발표자 노트 ----------
    for i, s in enumerate(sections, 1):
        notes = s.find("aside", class_="notes")
        if notes is None or not notes.get_text(strip=True):
            lint.add(17, "ERROR", f"S{i}: aside.notes(발표자 노트)가 없거나 비어 있음.")

    # ---------- 체크 18: 민감정보 ----------
    full_text = "\n".join(s.get_text("\n") for s in sections)
    for label, pat in SENSITIVE_PATTERNS:
        # finditer + group(0): 그룹이 있는 패턴에서 findall이 튜플을 돌려줘 예시가 깨지는 것을 막는다
        hits = [m.group(0).strip() for m in pat.finditer(full_text)]
        if hits:
            sample = re.sub(r"\s+", " ", hits[0])[:40]
            lint.add(18, "WARN", f"민감정보 의심 — {label}: 예 `{sample}` 외 {len(hits) - 1}건.")
            lint.safety_flags.append(f"{label} {len(hits)}건 검출 — 사용자 명시 확인 전 배포 금지 (STOP 게이트).")

    # ---------- 체크 19: 분량 ----------
    for i, s in enumerate(sections, 1):
        body_lines = 0
        for el in collect_el_elements(s):
            if el_kind(el) != "el-text":
                continue
            if has_class_up(el, ("source", "caption"), s):
                continue
            blocks = el.find_all(["p", "li"])
            body_lines += len([b for b in blocks if b.get_text(strip=True)])
        if body_lines > 6:
            lint.add(19, "ERROR", f"S{i}: 본문 {body_lines}줄 — 장당 6줄 초과.")
        for lst in s.find_all(["ul", "ol"]):
            n = len(lst.find_all("li", recursive=False))
            if n > 5:
                lint.add(19, "ERROR", f"S{i}: 불릿 {n}개 — 5개 초과.")

    # ---------- 체크 20: 표현 (격식체 + 브랜드 금지 표현) ----------
    for i, s in enumerate(sections, 1):
        stext = s.get_text(" ")
        for m in INFORMAL_RE.finditer(stext):
            lint.add(20, "WARN", f"S{i}: 비격식 종결어미 의심 `{m.group(0).strip()}` — 격식체(합쇼체) 확인 필요.")
            break  # 장당 1회 보고
        low = stext.lower()
        for phrase in banned_phrases:
            if phrase.lower() in low:
                lint.add(20, "ERROR", f"S{i}: 브랜드 금지 표현 `{phrase}` 사용 (design-system.md §6.1).")

    # ---------- 렌더 검사 ----------
    render_status = "SKIP(--no-render)"
    if render_skip_reason:
        render_status = f"SKIP({render_skip_reason})"
    elif not args.no_render:
        chrome = find_chrome()
        if chrome:
            run_render_check(os.path.abspath(args.deck), chrome, lint,
                             src=html_src if wrapped else None)
            render_status = f"실행됨 ({chrome})"
        else:
            lint.add(4, "WARN", "headless Chrome 미탐지 — 렌더 오버플로 검사 SKIP. "
                                "설치: https://www.google.com/chrome/ 또는 $CHROME_BIN 지정.")
            render_status = "SKIP(Chrome 부재)"

    # ---------- 보고서 ----------
    n_err = len(lint.errors())
    n_warn = len([f for f in lint.findings if f[1] == "WARN"])
    partial_label = "PARTIAL 모드 — 체크 1·2·16 생략"
    if args.partial:
        lines = [f"# Lint Report — {os.path.basename(args.deck)} ({partial_label})", ""]
    else:
        lines = ["# Lint Report — deck.html", ""]
    if lint.safety_flags:
        lines += ["## [안전 플래그] 민감정보 — 오케스트레이터 STOP 게이트 에스컬레이션", ""]
        lines += [f"- {f}" for f in lint.safety_flags]
        lines += [""]
    lines += [
        f"- 대상: `{args.deck}` (섹션 {len(sections)}개)",
        f"- 결과: **ERROR {n_err} / WARN {n_warn}**",
        f"- 렌더 검사: {render_status}",
    ]
    if args.partial:
        lines.append(f"- 모드: **{partial_label}** — 조각 단독 lint. 장수·cover/cta·시간 합은 조립 후 전체 lint에서 판정한다."
                     + (f" (<head>를 `{wrap_source}`에서 씌움{'' if args.wrap_head else ' — 자동 탐지'})" if wrapped else ""))
    lines += [
        "",
        "| # | 레벨 | 내용 |",
        "|---|---|---|",
    ]
    for no, level, msg in sorted(lint.findings, key=lambda x: (x[0], x[1])):
        esc = msg.replace("|", "\\|")  # f-string 내 백슬래시는 Python <3.12 SyntaxError
        lines.append(f"| {no} | {level} | {esc} |")
    if not lint.findings:
        lines.append("| - | INFO | 지적 사항 없음 — 체크 1~20 전체 통과 |")
    lines += ["", "> ERROR는 스프린트 핸드오프 전 반드시 0으로 만든다. WARN은 Evaluator가 판단한다."]
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    mode = f"lint[{partial_label}]" if args.partial else "lint"
    print(f"{mode}: ERROR {n_err} / WARN {n_warn} → {report_path}")
    sys.exit(1 if n_err else 0)


if __name__ == "__main__":
    main()
