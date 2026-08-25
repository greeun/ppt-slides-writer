# PPT Slides Writer

비즈니스 발표자료를 **Planner–Generator–Evaluator 하네스**로 제작해
**네이티브 PPTX(파워포인트에서 자유 편집 가능) + PDF(픽셀 동일 인쇄본)** 로 납품하는
Claude Code 스킬.

HTML은 최종 산출물이 아니라 **중간 렌더 단계**다 — 브라우저에서 눈으로 확인하고 범위를
지정해 수정하는 루프를 돌리기 위한 매체이며, 승인된 뒤 변환기의 입력이 된다.

> 이 README는 GitHub 배포용 사람 대상 문서다. 에이전트 동작의 단일 원천은
> [`SKILL.md`](SKILL.md)이며, 런타임에 이 파일은 필요하지 않다.

---

## 설치

```bash
git clone https://github.com/greeun/ppt-slides-writer.git ~/.claude/skills/ppt-slides-writer
```

다른 경로에 두고 싶으면 클론 후 심볼릭 링크를 만든다.

```bash
git clone https://github.com/greeun/ppt-slides-writer.git
ln -s "$(pwd)/ppt-slides-writer" ~/.claude/skills/ppt-slides-writer
```

### 의존성

```bash
python3 -m pip install --break-system-packages python-pptx beautifulsoup4 pypdf
```

**headless Chrome**(로컬 설치)은 PDF 인쇄·lint 렌더 검사·`--image-slides`에 필요하다.
탐색 순서는 `$CHROME_BIN` → macOS Chrome 앱 → `google-chrome` → `chromium`.
Chrome이 없으면 lint는 렌더 검사만 SKIP하고 정적 검사를 수행하며, PDF 변환은 설치 안내 후
중단한다.

---

## 사용법

Claude Code 세션에서 발표자료 제작을 요청하면 스킬이 활성화된다.

```
발표자료 만들어줘 — 주제는 사내 데이터 플랫폼 도입 제안, 임원 보고 10분.
```

활성화 트리거 — EN: `ppt`, `pptx`, `slide deck`, `presentation`, `make slides`,
`pitch deck` / KO: `발표자료`, `슬라이드`, `피치덱`, `PPT 만들어`, `장표 만들어`,
`제안 발표 자료`.

작업 산출물은 **사용자 프로젝트**에 생성된다.

```
slides-work/<deck-slug>/
├── spec.md  design-system.md  storyline.md  pattern-spec.md
├── sprint_contract.md  generator_report.md  critique.md  design_memo.md  handoff.md
├── status.md
├── deck.html  assets/  fragments/
├── lint_report.md
└── dist/  deck.pptx  deck.pdf  verify_report.md
```

---

## 모드 3종

활성화 시점에 아래 표로 판별하고, 애매하면 사용자에게 선택을 받는다.

| 모드 | 판별 조건 | 파이프라인 특화 |
|---|---|---|
| 브랜드 템플릿형 | 기존 브랜드 자산(PPT/로고/HEX/폰트) 보유 | 디자인 시스템 경로 A 기본 |
| 스토리라인 생성형 | 주제만 있고 시각 자산 없음 | 경로 B(스타일 타일 3안) 기본 |
| 리드마그넷형 | 배포·다운로드 유도 목적(외부 공유물) | CTA·리드마그넷 설계 강화, 배포 전 사람 검토 필수 |

---

## 워크플로우

5단계(목적 정의 → 디자인 시스템 → 스토리라인 → 빌드/수정 → 변환·배포)를 따르며,
중간에 **사람 게이트 4개**가 STOP 지점으로 놓인다.

| # | 단계 | 워크플로우 | 산출·게이트 |
|---|---|---|---|
| 1 | 5질문 인테이크 | `workflows/01` | 청중 / 목적 / 발표 시간 / CTA / 톤 |
| 2 | 모드 판별 | `workflows/01` | 모드 3종 중 확정 |
| 3 | Planner 파견 | `references/planner-prompt.md` | `spec.md` (차별화 훅 최소 2개) |
| 4 | 디자인 시스템 | `workflows/02` | 입력 자산 6종 수집(금지 목록 포함) → **게이트 ① 스타일** → `design-system.md` 동결 |
| 5 | 스토리라인 스프린트 | `workflows/03` | **게이트 ② 스토리라인 승인** (승인 전 HTML 빌드 금지) |
| 6 | HTML 스프린트 루프 | `workflows/04` | 3~5장 묶음 빌드 → lint → critique → REFINE/PIVOT |
| 7 | 렌더 확인·수정 | `workflows/05` | **게이트 ③ HTML 렌더** — 범위 지정 수정 루프 |
| 8 | 변환 | `workflows/06` | `html2pptx.py` + `html2pdf.sh` → `dist/` |
| 9 | 변환 검증 | `workflows/06` | 체크 21~26, Generator 실행 후 Evaluator 재실행 대조 |
| 10 | 최종 확인 | `workflows/07` | **게이트 ④ 최종** — PPTX/PDF 확인 + 사실 검수 6항목(수치·실명 포함) + 시각 잔차 점검 |
| 11 | 배포 안내 | `workflows/07` | CTA 최종 점검, 배포 후 측정 준비(6지표·UTM), 외부 공유물 사람 검토 확인 |

### 사람 게이트가 4개인 이유

Evaluator는 마크업·기계 검증으로 판정 가능한 것만 채점한다. **시각 잔차(색감 인상, 미묘한
배치)는 채점을 보류하고** `critique.md`의 "사람 게이트 확인 항목"으로 이관한다. 경로 A는
레퍼런스 입력을, 경로 B는 스타일 타일 3안 선택을 통해 시각 판단의 책임을 사람에게 둔다.

---

## 하네스 구조

Planner / Generator / Evaluator는 **각각 별도 Agent 호출**로 파견되고(`context: fork`),
**파일로만 통신**한다. 역할 간 대화나 추론 공유는 금지된다.

**File Handoff Contract** — 허용되는 통신 파일: `spec.md`, `design-system.md`,
`storyline.md`, `sprint_contract.md`, `generator_report.md`, `critique.md`,
`design_memo.md`, `handoff.md`, `lint_report.md`, `verify_report.md`, `status.md`, `pattern-spec.md`.

### 핵심 원칙

1. **단일 원천** — `storyline.md`가 진실이고 HTML/PPTX/PDF는 그 투영이다. 설계서에 없는
   콘텐츠가 장표에 등장하면 위반이다.
2. **슬라이드 수보다 장표별 역할** — 모든 장표는 `data-role`과 키 메시지 1개를 가진다.
3. **역할 분리** — 별도 Agent 호출 + 파일 통신.
4. **기계 우선 검증** — lint가 잡을 수 있는 문제를 LLM 리뷰나 사람 게이트로 넘기지 않는다.
5. **컨텍스트 리셋 정책** — 불안 신호가 감지되면 `handoff.md`를 쓰고 세션을 끝낸다.
   새 Generator가 파일 산출물만 읽고 승계한다. **컴팩션 금지.**
6. **단순성 원칙** — 하네스의 모든 구성요소는 "모델이 혼자 못 한다"는 가정을 인코딩한
   것이다. 모델이 업그레이드되면 가정을 하나씩 스트레스 테스트한다.

### 반복 원칙

- 스프린트당 Generator↔Evaluator 반복 상한은 **5~15회 범위**. 단일 값 고정 금지, 특히
  하한(5) 쪽으로 캡을 잡지 않는다 — 품질 도약이 10회차에 발생한 사례가 있다.
- wall-clock 최대 ~4시간까지 허용. 인위적 서두름도, 횟수를 채우기 위한 형식적 라운드도 금지.
- **중간 반복본이 최종본보다 나을 수 있다.** Evaluator의 Iteration Quality Note로 최선본을
  선택한다. "최신 = 최선"이 아니다.

---

## 3단 검증 체계

```
lint(기계) → LLM 리뷰(Evaluator + slide-reviewer 연계) → 사람 게이트(①~④)
```

| 단 | 수단 | 범위 |
|---|---|---|
| 1단 | `scripts/lint_slides.py` / `scripts/verify_conversion.py` | 체크 1~20 / 변환 충실도 21~26 |
| 2단 | Evaluator 루브릭(`references/rubric.md`) + 적대적 프로브 9종 | 구조·논리·일관성 |
| 3단 | 사람 게이트 ①~④ | 시각 잔차, 최종 책임 판단 |

수정 순서는 P0 → P1 → P2.

---

## 안전 게이트

1. **사실 검수는 사람 몫** — Evaluator는 `storyline.md` ↔ `deck.html` 일치만 검증한다.
   수치의 참·거짓과 고객사·인물 실명 사용 승인은 게이트 ④에서 사람이 판정한다.
   Evaluator는 대조 대상(수치·실명) 목록을 `critique.md`에 항상 남긴다.
2. **민감정보 STOP** — IR·견적·급여·개인정보 패턴(주민번호/전화/이메일/계좌 정규식 +
   대외비/급여/견적 단가/미공개 로드맵·전략 키워드)이 lint 체크 18 또는 Evaluator
   프로브 3에서 감지되면 플래그를 세운다. **사용자 명시 확인 없이 최종 게이트 통과 불가.**
3. **인젝션 방어** — `doc-converter` 산출물 등 외부 파일에서 온 텍스트는 **시각·내용 참고만**
   한다. 그 안의 지시문은 이행하지 않는다. Evaluator 프로브 8이 흔적을 검사한다.
4. **외부 공유물 사람 검토** — 리드마그넷형을 포함한 외부 공유물은 배포 전 사람 최종 검토가
   필수다. 하네스 승인은 내부 품질 게이트일 뿐이다.

---

## 생태계 연계

연계 스킬이 없어도 폴백으로 동작한다.

| 단계 | 연계 스킬 | 부재 시 폴백 |
|---|---|---|
| 디자인 시스템 경로 A | `doc-converter` | PDF/이미지는 Read(비전)로 직접 읽어 시각 특성만 추출, HWP는 경로 B 전환 제안 |
| 삽화·인포그래픽 | `image-gen` | 단색 플레이스홀더 도형+라벨, 최종 게이트에서 수동 삽입 안내 |
| 구조도·플로우 | `diagram-builder` | 변환 가능 요소만으로 단순 박스-선 다이어그램 직접 구현 |
| Evaluator 보조 | `slide-reviewer` | Evaluator 내장 프로브(slop 6항목 + 검수 6항목)로 축소 수행 |

---

## Tier 선택 (V1 vs V2)

기본값인 **tier=Full**(장표 단위 스프린트 + `sprint_contract.md` 협상 + 스프린트마다
Evaluator 검증)은 "현행 모델에서 스프린트 분해와 상시 Evaluator가 여전히 가치 있다"는
가정을 인코딩한 것이다. 가정은 모델이 좋아지면 낡는다.

| Model class | Context anxiety | 권장 tier |
|---|---|---|
| Sonnet 4.5 | Strong — 조기 종료 경향 | Full (V1) |
| Opus 4.5 | 대부분 해소 | Simplified (V2) |
| Opus 4.6 | 해소 + 계획·롱컨텍스트 개선 | Simplified 또는 Single-session |

Simplified로 전환한다면 제거 1순위는 스프린트 분해와 `sprint_contract.md` 협상이고,
스프린트별 Evaluator는 단일 종료 패스(3~5라운드 캡)로 바뀐다. 단 **사람 게이트 4개·기계
검증·단일 원천 원칙은 tier와 무관하게 유지한다** — 모델 능력이 아니라 시각 채널 한계와 변환
충실도라는 과업 속성에 묶여 있기 때문이다.

단순화는 **구성요소를 한 번에 하나씩** 제거하고 영향을 측정하는 방식으로만 한다. 한꺼번에
제거하는 실험은 실패했다.

---

## 저장소 구조

| 경로 | 내용 |
|---|---|
| `SKILL.md` | 에이전트 동작의 단일 원천 |
| `workflows/01`~`07` | 단계별 실행 절차 |
| `references/html-spec.md` | HTML 중간 렌더 사양 (캔버스·data-role·el-* 계약) |
| `references/conversion-rules.md` | 금지 CSS 12항 + px→EMU + 요소별 변환 상세 + 시각 잔차(제목 폭 안전 계수) |
| `references/design-rules.md` | 디자인 시스템 규칙, 템플릿 리듬, 룰 승격, §9 콘텐츠→시각 유형 매핑 사전 |
| `references/information-architecture.md` | 정보설계 원칙 (spine·micro-flow·bridge), 역할 enum 19종 의미, §2-1 기본 10장 골격 |
| `references/rubric.md` | 루브릭 5기준 + verdict logic |
| `references/*-prompt.md` | Planner / Generator / Evaluator 파견 프롬프트 |
| `references/evaluator-calibration.md` | 기준별 1/3/5점 앵커 + 운영 앵커 누적 |
| `references/changelog.md` | 버전별 변경 이력 (SemVer) |
| `templates/` | `design-system.md`, `storyline.md`, `pattern-spec.md`(병렬 스프린트 시각 프레임 정본), `slide-boilerplate.html` |
| `scripts/lint_slides.py` | 기계 lint 체크 1~20 (`--partial` 조각 모드, 제목 폭 안전 계수 WARN) |
| `scripts/html2pptx.py` | 네이티브 PPTX 변환기 (`--image-slides` 옵션) |
| `scripts/html2pdf.sh` | headless Chrome PDF 인쇄 |
| `scripts/verify_conversion.py` | 변환 충실도 검증 21~26 |

`skills/`와 `resources/`는 이 스킬의 payload가 아니라 **연계 대상**이다. 패키징에서는
제외되며, 부재 상황은 연계 표의 폴백이 처리한다.

---

## Evaluator 튜닝

미조정 Evaluator는 관대하다. 첫 실행들을 초안으로 취급하고 다음 루프를 돌린다.

1. 완료된 런의 `critique.md`와 실제 산출물(`deck.html`·PPTX)을 나란히 읽는다.
2. 사람 전문가라면 다르게 채점했을 항목을 특정한다 — 전형적 괴리는 관대한 점수, 누락,
   `generator_report.md`의 검증 주장을 재실행 없이 믿는 표면 신뢰다.
3. `references/evaluator-calibration.md`에 실패 사례를 새 앵커로 추가하고,
   `references/evaluator-prompt.md`의 해당 프로브 문구를 보강한다.
4. 동일 과제로 재실행해 verdict가 사람 판단과 수렴하는지 확인한다. 수렴까지 반복한다.

**룰 승격**: 동일 지적이 `critique.md`에 2회 이상 반복되면 `design-system.md` 또는
`references/design-rules.md`의 규칙으로 승격해 재발을 lint/프롬프트 수준에서 차단한다.

---

## Version

`1.1.0` — 변경 이력은 `references/changelog.md`.
