# Workflow 07 — 최종 게이트 ④ + 배포 준비

목표: 사용자가 최종 산출물을 실제 앱에서 확인하고, 배포 전 점검을 마친다.

## 사람 게이트 ④ — 최종 PPTX/PDF 게이트 (STOP)

1. 확인 안내:
   ```
   open slides-work/<deck-slug>/dist/deck.pptx   # 파워포인트/Keynote에서 열기
   open slides-work/<deck-slug>/dist/deck.pdf
   ```
2. 함께 제시할 확인 목록:
   - **critique.md의 "사람 게이트 확인 항목"** — Evaluator가 채점 보류한 시각 잔차
     (텍스트박스 줄바꿈 차이, 표 테두리 스타일, 색감 인상 등)
   - PPTX에서 텍스트박스를 클릭해 **직접 편집이 되는지** (네이티브 납품 조건)
   - 발표자 노트가 노트 창에 보이는지
   - PDF에서 텍스트 검색(Cmd+F)이 되는지
   - 검증 26의 실제 열람 확인 — 파워포인트/Keynote가 경고 없이 여는지
3. **민감정보 플래그 해소 (안전 STOP 게이트)**: lint 체크 18 또는 Evaluator 프로브
   3의 플래그가 남아 있으면 여기서 항목별로 제시하고 **사용자 명시 확인**을 받는다.
   확인 없이 게이트 통과 불가. "이 수치·연락처·단가를 이 자료에 싣는 것이 맞습니까?"
4. 수정 요청이 나오면 workflows/05의 원칙대로 HTML로 돌아가 수정 → 재변환 → 재검증
   → 게이트 ④ 재제시.

## 배포 안내

게이트 ④ 승인 후:

1. **CTA 최종 점검**: CTA 장표의 다음 행동이 여전히 유효한지 (일정·연락처·링크)
   1회 확인을 권한다.
2. **리드마그넷형 추가 절차**:
   - 배포 채널(랜딩 페이지·뉴스레터·세일즈 메일)별 파일 선택 안내 —
     다운로드 배포는 PDF, 편집 제공은 PPTX.
   - 다운로드 동선(어디서 어떤 대가로 받는가)과 후속 접점(다운로드 후 연락 흐름)
     설계가 storyline.md의 CTA 설계와 일치하는지 확인.
   - **외부 공유물은 배포 전 사람 최종 검토 필수** — 스킬·Evaluator 승인은 내부
     품질 게이트일 뿐, 대외 배포 책임 검토를 대체하지 않는다. 이 사실을 명시적으로
     고지하고 검토 완료 확인을 받는다.
3. **외부 공유 일반 원칙**: 리드마그넷형이 아니어도 자료가 조직 밖으로 나가는
   경우(고객 제안, 컨퍼런스)에는 같은 사람 최종 검토 고지를 적용한다.
4. **HTML 중간 산출물 보존 안내**: `slides-work/<deck-slug>/` 전체(특히 deck.html·
   storyline.md·design-system.md)를 보존하면 이후 수정 시 파이프라인을 재사용할 수
   있다 — "다음 수정은 PPTX가 아니라 여기서 다시 시작하는 것이 빠릅니다."
5. status.md 전 단계 ✅ 처리 + 최종 산출물 경로 요약:

```markdown
## 납품 요약
- PPTX (네이티브 편집 가능): slides-work/<deck-slug>/dist/deck.pptx
- PDF (픽셀 동일 인쇄본):   slides-work/<deck-slug>/dist/deck.pdf
- 검증 보고서:              slides-work/<deck-slug>/dist/verify_report.md
- 재수정 진입점:            slides-work/<deck-slug>/deck.html (+ storyline.md)
```
