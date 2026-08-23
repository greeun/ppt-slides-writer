#!/usr/bin/env python3
"""
슬라이드 섹션 스캐너
- slides/ 폴더의 마크다운 섹션 파일 분석
- frontmatter에서 메타데이터 추출, --- 구분자로 슬라이드 수 계산
- hub.md 업데이트용 데이터 생성

Usage:
    uv run section-scanner.py slides/2025-12-22-스펙주도개발/
    uv run section-scanner.py slides/2025-12-22-스펙주도개발/ --format markdown
    uv run section-scanner.py slides/2025-12-22-스펙주도개발/ --update-hub
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def parse_frontmatter(content: str) -> dict:
    """마크다운 파일의 frontmatter를 파싱하여 딕셔너리로 반환."""
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}

    fm = {}
    for line in match.group(1).strip().split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip().strip('"').strip("'")
    return fm


def count_slides(content: str) -> int:
    """--- 구분자 수로 슬라이드 수 계산 (frontmatter 제외)."""
    # frontmatter 제거
    fm_match = re.match(r"^---\s*\n.*?\n---\s*\n?", content, re.DOTALL)
    body = content[fm_match.end():] if fm_match else content

    if not body.strip():
        return 0

    # --- 로 분리된 슬라이드 수 = 구분자 수 + 1 (첫 슬라이드)
    # 단, 빈 body면 0
    slides = re.split(r"\n---\s*\n", body.strip())
    return len(slides)


def scan_section(md_file: Path) -> dict | None:
    """마크다운 섹션 파일 분석."""
    try:
        content = md_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)

        if not fm:
            return None

        slide_count = count_slides(content)

        return {
            "file": md_file.name,
            "section": fm.get("section"),
            "title": fm.get("title", "Unknown"),
            "duration": fm.get("duration", "?"),
            "slide_count": slide_count,
        }
    except Exception as e:
        print(f"Warning: {md_file.name} 파싱 실패: {e}", file=sys.stderr)
        return None


def scan_project(project_folder: Path) -> list[dict]:
    """프로젝트 폴더의 모든 섹션 스캔 (hub.md 제외)."""
    md_files = sorted(
        f for f in project_folder.glob("*.md")
        if f.name != "hub.md"
    )
    sections = []

    for f in md_files:
        section = scan_section(f)
        if section:
            sections.append(section)

    return sections


def format_markdown_table(sections: list[dict]) -> str:
    """마크다운 테이블 생성."""
    if not sections:
        return "섹션 없음"

    total_slides = sum(s["slide_count"] for s in sections)

    lines = [
        "| 섹션 | 파일 | 슬라이드 | 시간 |",
        "|------|------|:--------:|:----:|"
    ]

    for s in sections:
        sec_num = f"{s['section']}. " if s["section"] else ""
        lines.append(
            f"| {sec_num}{s['title']} | `{s['file']}` | {s['slide_count']}장 | {s['duration']} |"
        )

    lines.append(f"\n**총 슬라이드: {total_slides}장**")

    return "\n".join(lines)


def format_json(sections: list[dict]) -> str:
    """JSON 형식 출력."""
    import json
    return json.dumps(sections, ensure_ascii=False, indent=2)


def update_hub(project_folder: Path, sections: list[dict]) -> bool:
    """hub.md 파일 업데이트."""
    hub_file = project_folder / "hub.md"

    if not hub_file.exists():
        print(f"Warning: hub.md가 없습니다: {hub_file}")
        return False

    content = hub_file.read_text(encoding="utf-8")

    table = format_markdown_table(sections)

    marker_start = "## 섹션별 슬라이드"
    marker_end = "\n## "

    start_idx = content.find(marker_start)
    if start_idx == -1:
        print("Warning: '## 섹션별 슬라이드' 섹션을 찾을 수 없습니다")
        return False

    end_idx = content.find(marker_end, start_idx + len(marker_start))
    if end_idx == -1:
        end_idx = len(content)

    new_content = (
        content[:start_idx]
        + marker_start + "\n\n" + table + "\n\n"
        + content[end_idx:]
    )

    hub_file.write_text(new_content, encoding="utf-8")
    print(f"hub.md 업데이트 완료: {hub_file}")
    return True


def main():
    parser = argparse.ArgumentParser(description="슬라이드 섹션 스캐너")
    parser.add_argument("folder", help="슬라이드 프로젝트 폴더")
    parser.add_argument(
        "--format", "-f",
        choices=["table", "markdown", "json"],
        default="table",
        help="출력 형식",
    )
    parser.add_argument(
        "--update-hub",
        action="store_true",
        help="hub.md 자동 업데이트",
    )

    args = parser.parse_args()
    folder = Path(args.folder)

    if not folder.exists():
        print(f"Error: 폴더가 존재하지 않습니다: {folder}")
        sys.exit(1)

    sections = scan_project(folder)

    if not sections:
        print("섹션 파일이 없습니다")
        sys.exit(0)

    if args.update_hub:
        update_hub(folder, sections)
    elif args.format == "json":
        print(format_json(sections))
    else:
        print(format_markdown_table(sections))


if __name__ == "__main__":
    main()
