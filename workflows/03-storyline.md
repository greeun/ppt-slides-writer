# Workflow 03 — 스토리라인 스프린트 (S1) + 승인 게이트 ②

목표: storyline.md(단일 원천)를 만들고 사용자 승인을 받는다.
**승인 전 HTML 빌드 금지(STOP).** 원칙은 `references/information-architecture.md`.

## 1. 스프린트 계약 협상

1. Generator 파견 (Agent 호출 #2): `references/generator-prompt.md` 본문 치환 +
   "S1 스토리라인 스프린트" 범위 지정.
2. Generator가 sprint_contract.md 를 작성한다. S1 계약에 반드시 들어갈 체크:
   - storyline.md가 templates/storyline.md 서식(파싱 계약 포함)을 따른다
   - 전 장표에 역할(enum)·키 메시지·제목·부제·본문 원고·발표자 노트·예상 시간 존재
   - 시나리오 spine 표 존재 + 재등장 지점이 실제 장표와 일치
   - 섹션 전환부 bridge 3문장 존재
   - 장별 시간 합 = 발표 시간 ±10%
   - 모든 수치에 출처 표기 (출처 불명 수치는 "리서치 필요"로 명시)
3. Evaluator 파견 (Agent 호출 #3): 계약 검토 — spec.md 대비 약하면 반려·수정.

## 2. 작성 → 검증 루프

1. Generator가 storyline.md 작성 → `READY_FOR_QA:` 출력.
2. Evaluator가 rubric.md C1·C3·C5 중심으로 채점 (C2·C4는 HTML·변환 산출물이 없어
   해당 프로브만 축소 적용), 프로브 3(민감정보)·7(시간 정합)·9(단일 원천 — 이 단계
   에서는 spec.md 대비 storyline.md 초과 콘텐츠 검사)를 실행 → critique.md.
3. FAIL이면 Generator REFINE → 재검증. 스프린트당 반복 상한은 5~15회 범위
   (하한 고정 금지 — SKILL.md 반복 원칙 참조).
4. PASS 시 사람 게이트 ②로.

## 3. 사람 게이트 ② — 스토리라인 승인 (STOP)

사용자에게 **장별 역할·키 메시지·시간 배분 표**를 제시한다:

```markdown
| # | 역할 | 제목(주장) | 키 메시지 | 시간 |
|---|---|---|---|---|
| S1 | cover | ... | ... | 0.5분 |
...
합계: N분 / 발표 시간 M분
```

추가로 시나리오 spine 요약(어떤 수치가 어디서 재등장하는지)을 2~3줄로 보여 준다.

AskUserQuestion 선택지:
- **승인** — HTML 스프린트 진입 (workflows/04)
- **수정 요청** — 장표 번호 단위 피드백을 받아 Generator에 전달, 수정 후 재제시
- **구조 재설계** — spec.md 수준의 문제면 Planner 재파견 검토

승인 없이는 어떤 경우에도 HTML 빌드를 시작하지 않는다. "알아서 해줘" 모드에서도
이 게이트는 생략 불가 — 최소한 표 제시 + 명시적 승인 1회는 받는다.

## 4. 완료 조건

- storyline.md 승인 완료 + status.md 갱신 → workflows/04-html-sprint.md.
