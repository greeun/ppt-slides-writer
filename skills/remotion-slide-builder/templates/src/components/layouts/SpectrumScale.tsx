import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { colors } from "../../theme";

type SpectrumItem = {
  title: string;
  desc: string;
};

type SpectrumScaleProps = {
  items: SpectrumItem[];
  leftLabel?: string;
  rightLabel?: string;
  caption?: string;
  startFrom?: number;
};

export const SpectrumScale: React.FC<SpectrumScaleProps> = ({ items, leftLabel = "단순", rightLabel = "복합", caption, startFrom = 0.25 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{ flex: 1, display: "flex", flexDirection: "column", justifyContent: "center", gap: 28 }}>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 20, fontWeight: 800, color: colors.textLight }}>
        <span>{leftLabel}</span>
        <span>{rightLabel}</span>
      </div>
      <div style={{ position: "relative", height: 360 }}>
        <div
          style={{
            position: "absolute",
            left: 70,
            right: 70,
            top: 92,
            height: 12,
            borderRadius: 999,
            background: `linear-gradient(90deg, ${colors.accent}, ${colors.primary}, ${colors.secondary}, ${colors.amber})`,
          }}
        />
        <div style={{ display: "grid", gridTemplateColumns: `repeat(${items.length}, 1fr)`, gap: 18, position: "relative" }}>
          {items.map((item, index) => {
            const delay = startFrom + index * 0.12;
            const opacity = interpolate(frame, [delay * fps, (delay + 0.28) * fps], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            });
            const y = interpolate(frame, [delay * fps, (delay + 0.28) * fps], [24, 0], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            });

            return (
              <div key={item.title} style={{ opacity, transform: `translateY(${y}px)`, display: "flex", flexDirection: "column", alignItems: "center", gap: 18 }}>
                <div style={{ width: 54, height: 54, borderRadius: 27, backgroundColor: colors.cardBg, border: `4px solid ${colors.primary}`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 24, fontWeight: 900, color: colors.primary, marginTop: 70 }}>
                  {index + 1}
                </div>
                <div style={{ backgroundColor: colors.cardBg, border: `1px solid ${colors.border}`, borderRadius: 18, padding: "20px 22px", minHeight: 168, boxShadow: "0 10px 24px rgba(15,23,42,0.05)" }}>
                  <div style={{ fontSize: 26, fontWeight: 900, color: colors.text, lineHeight: 1.2 }}>{item.title}</div>
                  <div style={{ fontSize: 20, color: colors.textLight, lineHeight: 1.45, marginTop: 10 }}>{item.desc}</div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
      {caption && <div style={{ fontSize: 22, lineHeight: 1.55, color: colors.text, backgroundColor: `${colors.primary}08`, border: `1px solid ${colors.primary}20`, borderRadius: 14, padding: "16px 24px" }}>{caption}</div>}
    </div>
  );
};
