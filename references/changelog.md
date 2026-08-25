# 변경 이력 — ppt-slides-writer

SemVer. 버그 수정 = patch, 기능 추가 = minor, 호환성 파괴 = major.
출처 표기: 실전 테스트 백로그(`skill-wizard-output/live-test-notes.md`)는 (#N), 감사 후 REFINE은
(audit #N), salesclue 원문(`salesclue.io/blog/claude-design-ppt`) 대조 미준수분은 (SC-N).

## 1.1.0 (2026-08-26)

두 작업 흐름(실전 테스트 백로그 + salesclue 원문 대조)을 하나의 minor 릴리스로 통합했다.
체크 번호(1~20, 21~26)·게이트 ①~④·프로브 9종·verdict logic은 바뀌지 않았다.

### 실전 테스트 백로그 8건

- `scripts/verify_conversion.py` 체크 22가 HTML 주석(bs4 `Comment`)을 손실 텍스트로 오탐하던
  버그 수정. `scripts/html2pptx.py`도 `<p>` 안 주석이 run으로 새지 않게 차단. (#1)
- `scripts/lint_slides.py --partial [--wrap-head deck.html]`: 조각 단독 lint — 체크 1·2·16
  생략, 보고서 머리에 "PARTIAL 모드 — 체크 1·2·16 생략". `--wrap-head` 생략 시 상위 deck.html
  자동 적용, 없으면 렌더 검사 SKIP. 조립 마커 `<!-- APPEND: … -->`를 boilerplate에 추가. (#2)
- `templates/pattern-spec.md` 신설 + File Handoff Contract에 `pattern-spec.md` 추가.
  S2 종료 시 Generator 작성 → Evaluator "병렬 파견 판정" → 조각 Generator 입력. (#3)
- `references/design-rules.md` §9 콘텐츠→시각 유형 매핑 사전(네이티브 한정 12유형),
  workflows/05에서 모호한 시각화 피드백의 제안 카탈로그로 사용. (#4)
- 네이티브 우선 전략 명시(SKILL.md 생태계 연계, workflows/04, design-rules §7,
  generator-prompt): 차트·도식은 `.el-*` 기본, image-gen은 삽화 한정, API 키 부재 폴백 =
  기본 경로. (#5)
- 제목 줄 수 안전장치: lint 렌더 검사에 "h1 마지막 줄 실측 폭 > 박스 폭 × 0.92이고 박스에
  여유 줄 없음 → PPTX N+1줄 위험" WARN(체크 4, Chrome 부재 시 SKIP). 변환기 기하는 불변.
  conversion-rules §7에 해소 절차. (#6)
- Evaluator·Generator 프롬프트에 절 단위 부분 저장 규칙 + workflows/04 연결 끊김 복구. (#7)
- 오케스트레이터 파견 프롬프트의 토큰 의미 재정의·확장 금지(SKILL.md, workflows/05). (#8)

### 감사 후 REFINE 4건

- `--partial`에서 `--wrap-head` 생략 시 `fragments/` 상위 `deck.html`을 자동 적용하고, 그것도
  없으면 렌더 검사를 SKIP한다(절대 배치 CSS 없는 측정은 오탐이므로). 보고서 모드 줄에
  "자동 탐지" 표기. (audit #2)
- 제목 폭 WARN 조건을 "마지막 줄 실측 폭 > 박스 폭 × 0.92 AND 박스 높이 < (줄 수+1) ×
  line-height"로 확정 — 2줄 프레임에서 상시 발화하던 최대 폭 기준을 대체하고, 여유 줄을
  확보하면 면제된다. (audit #3)
- 조립 마커를 `<!-- APPEND: … -->` 하나로 통일(boilerplate·html-spec §8·pattern-spec §8·
  workflows/04·generator-prompt 3.c가 같은 마커를 가리킴). (audit #4)
- README.md Version 1.1.0 + changelog 참조, 저장소 구조 표에 changelog·pattern-spec·
  `--partial`·제목 폭 WARN·design-rules §9·conversion-rules 시각 잔차 반영. (audit #7)

### salesclue 원문 대조 미준수 4건

- 배포 후 측정: workflows/07에 지표 6종(열람·체류·다운로드·CTA 클릭·폼 제출·완독률) 확보
  방법, 링크 배포 권고, CTA 링크 UTM 부여, 측정 결과의 재작업 환류. `scripts/html2pptx.py`가
  `.el-text` 안 `<a href>`를 PPTX run 하이퍼링크(`run.hyperlink.address`)로 이관 —
  PPTX·PDF 양쪽에서 클릭 가능(클릭 추적의 유일한 경로). html-spec/conversion-rules/
  generator-prompt에 `a[href]` 허용·사용 규칙 명시. (SC-1)
- 역할 enum 확장 14 → 19종: `concept` / `process` / `tactics` / `caveats` / `application`
  추가(information-architecture §2, lint `ROLE_ENUM`, html-spec, storyline·boilerplate·
  pattern-spec 템플릿). information-architecture §2-1 기본 10장 골격 신설(고정 템플릿이
  아닌 출발점). 10장 이상 덱은 caveats(한계) 장표 기본 포함, 미포함 시 사유 명시(rubric C1,
  planner-prompt). (SC-2)
- 입력 자산 수집 확장: workflows/02에 입력 자산 6종 표(기존 덱·웹사이트·로고·폰트·샘플
  카피·금지 목록) 신설, 네거티브 리스트는 경로 A/B 모두에서 확보. `templates/design-system.md`
  §6.1 네거티브 리스트 서식 고정. lint가 §6.1을 파싱해 금지 색은 팔레트에서 제외 후 사용 시
  체크 6 ERROR, 금지 표현은 체크 20 ERROR. 미기입 플레이스홀더·구버전 파일은 무시. (SC-3)
- 사람 검수 체크리스트: workflows/07 게이트 ④에 사실 검수 6항목 표(메시지·수치·실명·브랜드·
  보안·흐름) — 수치 정확성과 고객사 실명은 사람 확인 없이 통과 불가. evaluator-prompt가
  대조 필요 수치·실명 사용처 목록을 critique.md에 상시 이관. SKILL.md 안전 게이트에 "사실
  검수는 사람 몫" 추가. lint 체크 18·Evaluator 프로브 3에 미공개(내부 전용) 로드맵·전략
  패턴 추가. (SC-4)

## 1.0.0 (2026-08-19)

- 최초 릴리스: Planner–Generator–Evaluator Full tier, 사람 게이트 4개, lint 체크 1~20,
  변환 검증 21~26, 네이티브 PPTX + PDF 납품.
