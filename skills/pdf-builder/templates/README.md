# PDF Builder 템플릿 (Assets)

문서 생성에 사용되는 Typst 템플릿 모음.

## 디자인 시스템 (Typst 단독)

| 파일 | 용도 |
|------|------|
| `typst/frentis-base.typ` | 공용 디자인 시스템 — 모든 .typ 문서가 import |

### Quarto Template-Partials

Quarto+Typst 렌더링 시 `_quarto.yml`의 `template-partials`로 참조.

| 파일 | 용도 |
|------|------|
| `typst/report/typst-show.typ` | 비즈니스 보고서 |
| `typst/book/typst-show.typ` | 기술서/출판물 (H1 pagebreak) |
| `typst/proposal/typst-show.typ` | 제안서 (넓은 줄간격) |
| `typst/catalog/typst-template.typ` | 카탈로그 (커버 포함) |

## 독립 Typst 문서 템플릿 (멀티 섹션)

| 템플릿 | 용도 | 빌드 |
|--------|------|------|
| `spec/` | 기능 요구사항 문서 | `typst compile` |
| `catalog/` | Q&A 카탈로그 | `typst compile` |
| `handout/` | 워크샵/교육 핸드아웃 | `typst compile` |

## 폰트

- 본문: Pretendard, Apple SD Gothic Neo
- 코드: Monoplex KR Nerd, Menlo
