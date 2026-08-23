import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { colors, fonts, fontSize, spacing } from "../theme";
import { PageNumber } from "./PageNumber";

type HandsOnSlideProps = {
  sectionLabel: string;
  blockNumber: number;
  title: string;
  instruction: string;
  command?: string;
  expectation: string;
  storyNote: string;
  pageNumber?: number;
  totalPages?: number;
};

export const HandsOnSlide: React.FC<HandsOnSlideProps> = ({
  sectionLabel,
  blockNumber,
  title,
  instruction,
  command,
  expectation,
  storyNote,
  pageNumber,
  totalPages,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const headerOpacity = interpolate(frame, [0, 0.3 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });
  const contentOpacity = interpolate(frame, [0.2 * fps, 0.6 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });
  const noteOpacity = interpolate(frame, [0.6 * fps, 1.0 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: colors.bgDark,
        fontFamily: fonts.body,
        padding: spacing.page,
        display: "flex",
        flexDirection: "column",
      }}
    >
      <div style={{ opacity: headerOpacity }}>
        <div
          style={{
            fontSize: fontSize.caption,
            fontWeight: 600,
            color: colors.accent,
            letterSpacing: 2,
            marginBottom: spacing.small,
          }}
        >
          {sectionLabel}
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: spacing.element }}>
          <div
            style={{
              padding: "8px 20px",
              borderRadius: 20,
              background: `linear-gradient(135deg, ${colors.accent}, #0891B2)`,
              color: "#fff",
              fontSize: fontSize.caption,
              fontWeight: 700,
            }}
          >
            BLOCK {blockNumber}
          </div>
          <h1
            style={{
              fontSize: fontSize.h1,
              fontWeight: 700,
              color: colors.textInvert,
              margin: 0,
            }}
          >
            {title}
          </h1>
        </div>
      </div>

      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          justifyContent: "flex-start",
          gap: spacing.section,
          opacity: contentOpacity,
        }}
      >
        <div
          style={{
            backgroundColor: "rgba(255,255,255,0.06)",
            borderRadius: 16,
            padding: "32px 40px",
            borderLeft: `5px solid ${colors.accent}`,
          }}
        >
          <div
            style={{
              fontSize: fontSize.body,
              color: "rgba(248,250,252,0.6)",
              marginBottom: 12,
              fontWeight: 600,
            }}
          >
            해볼 것
          </div>
          <div
            style={{
              fontSize: fontSize.h3,
              color: colors.textInvert,
              lineHeight: 1.6,
            }}
          >
            {instruction}
          </div>
        </div>

        {command && (
          <div
            style={{
              fontFamily: "monospace",
              fontSize: fontSize.h3,
              color: colors.accent,
              backgroundColor: "rgba(6,182,212,0.1)",
              padding: "20px 32px",
              borderRadius: 12,
              border: `1px solid rgba(6,182,212,0.3)`,
            }}
          >
            {command}
          </div>
        )}

        <div
          style={{
            backgroundColor: "rgba(255,255,255,0.06)",
            borderRadius: 16,
            padding: "32px 40px",
            borderLeft: `5px solid ${colors.primaryLight}`,
          }}
        >
          <div
            style={{
              fontSize: fontSize.body,
              color: "rgba(248,250,252,0.6)",
              marginBottom: 12,
              fontWeight: 600,
            }}
          >
            관찰 포인트
          </div>
          <div
            style={{
              fontSize: fontSize.h3,
              color: colors.textInvert,
              lineHeight: 1.6,
            }}
          >
            {expectation}
          </div>
        </div>
      </div>

      <div
        style={{
          opacity: noteOpacity,
          padding: "16px 24px",
          borderRadius: 12,
          backgroundColor: "rgba(79,70,229,0.15)",
          border: `1px solid rgba(79,70,229,0.3)`,
        }}
      >
        <span
          style={{
            fontSize: fontSize.body,
            color: colors.primaryLight,
            fontWeight: 600,
          }}
        >
          {storyNote}
        </span>
      </div>

      <PageNumber pageNumber={pageNumber} totalPages={totalPages} dark />

      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          right: 0,
          height: 4,
          background: `linear-gradient(90deg, ${colors.accent}, ${colors.gradientEnd})`,
        }}
      />
    </AbsoluteFill>
  );
};
