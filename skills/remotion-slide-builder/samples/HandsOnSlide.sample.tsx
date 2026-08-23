/**
 * HandsOnSlide 패턴 — 실습 안내용 독립(다크) 슬라이드
 *
 * 파일명: S0x_TopicName.tsx (S + 2자리 순번 + _ + PascalCase 주제명)
 * 용도:
 *   - 실습 블록 진입 슬라이드. "해볼 것 / 명령어 / 관찰 포인트 / 강사 메모"를 한 화면에 구성
 *   - SlideLayout을 쓰지 않고 AbsoluteFill 기반으로 화면을 꽉 채우는 독립 슬라이드입니다
 *   - 페이지 번호는 내부에서 PageNumber로 직접 렌더링합니다
 * 규칙:
 *   - blockNumber로 실습 블록 순번을 강조합니다(BLOCK n 배지)
 *   - command는 선택값. 없으면 코드 박스를 건너뜁니다
 *   - storyNote에는 강사가 강조할 한 줄 메시지를 적습니다
 */
import React from "react";
import { HandsOnSlide } from "../../components/HandsOnSlide";

export const S05_HandsOn: React.FC = () => {
  return (
    <HandsOnSlide
      sectionLabel="LO3 · 실습"
      blockNumber={4}
      title="첫 엔드포인트 호출하기"
      instruction="개발 서버를 띄우고 /chat 엔드포인트에 메시지를 보내 응답을 확인합니다"
      command={`curl -X POST localhost:8000/chat -d '{"message":"안녕"}'`}
      expectation="응답 JSON의 reply 필드에 모델이 생성한 답변이 담겨 옵니다"
      storyNote="여기서 막히면 서버 로그의 포트와 CORS 설정을 먼저 확인하세요"
      pageNumber={5}
      totalPages={9}
    />
  );
};
