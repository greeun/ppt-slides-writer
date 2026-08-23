# Intake — Phase 1: frentis 스킬 10종 원형 유지 고도화

## Domain
frentis-education의 강의 PT 제작 스킬 10종
(`/Users/uni4love/project/workspace/216-frentis/frentis-education/.claude/skills/`)을
**도메인·구조·이름·워크플로우 변형 없이 그대로** 최신 LLM 모델(Claude Opus/Sonnet 5 이상)
기준으로 고도화한 버전을 만든다.

절대 규칙 (사용자 명시):
- **변형 금지** — 교육 도메인(CAT/CU/LO, vault, 격식체), 스킬 이름, 폴더 구조, 워크플로우 유지
- **Remotion 그대로 사용** — HTML 덱 등 다른 렌더 스택으로 치환 금지
- **병합 금지** — 10개 스킬 각각 독립 유지

대상 10종: curriculum-builder / slide-builder / remotion-slide-builder / slide-reviewer /
diagram-builder / image-gen / pdf-builder / doc-converter / example-builder / self-study-assistant
+ 공유 리소스 `resources/ai-slop-checklist.md`

## 산출 위치
현재 저장소(claude-skills)에 생성. frentis 원본 불변.
- 각 스킬 = `ppt-slides-writer/skills/<원본 스킬명>/` (작업 폴더 내 집결)
- 공유 리소스 = `ppt-slides-writer/resources/ai-slop-checklist.md`
- 검증 후 frentis 반영 여부는 사용자 결정

## 고도화 백로그 (변형 아닌 현대화만)

### A. 모델·가격 정보 최신화 (사실 검증 필수)
1. SKILL.md/워크플로우 본문의 구세대 모델명 예시 갱신 — 예: slide-builder schema.md의
   `claude-sonnet-4-5-20250929` 코드 예시, structure-rules.md 팩트체크 예시("Claude Sonnet 4.6")
   → 최신 라인업(Claude 5 패밀리: Fable/Opus/Sonnet 5, Haiku 4.5) 기준으로 갱신
2. image-gen 프로바이더·모델·가격 표 전면 재검증 — Gemini 최신(나노바나나 2 계열),
   OpenAI gpt-image 최신 세대. **생성 시점에 웹 검색으로 실제 모델명·가격 확인 후 작성**
   (2026-05 표는 구버전 가능성). generate.py 모델 단축키 매핑 갱신
3. remotion-slide-builder templates/package.json 의존성 버전 최신 확인
4. OpenRouter 가격 조회 스니펫 등 검증 절차는 유지하되 예시 출력 갱신

### B. 모델 핀·위임 전략 재조정 (Opus/Sonnet 5+ 시대)
5. frontmatter `model:` 핀 재검토 — frentis는 비용 절약용 sonnet/haiku 핀.
   신규: 판단·설계 스킬은 핀 제거(세션 강모델 상속), 기계적 대량 처리(doc-converter 청크,
   병렬 슬라이드 생성)만 하위 모델 위임 유지. 스킬별 근거 명시
6. 컨텍스트 앤자이어티 소멸 전제 조정 — doc-converter 청크 기준 완화 검토(대형 컨텍스트),
   단 서브에이전트 위임(컨텍스트 위생) 자체는 유지
7. `context: fork` 유지, allowed-tools 점검 (현행 Claude Code 도구명 기준 —
   구식 `Task` 표기를 `Agent` 등 현행 명칭으로 정합화)

### C. 규칙·품질 체계 강화 (구조 불변, 내용 보강)
8. 전 스킬 frontmatter `version:` 필드 부여 (SemVer, 저장소 규칙) — 원본에 없는 스킬 다수
9. description 트리거 최적화 — 기능+트리거 키워드 병기 원칙 재점검 (구조 유지)
10. Maker-Reviewer·Phase 게이트·STOP 게이트 등 기존 문법은 그대로, 서술 모호한 곳만
    이진 판정 가능하게 다듬기 (예: "충분한 분량" 옆에 기존 수치 기준 연결)
11. slide-reviewer ↔ remotion-slide-builder ↔ resources/ 상호 참조 경로가 신규 배치에서도
    유효하도록 상대 경로 정리 (참조 관계 자체는 유지)

### D. 유지 (건드리지 않음)
- 워크플로우 Phase 구성, 템플릿 구조, 컴포넌트 라이브러리 설계, 문체 규칙(합쇼체),
  vault 경로 규약(education/ 등), 페르소나 구성, 디자인 토큰 수치, AI slop 블랙리스트 항목,
  Python 스크립트 로직 (경로·모델명 상수만 필요 시 갱신)

## Quality axes
1. **원형 충실도** (2× 가중) — 도메인·구조·워크플로우·이름 무변형. 원본 대비 diff가
   "현대화 항목"으로만 구성. 임의 재설계·삭제·병합 0건
2. **최신성 정확도** (2× 가중, Claude 약점 축) — 모델명·가격·버전이 웹 검증된 현재 사실.
   추측 기재 금지, 검증 불가 시 "(생성 시점 검증 필요)" 마킹
3. **생태계 정합성** — 스킬 간 상호 참조(경로·스킬명·서브에이전트명·공유 리소스) 전부 유효
4. **저장소 규칙 준수** — version frontmatter, SKILL.md 500줄 이하 유지, description 원칙

## Verification approach
이진 체크:
1. 10개 스킬 폴더 + 파일 트리가 원본과 동일 구조 (파일 추가·삭제는 근거 문서화 시만)
2. 각 SKILL.md frontmatter: name(원본 동일)/description/version 존재
3. 원본 대비 diff 산출 → 모든 변경이 백로그 A~C 항목에 매핑됨 (매핑표 작성)
4. 모델명·가격 변경분: 웹 검증 출처 URL 기록 (upgrade-notes.md)
5. 스킬 간 참조 경로 grep 검증 — 끊어진 참조 0건
6. Remotion 스택 언급 무손실 (제거·치환 0건)
7. SKILL.md 500줄 이하 전 스킬
8. Python 스크립트 실행 가능 (문법 체크 `python3 -m py_compile`)
9. 도메인 어휘 보존 — CU/LO/CAT/vault/합쇼체 규칙 잔존 확인
10. 사람 최종 검토 게이트 — 스킬별 diff 요약 승인

## Sensory limits
없음 (텍스트 스킬 산출물). 단 사람 게이트 1회: 스킬별 변경 요약(diff 매핑표) 사용자 승인.

## Model & tier
- Target model: Claude Opus/Sonnet 5 이상 (위저드 실행·산출 스킬 모두)
- Tier: Full — 스킬 단위 스프린트(스킬 1~2개씩 Generator 배정), 스프린트별 Evaluator 검증.
  병렬 생성 시 후처리(서식·버전 표기 통일) 필수
- Evaluator는 원본 파일과의 diff 대조 + 백로그 매핑 검증 중심

## User context
- Languages: KO (원본 스킬 전부 한국어 — 유지)
- 이미지 API: GEMINI_API_KEY / OPENAI_API_KEY 전제, web 모드 폴백 유지
- Phase 2 예정: 이 작업 완료 후 ppt/슬라이드 HTML 작성기 스킬 논의 재개
  (초안: intake-phase2-ppt-html.md 보관)
