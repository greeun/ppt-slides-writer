# Generator Report — ppt-slides-writer

작성: 2026-08-19. skill-spec.md(동결본)와 skill-wizard-harness 역할 프롬프트 템플릿
4종을 근거로 스킬 payload 전체를 구현하고, 스크립트 4종을 3장 픽스처로 실행 검증했다.

## Files produced (path — one-line purpose)

경로는 `ppt-slides-writer/` 루트 기준.

| 경로 | 목적 |
|---|---|
| `SKILL.md` | 라우터 + 핵심 원칙 + 오케스트레이터 11단계 플로우 + V1vsV2 + 튜닝 워크플로우 (253줄) |
| `workflows/01-purpose-intake.md` | 5질문 인테이크, 모드 판별, "알아서"/범위 밖 처리, 작업 폴더·status.md 생성, Planner 파견 |
| `workflows/02-design-system.md` | 경로 A(doc-converter+인젝션 방어)/경로 B(스타일 타일 3안), 게이트 ①, 동결 규칙, 복합 장표 샘플링 |
| `workflows/03-storyline.md` | S1 스프린트 계약 협상, Maker-Reviewer 루프, 게이트 ②(역할·키 메시지·시간 표) |
| `workflows/04-html-sprint.md` | 3~5장 묶음 스프린트, REFINE/PIVOT 처리, 병렬 fragments+후처리 통일, 시각 자산 연계, 컨텍스트 리셋 |
| `workflows/05-revision.md` | 게이트 ③, 범위 지정 수정 루프(단일 원천 유지), 토큰 변경=게이트 ① 재실행, 변환 후 수정 원칙 |
| `workflows/06-conversion.md` | 변환 명령, --image-slides 정책, 검증 21~26 실행 절차(Generator 1차→Evaluator 재실행), 실패 대응표 |
| `workflows/07-delivery.md` | 게이트 ④(시각 잔차+민감정보 해소 STOP), CTA 점검, 리드마그넷 배포, HTML 보존 안내 |
| `references/html-spec.md` | §7.1 사양: 1280×720 캔버스, data-role enum, 자기완결, 절대 배치, .el-* 계약, 분량 규칙, fragments |
| `references/conversion-rules.md` | 금지 CSS 12항, px→EMU(1px=9525), pt=px×0.75, 요소별 변환 상세, 오류 정책, 시각 잔차 목록 |
| `references/design-rules.md` | 경로 A/B 절차, 팔레트·의미 라벨, 템플릿 리듬, radius 계층, slop 6항목, 룰 승격 절차 |
| `references/information-architecture.md` | §1 원칙 8+1개: 단일 원천·역할·spine·micro-flow·bridge·역할 분리·표 셀 판단·시간 정합·감정 곡선 |
| `references/rubric.md` | C1~C5(2×/1× + weak-by-default 근거), 점수 가이드, verdict logic, 2차 점검 3렌즈 |
| `references/planner-prompt.md` | product-level hard rule, be ambitious, 차별화 훅 필수, spec.md 9섹션, DoD 확정 6항 |
| `references/generator-prompt.md` | 생산 프로세스 a~e, sprint contract, Strategic Decision(REFINE/PIVOT/ESCALATE), 불안 신호 4종, handoff |
| `references/evaluator-prompt.md` | 페르소나, 루브릭 삽입, 프로브 9종, 증거 의무+시각 잔차 이관, Iteration Quality Note, §Tuning |
| `references/evaluator-calibration.md` | 기준별 1/3/5 앵커 15개(스펙 §5.4 그대로) + 운영 앵커 누적 서식 |
| `templates/design-system.md` | 토큰 템플릿(팔레트/폰트/여백/radius/의미 라벨/금지/레퍼런스 메모) — lint HEX 파싱 계약 명시 |
| `templates/storyline.md` | 설계서 템플릿(장별 역할/키 메시지/원고/bridge/노트/시간 + spine 표) — lint 파싱 계약 명시 |
| `templates/slide-boilerplate.html` | deck.html 뼈대: @page, .slide, .el-* 클래스, 헤딩 inherit 규칙, 마지막 장 빈 페이지 방지 |
| `scripts/lint_slides.py` | 체크 1~20 (정적 파싱 + Chrome 렌더 오버플로, 부재 시 SKIP), lint_report.md + exit code |
| `scripts/html2pptx.py` | 네이티브 PPTX 변환기(python-pptx): el-text/image/shape/table/notes, var() 해석, --image-slides |
| `scripts/html2pdf.sh` | headless Chrome 인쇄(크롬 4단계 탐색+설치 안내), @page 기반 픽셀 동일 페이지 |
| `scripts/verify_conversion.py` | 검증 21~26, PNG/JPEG/GIF 해상도 자체 파서, verify_report.md + exit code |
| `skill-wizard-output/generator_report.md` | 본 보고서 |

## Spec mapping (스펙 섹션 → 구현 위치)

| 스펙 | 구현 위치 |
|---|---|
| §1 도메인 선언·모드 3종 | SKILL.md 서두+모드 표 / workflows/01 §2 |
| §1 정보설계 원칙 | references/information-architecture.md (8원칙 전부 + 감정 곡선) |
| §2.1 frontmatter | SKILL.md frontmatter — 스펙 텍스트 그대로 (YAML 파싱 검증 완료, EN 6+KO 8 트리거 확인) |
| §2.2 디렉터리 트리 | 전 파일 존재 (아래 Self-check find 출력). skills/·resources/는 무접촉 연계 대상 |
| §2.3 작업 폴더 | SKILL.md "작업 폴더" 절 + workflows/01 §4 (status.md 서식) |
| §3 루브릭·verdict | references/rubric.md (가중치·weak-by-default 근거 열·verdict logic·2차 점검 3렌즈 그대로) |
| §4 tier=Full·스프린트 구성 | SKILL.md 플로우 5·6단계 + workflows/03·04 (S1/S2..Sn/S-final) |
| §4 반복 상한 5~15·하한 경고·4시간·중간본 | SKILL.md "반복 원칙" + workflows/04 |
| §4 컨텍스트 리셋·컴팩션 금지 | SKILL.md 원칙 5 + generator-prompt.md 불안 신호 + workflows/04 "컨텍스트 리셋" |
| §4 File Handoff Contract 11파일 | SKILL.md "File Handoff Contract" |
| §4 사람 게이트 4개·시각 채널 대응 | SKILL.md 플로우 + "시각 채널 한계 대응" 절 + workflows/02·03·05·07 |
| §4 안전 게이트 3종 | SKILL.md "안전 게이트" + workflows/01 §3·02 §A3·07 |
| §4 V1 vs V2 | SKILL.md "V1 vs V2 가이드" (모델 표 원문 복사 + V2-1/2/3/4 + G-2/G-3/G-5) |
| §5.1 Planner | references/planner-prompt.md (hard rule·ambitious·훅 2개·섹션 3/4/6 치환·DoD 6항) |
| §5.2 Generator | references/generator-prompt.md (프로세스 a~e 스펙 문안 이식, Strategic Decision, 불안 신호 4종, 격식체·이모지 금지) |
| §5.3 Evaluator | references/evaluator-prompt.md (페르소나·프로브 9종·증거 의무·시각 잔차 이관·IQN·slide-reviewer 연계·§Tuning) |
| §5.4 캘리브레이션 앵커 | references/evaluator-calibration.md — 15개(기준별 1/3/5) 스펙 문안 그대로 |
| §6 오케스트레이터 11단계 | SKILL.md "오케스트레이터 활성화 플로우" 1~11 (게이트 ①~④ 명시) |
| §6 튜닝 (a)~(d)·룰 승격 | SKILL.md "Evaluator tuning workflow" + design-rules.md §8 |
| §7.1 HTML 사양 | references/html-spec.md + templates/slide-boilerplate.html |
| §7.1 금지 CSS 12항 | references/conversion-rules.md §1 + lint 체크 8 구현 |
| §7.2 px→EMU | references/conversion-rules.md §2 + html2pptx.py (EMU_PER_PX=9525, pt=px×0.75 0.5 반올림) |
| §7.3 lint 체크 1~20 | scripts/lint_slides.py (표의 판정·레벨 그대로: 3 enum외 WARN, 9~11·13·15·16·18·20 WARN, 나머지 ERROR, 18은 안전 플래그 병행) |
| §7.4 html2pptx | scripts/html2pptx.py (파싱 집합 외 요소 exit 2, --image-slides 2x 캡처+노트 이관) |
| §7.5 html2pdf | scripts/html2pdf.sh (스펙 명령·크롬 탐색 순서·설치 안내 그대로) |
| §7.6 생태계 연계 5행 | SKILL.md "생태계 연계" 표(스펙 표 그대로) + workflows/02(doc-converter)·04(image-gen·diagram-builder)·evaluator-prompt(slide-reviewer·SSOT) |
| §8 매핑 35행 | V1-1(SKILL 플로우 3·5·6) V1-2~5(rubric·calibration) V1-6/7/10/11(반복 원칙·IQN) V1-8(evaluator §Tuning) V1-9(generator Strategic Decision) V1-12~14(planner) V1-15(generator 3d·e, 규칙 5) V1-16(evaluator 프로브+증거) V1-17(rubric verdict) V1-18(sprint_contract 협상) V1-19(File Handoff Contract) V1-20(튜닝 a~d) V1-21(불안 신호 4종) V1-22(컴팩션 경고) V2-1/2(V1vsV2 "Simplified로 전환한다면") V2-3(Evaluator 비용 절) V2-4(모델 표) G-1(원칙 6+V1vsV2 서두) G-2(급진적 단순화) G-3(인용 2회) G-4(튜닝 절) G-5(마무리 지침) P-1(게이트 ①~④+시각 잔차 이관) P-2(planner 훅) P-3(튜닝 번호 절차) |
| §9.1 검증 21~26 | scripts/verify_conversion.py + workflows/06 (실행 절차 1~4 그대로) |
| §9.2 3단 검증 | SKILL.md "3단 검증 체계" |
| §9.3 자체 검증 | 본 보고서 Self-check + Script execution evidence |
| §10 시나리오 | 10.2(vague→5질문 전부+게이트 ② 생략 불가): workflows/01 §1 / 10.3(범위 밖 1문장 안내+대안): workflows/01 §1 / 10.4(민감정보 STOP): workflows/01 §3·07, lint 18, 프로브 3 / 10.1(happy path): 플로우 전체 |

## Script execution evidence (fixture 실행 로그)

픽스처: `<scratchpad>/p2-fixture/` — deck.html(3장: cover/evidence/cta, 표·이미지·
도형·노트 포함) + design-system.md + storyline.md + assets/chart.png(600×338 생성).
스킬 폴더 밖에 위치(`ls ppt-slides-writer/`에 p2-fixture 없음 확인).

의존성 설치:
```
$ python3 -m pip install --break-system-packages python-pptx beautifulsoup4 pypdf
Successfully installed XlsxWriter-3.2.9 soupsieve-2.9.2 pypdf-6.16.1 python-pptx-1.0.2 beautifulsoup4-4.15.0
deps OK 1.0.2 4.15.0 6.16.1   (Python 3.13.14)
```

**1) lint_slides.py — 실패→수정 이력 포함**

1차 실행 (렌더 검사가 실제 결함 검출):
```
$ python3 scripts/lint_slides.py deck.html design-system.md storyline.md
lint: ERROR 1 / WARN 0 → .../lint_report.md   EXIT=1
| 4 | ERROR | 렌더 오버플로 — S1 `el-text`: scroll 1088x230 > client 1088x140 |
```
원인: h1의 UA 기본 font-size(2em)가 `.el-text` 인라인 48px에 곱해져 96px로 렌더 →
컨테이너 초과. 수정: 기본 스타일시트에
`.el-text h1, .el-text h2, .el-text h3 { font-size: inherit; font-weight: inherit; }`
추가 (픽스처 + templates/slide-boilerplate.html + references/html-spec.md §6에 규칙
명문화 — 브라우저 렌더와 변환 좌표 일치 조건).

2차 실행:
```
lint: ERROR 0 / WARN 0 → lint_report.md   EXIT=0
- 렌더 검사: 실행됨 (/Applications/Google Chrome.app/Contents/MacOS/Google Chrome)
```

**2) html2pptx.py**
```
$ python3 scripts/html2pptx.py deck.html dist/deck.pptx
PPTX 저장 완료 (native, 3장): dist/deck.pptx   EXIT=0
```
python-pptx 재오픈 구조 덤프 (편집 가능한 텍스트박스·표·그림·노트 확인):
```
slide size EMU: 12192000 x 6858000
S1: [AUTO_SHAPE, TEXT_BOX(수작업 분류가 이익을 잠식하고 있…), TEXT_BOX(분류 오류 비용은…), TEXT_BOX(물류혁신팀 · 2026년 8월…)] / notes: 안녕하십니까...
S2: [TEXT_BOX(오분류 비용은 연 3.2억 원입니…), TEXT_BOX(반품 처리 인건비가…), PICTURE, TABLE, TEXT_BOX(출처: 사내 물류 운영 데이터…)] / notes: 오분류율 3.7%는...
S3: [TEXT_BOX(다음 단계는 현장 진단 미팅입니다…), AUTO_SHAPE, TEXT_BOX(2주 현장 진단으로…), TEXT_BOX(산출 근거…), TEXT_BOX(문의: 물류혁신팀…)] / notes: 진단은 무상으로...
```
--image-slides 옵션:
```
$ python3 scripts/html2pptx.py deck.html dist/deck-image.pptx --image-slides
PPTX 저장 완료 (image-slides, 3장)   — 장당 shape 1개(PICTURE), 노트 이관 확인
```

**3) html2pdf.sh** (Chrome 존재 — SKIP 아님)
```
$ bash scripts/html2pdf.sh deck.html dist/deck.pdf
225654 bytes written to file dist/deck.pdf
PDF 저장 완료: dist/deck.pdf   EXIT=0
```
(mac Chrome의 task_policy_set 경고 stderr는 무해 — 산출물 정상.)

**4) verify_conversion.py**
```
$ python3 scripts/verify_conversion.py deck.html dist/deck.pptx dist/deck.pdf --report dist/verify_report.md
verify: FAIL 0 / WARN 0 → dist/verify_report.md   EXIT=0
| 21 | PASS | 재오픈 성공, 슬라이드 3 == 섹션 3 |
| 22 | PASS | HTML 텍스트 노드 전부가 슬라이드 텍스트 프레임에 존재 (손실 0) |
| 23 | PASS | 전 장표 노트 일치 (공백 정규화 기준) |
| 24 | PASS | 이미지 수량 일치, 해상도 하한 충족 (검사 1건) |
| 25 | PASS | 페이지 3 == 장수, 전 페이지 텍스트 레이어 존재 |
| 26 | PASS | round-trip 재저장·재오픈 성공 |
```
25번이 3페이지인 것은 boilerplate의 `.slide:last-of-type { page-break-after: auto }`
(말미 빈 페이지 방지) 덕분 — 이 규칙도 html-spec.md에 명문화했다.

최종 일괄 재실행: lint exit=0, verify exit=0 (보고서 작성 직전 재확인).

## Self-check

- [x] All §2.2 files exist — `find` 출력 24파일: SKILL.md 1 + workflows 7 +
      references 9 + templates 3 + scripts 4 (전체 목록은 위 표와 일치)
- [x] SKILL.md ≤500줄 — **actual 253줄** (`wc -l`)
- [x] calibration anchors 15개 — `grep -c '^\- \*\*[135]/5\*\*'` = **15**,
      기준별 C1~C5 각 3개(1/3/5)
- [x] Full tier machinery — sprint_contract.md 협상(generator-prompt 규칙 2,
      evaluator-prompt 워크플로우 2, workflows/03 §1) + per-sprint Evaluator
      (workflows/04 Maker-Reviewer 루프, SKILL.md 플로우 6)
- [x] No placeholders — `grep -rn '\[DOMAIN\]\|\[OUTPUT_TYPE\]\|TBD\|TODO\|PLACEHOLDER\]'`
      → **no matches** (templates/의 `{…}` 채움 슬롯은 사용자 런타임 서식,
      `{WORK_DIR}`/`{SKILL_DIR}`는 파견 시 치환되는 운영 변수로 각 파일 상단에 정의)
- [x] Model table + G-요소 + tuning (a)~(d) + 게이트 ①~④ — grep 확인:
      Sonnet 4.5/Opus 4.5/Opus 4.6 표(SKILL.md), "find the simplest solution
      possible" 인용 2회(41행·216행), 컴팩션 경고(SKILL.md 38행·generator-prompt
      97행), 급진적 단순화(213행), 하네스 공간 이동(218행), (a)~(d)(178~185행),
      게이트 ①~④(86·90·95·104행)
- [x] scripts 4종 fixture 실행 통과 — 위 실행 로그 (lint exit 0 / PPTX 재오픈 /
      PDF 3페이지 / 21~26 전체 PASS)
- [x] 기존 skills/·resources/·upgrade-notes.md 무접촉 — mtime 증거:
      upgrade-notes.md 2026-08-18 01:28, resources/ai-slop-checklist.md 2026-06-21,
      skills/*/SKILL.md 2026-08-17 (본 작업일 2026-08-19 이전 그대로)
- [x] frontmatter 검증 — YAML 파싱 성공, name/version/context/allowed-tools 정상,
      EN 트리거 6/6·KO 트리거 8/8, 하네스·PPTX+PDF 명시 확인

## Known limitations

1. **표 테두리 스타일 미이관**: html2pptx는 표 테두리를 PPTX 테마 기본값에 맡긴다
   (python-pptx 셀 테두리 API 제약). conversion-rules.md §3·§7에 시각 잔차로 명시,
   사람 게이트 ④ 확인 항목으로 흡수된다.
2. **colspan/rowspan 미지원**: 변환기 오류로 조기 검출(exit 2)하고 셀 분해를
   안내한다 — 무단 근사 변환보다 안전한 선택.
3. **lint 격식체(체크 20)·민감정보(체크 18)는 휴리스틱**: 오탐·미탐 가능. 둘 다
   WARN 레벨이고 Evaluator 프로브(3)·사람 게이트가 이중 방어한다. 계좌번호 정규식은
   전화번호 형태와 겹칠 수 있어 안전 플래그 쪽으로 과탐하도록 설계했다.
4. **렌더 검사는 Chrome 의존**: 부재 시 SKIP+경고로 강등(정적 검사는 유지). PDF
   생성 자체는 Chrome 필수이므로 파이프라인 완주에는 결국 Chrome이 필요하다.
5. **--image-slides 산출물은 검증 22~24 비대상**: 텍스트가 이미지라 정의상 성립
   불가. verify_conversion.py 헤더·workflows/06에 명시했고 기본 납품물은 네이티브.
6. **인라인 `<br>` run 처리**: html2pptx가 `\v`(수직 탭)로 줄바꿈을 근사한다 —
   python-pptx 버전에 따라 표시가 다를 수 있어 html-spec은 블록(p/li) 분리를 권장.
7. 픽스처는 스크래치 디렉터리(`p2-fixture/`)에 있으며 스킬 payload에 포함되지 않는다.

## Retry context

(해당 없음 — 초회 실행에서 완료.)
