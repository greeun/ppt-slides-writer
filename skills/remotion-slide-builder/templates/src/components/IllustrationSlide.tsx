import React from "react";
import {
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
} from "remotion";
import { SlideLayout } from "./SlideLayout";

type Props = {
  title: string;
  subtitle?: string;
  sectionLabel: string;
  image: string;
  source?: string;
  pageNumber?: number;
  totalPages?: number;
};

export const IllustrationSlide: React.FC<Props> = ({
  title,
  subtitle,
  sectionLabel,
  image,
  source,
  pageNumber,
  totalPages,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(
    frame,
    [0.3 * fps, 0.9 * fps],
    [0, 1],
    { extrapolateRight: "clamp", extrapolateLeft: "clamp" },
  );
  const scale = interpolate(
    frame,
    [0.3 * fps, 0.9 * fps],
    [0.97, 1],
    { extrapolateRight: "clamp", extrapolateLeft: "clamp" },
  );

  return (
    <SlideLayout
      title={title}
      subtitle={subtitle}
      sectionLabel={sectionLabel}
      source={source}
      pageNumber={pageNumber}
      totalPages={totalPages}
    >
      <div
        style={{
          flex: 1,
          minHeight: 0,
          width: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          padding: "8px 0 72px",
          boxSizing: "border-box",
          overflow: "hidden",
        }}
      >
        <img
          src={staticFile(image)}
          alt=""
          style={{
            width: "auto",
            height: "auto",
            maxWidth: "100%",
            maxHeight: 560,
            objectFit: "contain",
            borderRadius: 16,
            opacity,
            transform: `scale(${scale})`,
          }}
        />
      </div>
    </SlideLayout>
  );
};
