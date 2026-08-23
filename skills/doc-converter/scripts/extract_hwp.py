#!/usr/bin/env python3
"""HWP/HWPX 텍스트 추출 스크립트

Usage:
    python3 extract_hwp.py <hwpx_path>
    python3 extract_hwp.py <hwpx_path> --tables-only
    python3 extract_hwp.py <hwpx_path> --meta-only

Output (stdout):
    - 정상: <!-- META: {...} --> + 마크다운 텍스트
    - 에러: {"status": "ERROR", "message": "..."}
"""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


def extract_hwpx_meta(path: str) -> dict:
    """HWPX 메타정보 추출."""
    try:
        with zipfile.ZipFile(path, "r") as z:
            sections = [
                n for n in z.namelist()
                if n.startswith("Contents/section") and n.endswith(".xml")
            ]
            total_chars = 0
            for name in sections:
                root = ET.fromstring(z.read(name))
                for elem in root.iter():
                    if elem.text and elem.text.strip():
                        total_chars += len(elem.text.strip())
            return {
                "status": "OK",
                "format": "hwpx",
                "sections": len(sections),
                "chars": total_chars,
            }
    except zipfile.BadZipFile:
        return {"status": "ERROR", "message": "HWPX가 아닌 파일 (BadZipFile). HWP 바이너리일 수 있음."}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}


def extract_hwpx_text(path: str) -> str:
    """HWPX에서 텍스트를 마크다운으로 추출."""
    try:
        from hwpx.document import HwpxDocument

        doc = HwpxDocument.open(path)
        lines = []
        for para in doc.paragraphs:
            text = para.text.strip()
            lines.append(text if text else "")
        return "\n".join(lines)
    except ImportError:
        # python-hwpx 없으면 ZIP 직접 파싱
        return extract_hwpx_text_raw(path)


def extract_hwpx_text_raw(path: str) -> str:
    """ZIP 직접 파싱으로 HWPX 텍스트 추출 (라이브러리 불필요)."""
    lines = []
    with zipfile.ZipFile(path, "r") as z:
        for name in sorted(z.namelist()):
            if name.startswith("Contents/section") and name.endswith(".xml"):
                root = ET.fromstring(z.read(name))
                for elem in root.iter():
                    if elem.text and elem.text.strip():
                        lines.append(elem.text.strip())
    return "\n".join(lines)


def extract_hwpx_tables(path: str) -> str:
    """HWPX에서 표만 마크다운 테이블로 추출."""
    try:
        from hwpx.document import HwpxDocument

        doc = HwpxDocument.open(path)
        output = []
        for si, section in enumerate(doc.sections):
            for ti, table in enumerate(section.tables):
                output.append(f"### 표 {si + 1}-{ti + 1} ({table.row_count}x{table.col_count})")
                output.append("")
                for ri in range(table.row_count):
                    cells = []
                    for ci in range(table.col_count):
                        cell_text = table.get_cell_text(ri, ci) or ""
                        cells.append(cell_text.strip())
                    output.append("| " + " | ".join(cells) + " |")
                    if ri == 0:
                        output.append("|" + "|".join(["---"] * len(cells)) + "|")
                output.append("")
        return "\n".join(output) if output else "표가 없습니다."
    except ImportError:
        return '{"status": "ERROR", "message": "python-hwpx 필요: pip install python-hwpx"}'


def main():
    parser = argparse.ArgumentParser(description="HWP/HWPX to Markdown extractor")
    parser.add_argument("path", help="HWPX 파일 경로")
    parser.add_argument("--tables-only", action="store_true", help="표만 추출")
    parser.add_argument("--meta-only", action="store_true", help="메타정보만 출력")
    args = parser.parse_args()

    path = args.path
    if not Path(path).exists():
        print(json.dumps({"status": "ERROR", "message": f"파일 없음: {path}"}))
        sys.exit(1)

    if args.meta_only:
        print(json.dumps(extract_hwpx_meta(path), ensure_ascii=False))
        return

    if args.tables_only:
        print(extract_hwpx_tables(path))
        return

    # 메타정보 확인
    meta = extract_hwpx_meta(path)
    if meta["status"] != "OK":
        print(json.dumps(meta, ensure_ascii=False))
        sys.exit(1)

    # 텍스트 추출
    text = extract_hwpx_text(path)
    print(f"<!-- META: {json.dumps(meta, ensure_ascii=False)} -->")
    print(text)


if __name__ == "__main__":
    main()
