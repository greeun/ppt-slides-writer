/**
 * CheckpointSlide 패턴 — LO 마무리 요약
 *
 * 파일명: S<NN>_Checkpoint.tsx (항상 섹션 마지막)
 * 규칙:
 *   - points: 해당 LO의 핵심 요약 2~5개
 *   - sectionLabel: LO 인덱스의 sectionLabel과 동일
 *   - 퀴즈/설문 없이 자기 확인 리스트로만 구성
 */
import React from "react";
import { CheckpointSlide } from "../../components/CheckpointSlide";

export const S04_Checkpoint: React.FC = () => (
  <CheckpointSlide
    sectionLabel="LO1 · 주제명"
    title="체크포인트"
    points={[
      "첫 번째 핵심 개념을 이해하였습니다",
      "두 번째 핵심 개념의 차이점을 구분할 수 있습니다",
      "실습을 통해 직접 적용해 보았습니다",
    ]}
  />
);
