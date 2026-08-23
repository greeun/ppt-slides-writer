---
name: self-study-assistant
description: |
  복잡한 코드나 개념을 Top-Down 방식으로 재귀적 분해하여 독학을 지원하는 스킬.
  "독학 도와줘", "이거 공부할래", "설명해줘", "이해가 안돼",
  "알려줘", "배우고 싶어", "튜토리얼", "개념 정리해줘", "깊이 파고들어" 등
  학습이나 개념 이해가 필요할 때 사용할 것.
version: 1.0.0
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch, AskUserQuestion]
context: fork
---

# Self-Study Assistant (Top-Down Learning)

Gabriel Petersson 방식의 AI 활용 독학을 지원하는 스킬입니다.

## 핵심 철학

> "대학이 더 이상 기초 지식을 독점하지 않는다. ChatGPT에서 어떤 기초 지식이든 얻을 수 있다."
> - Gabriel Petersson

**Top-Down Learning**: 복잡한 문제 → 모르는 부분 발견 → 질문 → 더 모르는 개념 발견 → 재귀적 탐구 → 기초 도달

| 전통 | Top-Down |
|------|----------|
| 기초 → 응용 | 응용 → 기초 |
| 체계적 커리큘럼 | 필요 기반 학습 |
| 이론 먼저 | 실전 먼저 |
| 순차적 | 재귀적 |

## 4가지 핵심 기능

| 기능 | 트리거 | 워크플로우 |
|------|--------|-----------|
| **Context Extractor** | "정리해줘", "노트로 만들어줘" | Read `workflows/context-extractor.md` for details |
| **Code Dissector** | "이 코드 분석해줘", "한 줄씩 설명해줘" | Read `workflows/code-dissector.md` for details |
| **Concept Explorer** | "~가 뭐야?", "이해하고 싶어" | Read `workflows/concept-explorer.md` for details |
| **Study Session** | "학습 시작", "복습할 거 있어?" | Read `workflows/study-session.md` for details |

## 워크플로우 요약

### Phase 1: 학습 대상 파악

사용자 입력을 분석하여 적절한 기능으로 라우팅:

- 코드 파일/스니펫 제공 → **Code Dissector**
- 개념/용어 질문 → **Concept Explorer**
- "학습", "세션", "복습" 언급 → **Study Session**
- "정리해줘", "노트로 만들어줘" → **Context Extractor**

### Phase 2: 기능별 실행

각 기능의 상세 워크플로우는 `workflows/` 디렉토리 참조.

**공통 원칙:**
- 항상 실제 예시/코드와 함께 설명
- 재귀적 탐구 시 AskUserQuestion으로 선행지식 선택 유도
- 기본 탐구 깊이: Level 2, 요청 시 Level 4까지
- 사용자가 "충분해" 하면 중단

### Phase 3: 학습 기록

- 탐구 경로를 Mermaid 다이어그램으로 시각화
- 적절한 템플릿으로 노트 생성 (`templates/` 참조)
- 기존 노트와 [[위키링크]] 연결
- 복습 일정 제안 (1일 → 3일 → 7일 → 30일)

## 템플릿

| 템플릿 | 용도 | 파일 |
|--------|------|------|
| Context Extraction | 대화 추출 노트 | `templates/context-extraction.md` |
| Study Session | 학습 세션 기록 | `templates/study-session.md` |
| Concept Note | 개념 노트 | `templates/concept-note.md` |
| Code Analysis | 코드 분석 기록 | `templates/code-analysis.md` |

## 학습 기록 위치

```
notes/Learning/
├── sessions/          # 학습 세션 기록
├── Concepts/          # 개념 노트
└── Code-Analysis/     # 코드 분석 기록
```

## 체크리스트

### 매 상호작용 시
- [ ] 학습 모드 파악 (코드/개념/세션/추출)
- [ ] 사용자 수준 고려
- [ ] 재귀적 탐구 필요성 판단
- [ ] 적절한 깊이에서 멈추기 (판정 기준: 공통 원칙의 "기본 탐구 깊이: Level 2, 요청 시 Level 4까지" — 요청 없이 Level 2를 넘으면 과잉)

### 세션 종료 시
- [ ] 배운 내용 요약
- [ ] 노트 생성 여부 확인
- [ ] 복습 일정 제안
- [ ] 다음 학습 주제 제안

## DO / DON'T

**DO:** 실제 예시와 함께 설명, 수준 맞춤 설명, 경로 추적, 체계적 기록, 복습 제안

**DON'T:** 과도한 깊이로 혼란, 추상적 설명만 제공, 학습 기록 누락, 사용자 질문 무시

## 참고

- Read `workflows/examples.md` for usage examples
- [[Gabriel Petersson - ChatGPT로 OpenAI 연구원이 된 사례]]
- [[Top-Down Learning]]
