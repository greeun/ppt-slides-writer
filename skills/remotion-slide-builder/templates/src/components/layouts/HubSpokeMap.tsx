import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { colors } from "../../theme";

type Spoke = {
  title: string;
  desc: string;
};

type HubSpokeMapProps = {
  hubTitle: string;
  hubDesc: string;
  spokes: Spoke[];
  startFrom?: number;
};

export const HubSpokeMap: React.FC<HubSpokeMapProps> = ({ hubTitle, hubDesc, spokes, startFrom = 0.25 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const visibleSpokes = spokes.slice(0, 6);

  return (
    <div style={{ position: "relative", flex: 1, minHeight: 600 }}>
      <div
        style={{
          position: "absolute",
          left: "50%",
          top: "50%",
          transform: "translate(-50%, -50%)",
          width: 360,
          height: 210,
          borderRadius: 26,
          background: `linear-gradient(135deg, ${colors.primary}, ${colors.secondary})`,
          color: colors.white,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          padding: 34,
          boxShadow: "0 24px 54px rgba(79,70,229,0.25)",
          zIndex: 2,
        }}
      >
        <div style={{ fontSize: 34, fontWeight: 900, lineHeight: 1.18 }}>{hubTitle}</div>
        <div style={{ fontSize: 20, lineHeight: 1.5, opacity: 0.78, marginTop: 12 }}>{hubDesc}</div>
      </div>
      {visibleSpokes.map((spoke, index) => {
        const delay = startFrom + index * 0.12;
        const opacity = interpolate(frame, [delay * fps, (delay + 0.28) * fps], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        const positions = [
          { left: "5%", top: "8%" },
          { left: "60%", top: "8%" },
          { left: "72%", top: "39%" },
          { left: "60%", top: "70%" },
          { left: "5%", top: "70%" },
          { left: "0%", top: "39%" },
        ];
        const pos = positions[index] ?? positions[0];

        return (
          <div
            key={spoke.title}
            style={{
              position: "absolute",
              ...pos,
              width: 420,
              minHeight: 126,
              opacity,
              backgroundColor: colors.cardBg,
              border: `1px solid ${colors.border}`,
              borderRadius: 18,
              padding: "22px 24px",
              boxShadow: "0 10px 26px rgba(15,23,42,0.06)",
            }}
          >
            <div style={{ fontSize: 26, fontWeight: 800, color: colors.text, lineHeight: 1.25 }}>{spoke.title}</div>
            <div style={{ fontSize: 20, color: colors.textLight, lineHeight: 1.5, marginTop: 8 }}>{spoke.desc}</div>
          </div>
        );
      })}
    </div>
  );
};
