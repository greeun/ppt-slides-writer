/**
 * HubSpokeMap 패턴 — 중심 개념과 주변 요소를 방사형으로 배치하는 레이아웃
 *
 * 파일명: S0x_TopicName.tsx (S + 2자리 순번 + _ + PascalCase 주제명)
 * 용도:
 *   - 하나의 중심(Hub)과 이를 둘러싼 구성 요소(Spoke)의 관계 표현
 *   - 예: "에이전트(중심) ↔ 도구·메모리·플래너·실행기(주변)"
 * 규칙:
 *   - SlideLayout 안에서 사용. spokes는 최대 6개까지 표시됩니다
 *   - hubTitle/hubDesc는 짧게, spoke는 제목 한 줄과 설명 한 줄 권장
 */
import React from "react";
import { SlideLayout } from "../../components/SlideLayout";
import { HubSpokeMap } from "../../components/layouts";

export const S07_HubSpokeMap: React.FC = () => {
  return (
    <SlideLayout
      title="에이전트를 둘러싼 구성 요소"
      subtitle="중심의 에이전트가 주변 모듈을 호출하며 작업을 완성합니다"
      sectionLabel="LO2 · 에이전트 구조"
      source="Anthropic, 'Building Effective Agents', 2024"
      pageNumber={7}
      totalPages={9}
    >
      <HubSpokeMap
        hubTitle="에이전트"
        hubDesc="목표를 받아 단계를 계획하고 실행합니다"
        spokes={[
          { title: "플래너", desc: "작업을 하위 단계로 분해합니다" },
          { title: "도구 호출", desc: "검색·코드 실행 등 외부 기능을 사용합니다" },
          { title: "메모리", desc: "대화와 중간 결과를 보관합니다" },
          { title: "실행기", desc: "계획을 실제 동작으로 옮깁니다" },
          { title: "검증기", desc: "결과의 정합성을 점검합니다" },
          { title: "응답 생성", desc: "사용자에게 최종 답변을 정리합니다" },
        ]}
      />
    </SlideLayout>
  );
};
