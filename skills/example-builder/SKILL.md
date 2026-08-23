---
name: example-builder
description: |
  교육용 데모/실습 코드를 course-materials 레포에 생성하는 스킬.
  "데모 만들어", "예제 코드 작성", "시연 코드", "sample code", "example 추가",
  "데모 코드", "실습 코드", "labs 만들어", "course-materials에 추가",
  "라이브 코딩 준비", "실습 환경 구성" 등 교육 자료의 실행 가능한 코드가 필요할 때 사용할 것.
version: 1.0.0
allowed-tools: WebSearch, WebFetch, Read, Glob, Grep, Edit, Write, Bash, Agent, AskUserQuestion
argument-hint: [LO 이름 또는 데모 설명]
context: fork
---

# Example Builder

교육용 데모(examples) 및 실습(labs) 코드를 생성하는 스킬입니다.

> 상세 워크플로우: `workflows/example-build.md` 참조

## 산출물 위치

CU 폴더 내 `labs/`에 독립 git repo로 관리한다

```
CU-{주제}/labs/              ← 독립 git repo (CU slug를 레포명으로 사용)
├── .gitignore
├── lab1-{주제}/             ← 실습 1
│   ├── README.md            ← 실습 가이드 (필수)
│   ├── starter/             ← 수강생 시작 코드
│   └── solution/            ← 정답 코드 + eval.py
├── lab2-{주제}/             ← 실습 2
└── examples/{slug}/         ← 시연용 (브리핑, 세미나)
    ├── README.md
    ├── src/
    └── output/
```

- 레포명은 CU frontmatter의 `slug` 값 사용 (한글 경로 금지)
- 하나의 CU에 실습이 여러 개면 단일 레포 안에 lab 폴더로 구분
- 독립 재사용이 필요한 경우에만 lab별 별도 레포 생성

## 핵심 원칙

- **시나리오 합의 우선**: README 시나리오를 사용자와 합의한 후에 코드를 작성한다.
- **Maker-Reviewer 패턴**: 코드 작성 후 반드시 Reviewer 서브에이전트로 검증한다.

## 워크플로우 요약

### Phase 1: 맥락 확인

1. 대상 LO 읽기 — 학습 목표, 핵심 개념, 데모 시나리오 확인
2. 대상 CU 읽기 — 역할/범위 경계, 데모 목록에서 이 데모의 위치 확인
3. 기존 코드 확인 — `course-materials/examples/{slug}` 또는 `labs/{slug}` 이미 존재하는지

### Phase 2: 시나리오 설계 및 합의

README 초안(시연 목표, 시연 순서, 핵심 멘트, 구성 파일)을 콘솔에 보여준 뒤 합의.

- 시연 흐름과 순서, 핵심 멘트, 기술 스택/버전, examples vs labs 구분 확정
- **사용자 승인 없이 Phase 3으로 넘어가지 않는다**

### Phase 3: 코드 작성 (Maker)

사전 조사 필수: WebSearch로 최신 버전 확인, 공식 문서 API 변경 확인, 의존성 호환성 확인.

코드 품질 기준:
- 실행 가능한 완전한 코드 (복붙으로 즉시 실행)
- 주석으로 각 부분 설명 (한국어)
- `.env.example` 사용 (API 키 하드코딩 금지)
- 최소 의존성, 에러 시 명확한 메시지

### Phase 4: 검증 (Reviewer)

Agent 도구로 실행하는 서브에이전트로 Reviewer를 호출하여 검증.

| 항목 | 통과 기준 |
|------|----------|
| CU/LO 커버리지 | 주요 키워드 80% 이상 반영 |
| README 완성도 | 시연 목표, 순서, 핵심 멘트, 백업 플랜 존재 |
| 실행 가능성 | 에러 없이 실행 |
| 최신 스펙 | 6개월 이내 릴리즈 기준 |
| 보안 | 하드코딩된 시크릿 없음 |

미통과 시 피드백 기반 수정 후 재검증.

### Phase 5: 마무리

1. output/ 생성 — 실행 결과 캡처
2. LO 본문에 데모 코드 참조 추가
3. **CU 실습 코드 섹션 갱신** — CU 본문에 GitHub 레포 URL, lab별 폴더/용도/관련 LO 테이블, clone 명령어를 추가
4. GitHub 레포 생성 및 push (사용자 승인 후)
5. Git 커밋 (사용자 승인 후)

## 금지 사항

- 시나리오 합의 없이 코드 작성 금지
- API 키/시크릿 하드코딩 금지
- 오래된 버전 사용 금지
- README 없이 코드만 제출 금지
- Reviewer 건너뛰기 금지
