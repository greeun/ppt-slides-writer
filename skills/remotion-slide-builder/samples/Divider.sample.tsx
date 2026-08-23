/**
 * SectionDivider 패턴 — LO 시작 간지 (다크 배경)
 *
 * 파일명: S01_Divider.tsx (항상 섹션 첫 번째)
 * 규칙:
 *   - sectionNumber: CU 내 순서 (0부터)
 *   - objectives: LO의 학습 목표에서 추출 (2~4개)
 *   - duration: CU의 시간 배분에서 추출
 */
import React from "react";
import { SectionDivider } from "../../components/SectionDivider";

export const S01_Divider: React.FC = () => (
  <SectionDivider
    sectionNumber={1}
    title="학습 주제명"
    objectives={[
      "첫 번째 학습 목표를 이해합니다",
      "두 번째 핵심 개념을 적용합니다",
      "세 번째 실습 내용을 수행합니다",
    ]}
    duration="50분"
  />
);
