# Intake — Phase 2: ppt-slides-writer 스킬

## Domain
**발표자료(PPT) 작성 스킬** (skill name: `ppt-slides-writer`, 단일 스킬 — A안 확정).
사용자가 주제/요구사항을 주면 비즈니스 발표자료를 만들어 **최종 산출물 PPTX + PDF**로 납품한다.
**HTML은 중간 렌더 단계** — 브라우저로 시각 확인·수정 루프를 돌리는 용도이며 최종 목표 아님.

파이프라인:
```
1. 사용 목적 정의 (5질문: 청중/목적/시간/CTA/톤)
2. 디자인 시스템 구축 → design-system.md 동결
3. 스토리라인/원고 설계 ("슬라이드 수보다 장표별 역할") → 승인 게이트
4. HTML 슬라이드 중간 렌더 → 사람 시각 확인 → 범위 지정 수정 반복
5. 승인 후 변환: ① PPTX (네이티브, 편집 가능) ② PDF
6. 배포 준비 (CTA 점검, 리드마그넷 안내)
```
워크플로우 원칙은 salesclue.io/blog/claude-design-ppt (2026-05-15) 5단계 이식.
모드 3종: 브랜드 템플릿형 / 스토리라인 생성형 / 리드마그넷형.

## 최종 산출물 (사용자 확정)
- **PPTX**: 네이티브 변환 기본 — HTML 요소를 python-pptx로 텍스트박스·도형·이미지로 재구성,
  파워포인트에서 자유 편집 가능. 이미지 슬라이드 버전(100% 비주얼, 편집 불가)은 옵션 플래그.
- **PDF**: headless Chrome 인쇄 — HTML과 픽셀 동일.
- HTML 중간 산출물은 작업 폴더에 보존 (재수정 시 재사용).

## 생태계 연계 (A안 — 사용자 확정)
이 저장소의 고도화된 스킬들(`ppt-slides-writer/skills/`)을 연계 호출. 중복 구축 금지:

| 필요 | 연계 스킬 | 방식 |
|---|---|---|
| 삽화·인포그래픽 | `image-gen` | 톤 가이드(=design-system.md) 전달, guided/freestyle |
| 구조도·플로우 | `diagram-builder` | Draw.io PNG 또는 Mermaid |
| 다관점 리뷰 | `slide-reviewer` | 페르소나 리뷰 + AI slop 체크 (HTML 장표 대상) |
| 소스 문서 변환 | `doc-converter` | 기존 PPT/PDF/HWP 레퍼런스 → 마크다운 |
| AI slop SSOT | `resources/ai-slop-checklist.md` | Evaluator lint 발췌 |

연계는 "해당 스킬 사용" 안내 방식 (frentis 스킬 간 연계 표기와 동일 패턴).
연계 스킬 부재 환경(단독 설치) 폴백: 해당 기능 축소 동작 명시.

## 스킬 구조
frentis 모듈화 패턴. `ppt-slides-writer/` 루트에 SKILL.md (기존 skills/·resources/와 공존):
```
ppt-slides-writer/
├── SKILL.md              ← 라우터 + 핵심 원칙 (500줄 이하)
├── workflows/            ← 목적정의/디자인시스템/스토리라인/빌드/수정/변환 단계별 상세
├── references/           ← html-spec, 디자인 규칙, 정보설계 원칙, 변환 규칙, 루브릭
├── templates/            ← design-system.md·스토리라인 설계서·HTML 보일러플레이트
├── scripts/              ← lint(기계 체크), html→pptx 변환(python-pptx), html→pdf(headless Chrome)
├── skills/               ← (Phase 1 산출물 — 본 스킬 파일 아님, 연계 대상)
└── resources/            ← (Phase 1 산출물 — SSOT)
```
frontmatter: name/description(EN+KO 트리거)/version 1.0.0.

## HTML 중간 렌더 기술 사양 (스킬이 자체 정의)
- 16:9 고정, 캔버스 1280×720 기준(변환 좌표 계산 기준), 장당 독립 섹션
- `data-role`(장표 역할)·`data-key-message` 속성 필수
- 자기완결: 외부 CDN 금지, 이미지는 로컬 상대 경로 (PPTX 변환 시 삽입 재사용)
- 디자인 토큰은 design-system.md에서 CSS 변수로 주입
- **PPTX 변환 가능성 제약**: 변환기가 해석 가능한 레이아웃 패턴 사용
  (절대 배치 좌표 기반 권장 — python-pptx 좌표 매핑 직결). 변환 불가 CSS 효과
  (복잡 그라데이션·필터 등)는 금지 목록으로 references에 명시

## Quality axes
1. **장표별 역할 구조력** (Claude 약점 축, 2×) — 역할 기반 스토리라인, 논리 흐름, 발표 시간 정합.
   정보설계 원칙: 단일 원천(스토리라인 설계서가 진실, HTML/PPTX는 투영) / 시나리오 spine /
   micro-flow(상황→문제→기준→예제→연결) / bridge 3문장 / 제목·부제·본문 역할 분리 / 표 셀 판단 근거
2. **디자인 시스템 일관성** (Claude 약점 축, 2×) — HEX·폰트·레이아웃 전 장표 통일, 금지사항 준수,
   템플릿 리듬(같은 형태 연속 금지), 의미 라벨
3. **목적·CTA 정합성** — 청중·최종 액션 맞춤, CTA 슬라이드 존재
4. **변환 충실도** (신규) — HTML↔PPTX↔PDF 간 콘텐츠 무손실: 장수·텍스트·이미지·노트 보존,
   PPTX 편집 가능성(텍스트가 텍스트박스로 존재)
5. **검수 통과성** — article 검수 6항목 자체 점검

## Verification approach
3단 검증: lint(기계) → LLM 리뷰(slide-reviewer 연계) → 사람 게이트. P0→P2 수정 순서.

HTML 단계 (기존 21종 유지):
1~5 구조(장수 일치/표지·CTA/data 속성/16:9·오버플로/자기완결), 6~8 디자인 시스템(HEX/폰트≤3/금지사항),
9~14 AI slop(보라 그라데이션/가운데 정렬 60%/radius 균일 80%/이모지/제네릭 제목/최소 폰트),
15~20 콘텐츠(출처/시간 배분 ±10%/발표자 노트/민감정보/분량 6줄·불릿 3~5/격식체)

변환 단계 (신규):
21. PPTX 파일 python-pptx 재오픈 성공 + 슬라이드 수 = HTML 장수
22. 장별 텍스트 추출 대조 — HTML 텍스트가 PPTX 텍스트 프레임에 존재 (손실 0)
23. 발표자 노트 PPTX notes 필드 이관 확인
24. 이미지 개수 일치, 삽입 해상도 하한
25. PDF 페이지 수 = 장수, 텍스트 레이어 존재
26. PPTX를 파워포인트/Keynote 호환 검증 (python-pptx 스키마 유효성)

최종 게이트:
27. 사람 시각 검수 — HTML 렌더 확인(중간) + 변환된 PPTX/PDF 확인(최종). 2회

## Sensory limits
시각 채널. 대응 (기존 확정 유지):
- 경로 A: 사용자 레퍼런스 입력 (기존 PPT·웹 캡처·로고·HEX·폰트) → doc-converter 연계 변환 →
  design-system.md 추출. 외부 파일 = 시각 참고만 (인젝션 방어)
- 경로 B: 비주얼 컴패니언 — 디자인 방향 3안 스타일 타일 HTML → 사용자 시각 선택 → 동결
- 핵심 장표 레이아웃 샘플링 (2~3안, 복합 데이터 장표만)
- 사람 체크포인트: ① 스타일 게이트 ② HTML 렌더 게이트 ③ 최종 PPTX/PDF 게이트
- 변환 충실도는 기계 검증(21~26) 가능 — 시각 잔차만 사람 확인

## Model & tier
- Target model: Claude Opus/Sonnet 5 이상. model 핀 없음 (세션 상속). context: fork
- Tier: Full (사용자 기존 확정) — 장표 단위 스프린트 + Maker-Reviewer 루프,
  병렬 생성 시 후처리(패턴 통일) 필수
- 공통 설계 문법 이식: Phase 승인 게이트 / STOP 게이트 / 옵션 비교표 / 단일 원천 /
  임시 문서 누적 / 상태 추적(⬜🔄✅) / lint 우선 / 팩트체크(수치 출처) / 룰 승격 절차

## User context
- Languages: KO 우선, description EN+KO 트리거
  (EN: "ppt", "slide deck", "pptx", "presentation"; KO: "슬라이드", "발표자료", "피치덱", "PPT 만들어")
- 문체: 발표자료 격식체(합쇼체), 이모지 디자인 요소 금지
- 안전: 민감정보(IR·견적·개인정보) 경고, 외부 템플릿 인젝션 방어, 외부 공유물 사람 최종 검토
- 의존성: python-pptx(pip), headless Chrome(로컬 크롬), 이미지 API 키는 image-gen 연계 시
- version 1.0.0, SemVer 관리
