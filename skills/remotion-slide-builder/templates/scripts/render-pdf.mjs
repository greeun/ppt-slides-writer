#!/usr/bin/env node
/**
 * Remotion 슬라이드 → PDF 변환 스크립트
 *
 * 각 슬라이드의 마지막 프레임(애니메이션 완료, 전환 직전)을 캡처하여
 * 단일 PDF로 결합합니다.
 *
 * Usage:
 *   pnpm pdf                    # 전체 프레젠테이션
 *   pnpm pdf -- --section 0     # 특정 섹션만
 *
 * {{SECTIONS}} 배열을 프로젝트에 맞게 수정하세요.
 */

import { execSync } from "child_process";
import { readFileSync, writeFileSync, mkdirSync, readdirSync, rmSync } from "fs";
import { join } from "path";
import { PDFDocument } from "pdf-lib";

const FPS = 30;
const TRANSITION_FRAMES = 15;

// {{SECTIONS}} — Composition ID와 LO index 파일 경로
const sections = [
  // { id: "0-Course-Intro", file: "src/slides/overview/Overview.tsx" },
  // { id: "1-Topic-Name", file: "src/slides/lo1-topic/LO1.tsx" },
];

// Parse CLI args
const args = process.argv.slice(2);
const sectionArgIdx = args.indexOf("--section");
const targetSection = sectionArgIdx !== -1 ? parseInt(args[sectionArgIdx + 1]) : null;
const outputName = targetSection !== null
  ? `section-${targetSection}.pdf`
  : "presentation.pdf";

/**
 * LO index 파일에서 SLIDE_DURATIONS 배열 추출
 */
function extractDurations(filePath) {
  const content = readFileSync(filePath, "utf-8");
  const match = content.match(/SLIDE_DURATIONS\s*=\s*\[([\s\S]*?)\]/);
  if (!match) throw new Error(`SLIDE_DURATIONS not found in ${filePath}`);
  return match[1]
    .split(",")
    .map((s) => s.replace(/\/\/.*$/gm, "").trim())
    .filter((s) => s.length > 0)
    .map((s) => parseInt(s));
}

/**
 * TransitionSeries 내 각 슬라이드의 캡처 프레임 계산
 *
 * 전환(15프레임)이 양쪽 슬라이드를 겹치므로:
 * - 슬라이드 i의 시작: sum(D[0..i-1]) * fps - i * TRANSITION_FRAMES
 * - 캡처 프레임: 시작 + D[i]*fps - TRANSITION_FRAMES - 1 (마지막 슬라이드는 -1만)
 */
function calculateCaptureFrames(durations) {
  const frames = [];
  let start = 0;

  for (let i = 0; i < durations.length; i++) {
    const durationFrames = durations[i] * FPS;
    const isLast = i === durations.length - 1;

    // 애니메이션 완료 + 전환 시작 직전 프레임
    const captureFrame = isLast
      ? start + durationFrames - 1
      : start + durationFrames - TRANSITION_FRAMES - 1;

    frames.push(Math.max(0, captureFrame));

    if (!isLast) {
      start = start + durationFrames - TRANSITION_FRAMES;
    }
  }

  return frames;
}

/**
 * PNG를 PDF로 결합 (1920×1080 landscape)
 */
async function combineToPdf(pngDir, outputPath) {
  const pdfDoc = await PDFDocument.create();
  const files = readdirSync(pngDir)
    .filter((f) => f.endsWith(".png"))
    .sort();

  for (const file of files) {
    const pngBytes = readFileSync(join(pngDir, file));
    const pngImage = await pdfDoc.embedPng(pngBytes);
    const pageWidth = 1920 * 0.5; // 960pt
    const pageHeight = 1080 * 0.5; // 540pt
    const page = pdfDoc.addPage([pageWidth, pageHeight]);
    page.drawImage(pngImage, {
      x: 0,
      y: 0,
      width: pageWidth,
      height: pageHeight,
    });
  }

  const pdfBytes = await pdfDoc.save();
  writeFileSync(outputPath, pdfBytes);
  return files.length;
}

// Main
async function main() {
  const tmpDir = "out/.tmp-slides";
  const outDir = "out";

  mkdirSync(tmpDir, { recursive: true });
  mkdirSync(outDir, { recursive: true });

  const targetSections = targetSection !== null
    ? sections.filter((_, i) => i === targetSection)
    : sections;

  if (targetSections.length === 0) {
    console.error(`Section ${targetSection} not found (0-${sections.length - 1})`);
    process.exit(1);
  }

  let globalSlideIdx = 0;
  let totalSlides = 0;

  for (const section of targetSections) {
    const durations = extractDurations(section.file);
    totalSlides += durations.length;
  }

  console.log(`\n📄 Rendering ${totalSlides} slides to PDF...\n`);

  for (const section of targetSections) {
    const durations = extractDurations(section.file);
    const captureFrames = calculateCaptureFrames(durations);

    for (let i = 0; i < captureFrames.length; i++) {
      const frame = captureFrames[i];
      const outFile = join(tmpDir, `slide-${String(globalSlideIdx).padStart(3, "0")}.png`);
      globalSlideIdx++;

      const progress = `[${globalSlideIdx}/${totalSlides}]`;
      console.log(`${progress} ${section.id} slide ${i + 1}/${durations.length} @ frame ${frame}`);

      execSync(
        `npx remotion still "${section.id}" --frame=${frame} --output="${outFile}" --log=error`,
        { stdio: "inherit" }
      );
    }
  }

  const outputPath = join(outDir, outputName);
  console.log(`\n📑 Combining ${globalSlideIdx} slides into PDF...`);
  const pageCount = await combineToPdf(tmpDir, outputPath);
  console.log(`\n✅ ${outputPath} (${pageCount} pages)\n`);

  rmSync(tmpDir, { recursive: true });
}

main().catch((err) => {
  console.error("Error:", err.message);
  process.exit(1);
});
