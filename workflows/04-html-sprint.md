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

0. **pattern-spec.md(시각 프레임 정본) 선행**: S2(첫 묶음) 종료 시 Generator가
   `templates/pattern-spec.md` 서식으로 작업 폴더 `pattern-spec.md`를 실측 좌표로
   작성한다(§0 변환기 사실, 제목 프레임, 유형별 좌표 규격, 장별 배정표, spine 첫 등장
   배치 의무, 조립 체크리스트). Evaluator가 critique.md에 **"병렬 파견 판정: 승인"**을
   내린 뒤에만 조각 Agent를 파견한다 — 반려면 S2 REFINE으로 되돌린다. 조각 Agent가
   자기 장표의 시각 유형을 즉석에서 발명하는 것이 병렬 생성의 최대 불일치 원인이다.
1. 조각은 `fragments/NN.html` — 파일당 섹션 1개. 각 조각 Agent에는 design-system.md
   토큰 표, 승인된 pattern-spec.md, 해당 장표의 storyline.md 블록만 전달한다.
   파견 프롬프트는 토큰 의미를 재정의·확장하지 않는다(design-system.md 참조만).
2. **조각 단독 lint 허용 조건**: 조각은 조립 전에도 lint한다 — 단 `--partial`로:
   ```bash
   python3 {SKILL_DIR}/scripts/lint_slides.py {WORK_DIR}/fragments/NN.html \
       {WORK_DIR}/design-system.md {WORK_DIR}/storyline.md \
       --partial --wrap-head {WORK_DIR}/deck.html --report {WORK_DIR}/fragments/lint_NN.md
   ```
   - `--partial`은 조각에서 성립하지 않는 체크 1(장수)·2(cover/cta)·16(시간 합)만
     생략하고 보고서 머리에 "PARTIAL 모드 — 체크 1·2·16 생략"을 남긴다. 나머지
     체크(3~15·17~20, 렌더 오버플로, 제목 폭 안전 계수)는 그대로 ERROR/WARN이다.
   - `--wrap-head`는 조각에 `<head>`가 없을 때 deck.html의 `<head>`(:root 토큰·기본
     CSS)를 씌운다 — 토큰 해석(체크 6·14)과 Chrome 렌더 검사가 :root에 의존한다.
     생략하면 조각 폴더의 상위 `deck.html`(fragments/ 규약)을 **자동 적용**하고, 그것도
     없으면 렌더 검사를 SKIP한다(절대 배치 CSS 없이 측정하면 오탐 ERROR가 나므로
     건너뛴다). 즉 `--partial`만으로도 exit 코드는 조각 자체 결함만 반영한다.
   - 조각 lint ERROR 0은 조립 전제 조건일 뿐 스프린트 완료 조건이 아니다 — 조립 후
     전체 모드 lint(체크 1·2·16 포함) ERROR 0이 완료 조건이다.
3. 조립: 조각을 순서대로 deck.html의 조립 마커 `<!-- APPEND: … -->`(boilerplate가
   `</body>` 직전에 둔다 — html-spec §8) 앞에 삽입. 마커는 남겨도 무해하다.
4. **후처리 패스(단일 패스, 생략 금지)**: 조립된 전 장표를 한 번에 훑으며 통일한다
   (pattern-spec.md §8 체크리스트) —
   - 팔레트: 조각별 미세 색 편차 제거 (토큰 변수로 환원)
   - 여백 리듬: 제목 top 좌표·가장자리 여백 정렬
   - 라벨 표기: 동일 개념의 표기 통일 (예: "연 3.2억 원" vs "3.2억원/년")
   - 데이터 시각화 스타일: 차트·표 스타일 통일
   - radius 계층: 대형/소형/직각 규칙 재적용
5. 후처리 없이 READY_FOR_QA 금지. 병렬 생성은 속도를 사고 일관성을 파는 거래이며,
   후처리가 그 대금이다.

## 시각 자산 연계

- **네이티브 우선**: 차트·도식·표는 `.el-shape`/`.el-text`/`.el-table`로 직접
  구현하는 것이 기본 경로다(유형 선택은 `references/design-rules.md` §9 사전, 좌표는
  pattern-spec.md). PPTX에서 편집 가능하고 수정 비용이 0이다. image-gen은 삽화·사진풍
  비주얼에 한정한다 — 따라서 **image-gen API 키가 없을 때의 폴백(도형+라벨)은
  차트·도식에서는 기본 경로와 동일**하며, 삽화만 플레이스홀더로 남는다.
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

**연결 끊김 복구**: Evaluator·Generator는 critique.md·generator_report.md를 절 단위로
부분 저장한다(역할 프롬프트 규칙). 완료 태그(`CRITIQUE_READY:`/`READY_FOR_QA:`) 없이
끊기면 파일의 마지막 기록 절을 확인하고 "다음 절부터 재개"를 명시해 같은 역할을
재파견한다 — 처음부터 다시 시키지 않는다.

## 완료 조건

- 전 장표 빌드 + lint ERROR 0 + Evaluator PASS → workflows/05 렌더 게이트로.
