# HWP/HWPX → 마크다운 변환

HWP(바이너리) 및 HWPX(ZIP+XML) 파일의 텍스트 추출 워크플로우.

## 포맷 판별

```bash
file "${INPUT_FILE}"
# HWPX → ZIP archive
# HWP  → OLE Compound Document (또는 Hangul)
```

| 확장자 | 포맷 | 추출 방식 |
|--------|------|----------|
| `.hwpx` | ZIP + XML | python-hwpx 또는 ZIP 직접 파싱 |
| `.hwp` | OLE Binary | pyhwp (hwp5txt) 또는 비전 폴백 |

## HWPX 추출

### 방법 1: python-hwpx (권장)

```bash
uv run python3 .claude/skills/doc-converter/scripts/extract_hwp.py "${HWPX_PATH}"
```

### 방법 2: ZIP 직접 파싱 (python-hwpx 없을 때)

```bash
python3 -c "
import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile('${HWPX_PATH}', 'r') as z:
    for name in sorted(z.namelist()):
        if name.startswith('Contents/section') and name.endswith('.xml'):
            root = ET.fromstring(z.read(name))
            for elem in root.iter():
                if elem.text and elem.text.strip():
                    print(elem.text.strip())
"
```

## HWP (레거시) 추출

`extract_hwp.py`는 HWPX(ZIP+XML)만 처리합니다. 레거시 HWP(OLE 바이너리)는 아래 방법으로 추출합니다.

```bash
# 방법 1: pyhwp (권장)
uv run python3 -c "
from hwp5.hwp5txt import Hwp5Txt
txt = Hwp5Txt('${HWP_PATH}')
print(txt.text())
"

# 방법 2: hwp5txt CLI (pyhwp 설치 시 함께 제공)
uv run hwp5txt "${HWP_PATH}" > "${OUTPUT_MD}"

# 방법 3: 비전 폴백 (라이브러리 없을 때)
# Claude Read 도구로 직접 읽기 시도
```

## 표 추출

HWPX의 표를 마크다운 테이블로 변환:

```bash
uv run python3 .claude/skills/doc-converter/scripts/extract_hwp.py "${HWPX_PATH}" --tables-only
```

## 에러 처리

| 에러 | 원인 | 해결 |
|------|------|------|
| `BadZipFile` | HWP를 HWPX로 열려고 함 | 확장자/포맷 확인 |
| 한글 깨짐 | 인코딩 문제 | UTF-8 확인 |
| 빈 텍스트 | 이미지/도형만 있는 문서 | 비전 폴백 |
| 라이브러리 없음 | python-hwpx/pyhwp 미설치 | ZIP 직접 파싱 또는 비전 폴백 |
