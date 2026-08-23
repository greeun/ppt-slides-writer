import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { colors, fontSize, spacing } from "../theme";

// 예제 코드를 한 줄씩, 오른쪽에 의미 주석을 붙여 읽는 격자형 블록.
// "한 줄씩 읽기 / 뜯어보기" 류 설명 슬라이드의 공통 포맷.
const NOTE_COLOR = "#86EFAC"; // 코드 주석 느낌의 연한 초록

export type CodeLine = { code: string; note?: string };

type AnnotatedCodeProps = {
  fileName: string;
  lines: CodeLine[];
  callout?: { label?: string; text: string };
  codeFontSize?: number;
  noteFontSize?: number;
  animate?: boolean;
  staggerDelay?: number;
};

export const AnnotatedCode: React.FC<AnnotatedCodeProps> = ({
  fileName,
  lines,
  callout,
  codeFontSize = 26,
  noteFontSize = 21,
  animate = true,
  staggerDelay = 0.12,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div
      style={{
        flex: 1,
        display: "flex",
        flexDirection: "column",
        justifyContent: "flex-start",
        gap: spacing.element,
      }}
    >
      {/* 주석 달린 코드 블록 */}
      <div
        style={{
          backgroundColor: colors.bgDark,
          borderRadius: 16,
          overflow: "hidden",
          border: `1px solid rgba(255,255,255,0.08)`,
        }}
      >
        {/* 파일 탭 */}
        <div
          style={{
            padding: "12px 24px",
            backgroundColor: "rgba(255,255,255,0.05)",
            borderBottom: `1px solid rgba(255,255,255,0.08)`,
            fontSize: fontSize.small,
            fontFamily: "monospace",
            color: "rgba(248,250,252,0.55)",
          }}
        >
          {fileName}
        </div>

        {/* 코드 라인 + 주석 */}
        <div style={{ padding: "20px 0" }}>
          {lines.map((line, i) => {
            const delay = i * staggerDelay;
            const opacity = animate
              ? interpolate(frame, [delay * fps, (delay + 0.3) * fps], [0, 1], {
                  extrapolateLeft: "clamp",
                  extrapolateRight: "clamp",
                })
              : 1;
            return (
              <div
                key={i}
                style={{
                  opacity,
                  display: "grid",
                  gridTemplateColumns: "1.1fr 1fr",
                  alignItems: "center",
                  minHeight: 52,
                }}
              >
                <div
                  style={{
                    fontFamily: "monospace",
                    fontSize: codeFontSize,
                    color: colors.textInvert,
                    whiteSpace: "pre",
                    padding: "0 28px",
                  }}
                >
                  {line.code}
                </div>
                {line.note ? (
                  <div
                    style={{
                      fontSize: noteFontSize,
                      color: NOTE_COLOR,
                      lineHeight: 1.4,
                      padding: "0 28px",
                      borderLeft: `1px solid rgba(255,255,255,0.12)`,
                    }}
                  >
                    {line.note}
                  </div>
                ) : (
                  <div style={{ borderLeft: `1px solid rgba(255,255,255,0.12)`, height: "100%" }} />
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* 코드 밖 동작/주의 — 별도 콜아웃 */}
      {callout && (
        <div
          style={{
            backgroundColor: colors.cardBg,
            border: `1px solid ${colors.border}`,
            borderLeft: `5px solid ${colors.accent}`,
            borderRadius: 12,
            padding: "18px 26px",
          }}
        >
          <span style={{ fontSize: fontSize.caption, color: colors.text, lineHeight: 1.6 }}>
            {callout.label ? <b>{callout.label} </b> : null}
            {callout.text}
          </span>
        </div>
      )}
    </div>
  );
};
