/**
 * Root.tsx — Composition 등록
 *
 * 사용법: 섹션 추가 시 import + Composition 블록 추가
 * {{SECTIONS}} 주석을 실제 섹션으로 교체
 */
import React from "react";
import { Composition, Folder } from "remotion";
import { COMP_WIDTH, COMP_HEIGHT, FPS } from "./theme";
import {
  FullPresentation,
  getFullPresentationDurationInFrames,
} from "./FullPresentation";

// {{SECTION_IMPORTS}}
// import { Overview, getOverviewDurationInFrames } from "./slides/overview/Overview";
// import { LO1, getLO1DurationInFrames } from "./slides/lo1-topic/LO1";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="Full-Presentation"
        component={FullPresentation}
        durationInFrames={getFullPresentationDurationInFrames(FPS)}
        fps={FPS}
        width={COMP_WIDTH}
        height={COMP_HEIGHT}
      />

      <Folder name="Sections">
        {/* {{SECTION_COMPOSITIONS}}
        <Composition
          id="0-Course-Intro"
          component={Overview}
          durationInFrames={getOverviewDurationInFrames(FPS)}
          fps={FPS}
          width={COMP_WIDTH}
          height={COMP_HEIGHT}
        />
        <Composition
          id="1-Topic-Name"
          component={LO1}
          durationInFrames={getLO1DurationInFrames(FPS)}
          fps={FPS}
          width={COMP_WIDTH}
          height={COMP_HEIGHT}
        />
        */}
      </Folder>
    </>
  );
};
