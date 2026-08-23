# 표준 챕터 패턴

모든 실습 중심 챕터는 아래 구조를 따른다. (kosta-jenkins-cicd LO4에서 확립)

```
S01_Divider          ← SectionDivider (간지, 다크 배경)
S02_ChapterIntro     ← "이 챕터에서는" + 순서 테이블
S03_TheoryA          ← 이론 슬라이드 1 (개념 설명)
S04_TheoryB          ← 이론 슬라이드 2 (필수 요소, 비교 등)
S05_Lab1Overview     ← 실습 1 개요 (DataTable + 안내 박스)
S06_Lab1Step         ← 실습 1 내용 (코드, 설정 등)
S07_Lab1Result       ← 실습 1 결과 (Console Output, Stage View 등)
S08_Lab2Overview     ← 실습 2 개요
S09_Lab2Prepare      ← 실습 2 준비 (프로젝트 구조, 핵심 명령)
S10_Lab2Code         ← 실습 2 코드
S11_Lab2Result       ← 실습 2 결과
S12_Lab3Overview     ← 실습 3 개요 (있는 경우)
...
SNN_DeepDive         ← 심화 (참고 자료, 비교표)
SNN_Checkpoint       ← 체크포인트 (CheckpointSlide)
```

## 챕터 소개 슬라이드 (ChapterIntro)

반드시 **순서 테이블**을 포함한다:

```tsx
<DataTable
  headers={["순서", "내용"]}
  rows={[
    ["이론", "CI 파이프라인이란? Jenkinsfile과 3가지 필수 요소"],
    ["실습 1", "Hello Pipeline: 저장소의 Jenkinsfile을 Jenkins에서 실행"],
    ["실습 2", "Backend CI: 4개 Stage로 코드 품질 검증하기"],
    ["실습 3", "실패 실험: 일부러 버그를 넣어 CI 차단 체험하기"],
    ["심화", "Groovy 문법, 파이프라인 옵션, npm ci"],
  ]}
/>
```

## 실습 개요 슬라이드 (LabOverview)

각 실습 시작 전 **개요 테이블 + 안내 박스**:

```tsx
<SlideLayout title="실습 1: Hello Pipeline" subtitle="저장소에 이미 있는 Jenkinsfile을 Jenkins에서 실행합니다">
  <DataTable
    headers={["단계", "내용"]}
    rows={[
      ["확인", "저장소의 Jenkinsfile 내용 확인"],
      ["Jenkins 설정", "Pipeline Job 생성, GitHub 연결"],
      ["실행", "Build Now 클릭"],
      ["결과", "Stage View + Console Output 확인"],
    ]}
  />
  <div style={{ /* 안내 박스 */ }}>
    Fork한 저장소에 이미 Hello Pipeline이 작성되어 있습니다.
  </div>
</SlideLayout>
```

## 실습 번호 규칙

| 위치 | 번호 체계 | 예시 |
|------|----------|------|
| 슬라이드 제목 | **"실습 1", "실습 2"만** | `title="실습 2: Backend CI 파이프라인"` |
| 슬라이드 내부 | 세부 번호 없음, 동작 기반 제목 | `title="Jenkinsfile을 Backend CI로 수정"` |
| 마크다운 (강사용) | 세부 단계 허용 | `## 실습 2-1: Jenkinsfile 전체 교체` |
| LO 문서 (강사 전용) | 가장 상세 | 단계별 체크리스트 |

## 이론 슬라이드 충실도

이론 파트는 **개념이 무엇인지** 충분히 설명해야 한다. "파이프라인이 뭔지"도 모르는 수강생을 가정한다.

- 핵심 개념마다 최소 1장 (ConceptCard 또는 AnimatedList)
- 비교표로 "왜 필요한지" 동기 부여 (DataTable)
- 코드와 개념을 2컬럼으로 병치 (좌: CodeBlock, 우: ConceptCard/AnimatedList)

## 실습 슬라이드 필수 포함 항목

실습 섹션에는 아래 항목을 반드시 포함한다:

| 항목 | 설명 |
|------|------|
| 설치 검증 | 도구 설치 후 버전 확인 명령어 (예: `claude --version`) |
| 트러블슈팅 | 흔한 설치/실행 오류와 해결법 (1-2개) |
| OS별 분기 | Windows/macOS/Linux 차이가 있으면 명시 (특히 Windows) |
| 환경변수 영구 설정 | 임시 설정(`export`)과 영구 설정(`.zshrc`, `$PROFILE`) 구분 |
| 체크포인트 | 실습 완료 확인 기준 (예: "터미널에 `v1.2.3`이 출력되면 성공") |

## CLI 도구 슬라이드 입력 예시

CLI 도구를 다루는 슬라이드에는 반드시 **"뭘 입력해야 하는지"** 실제 입력 예시를 포함한다.
추상적 설명("명령어를 입력합니다")이 아닌, 복사 가능한 구체적 명령어를 보여준다.

```tsx
// 좋은 예
<CodeBlock title="터미널" code={`claude "src/utils/auth.ts 파일의 validateToken 함수에\n타임아웃 처리를 추가해주세요"`} />

// 나쁜 예
<ConceptCard title="명령 실행" description="Claude Code에 원하는 작업을 입력합니다" />
```

## 실습 명령어 정합성 검증

실습 슬라이드에 CLI 명령어, URL, 파일 경로를 쓸 때 **실제 소스코드와 대조** 필수:

| 확인 항목 | 방법 |
|----------|------|
| API 엔드포인트 | 앱 소스(라우터/컨트롤러)에서 실제 경로 확인 (`/api/health` vs `/health`) |
| 포트 번호 | docker-compose, Dockerfile, 앱 설정에서 확인 |
| 이미지/컨테이너명 | docker-compose 서비스 이름과 일치 |
| 사전 조건 | 이미지 빌드, 기존 컨테이너 정리(down) 등 누락 없는지 확인 |

**"당연한 정보" 생략 원칙**: 실행 위치가 저장소 루트로 전제되면 매번 반복하지 않는다.

## 멀티레포 일괄 수정

같은 명령어/경로가 마크다운 슬라이드, Remotion 슬라이드, 실습 저장소(solutions/) 3곳에 걸쳐 있을 수 있다. 수정 시 `Grep`으로 전체 검색 후 일괄 반영한다.

## 실습 코드 저장소 연동

실습 코드가 이미 저장소에 있으면 **"직접 작성" 대신 "확인 후 실행"** 패턴을 사용한다:

```
저장소에 이미 있는 경우:  "저장소의 Jenkinsfile을 확인합니다" → 코드 보여주기 → 실행
수강생이 작성하는 경우:  "다음 코드로 전체 교체합니다" → 코드 보여주기 → Push → 실행
정답 참조 안내:          "solutions/01-ci-backend.Jenkinsfile을 참고할 수 있습니다"
```
