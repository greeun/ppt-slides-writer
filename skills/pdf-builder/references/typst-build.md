# Typst Build — PDF 빌드 워크플로우

## 트리거

- "PDF 빌드", "컴파일", "typst"

## 절차

### 1. 입력 확인

```
"docs/workshop/pdf/main.typ 빌드"
"이 보고서 PDF로"
```

### 2. frentis-base 사용 여부 확인

```typst
// frentis-base import가 있으면 --root 필요
#import "/.claude/skills/pdf-builder/templates/typst/frentis-base.typ": *
```

### 3. 빌드 실행

**frentis-base 사용 시 (절대 경로 import):**
```bash
typst compile --root <vault-root> {input} {output}
```

**독립 .typ 파일 (import 없음):**
```bash
typst compile {input} {output}
```

### 4. 결과 확인

```
✅ PDF 빌드 완료

입력: business/reports/REP-2026-02-19-SAM-AI-주간보고.typ
출력: business/reports/REP-2026-02-19-SAM-AI-주간보고.pdf
크기: 29KB
```

## 새 .typ 파일 작성 가이드

```typst
#import "/.claude/skills/pdf-builder/templates/typst/frentis-base.typ": *

// 1페이지 주간보고 (compact)
#show: frentis-doc.with(
  title: "제목",
  subtitle: "부제",
  cover: false,
  header-footer: false,
  numbering: none,
  fontsize: 9pt,
  margin: (top: 1.2cm, bottom: 1.2cm, left: 1.2cm, right: 1.2cm),
  leading: 0.85em,
)

// 기술 보고서 (헤더 + 로고, 표지 없음)
#show: frentis-doc.with(
  title: "제목",
  subtitle: "부제",
  cover: false,
  logo: "/path/to/company_logo.png",
  header-footer: true,
  header-text: "프로젝트명",
  numbering: "1.1.1",
)

// 정식 보고서 (그라데이션 표지 + 목차)
#show: frentis-doc.with(
  title: "제목",
  subtitle: "부제",
  author: "프렌티스",
  date: "2026년 2월",
  cover: true,
  cover-style: "gradient",
  logo: "/path/to/company_logo.png",
  toc: true,
  header-footer: true,
)

// 제안서 (심플 표지)
#show: frentis-doc.with(
  title: "제목",
  subtitle: "부제",
  author: "프렌티스",
  date: "2026년 2월",
  cover: true,
  cover-style: "simple",
  logo: "/path/to/company_logo.png",
  toc: true,
)
```

## 절대 금지

- **ASCII 아트 다이어그램 금지** — 다이어그램은 diagram-builder 스킬로 Draw.io PNG 생성 후 이미지 삽입

## 일괄 빌드

```bash
# vault 내 모든 .typ → PDF
for f in *.typ; do typst compile --root <vault-root> "$f" "${f%.typ}.pdf"; done
```

## 에러 처리

| 오류 | 원인 | 해결 |
|------|------|------|
| cannot read file outside of project root | frentis-base 절대 경로 | `--root <vault-root>` 추가 |
| 폰트 없음 | Pretendard 미설치 | `brew install --cask font-pretendard` |
| 문법 오류 | Typst 문법 문제 | 오류 위치 확인 후 수정 |

## 한글 렌더링 함정

### 1. 백틱 인라인 코드 안의 한글이 깨짐

**증상**: ``` `AI교육과정설계제안-260501.xlsx` ``` 같은 인라인 코드에서 한글이 자모 분해된 것처럼 깨져 표시됨.

**원인**: typst의 raw(백틱) 텍스트는 기본 monospace 폰트(Fira Code 등 영문 위주)로 렌더링되는데, 영문 monospace 폰트에 한글 글리프가 없어 fallback이 잘못 처리됨.

**해결**: typst 파일 상단에 raw 텍스트의 폰트 fallback을 명시적으로 설정.

```typst
#set text(
  font: ("Apple SD Gothic Neo", "Pretendard"),
  size: 9.5pt,
  lang: "ko",
)

// 인라인 코드(백틱) 안에 한글이 들어가는 경우 필수
#show raw: set text(font: ("Apple SD Gothic Neo", "Pretendard"), size: 9pt)
```

> **주의**: frentis-base 템플릿을 사용하지 않고 직접 `#set text` 만으로 폰트를 설정하는 경우 이 `#show raw` 설정이 별도로 필요. frentis-base에는 기본 적용되어 있는지 확인.

### 2. 한글 텍스트가 자모 분해 형태(NFD)로 들어간 경우

**증상**: macOS 파일명을 그대로 typst에 붙여넣었을 때 자모가 분해된 채로 보임.

**원인**: macOS 파일 시스템(HFS+/APFS)이 한글을 NFD 형태로 저장. 클립보드를 통해 붙여넣으면 NFD 형태가 typst에 들어갈 수 있음.

**해결**: NFC 정규화 적용 (입력 측 또는 typst 후처리)

```bash
python3 -c "
import unicodedata
with open('input.typ', 'r', encoding='utf-8') as f: text = f.read()
nfc = unicodedata.normalize('NFC', text)
with open('input.typ', 'w', encoding='utf-8') as f: f.write(nfc)
"
```

### 3. 한글 폰트 우선순위

macOS 환경에서는 `Apple SD Gothic Neo`를 1순위로 두는 것이 가장 안정적. Pretendard는 가독성이 좋지만 일부 환경에서 임베딩·렌더링 이슈가 발생 가능.

```typst
#set text(font: ("Apple SD Gothic Neo", "Pretendard"))
```

## 감시 모드

```bash
typst watch --root <vault-root> input.typ output.pdf
```
