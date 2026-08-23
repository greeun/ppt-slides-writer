/**
 * LO Index 패턴 — TransitionSeries로 슬라이드 연결
 *
 * 파일명: src/slides/lo1-topic/LO1.tsx
 * 규칙:
 *   - SLIDE_DURATIONS: 초 단위, 슬라이드 수와 동일
 *   - 전환: 디바이더→첫콘텐츠 fade(), 콘텐츠→콘텐츠 slide(), 마지막→체크포인트 fade()
 *   - getDuration export 필수 (Root.tsx, FullPresentation.tsx에서 사용)
 */
import React from "react";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { useVideoConfig } from "remotion";
import "../../load-fonts";

import { S01_Divider } from "./S01_Divider";
import { S02_FirstTopic } from "./S02_FirstTopic";
import { S03_SecondTopic } from "./S03_SecondTopic";
import { S04_Checkpoint } from "./S04_Checkpoint";

// 초 단위: 모든 슬라이드 기본 5초
const SLIDE_DURATIONS = [5, 5, 5, 5];
const TRANSITION_FRAMES = 15;

const slides = [
  S01_Divider,
  S02_FirstTopic,
  S03_SecondTopic,
  S04_Checkpoint,
];

export const LO1: React.FC = () => {
  const { fps } = useVideoConfig();

  return (
    <TransitionSeries>
      {slides.map((SlideComponent, i) => (
        <React.Fragment key={i}>
          {i > 0 && (
            <TransitionSeries.Transition
              presentation={
                i === 1 || i === slides.length - 1
                  ? fade()
                  : slide({ direction: "from-right" })
              }
              timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
            />
          )}
          <TransitionSeries.Sequence
            durationInFrames={SLIDE_DURATIONS[i] * fps}
          >
            <SlideComponent />
          </TransitionSeries.Sequence>
        </React.Fragment>
      ))}
    </TransitionSeries>
  );
};

export const getLO1DurationInFrames = (fps: number) => {
  const totalSlideFrames = SLIDE_DURATIONS.reduce((a, b) => a + b * fps, 0);
  return totalSlideFrames - (slides.length - 1) * TRANSITION_FRAMES;
};
