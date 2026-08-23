import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { colors, fontSize, spacing } from "../theme";

type PipelineNode = {
  label: string;
  sub?: string;
  color?: string;
};

type PipelineProps = {
  nodes: PipelineNode[];
  startFrom?: number;
  dark?: boolean;
  arrowLabel?: string;
};

// 풀체인 아키텍처 가로 흐름 (React → Spring → FastAPI → OpenAI)
export const Pipeline: React.FC<PipelineProps> = ({
  nodes,
  startFrom = 0.3,
  dark = true,
  arrowLabel,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const textColor = dark ? colors.textInvert : colors.text;
  const subColor = dark ? "rgba(248,250,252,0.6)" : colors.textLight;

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        gap: spacing.element,
        width: "100%",
        flexWrap: "wrap",
      }}
    >
      {nodes.map((node, i) => {
        const delay = startFrom + i * 0.2;
        const opacity = interpolate(
          frame,
          [delay * fps, (delay + 0.3) * fps],
          [0, 1],
          { extrapolateRight: "clamp", extrapolateLeft: "clamp" }
        );
        const scale = interpolate(
          frame,
          [delay * fps, (delay + 0.3) * fps],
          [0.85, 1],
          { extrapolateRight: "clamp", extrapolateLeft: "clamp" }
        );
        const arrowDelay = delay + 0.1;
        const arrowOpacity = interpolate(
          frame,
          [arrowDelay * fps, (arrowDelay + 0.25) * fps],
          [0, 1],
          { extrapolateRight: "clamp", extrapolateLeft: "clamp" }
        );

        return (
          <React.Fragment key={i}>
            {i > 0 && (
              <div
                style={{
                  opacity: arrowOpacity,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  gap: 4,
                }}
              >
                <span
                  style={{
                    fontSize: 40,
                    color: colors.accent,
                    fontWeight: 700,
                  }}
                >
                  ›
                </span>
              </div>
            )}
            <div
              style={{
                opacity,
                transform: `scale(${scale})`,
                backgroundColor: dark ? "rgba(255,255,255,0.06)" : colors.cardBg,
                border: `2px solid ${node.color || colors.primary}`,
                borderRadius: 16,
                padding: "24px 28px",
                minWidth: 200,
                textAlign: "center",
                display: "flex",
                flexDirection: "column",
                gap: 6,
              }}
            >
              <div
                style={{
                  fontSize: fontSize.h3,
                  fontWeight: 700,
                  color: node.color || textColor,
                  lineHeight: 1.2,
                }}
              >
                {node.label}
              </div>
              {node.sub && (
                <div
                  style={{
                    fontSize: fontSize.caption,
                    color: subColor,
                    lineHeight: 1.4,
                  }}
                >
                  {node.sub}
                </div>
              )}
            </div>
          </React.Fragment>
        );
      })}
      {arrowLabel && null}
    </div>
  );
};
