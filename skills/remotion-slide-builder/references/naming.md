# 네이밍 컨벤션

## 파일명 (표준 챕터 패턴)

```
src/slides/<폴더명>/
├── LO<N>.tsx              # 인덱스 (TransitionSeries)
├── S01_Divider.tsx        # SectionDivider (간지)
├── S02_ChapterIntro.tsx   # 챕터 소개 + 순서 테이블
├── S03_TheoryA.tsx        # 이론 슬라이드
├── S04_TheoryB.tsx        # 이론 슬라이드 (필수 요소 등)
├── S05_Lab1Overview.tsx   # 실습 1 개요
├── S06_Lab1Step.tsx       # 실습 1 내용
├── S07_Lab1Result.tsx     # 실습 1 결과
├── S08_Lab2Overview.tsx   # 실습 2 개요
├── S09_Lab2Prepare.tsx    # 실습 2 준비
├── S10_Lab2Code.tsx       # 실습 2 코드
├── S11_Lab2Result.tsx     # 실습 2 결과
├── ...
├── S<NN>_DeepDive.tsx     # 심화 (참고 자료)
└── S<NN>_Checkpoint.tsx   # 체크포인트
```

> 파일명의 LabN 접두사는 참조용. 슬라이드 **title에는 세부 번호를 넣지 않는다.**
> 좋은 예: `title="Jenkinsfile을 Backend CI로 수정"`
> 나쁜 예: `title="실습 2-1: Jenkinsfile 전체 교체"`

## Composition ID

- 영문, 숫자, 하이픈만 (한글 불가)
- 숫자 접두사로 순서: `0-Course-Intro`, `1-Topic-Name`
- `Full-Presentation` — 전체 연결

## 폴더명

- 소문자, 하이픈 구분: `lo1-openai`, `lo2-langchain`
- overview, closing 등 특수 섹션은 그대로

## LO index 패턴

> 전체 코드: `samples/LOIndex.sample.tsx` 참조

핵심 구조:
- `SLIDE_DURATIONS`: 초 단위 배열 (슬라이드 수와 일치)
- `TRANSITION_FRAMES = 15`: 전환 겹침 프레임
- 전환: 디바이더에서 첫콘텐츠 `fade()`, 콘텐츠에서 콘텐츠 `slide()`, 마지막에서 체크포인트 `fade()`
- `getLO<N>DurationInFrames` export 필수 (Root.tsx, FullPresentation.tsx에서 사용)

## 슬라이드 시간 배분

**모든 슬라이드는 5초 균일.** PDF 렌더링 시 각 슬라이드를 트랜지션 직전 프레임에서 캡처하는데, 5초 균일이 가장 안정적이다. 슬라이드 유형에 따라 duration을 달리하지 않는다.

```typescript
// 올바른 예 (모든 값 5)
const SLIDE_DURATIONS = [5, 5, 5, 5, 5, 5, 5];

// 잘못된 예 (유형별 차등)
const SLIDE_DURATIONS = [3, 6, 5, 6, 5, 6, 4];
```

## 전환 규칙

| 위치 | 전환 효과 |
|------|----------|
| 디바이더에서 첫 콘텐츠 | `fade()` |
| 콘텐츠에서 콘텐츠 | `slide({ direction: "from-right" })` |
| 마지막 콘텐츠에서 체크포인트 | `fade()` |
| 전환 프레임 | 15프레임 (0.5초) |

## 애니메이션 규칙

- `useCurrentFrame()` + `interpolate()` 전용 (CSS transition 금지)
- 등장: 0.3~0.5초, opacity + translateY(20px에서 0)
- 순차 등장: 0.15초 stagger
- `loadFont()` — `.catch()` 에러 무시 (await 금지)

## CU/LO에서 슬라이드 변환

```
LO 구조                    → 슬라이드 매핑
────────────────────        ─────────────────────
학습 목표 (objectives)     → SectionDivider의 objectives[]
핵심 개념 (concepts)       → 이론 슬라이드 (ConceptCard, AnimatedList 등)
비교/대조                  → DataTable 또는 2컬럼 레이아웃
코드 예시                  → CodeBlock (실습 코드 저장소에서 발췌)
실습                       → LabOverview(DataTable) + 단계별 슬라이드 + 결과
체크포인트                 → CheckpointSlide (핵심 3~5개)
```

## 실습 중심 챕터의 슬라이드 산정

```
디바이더:     1장
챕터 소개:    1장
이론:         2~3장 (개념 수에 따라)
실습 1:       2~3장 (개요 + 내용 + 결과)
실습 2:       3~4장 (개요 + 준비 + 코드 + 결과)
실습 3:       3~4장 (개요 + 내용 + 결과 + 정리)
심화:         1장
체크포인트:   1장
합계:         14~20장
```

## 콘텐츠 밀도

- **1개념 1슬라이드** 원칙
- 이론은 충분히 설명 (수강생이 개념을 모른다고 가정)
- 텍스트 분량 충분히 허용 (강의 자료 = 정보량 우선)
- 핵심 메시지는 시각적 강조 (그라디언트 텍스트, 카드, 아이콘)
