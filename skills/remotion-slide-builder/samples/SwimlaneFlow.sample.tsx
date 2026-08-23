/**
 * SwimlaneFlow 패턴 — 주체(레인)별 흐름을 가로로 펼치는 레이아웃
 *
 * 파일명: S0x_TopicName.tsx (S + 2자리 순번 + _ + PascalCase 주제명)
 * 용도:
 *   - 여러 주체(사용자/프런트엔드/백엔드 등)가 단계별로 주고받는 흐름 표현
 *   - 같은 lane 값을 가진 step들이 한 레인에 가로로 나열되고 화살표로 이어집니다
 * 규칙:
 *   - SlideLayout 안에서 사용. lane은 최대 4개까지 표시됩니다
 *   - steps의 등장 순서대로 left-to-right 흐름을 구성합니다
 */
import React from "react";
import { SlideLayout } from "../../components/SlideLayout";
import { SwimlaneFlow } from "../../components/layouts";

export const S08_SwimlaneFlow: React.FC = () => {
  return (
    <SlideLayout
      title="요청 처리 흐름"
      subtitle="주체별로 무엇을 책임지는지 한 줄에서 따라갑니다"
      sectionLabel="LO3 · 처리 흐름"
      source="교육팀, 2025"
      pageNumber={8}
      totalPages={9}
    >
      <SwimlaneFlow
        steps={[
          { lane: "사용자", title: "질문 입력", desc: "채팅창에 메시지를 보냅니다" },
          { lane: "프런트엔드", title: "요청 전송", desc: "API로 메시지를 전달합니다" },
          { lane: "백엔드", title: "검증·라우팅", desc: "인증을 확인하고 AI 서버로 보냅니다" },
          { lane: "백엔드", title: "응답 정리", desc: "모델 결과를 가공해 반환합니다" },
          { lane: "AI 서버", title: "모델 추론", desc: "LLM이 답변을 생성합니다" },
        ]}
      />
    </SlideLayout>
  );
};
