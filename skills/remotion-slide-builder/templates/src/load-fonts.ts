import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

const fonts = [
  { weight: "400" as const, file: "Pretendard-Regular.woff2" },
  { weight: "500" as const, file: "Pretendard-Medium.woff2" },
  { weight: "600" as const, file: "Pretendard-SemiBold.woff2" },
  { weight: "700" as const, file: "Pretendard-Bold.woff2" },
  { weight: "800" as const, file: "Pretendard-ExtraBold.woff2" },
];

for (const f of fonts) {
  loadFont({
    family: "Pretendard",
    url: staticFile(`fonts/${f.file}`),
    weight: f.weight,
  }).catch(() => {
    // Font loading may fail during initial build, will retry on render
  });
}
