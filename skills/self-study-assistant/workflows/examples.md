# 사용 예시

## 예시 0: 대화 컨텍스트 추출 (핵심!)

```
[긴 대화 후...]

사용자: "지금까지 대화 정리해줘"

Claude:
1. 대화 전체 분석
2. 학습 관련 내용 식별:
   - 시작 질문: "Gabriel Petersson이 누구야?"
   - 후속 탐구: Top-Down Learning, ChatGPT 활용법
   - 파생 주제: 독학 스킬 설계

3. 구조화된 추출:
   ## 탐구 경로
   Gabriel Petersson → 학습 방법론 → Top-Down Learning → 스킬 설계

   ## 핵심 개념
   | 개념 | 정의 | 맥락 |
   |------|------|------|
   | Top-Down Learning | 복잡한 것에서 기초로 | 학습 방법 질문 |
   | Context Extraction | 대화에서 지식 추출 | 스킬 설계 |

   ## 질문-답변 기록
   ### Q1: Gabriel Petersson이 누구야?
   **핵심:** 스웨덴 출신, 고졸, ChatGPT로 독학, OpenAI 입사
   ...

4. 노트 생성:
   notes/Learning/sessions/2025-12-18 Gabriel Petersson과 Top-Down Learning.md

5. 개별 개념 노트 제안:
   "[[Top-Down Learning]] 노트를 별도로 만들까요?"
```

## 예시 1: 코드 분석 시작

```
사용자: "이 Transformer 코드 분석해줘" + 코드 첨부

Claude:
1. 전체 구조 파악 및 요약
2. 섹션별 분석 시작
3. "Attention 메커니즘" 부분에서:
   "이 부분을 이해하려면 Query/Key/Value 개념을 알아야 합니다.
   설명해드릴까요?"
4. 사용자가 "응" → Concept Explorer로 전환
5. 학습 완료 후 노트 생성
```

## 예시 2: 개념 탐구

```
사용자: "Diffusion Model이 뭐야?"

Claude:
1. 개요 제공
2. 선행 지식 매핑:
   - Markov Chain
   - Gaussian Distribution
   - U-Net Architecture
3. "어떤 개념부터 탐구할까요?"
4. 사용자 선택에 따라 재귀적 탐구
5. 탐구 경로 기록
```

## 예시 3: 학습 세션

```
사용자: "오늘 PyTorch 공부 시작할게"

Claude:
1. 세션 시작, 목표 설정
2. "어떤 주제부터 할까요?"
3. 학습 진행 (Code Dissector + Concept Explorer)
4. 세션 종료 시:
   - 배운 개념 요약
   - 노트 생성
   - 복습 일정 제안
```
