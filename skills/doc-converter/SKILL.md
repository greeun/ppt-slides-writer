---
name: doc-converter
description: |
  PDF/HWP/이미지 → 마크다운 변환. 서브에이전트로 처리하여 컨텍스트 절약.
  사용 시점: "PDF 변환", "이미지 변환", "HWP 변환", "문서 추출", "마크다운으로 바꿔", "한글 파일 읽어"
version: 1.0.0
allowed-tools: [Read, Write, Bash, Agent, AskUserQuestion]
model: haiku
context: fork
---

# Document Converter Skill

PDF, HWP/HWPX, 이미지 파일을 마크다운으로 변환하는 스킬입니다.
**핵심 목적:** 서브에이전트가 변환 처리 → 메인 에이전트는 텍스트만 수신 (컨텍스트 절약)

## 변환 철학: AI-Readable 재구성

> "원본 충실 변환" ❌ → "AI-Readable 재구성" ✅

원본 레이아웃을 그대로 복제하려 하면 깨진다. 대신:
- 텍스트를 **프로그래밍적으로 정확 추출** (pymupdf4llm)
- AI가 내용을 **이해하고 재구성** (서브에이전트)
- 머리글/바닥글/페이지번호 등 **노이즈 제거**
- 의미적으로 자연스러운 **계층 재설계**

## 아키텍처

```
입력 파일
  ↓ 유형 판별 (확장자)
  ├─ PDF  → extract_pdf.py (pymupdf4llm)
  ├─ HWPX → extract_hwp.py (python-hwpx / ZIP 파싱)
  ├─ HWP  → pyhwp (hwp5txt) / 비전 폴백
  └─ 이미지 → Claude Read (비전)
  ↓
원시 텍스트 + 메타정보
  ↓
[AI 서브에이전트] 내용 이해 → AI-Readable MD 재구성
  ↓
깔끔한 마크다운 파일
```

**유형별 상세:**
- PDF: 아래 Workflow 섹션 참조
- HWP/HWPX: `Read workflows/hwp.md`
- 이미지/스캔: 비전 폴백 (아래 비전 폴백 섹션)

## Conversion Modes

| 모드 | 설명 | 용도 |
|------|------|------|
| **summary** | 핵심 내용만 요약 (1-2페이지) | 빠른 파악, 개요 확인 |
| **full** | AI-Readable MD로 전체 재구성 | 상세 분석, 문서화 |
| **extract** | 특정 섹션/정보만 추출 | 표, 그림, 특정 챕터 |

## Workflow

### Step 1: 파일 확인 및 모드 선택

```
User: "이 PDF 마크다운으로 변환해줘: /path/to/file.pdf"

Claude:
1. 파일 경로 확인
2. AskUserQuestion으로 모드 선택:
   - 요약 (핵심 내용만, 1-2페이지)
   - 전체 변환 (AI-Readable 재구성)
   - 특정 추출 (표, 그림, 섹션 지정)
```

### Step 2: 텍스트 추출 (유형별 분기)

#### PDF 파일 (pymupdf4llm)

```bash
python3 .claude/skills/doc-converter/scripts/extract_pdf.py "{pdf_path}"
```

결과 확인:
- `"status": "OK"` → 원시 텍스트 획득 성공 → Step 3으로
- `"status": "SCANNED"` → 텍스트 레이어 없음 → Step 3 비전 폴백
- `"status": "GARBLED"` → 폰트 인코딩 깨짐 → Step 3 비전 폴백
- `"status": "ERROR"` → 에러 메시지 확인

#### HWP/HWPX 파일

상세: `Read workflows/hwp.md`

```bash
# HWPX
python3 .claude/skills/doc-converter/scripts/extract_hwp.py "{hwpx_path}"
# 메타만
python3 .claude/skills/doc-converter/scripts/extract_hwp.py "{hwpx_path}" --meta-only
# 표만
python3 .claude/skills/doc-converter/scripts/extract_hwp.py "{hwpx_path}" --tables-only
```

- `"status": "OK"` → 텍스트 획득 → Step 3으로
- `"status": "ERROR"` + "BadZipFile" → HWP 바이너리일 수 있음 → pyhwp 또는 비전 폴백
- HWP(바이너리): `workflows/hwp.md`의 HWP 레거시 추출 참조

#### 이미지 파일 (PNG/JPG 등)

- 텍스트 추출 단계 건너뛰고 바로 Step 3 비전 모드로

**청크 분할 기준:**

반드시 `--meta-only`로 먼저 분량을 확인하고, 아래 기준에 따라 처리:

| 분량 | 처리 방식 |
|------|----------|
| ~30페이지 (chars < 90,000) | 한번에 추출 → 서브에이전트 1회 |
| 31~90페이지 | 30페이지씩 청크 분할 → 서브에이전트 N회 → 결과 합치기 |
| 91페이지+ | 30페이지씩 청크 분할 → 서브에이전트 N회 → 결과 합치기 (병렬 서브에이전트 권장) |

**청크 추출 방법:**
```bash
# 청크 1: 0~29페이지
python3 .../extract_pdf.py "{pdf_path}" --pages 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29
# 청크 2: 30~59페이지
python3 .../extract_pdf.py "{pdf_path}" --pages 30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59
# ... 반복
```

각 청크를 별도 서브에이전트로 처리한 후, 결과를 순서대로 합쳐서 최종 파일로 저장.

### Step 3: 서브에이전트로 변환 실행

#### 요약 모드 (summary)

```
Agent 도구 호출:
  subagent_type: "general-purpose"
  model: "haiku"
  prompt: |
    당신은 문서 전문가입니다. 아래 PDF에서 추출한 원시 텍스트를 읽고
    핵심 내용을 마크다운으로 요약해주세요.

    원칙:
    - 문서의 목적과 핵심 메시지를 먼저 파악
    - 주요 섹션별 핵심 포인트 (bullet points)
    - 중요한 수치, 날짜, 고유명사는 정확히 보존
    - 머리글, 바닥글, 페이지 번호 등 노이즈 무시

    출력 형식:
    # {문서 제목}

    ## 개요
    [1-2문장 요약]

    ## 핵심 내용
    - ...

    ## 주요 정보
    - ...

    ---
    추출된 원시 텍스트:
    {extracted_text}
```

#### 전체 변환 모드 (full)

```
Agent 도구 호출:
  subagent_type: "general-purpose"
  model: "haiku"
  prompt: |
    아래는 PDF에서 프로그래밍적으로 추출한 원시 텍스트입니다.
    이것을 깔끔한 마크다운으로 정리하세요.

    작업 범위 (구조 정리만, 내용 삭제/수정 금지):
    - 머리글, 바닥글, 페이지 번호, 반복되는 면책조항 등 노이즈만 제거
    - 의미에 맞는 제목 계층(H1~H3) 부여
    - 표는 마크다운 테이블로 유지. 깨진 표는 내용을 리스트/텍스트로 변환하되, 안에 있는 텍스트 내용은 반드시 보존
    - 불필요한 빈 줄 제거
    - 원본 텍스트의 표현, 문장, 수치, 고유명사를 그대로 보존 (의역/추가 금지)

    절대 금지:
    - 원본에 있는 섹션, 항목, 문단을 삭제하지 마세요
    - 깨진 표라도 그 안의 텍스트 내용은 리스트나 문단으로 반드시 보존하세요
    - "중복"으로 보여도 원본에 있으면 유지하세요 (실제로 다른 내용일 수 있음)

    결과물을 Write 도구로 아래 경로에 저장하세요:
    {output_path}

    ---
    추출된 원시 텍스트:
    {extracted_text}
```

#### 특정 추출 모드 (extract)

```
Agent 도구 호출:
  subagent_type: "general-purpose"
  model: "haiku"
  prompt: |
    아래 PDF에서 추출한 원시 텍스트에서 특정 정보를 추출·정리해주세요.
    추출 대상: {extraction_target}

    원칙:
    - 요청된 정보만 깔끔하게 정리
    - 표는 마크다운 테이블로, 깨진 표는 리스트로
    - 핵심 수치, 날짜, 고유명사 정확히 보존
    - 출처 페이지/섹션 참조 표기

    결과물을 Write 도구로 아래 경로에 저장하세요:
    {output_path}

    ---
    추출된 원시 텍스트:
    {extracted_text}
```

#### 비전 폴백 (스캔 PDF / 인코딩 깨짐 / 이미지)

스캔 PDF, 폰트 인코딩 깨진 PDF(GARBLED), 이미지 파일의 경우, 서브에이전트가 직접 Read tool로 파일을 읽는다:

```
Agent 도구 호출:
  subagent_type: "general-purpose"
  model: "haiku"
  prompt: |
    아래 파일을 Read 도구로 읽고(비전), 깔끔한 마크다운으로 정리하세요.
    파일: {file_path}

    작업 범위 (구조 정리만, 내용 수정 금지):
    - 머리글, 바닥글, 페이지 번호 등 노이즈 제거
    - 의미에 맞는 제목 계층(H1~H3) 부여
    - 표는 마크다운 테이블로 유지
    - 원본 텍스트의 표현, 문장, 수치, 고유명사를 그대로 보존 (의역/추가 금지)

    결과물을 Write 도구로 아래 경로에 저장하세요:
    {output_path}
```

### Step 4: 결과 처리

서브에이전트 결과 수신 후:

1. **파일 저장 여부 확인** (서브에이전트가 직접 저장하지 않은 경우)
   ```
   AskUserQuestion:
   - "변환 결과를 파일로 저장할까요?"
     - 예 → 지정 경로에 저장
     - 아니오 → 결과만 표시
   ```

2. **결과 반환**
   - 변환된 마크다운 텍스트 출력
   - 원본 파일 정보 (경로, 페이지 수, 추출 방식)

## File Type Support

| 파일 유형 | 추출 방식 | 스크립트 | 비고 |
|-----------|----------|----------|------|
| PDF (텍스트) | pymupdf4llm | `scripts/extract_pdf.py` | 정확한 텍스트 추출 |
| PDF (스캔) | Claude Read (비전) | — | 텍스트 레이어 없는 경우 폴백 |
| HWPX | python-hwpx / ZIP 파싱 | `scripts/extract_hwp.py` | ZIP+XML 구조 |
| HWP | pyhwp (hwp5txt) | — | 바이너리, 비전 폴백 가능 |
| PNG/JPG/GIF/WebP | Claude Read (비전) | — | OCR + 이미지 설명 |
| PPTX | Claude Read (비전) | — | 슬라이드별 변환 |
| DOCX | Claude Read (비전) | — | 구조 유지 변환 |

## Error Handling

1. **파일 없음**: 경로 확인 요청
2. **지원 안 되는 형식**: 지원 형식 안내
3. **스캔 PDF**: 비전 폴백 자동 전환 (사용자에게 알림)
4. **추출 실패**: 에러 메시지 표시, 비전 폴백 제안
5. **대용량 PDF**: `--meta-only`로 분량 확인 후 청크 처리

## Configuration

### 기본 설정

```yaml
default_mode: summary
default_model:
  summary: haiku
  full: haiku
  extract: haiku
save_results: ask  # always, never, ask
extract_script: .claude/skills/doc-converter/scripts/extract_pdf.py
```

## Do's and Don'ts

### DO

- 항상 서브에이전트로 처리 (컨텍스트 절약)
- PDF는 반드시 pymupdf4llm으로 먼저 텍스트 추출
- "AI-Readable 재구성" 철학 적용
- 스캔 PDF/이미지는 비전 폴백
- 모드 선택 기회 제공

### DON'T

- 메인 에이전트에서 직접 PDF 읽기 (토큰 낭비)
- "원본 레이아웃 유지" 시도 (깨짐의 원인)
- 모드 확인 없이 기본값 적용
- 대용량 파일 전체를 한번에 서브에이전트에 전달 (청크 분할 필요)

## Integration with Other Skills

| 스킬 | 연계 |
|------|------|
| curriculum-builder | 교재 PDF → LO 추출 |
| literature | 논문 PDF → Literature 노트 |
