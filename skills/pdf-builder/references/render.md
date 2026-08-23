# Render — PDF 렌더링 상세 절차

PDF 렌더링 시 방식 판별부터 결과 확인까지의 상세 절차.

## 방식 판별

| 조건 | 방식 | 명령 |
|------|------|------|
| `.typ` 파일 (Typst 단독) | **typst-build** | `typst compile --root <vault-root>` |
| `_quarto.yml` 있음 | **Quarto + Typst** | `quarto render --to typst` |
| `.md` 파일만 있음 | **convert 먼저** | workflows/convert.md 참조 |

## Typst 단독 렌더 (기본)

```bash
# vault 루트에서 실행
typst compile --root . business/reports/보고서.typ business/reports/보고서.pdf
```

> frentis-base.typ import 시 반드시 `--root` 필요

## Quarto + Typst 렌더 (예외)

### Phase 1: 검사

1. `_quarto.yml` 존재 + `format: typst` 확인
2. 필수 파일 체크: `typst-show.typ`, `*.qmd`
3. 문제 보고

### Phase 2: 준비

1. 템플릿 선택 (새 프로젝트): report / book / proposal / catalog
2. 설정 파일 복사: `cp -r .claude/skills/pdf-builder/templates/typst/{type}/* ./`
3. 참고문헌 동기화: `uv run .claude/scripts/lit-to-bib.py`

**Quarto 폰트 주의사항:**
```yaml
# _quarto.yml — mainfont 제거!
format:
  typst:
    papersize: a4
    # mainfont: "Pretendard"  ← 제거! typst-show.typ에서만 정의
    fontsize: 11pt
    template-partials: [typst-show.typ]
```

### Phase 3: 렌더

```bash
quarto render --to typst        # 전체
quarto render content.qmd --to typst  # 특정 파일
```

## 결과 확인

```
✅ 렌더링 완료
📄 출력: _output/document.pdf
📊 페이지: N페이지, 파일 크기: X MB
```

## 오류 처리

| 오류 | 원인 | 해결 |
|------|------|------|
| 폰트 없음 | Pretendard 미설치 | 폰트 설치 안내 |
| 한글 깨짐 | _quarto.yml mainfont 문제 | mainfont 제거, typst-show.typ에서 정의 |
| project root 오류 | frentis-base import | `--root` 플래그 추가 |
| 참조 깨짐 | 누락된 인용 | 참고문헌 동기화 |

## 출력 경로

| 프로젝트 | 출력 |
|---------|------|
| Quarto 프로젝트 | `_output/` |
| Typst 단독 | 같은 폴더 |
