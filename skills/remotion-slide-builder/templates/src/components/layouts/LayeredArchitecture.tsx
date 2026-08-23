import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { colors } from "../../theme";

type Layer = {
  title: string;
  desc: string;
  tone?: string;
};

type LayeredArchitectureProps = {
  layers: Layer[];
  caption?: string;
  startFrom?: number;
};

export const LayeredArchitecture: React.FC<LayeredArchitectureProps> = ({ layers, caption, startFrom = 0.25 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const tones = [colors.primary, colors.accent, colors.amber, colors.secondary, "#10B981"];

  return (
    <div style={{ display: "flex", flexDirection: "column", flex: 1, justifyContent: "center", gap: 22 }}>
      <div style={{ display: "flex", flexDirection: "column-reverse", gap: 14 }}>
        {layers.map((layer, index) => {
          const delay = startFrom + index * 0.12;
          const opacity = interpolate(frame, [delay * fps, (delay + 0.3) * fps], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          const y = interpolate(frame, [delay * fps, (delay + 0.3) * fps], [20, 0], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          const tone = layer.tone ?? tones[index % tones.length];

          return (
            <div
              key={layer.title}
              style={{
                opacity,
                transform: `translateY(${y}px)`,
                display: "grid",
                gridTemplateColumns: "280px 1fr",
                alignItems: "center",
                minHeight: 92,
                borderRadius: 18,
                overflow: "hidden",
                border: `1px solid ${colors.border}`,
                backgroundColor: colors.cardBg,
                boxShadow: "0 8px 22px rgba(15,23,42,0.05)",
              }}
            >
              <div
                style={{
                  height: "100%",
                  background: `linear-gradient(135deg, ${tone}, ${tone}AA)`,
                  color: colors.white,
                  display: "flex",
                  alignItems: "center",
                  padding: "0 28px",
                  fontSize: 26,
                  fontWeight: 800,
                  lineHeight: 1.25,
                }}
              >
                {layer.title}
              </div>
              <div style={{ padding: "20px 28px", fontSize: 23, color: colors.text, lineHeight: 1.55 }}>{layer.desc}</div>
            </div>
          );
        })}
      </div>
      {caption && (
        <div style={{ fontSize: 22, color: colors.text, lineHeight: 1.55, padding: "16px 24px", backgroundColor: `${colors.primary}08`, borderRadius: 14, border: `1px solid ${colors.primary}22` }}>
          {caption}
        </div>
      )}
    </div>
  );
};
