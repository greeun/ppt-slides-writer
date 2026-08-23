import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { colors } from "../../theme";

type ModuleNode = {
  title: string;
  desc: string;
};

type ModuleConstellationProps = {
  centerTitle: string;
  centerDesc: string;
  nodes: ModuleNode[];
  caption?: string;
  startFrom?: number;
};

export const ModuleConstellation: React.FC<ModuleConstellationProps> = ({
  centerTitle,
  centerDesc,
  nodes,
  caption,
  startFrom = 0.25,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const visibleNodes = nodes.slice(0, 6);
  const positions = [
    { left: "4%", top: "7%" },
    { left: "38%", top: "4%" },
    { left: "68%", top: "16%" },
    { left: "68%", top: "62%" },
    { left: "34%", top: "72%" },
    { left: "4%", top: "56%" },
  ];

  return (
    <div style={{ position: "relative", flex: 1, minHeight: 600 }}>
      <div
        style={{
          position: "absolute",
          left: "50%",
          top: "49%",
          transform: "translate(-50%, -50%)",
          width: 390,
          minHeight: 190,
          borderRadius: 28,
          backgroundColor: colors.bgDark,
          color: colors.textInvert,
          padding: "30px 34px",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          boxShadow: "0 22px 54px rgba(15,23,42,0.22)",
          zIndex: 2,
        }}
      >
        <div style={{ fontSize: 34, fontWeight: 900, lineHeight: 1.2 }}>{centerTitle}</div>
        <div style={{ fontSize: 20, opacity: 0.78, lineHeight: 1.5, marginTop: 12 }}>{centerDesc}</div>
      </div>
      {visibleNodes.map((node, index) => {
        const delay = startFrom + index * 0.12;
        const opacity = interpolate(frame, [delay * fps, (delay + 0.28) * fps], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        const scale = interpolate(frame, [delay * fps, (delay + 0.28) * fps], [0.94, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        const pos = positions[index] ?? positions[0];
        const accent = [colors.primary, colors.accent, colors.amber, colors.secondary, "#10B981", colors.clay][index % 6];

        return (
          <div
            key={node.title}
            style={{
              position: "absolute",
              ...pos,
              width: 430,
              minHeight: 128,
              opacity,
              transform: `scale(${scale})`,
              backgroundColor: colors.cardBg,
              border: `1px solid ${colors.border}`,
              borderLeft: `8px solid ${accent}`,
              borderRadius: 20,
              padding: "22px 24px",
              boxShadow: "0 12px 28px rgba(15,23,42,0.07)",
            }}
          >
            <div style={{ fontSize: 25, fontWeight: 900, color: colors.text, lineHeight: 1.22 }}>{node.title}</div>
            <div style={{ fontSize: 19, color: colors.textLight, lineHeight: 1.45, marginTop: 8 }}>{node.desc}</div>
          </div>
        );
      })}
      {caption && (
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            bottom: 0,
            fontSize: 22,
            color: colors.text,
            lineHeight: 1.5,
            backgroundColor: `${colors.primary}08`,
            border: `1px solid ${colors.primary}20`,
            borderRadius: 14,
            padding: "15px 22px",
          }}
        >
          {caption}
        </div>
      )}
    </div>
  );
};
