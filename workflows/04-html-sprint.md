# Workflow 04 — HTML 스프린트 루프 (S2..Sn)

목표: 승인된 storyline.md를 원천으로 deck.html을 장표 묶음 단위로 빌드한다.
사양은 `references/html-spec.md`, 시작점은 `templates/slide-boilerplate.html`.

## 스프린트 구성

- **묶음 크기: 3~5장** (예: 12장 덱 = 스프린트 3회). 묶음은 섹션 경계에 맞춘다.
- 스프린트마다: sprint_contract.md 협상 → 빌드 → lint → Evaluator critique →
  REFINE/PIVOT 판단 → 반복.
- 스프린트 계약의 표준 체크:
  - 이번 묶음 장표가 storyline.md의 해당 장표와 1:1 대응 (역할·키 메시지·원고)
  - design-system.md 토큰만 사용 (:root 변수 주입)
  - lint_slides.py ERROR 0 (렌더 오버플로 포함)
  - 발표자 노트 이관 완료 (storyline.md 원고와 일치)
  - 시각 요소(이미지·다이어그램)는 assets/ 로컬 파일로 존재

## Maker-Reviewer 루프 (Generator ↔ Evaluator)

1. Generator 빌드 → 자체 lint (ERROR 0까지) → `READY_FOR_QA:`.
2. Evaluator: lint 재확인 + 프로브 9종 실행 + rubric 채점 → critique.md.
3. Generator: critique.md 를 읽고 Strategic Decision (REFINE/PIVOT/ESCALATE):
   - REFINE — 구체 지적 반영 3~5개 나열 후 수정.
   - PIVOT — `REDIRECT:` 또는 승인된 design_memo.md가 있을 때만. 동결 토큰 변경이
     필요한 피벗은 게이트 ① 재실행 사안 — 오케스트레이터에 보고하고 정지.
   - ESCALATE — `DEADLOCK:` 출력 시 오케스트레이터가 사용자에게 쟁점을 가져간다.
4. **반복 상한: 스프린트당 5~15회 범위.** 하한(5) 쪽으로 캡을 잡지 말 것 — 품질
   도약은 후반 반복에서 나온다. 중간 반복본이 최종본보다 나을 수 있으므로
   Evaluator의 Iteration Quality Note를 확인해 최선본을 선택한다.

## 병렬 생성 + 후처리 패턴 통일 (필수)

여러 장표를 병렬 Agent로 나눠 만들 때:

1. 조각은 `fragments/NN.html` — 파일당 섹션 1개. 각 조각 Agent에는 design-system.md
   토큰 표와 해당 장표의 storyline.md 블록만 전달한다.
2. 조립: 조각을 순서대로 deck.html `<body>`에 삽입.
3. **후처리 패스(단일 패스, 생략 금지)**: 조립된 전 장표를 한 번에 훑으며 통일한다 —
   - 팔레트: 조각별 미세 색 편차 제거 (토큰 변수로 환원)
   - 여백 리듬: 제목 top 좌표·가장자리 여백 정렬
   - 라벨 표기: 동일 개념의 표기 통일 (예: "연 3.2억 원" vs "3.2억원/년")
   - 데이터 시각화 스타일: 차트·표 스타일 통일
   - radius 계층: 대형/소형/직각 규칙 재적용
4. 후처리 없이 READY_FOR_QA 금지. 병렬 생성은 속도를 사고 일관성을 파는 거래이며,
   후처리가 그 대금이다.

## 시각 자산 연계

- 삽화·인포그래픽: → 이 작업은 image-gen 스킬을 사용한다. (부재 시: 단색
  플레이스홀더 도형+라벨로 대체하고 최종 게이트에서 수동 삽입 안내)
  - design-system.md를 톤 가이드로 전달한다 — 작업 폴더에 `tone-guide.md` 사본을
    배치해 image-gen의 톤 가이드 탐색 규약을 충족시킨다. guided/freestyle 모드는
    image-gen 규칙을 따른다.
- 구조도·플로우: → 이 작업은 diagram-builder 스킬을 사용한다. (부재 시: 변환 가능
  요소 .el-shape/.el-text만으로 단순 박스-선 다이어그램 직접 구현)
  - Draw.io PNG(--scale 2) 또는 Mermaid→PNG를 `assets/`에 저장 후 `.el-image` 삽입.
- 생성 이미지 해상도는 배치 px의 2배 이상 (검증 24 WARN 기준).

## lint 실행 (매 스프린트 종료 전)

```bash
python3 {SKILL_DIR}/scripts/lint_slides.py {WORK_DIR}/deck.html \
    {WORK_DIR}/design-system.md {WORK_DIR}/storyline.md
```
ERROR 0 전 핸드오프 금지. lint 우선 원칙: 기계로 잡히는 문제를 Evaluator·사람
게이트로 넘기지 않는다.

## 컨텍스트 리셋

Generator가 `HANDOFF_NEEDED: handoff.md` 를 출력하면:
1. handoff.md(남은 장표 목록 + 각 장표에 필요한 것)를 확인한다.
2. **새 Generator 세션**을 파견한다 — handoff.md + 파일 산출물(spec/design-system/
   storyline/deck.html/critique)만 읽고 승계한다. 컴팩션 금지.
3. status.md에 리셋 이력을 남긴다.

## 완료 조건

- 전 장표 빌드 + lint ERROR 0 + Evaluator PASS → workflows/05 렌더 게이트로.
