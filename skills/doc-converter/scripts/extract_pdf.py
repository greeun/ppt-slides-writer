#!/usr/bin/env python3
"""PDF 텍스트 추출 스크립트 (pymupdf4llm 기반)

Usage:
    python3 extract_pdf.py <pdf_path> [--pages 0,1,2] [--meta-only]

Output (stdout):
    - 정상: <!-- META: {...} --> + 마크다운 텍스트
    - 스캔 PDF: {"status": "SCANNED", "pages": N}
    - 인코딩 깨짐: {"status": "GARBLED", "pages": N, ...}
    - 에러: {"status": "ERROR", "message": "..."}
"""

import sys
import json
import argparse
import unicodedata

import fitz
import pymupdf4llm


def detect_scanned(doc, threshold=100):
    """스캔 PDF 감지: 페이지당 평균 텍스트가 threshold자 미만이면 스캔으로 판단"""
    if len(doc) == 0:
        return True
    total_text = sum(len(page.get_text()) for page in doc)
    avg_per_page = total_text / len(doc)
    return avg_per_page < threshold


def detect_garbled(doc, sample_pages=5):
    """폰트 인코딩 깨짐 감지.

    두 가지 패턴을 감지:
    1. 대체 문자(U+FFFD), PUA, 미할당 코드포인트 비율이 높은 경우
    2. 비ASCII 텍스트가 대부분 Latin1-Supplement(0xC0-0xFF)인 경우
       (한국어/CJK 문서인데 한글이 거의 없고 Latin 문자가 대부분)
    """
    pages_to_check = min(sample_pages, len(doc))
    total_chars = 0
    suspect_chars = 0
    latin1_supp = 0
    hangul_cjk = 0

    for i in range(pages_to_check):
        text = doc[i].get_text()
        for ch in text:
            if ch.isspace():
                continue
            total_chars += 1
            cp = ord(ch)

            # 패턴 1: 명백한 깨짐 문자
            if ch == '\ufffd':
                suspect_chars += 1
            elif unicodedata.category(ch).startswith('Co'):
                suspect_chars += 1
            elif cp > 0x7F and unicodedata.category(ch) == 'Cn':
                suspect_chars += 1

            # 패턴 2: 블록 분류
            if 0x00C0 <= cp <= 0x024F:
                latin1_supp += 1
            elif 0xAC00 <= cp <= 0xD7AF or 0x4E00 <= cp <= 0x9FFF:
                hangul_cjk += 1

    if total_chars == 0:
        return False

    # 패턴 1: 대체 문자/PUA 비율 30% 이상
    if (suspect_chars / total_chars) > 0.3:
        return True

    # 패턴 2: 비ASCII가 존재하고, Latin1이 높으면서 한글/CJK가 거의 없는 경우
    non_ascii = total_chars - sum(1 for i in range(pages_to_check)
                                  for ch in doc[i].get_text()
                                  if not ch.isspace() and ord(ch) < 0x80)
    if non_ascii > 50 and latin1_supp > 0:
        latin1_ratio = latin1_supp / non_ascii
        if latin1_ratio > 0.5 and hangul_cjk == 0:
            return True

    return False


def count_images(doc):
    """전체 이미지 수 카운트"""
    count = 0
    for page in doc:
        count += len(page.get_images(full=False))
    return count


def extract(pdf_path, pages=None, meta_only=False):
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(json.dumps({"status": "ERROR", "message": str(e)}))
        sys.exit(1)

    total_pages = len(doc)

    # 스캔 PDF 감지
    if detect_scanned(doc):
        result = {
            "status": "SCANNED",
            "pages": total_pages,
            "images": count_images(doc),
        }
        print(json.dumps(result))
        doc.close()
        return

    # 폰트 인코딩 깨짐 감지
    if detect_garbled(doc):
        result = {
            "status": "GARBLED",
            "pages": total_pages,
            "images": count_images(doc),
            "message": "폰트 인코딩 문제로 텍스트 추출 불가. 비전 폴백 필요.",
        }
        print(json.dumps(result))
        doc.close()
        return

    # 메타정보만 요청한 경우
    if meta_only:
        total_chars = sum(len(page.get_text()) for page in doc)
        result = {
            "status": "OK",
            "pages": total_pages,
            "chars": total_chars,
            "images": count_images(doc),
        }
        print(json.dumps(result))
        doc.close()
        return

    # 페이지 범위 파싱
    page_list = None
    if pages is not None:
        page_list = [int(p) for p in pages.split(",")]

    # pymupdf4llm으로 마크다운 추출
    md = pymupdf4llm.to_markdown(doc, pages=page_list)

    # 메타정보 헤더
    meta = {
        "status": "OK",
        "pages": total_pages,
        "extracted_pages": len(page_list) if page_list else total_pages,
        "method": "pymupdf4llm",
        "chars": len(md),
        "images": count_images(doc),
    }
    print(f"<!-- META: {json.dumps(meta)} -->")
    print(md)

    doc.close()


def main():
    parser = argparse.ArgumentParser(description="PDF to Markdown extractor")
    parser.add_argument("pdf_path", help="PDF 파일 경로")
    parser.add_argument("--pages", help="추출할 페이지 (0-indexed, 콤마 구분)", default=None)
    parser.add_argument("--meta-only", action="store_true", help="메타정보만 출력")
    args = parser.parse_args()

    extract(args.pdf_path, pages=args.pages, meta_only=args.meta_only)


if __name__ == "__main__":
    main()
