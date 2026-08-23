/**
 * 콘텐츠 슬라이드 패턴 — 일반적인 개념 설명 슬라이드
 *
 * 파일명: S02_TopicName.tsx (S + 2자리 순번 + _ + PascalCase 주제명)
 * 규칙:
 *   - SlideLayout 필수 (title, sectionLabel, pageNumber, totalPages)
 *   - 애니메이션: useCurrentFrame() + interpolate() 만 사용
 *   - 등장: opacity 0→1 + translateY 20→0, 0.3~0.5초
 *   - 순차 등장: AnimatedList의 staggerDelay 또는 수동 0.15초 간격
 */
import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { SlideLayout } from "../../components/SlideLayout";
import { AnimatedList } from "../../components/AnimatedList";
import { ConceptCard } from "../../components/ConceptCard";
import { colors, fontSize, spacing } from "../../theme";

export const S02_TopicName: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 우측 패널 등장 애니메이션
  const rightOpacity = interpolate(
    frame,
    [0.6 * fps, 0.9 * fps],
    [0, 1],
    { extrapolateRight: "clamp", extrapolateLeft: "clamp" }
  );

  return (
    <SlideLayout
      title="슬라이드 제목"
      subtitle="핵심 메시지를 한 줄로 요약합니다"
      sectionLabel="LO1 · 주제명"
      pageNumber={1}
      totalPages={7}
    >
      <div style={{ display: "flex", gap: spacing.section, flex: 1 }}>
        {/* 좌측: 리스트 */}
        <div style={{ flex: 1 }}>
          <div
            style={{
              fontSize: fontSize.h3,
              fontWeight: 700,
              color: colors.text,
              marginBottom: spacing.element,
            }}
          >
            소주제
          </div>
          <AnimatedList
            items={[
              "첫 번째 포인트를 설명합니다",
              "두 번째 포인트를 설명합니다",
              "세 번째 포인트를 설명합니다",
            ]}
            startFrom={0.3}
          />
        </div>

        {/* 우측: 시각적 요소 (카드, 다이어그램 등) */}
        <div style={{ flex: 1, opacity: rightOpacity }}>
          <ConceptCard
            items={[
              {
                icon: "🔧",
                title: "개념 A",
                description: "개념 A에 대한 설명입니다",
                color: colors.primary,
              },
              {
                icon: "📊",
                title: "개념 B",
                description: "개념 B에 대한 설명입니다",
                color: colors.secondary,
              },
            ]}
            startFrom={0.8}
            columns={1}
          />
        </div>
      </div>
    </SlideLayout>
  );
};
