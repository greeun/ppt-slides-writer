/**
 * InstructorSlide — 공용 강사 소개 컴포넌트
 *
 * 모든 교육 Remotion 프로젝트에서 재사용합니다.
 * 새 프로젝트 생성 시 이 파일을 src/components/에 복사하세요.
 */
import React from "react";
import { SlideLayout } from "./SlideLayout";
import { AnimatedList } from "./AnimatedList";
import { ConceptCard } from "./ConceptCard";
import { colors, fontSize, spacing } from "../theme";

interface InstructorSlideProps {
  sectionLabel?: string;
  pageNumber?: number;
  totalPages?: number;
}

export const InstructorSlide: React.FC<InstructorSlideProps> = ({
  sectionLabel = "OVERVIEW",
  pageNumber,
  totalPages,
}) => {
  return (
    <SlideLayout
      title="강사 소개: 홍길동"
      subtitle="교육 사업부"
      sectionLabel={sectionLabel}
      pageNumber={pageNumber}
      totalPages={totalPages}
    >
      <div style={{ display: "flex", gap: spacing.section, flex: 1 }}>
        <div style={{ flex: 1 }}>
          <ConceptCard
            items={[
              {
                icon: "AI",
                title: "AI Engineering",
                description:
                  "LLM 애플리케이션, RAG 시스템, Agentic AI 설계",
                color: colors.primary,
              },
              {
                icon: "Dev",
                title: "Software Engineering",
                description:
                  "스펙 주도 개발(SDD), DevOps, 클라우드 인프라",
                color: colors.secondary,
              },
            ]}
            startFrom={0.3}
            columns={2}
          />
        </div>

        <div style={{ flex: 1 }}>
          <div
            style={{
              fontSize: fontSize.h3,
              fontWeight: 700,
              color: colors.text,
              marginBottom: spacing.element,
            }}
          >
            주요 교육 과정
          </div>
          <AnimatedList
            items={[
              "AI 기반 SW 개발 방법론",
              "Agentic AI 시스템 구축",
              "RAG 애플리케이션 개발",
              "생성형 AI 비즈니스 활용",
              "Docker / Kubernetes / CI/CD",
            ]}
            startFrom={0.5}
          />
        </div>
      </div>
    </SlideLayout>
  );
};
