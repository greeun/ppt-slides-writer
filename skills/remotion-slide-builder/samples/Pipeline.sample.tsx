/**
 * Pipeline 패턴 — 가로 흐름으로 아키텍처 단계를 잇는 슬라이드
 *
 * 파일명: S0x_TopicName.tsx (S + 2자리 순번 + _ + PascalCase 주제명)
 * 용도:
 *   - 풀체인 흐름(예: React → Spring → FastAPI → OpenAI)을 노드와 화살표로 표현
 *   - 노드 수가 많으면 자동 줄바꿈됩니다(flexWrap)
 *   - dark={false}로 밝은 배경 슬라이드에도 사용할 수 있습니다
 * 규칙:
 *   - SlideLayout 안에서 사용. 노드는 3~5개 권장
 *   - node.color로 단계별 강조색을 지정합니다
 */
import React from "react";
import { SlideLayout } from "../../components/SlideLayout";
import { Pipeline } from "../../components/Pipeline";
import { colors } from "../../theme";

export const S04_Pipeline: React.FC = () => {
  return (
    <SlideLayout
      title="요청이 거치는 전체 경로"
      subtitle="프런트엔드부터 모델 호출까지 한눈에 봅니다"
      sectionLabel="LO1 · 시스템 구성"
      source="교육팀, 2025"
      pageNumber={4}
      totalPages={9}
    >
      <div style={{ flex: 1, display: "flex", alignItems: "center" }}>
        <Pipeline
          nodes={[
            { label: "React", sub: "사용자 입력", color: colors.accent },
            { label: "Spring", sub: "인증·라우팅", color: colors.primary },
            { label: "FastAPI", sub: "AI 게이트웨이", color: colors.secondary },
            { label: "OpenAI", sub: "모델 추론", color: colors.amber },
          ]}
          startFrom={0.3}
        />
      </div>
    </SlideLayout>
  );
};
