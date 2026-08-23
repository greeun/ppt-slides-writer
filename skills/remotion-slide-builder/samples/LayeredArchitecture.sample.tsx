/**
 * LayeredArchitecture 패턴 — 계층 구조를 아래에서 위로 쌓아 보여주는 레이아웃
 *
 * 파일명: S0x_TopicName.tsx (S + 2자리 순번 + _ + PascalCase 주제명)
 * 용도:
 *   - 인프라/플랫폼/애플리케이션처럼 위로 쌓이는 계층 구조 표현
 *   - layers는 아래 계층부터 순서대로 적습니다(렌더링은 column-reverse로 위로 쌓음)
 *   - caption으로 전체 구조의 핵심 메시지를 한 줄 덧붙입니다
 * 규칙:
 *   - SlideLayout 안에서 사용. 계층은 3~5개 권장
 *   - layer.tone으로 계층별 색을 지정할 수 있고, 생략하면 자동 배색됩니다
 */
import React from "react";
import { SlideLayout } from "../../components/SlideLayout";
import { LayeredArchitecture } from "../../components/layouts";

export const S06_LayeredArchitecture: React.FC = () => {
  return (
    <SlideLayout
      title="AI 애플리케이션의 계층 구조"
      subtitle="아래에서 위로, 인프라부터 사용자 경험까지 쌓입니다"
      sectionLabel="LO1 · 아키텍처"
      source="교육팀, 2025"
      pageNumber={6}
      totalPages={9}
    >
      <LayeredArchitecture
        layers={[
          { title: "인프라", desc: "GPU 서버, 컨테이너, 네트워크 등 실행 기반" },
          { title: "모델 계층", desc: "LLM, 임베딩, 벡터 저장소 등 추론 자원" },
          { title: "오케스트레이션", desc: "프롬프트, 도구 호출, 워크플로우 제어" },
          { title: "애플리케이션", desc: "사용자가 직접 마주하는 화면과 API" },
        ]}
        caption="각 계층은 아래 계층을 추상화하여 위 계층에 안정된 인터페이스를 제공합니다"
      />
    </SlideLayout>
  );
};
