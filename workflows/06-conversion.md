# Workflow 06 — 변환 (S-final) + 검증 21~26

목표: 승인된 deck.html을 **네이티브 PPTX + 픽셀 동일 PDF**로 변환하고 충실도를
기계 검증한다. 규칙은 `references/conversion-rules.md`.

## 의존성 확인 (최초 1회)

```bash
python3 -m pip install --break-system-packages python-pptx beautifulsoup4 pypdf
```
headless Chrome 필요 (PDF·렌더 검사·--image-slides). 부재 시 스크립트가 설치 안내를
출력한다.

## 1. 변환 실행 (Generator, S-final 스프린트)

```bash
# 네이티브 PPTX (기본 납품물 — 파워포인트에서 텍스트박스 자유 편집)
python3 <SKILL_DIR>/scripts/html2pptx.py <WORK_DIR>/deck.html <WORK_DIR>/dist/deck.pptx

# PDF (픽셀 동일 인쇄본)
bash <SKILL_DIR>/scripts/html2pdf.sh <WORK_DIR>/deck.html <WORK_DIR>/dist/deck.pdf
```

- 변환기가 오류 목록(파싱 집합 외 요소, 좌표 누락, colspan 등)과 함께 exit 2로
  끝나면 deck.html을 수정 후 재실행한다 — 부분 변환물 금지.
- **`--image-slides` 옵션**: 사용자가 "100% 비주얼 동일"을 명시 요구할 때만 별도
  파일(deck-image.pptx)로 추가 생성한다. 텍스트 편집 불가 옵션임을 반드시 고지하고,
  기본 납품물은 항상 네이티브 PPTX다. 이미지 버전은 검증 22~24 대상이 아니다
  (사람 게이트 ④에서 시각 확인).

## 2. 검증 21~26 실행 절차

```bash
python3 <SKILL_DIR>/scripts/verify_conversion.py <WORK_DIR>/deck.html \
    <WORK_DIR>/dist/deck.pptx <WORK_DIR>/dist/deck.pdf \
    --report <WORK_DIR>/dist/verify_report.md
```

| # | 체크 | 판정 |
|---|---|---|
| 21 | PPTX 재오픈+장수 | 재오픈 성공 AND 슬라이드 수 == 섹션 수 |
| 22 | 텍스트 무손실 | HTML 텍스트 노드(공백 정규화) ⊆ 슬라이드 텍스트 프레임, 손실 0 |
| 23 | 노트 이관 | aside.notes == notes_slide (공백 정규화) |
| 24 | 이미지 | 수량 일치 + 원본 해상도 ≥ 배치 px (2배 미만 WARN) |
| 25 | PDF | 페이지 수 == 장수 AND 전 페이지 텍스트 레이어 존재 |
| 26 | 스키마 호환 | round-trip 재저장 성공 (실제 열람은 게이트 ④) |

**실행 주체와 순서 (신뢰 분리)**:
1. **Generator가 변환 직후 1차 실행** (자체 검증) — 실패 항목 수정 후 핸드오프.
2. **Evaluator가 재실행해 결과 대조** — Generator 보고를 신뢰하지 않는다.
   Evaluator는 프로브 2로 verify_conversion.py를 직접 다시 돌린다.
3. 실패 항목은 **P0로 즉시 수정** → 재변환 → 재검증.
4. **21~26 전체 통과 전 최종 게이트(④) 진입 금지** — 이것은 C4 점수와 무관한
   하드 게이트다.

## 3. 흔한 실패와 수정 방향

| 실패 | 원인 | 수정 |
|---|---|---|
| 21 장수 불일치 | 섹션 누락·중복 | deck.html 섹션 수 == storyline 장수 재확인 |
| 22 텍스트 손실 | 파싱 집합 외 태그에 텍스트 | 해당 텍스트를 .el-text 블록으로 이동 |
| 23 노트 불일치 | 노트 수정이 한쪽만 반영 | storyline.md → deck.html 재동기화 |
| 24 해상도 미달 | 저해상 이미지 배치 | image-gen 재생성(2x) 또는 배치 크기 축소 |
| 25 빈 텍스트 레이어 | 텍스트가 이미지에만 존재 | 텍스트를 .el-text로, 이미지는 시각 보조로 |
| 26 round-trip 실패 | 비정상 도형 속성 | 오류 메시지의 도형을 단순화 |

## 완료 조건

- 21~26 전체 PASS + Evaluator 재실행 대조 완료 + status.md 갱신
  → workflows/07-delivery.md (사람 게이트 ④ 포함).
