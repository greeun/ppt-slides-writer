/**
 * AnnotatedCode 패턴 — 코드를 한 줄씩 의미 주석과 함께 읽는 슬라이드
 *
 * 파일명: S0x_TopicName.tsx (S + 2자리 순번 + _ + PascalCase 주제명)
 * 용도:
 *   - "코드 한 줄씩 뜯어보기" 류 설명. 좌측 코드, 우측 주석을 격자로 배치
 *   - lines 배열에서 note가 없는 줄은 빈 칸으로 정렬 유지
 *   - callout으로 코드 밖 동작/주의를 별도 박스에 표기
 * 규칙:
 *   - SlideLayout 안에서 사용. 코드는 6~9줄 권장(콘텐츠 영역 초과 방지)
 *   - codeFontSize/noteFontSize로 줄 수에 맞춰 가독성 조정
 */
import React from "react";
import { SlideLayout } from "../../components/SlideLayout";
import { AnnotatedCode } from "../../components/AnnotatedCode";

export const S03_AnnotatedCode: React.FC = () => {
  return (
    <SlideLayout
      title="FastAPI 엔드포인트 한 줄씩 읽기"
      subtitle="요청을 받아 LLM 호출 결과를 반환하는 최소 구성입니다"
      sectionLabel="LO2 · 백엔드 연동"
      source="FastAPI 공식 문서, 2024"
      pageNumber={3}
      totalPages={9}
    >
      <AnnotatedCode
        fileName="app/main.py"
        lines={[
          { code: "@app.post('/chat')", note: "POST 요청을 받는 경로를 선언합니다" },
          { code: "async def chat(req: ChatRequest):", note: "Pydantic 모델로 요청 본문을 검증합니다" },
          { code: "    reply = await llm.ainvoke(req.message)", note: "LLM을 비동기로 호출합니다" },
          { code: "    return {'reply': reply.content}", note: "응답을 JSON으로 반환합니다" },
        ]}
        callout={{
          label: "주의",
          text: "ainvoke는 이벤트 루프를 막지 않으므로 동시 요청 처리에 유리합니다",
        }}
      />
    </SlideLayout>
  );
};
