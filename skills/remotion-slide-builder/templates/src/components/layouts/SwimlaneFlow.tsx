import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { colors } from "../../theme";

type SwimlaneStep = {
  lane: string;
  title: string;
  desc: string;
};

type SwimlaneFlowProps = {
  steps: SwimlaneStep[];
  startFrom?: number;
};

export const SwimlaneFlow: React.FC<SwimlaneFlowProps> = ({ steps, startFrom = 0.25 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const lanes = Array.from(new Set(steps.map((step) => step.lane))).slice(0, 4);
  const laneColors = [colors.primary, colors.accent, colors.amber, colors.secondary];

  return (
    <div style={{ flex: 1, display: "grid", gridTemplateRows: `repeat(${lanes.length}, 1fr)`, gap: 14 }}>
      {lanes.map((lane, laneIndex) => {
        const laneSteps = steps.filter((step) => step.lane === lane);
        return (
          <div key={lane} style={{ display: "grid", gridTemplateColumns: "210px 1fr", gap: 14 }}>
            <div
              style={{
                borderRadius: 16,
                backgroundColor: `${laneColors[laneIndex % laneColors.length]}18`,
                color: laneColors[laneIndex % laneColors.length],
                fontSize: 25,
                fontWeight: 900,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                textAlign: "center",
                padding: 18,
              }}
            >
              {lane}
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
              {laneSteps.map((step, stepIndex) => {
                const globalIndex = steps.indexOf(step);
                const delay = startFrom + globalIndex * 0.1;
                const opacity = interpolate(frame, [delay * fps, (delay + 0.25) * fps], [0, 1], {
                  extrapolateLeft: "clamp",
                  extrapolateRight: "clamp",
                });

                return (
                  <React.Fragment key={`${lane}-${step.title}`}>
                    <div
                      style={{
                        opacity,
                        flex: 1,
                        minHeight: 116,
                        backgroundColor: colors.cardBg,
                        border: `1px solid ${colors.border}`,
                        borderRadius: 16,
                        padding: "20px 22px",
                      }}
                    >
                      <div style={{ fontSize: 24, fontWeight: 800, color: colors.text }}>{step.title}</div>
                      <div style={{ fontSize: 19, lineHeight: 1.45, color: colors.textLight, marginTop: 8 }}>{step.desc}</div>
                    </div>
                    {stepIndex < laneSteps.length - 1 && <div style={{ fontSize: 24, color: colors.textLight }}>→</div>}
                  </React.Fragment>
                );
              })}
            </div>
          </div>
        );
      })}
    </div>
  );
};
