/**
 * FullPresentation.tsx — 전체 섹션 Series 연결
 *
 * {{SECTIONS}} 주석을 실제 섹션으로 교체
 */
import React from "react";
import { Series, useVideoConfig } from "remotion";
import "./load-fonts";

// {{SECTION_IMPORTS}}
// import { Overview, getOverviewDurationInFrames } from "./slides/overview/Overview";
// import { LO1, getLO1DurationInFrames } from "./slides/lo1-topic/LO1";

const sections: Array<{
  Component: React.FC;
  getDuration: (fps: number) => number;
}> = [
  // {{SECTION_ENTRIES}}
  // { Component: Overview, getDuration: getOverviewDurationInFrames },
  // { Component: LO1, getDuration: getLO1DurationInFrames },
];

export const FullPresentation: React.FC = () => {
  const { fps } = useVideoConfig();

  return (
    <Series>
      {sections.map(({ Component, getDuration }, i) => (
        <Series.Sequence key={i} durationInFrames={getDuration(fps)}>
          <Component />
        </Series.Sequence>
      ))}
    </Series>
  );
};

export const getFullPresentationDurationInFrames = (fps: number) => {
  return sections.reduce((total, { getDuration }) => total + getDuration(fps), 0);
};
