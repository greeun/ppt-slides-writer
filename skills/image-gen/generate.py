#!/usr/bin/env python3
"""이미지 생성 스크립트 — image-gen 스킬용 (Gemini + OpenAI 듀얼 프로바이더)"""

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Optional

# 모델 단축키 → (provider, model_id) 매핑
MODELS = {
    # Gemini
    "2.5": ("gemini", "gemini-2.5-flash-image"),
    "3.1": ("gemini", "gemini-3.1-flash-image"),
    "lite": ("gemini", "gemini-3.1-flash-lite-image"),
    "pro": ("gemini", "gemini-3-pro-image"),
    # OpenAI gpt-image 시리즈 (2026-08 기준)
    "gpt2": ("openai", "gpt-image-2"),           # 최신 플래그십 (한글 95%+)
    "gpt2-mini": ("openai", "gpt-image-1-mini"), # 비용 최저
    "gpt1.5": ("openai", "gpt-image-1.5"),       # 직전 플래그십
    "dalle3": ("openai", "dall-e-3"),            # 구세대 (비권장)
}

# 모델별 가격 참고 (장당, 2026-08 공식 출처 확인값)
# Gemini 2.5: $0.039 (≤1024²) / Batch $0.0195
# Gemini 3.1: 512px $0.045 / 1K $0.067 / 2K $0.101 / 4K $0.151
# Gemini 3.1 Lite: 1K $0.0336 / Batch $0.0168
# Gemini 3 Pro: 1K~2K $0.134 / 4K $0.240
# gpt-image-2 high: 1024² $0.211 / 1024×1536 $0.165 / 1536×1024 $0.165
# gpt-image-2 medium: 1024² $0.053 / 1024×1536 $0.041 / 1536×1024 $0.041
# gpt-image-2 low: 1024² $0.006 / 1024×1536 $0.005 / 1536×1024 $0.005
# gpt-image-1-mini high: 1024² $0.036 / 1024×1536 $0.052 / 1536×1024 $0.052
# gpt-image-1-mini medium: 1024² $0.011 / 1024×1536 $0.015 / 1536×1024 $0.015
# gpt-image-1-mini low: 1024² $0.005 / 1024×1536 $0.006 / 1536×1024 $0.006
# gpt-image-1.5 high: 1024² $0.133 / 1024×1536 $0.200 / 1536×1024 $0.200
# Batch API: 모든 모델 50% 할인

VALID_GEMINI_RATIOS = [
    "1:1", "1:4", "1:8", "2:3", "3:2", "3:4", "4:1",
    "4:3", "4:5", "5:4", "8:1", "9:16", "16:9", "21:9",
]

# OpenAI gpt-image 시리즈는 size를 직접 지정한다.
# 비율+해상도를 size 픽셀값으로 매핑한다. gpt-image-2는 flex 지원.
# gpt-image-1-mini는 1024x1024, 1024x1536, 1536x1024만 허용한다.
def aspect_to_openai_size(aspect: str, resolution: str, model_id: str) -> str:
    """비율+해상도를 OpenAI size 문자열로 매핑. 모델별 제한을 적용한다."""

    # 1024x1024, 1024x1536, 1536x1024만 지원하는 mini 모델
    is_restricted = "mini" in model_id

    base_map = {"512px": 512, "1K": 1024, "2K": 2048}
    base = base_map.get(resolution, 1024)

    try:
        w_ratio, h_ratio = (int(x) for x in aspect.split(":"))
    except ValueError:
        return "1024x1024"

    # 긴 변을 base에 맞춤
    if w_ratio >= h_ratio:
        w = base
        h = int(round(base * h_ratio / w_ratio))
    else:
        h = base
        w = int(round(base * w_ratio / h_ratio))

    # 16의 배수로 정렬 (gpt-image-2 요구사항: width/height must be divisible by 16)
    # 반올림으로 가장 가까운 16배수에 맞춤 (실제 비율과의 오차 최소화)
    w = max(16, int(round(w / 16)) * 16)
    h = max(16, int(round(h / 16)) * 16)

    if is_restricted:
        # mini는 1024 기준 3종만 허용. 가장 가까운 것으로 폴백.
        if w == h:
            return "1024x1024"
        return "1536x1024" if w > h else "1024x1536"

    return f"{w}x{h}"


def write_sidecar(output: str, model_id: str, meta_line: str, prompt: str) -> None:
    """이미지 옆에 .prompt.md 사이드카 파일을 작성한다."""
    prompt_path = os.path.splitext(output)[0] + ".prompt.md"
    with open(prompt_path, "w", encoding="utf-8") as pf:
        pf.write(f"<!-- model: {model_id} | {meta_line} -->\n\n")
        pf.write(prompt)
        pf.write("\n")


def generate_gemini(api_key: str, model_id: str, prompt: str, output: str,
                    aspect: str, resolution: str) -> None:
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model_id}:generateContent?key={api_key}"
    )
    config = {
        "responseModalities": ["TEXT", "IMAGE"],
        "imageConfig": {
            "aspectRatio": aspect,
            "imageSize": resolution,
        },
    }
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": config,
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=180) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    for candidate in result.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            if "inlineData" in part:
                img_data = base64.b64decode(part["inlineData"]["data"])
                os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
                with open(output, "wb") as f:
                    f.write(img_data)
                size_kb = len(img_data) / 1024
                write_sidecar(output, model_id, f"{aspect} {resolution}", prompt)
                print(f"OK: {output} ({size_kb:.0f}KB)")
                return
            elif "text" in part:
                print(f"TEXT: {part['text'][:200]}", file=sys.stderr)

    print("ERROR: No image in Gemini response", file=sys.stderr)
    print(json.dumps(result, indent=2, ensure_ascii=False)[:500], file=sys.stderr)
    sys.exit(1)


def generate_openai(api_key: str, model_id: str, prompt: str, output: str,
                    size: str, quality: str, output_format: str,
                    background: Optional[str]) -> None:
    url = "https://api.openai.com/v1/images/generations"

    payload = {
        "model": model_id,
        "prompt": prompt,
        "size": size,
        "quality": quality,
        "n": 1,
    }
    # gpt-image 시리즈는 b64_json만 반환. dall-e-3는 url 기본이지만 통일.
    if not model_id.startswith("dall-e"):
        payload["output_format"] = output_format
        if background:
            payload["background"] = background

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"ERROR: OpenAI API {e.code}: {body[:500]}", file=sys.stderr)
        sys.exit(1)

    data = result.get("data", [])
    if not data:
        print("ERROR: No image in OpenAI response", file=sys.stderr)
        print(json.dumps(result, indent=2, ensure_ascii=False)[:500], file=sys.stderr)
        sys.exit(1)

    item = data[0]
    if "b64_json" in item:
        img_data = base64.b64decode(item["b64_json"])
    elif "url" in item:
        with urllib.request.urlopen(item["url"], timeout=60) as r:
            img_data = r.read()
    else:
        print("ERROR: OpenAI response has neither b64_json nor url", file=sys.stderr)
        sys.exit(1)

    os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
    with open(output, "wb") as f:
        f.write(img_data)
    size_kb = len(img_data) / 1024
    write_sidecar(output, model_id, f"{size} {quality}/{output_format}", prompt)
    print(f"OK: {output} ({size_kb:.0f}KB)")


def main():
    parser = argparse.ArgumentParser(
        description="이미지 생성 스킬 — Gemini와 OpenAI 듀얼 프로바이더"
    )
    parser.add_argument("--prompt", required=True, help="이미지 생성 프롬프트")
    parser.add_argument("--output", required=True, help="출력 파일 경로 (.png 등)")
    parser.add_argument(
        "--model",
        choices=list(MODELS.keys()) + ["web"],
        default="3.1",
        help=(
            "모델 단축키. Gemini: 2.5/3.1/lite/pro, "
            "OpenAI: gpt2(=gpt-image-2)/gpt2-mini/gpt1.5/dalle3, "
            "또는 web(프롬프트만 출력)"
        ),
    )
    parser.add_argument(
        "--provider",
        choices=["gemini", "openai", "auto"],
        default="auto",
        help="프로바이더 강제 지정. 기본은 모델로부터 자동 추론.",
    )
    parser.add_argument("--model-id", help="모델 ID 직접 지정 (--model 무시, --provider 필수)")
    parser.add_argument(
        "--aspect-ratio",
        default="16:9",
        help=f"비율 (기본: 16:9). Gemini 지원: {', '.join(VALID_GEMINI_RATIOS)}",
    )
    parser.add_argument(
        "--resolution",
        default="1K",
        help="해상도: 512px/1K/2K/4K (기본: 1K). Gemini는 imageSize, OpenAI는 size 매핑에 사용.",
    )
    # OpenAI 전용
    parser.add_argument(
        "--quality",
        choices=["low", "medium", "high", "auto"],
        default="high",
        help="(OpenAI 전용) 품질 (기본: high)",
    )
    parser.add_argument(
        "--output-format",
        choices=["png", "jpeg", "webp"],
        default="png",
        help="(OpenAI gpt-image 전용) 출력 포맷 (기본: png)",
    )
    parser.add_argument(
        "--background",
        choices=["transparent", "opaque", "auto"],
        help="(OpenAI gpt-image 전용) 배경 — 투명 PNG가 필요할 때 transparent",
    )
    parser.add_argument(
        "--size",
        help="(OpenAI 전용) size 직접 지정 (예: 1536x1024). 지정 시 --aspect-ratio/--resolution 무시.",
    )
    args = parser.parse_args()

    # web 모드는 프로바이더 무관. 프롬프트만 출력.
    if args.model == "web":
        print("=== 아래 프롬프트를 웹 Gemini/ChatGPT에 붙여넣기 ===\n")
        print(args.prompt)
        print("\n=== 생성 후 이미지를 다음 경로에 저장 ===")
        print(f"  {args.output}")
        return

    # 프로바이더와 모델 ID 결정
    if args.model_id:
        if args.provider == "auto":
            print("ERROR: --model-id 사용 시 --provider 명시 필요", file=sys.stderr)
            sys.exit(1)
        provider = args.provider
        model_id = args.model_id
    else:
        provider, model_id = MODELS[args.model]
        if args.provider != "auto" and args.provider != provider:
            print(
                f"ERROR: --provider {args.provider}와 모델 {args.model}({provider})가 불일치",
                file=sys.stderr,
            )
            sys.exit(1)

    if provider == "gemini":
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("ERROR: GEMINI_API_KEY 환경변수가 설정되지 않았습니다.", file=sys.stderr)
            sys.exit(1)
        if args.aspect_ratio not in VALID_GEMINI_RATIOS:
            print(f"ERROR: Gemini 지원하지 않는 비율 '{args.aspect_ratio}'", file=sys.stderr)
            print(f"  지원 비율: {', '.join(VALID_GEMINI_RATIOS)}", file=sys.stderr)
            sys.exit(1)
        print(f"Provider: gemini | Model: {model_id} | {args.aspect_ratio} {args.resolution}")
        generate_gemini(
            api_key, model_id, args.prompt, args.output,
            args.aspect_ratio, args.resolution,
        )
        return

    if provider == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("ERROR: OPENAI_API_KEY 환경변수가 설정되지 않았습니다.", file=sys.stderr)
            sys.exit(1)
        size = args.size or aspect_to_openai_size(args.aspect_ratio, args.resolution, model_id)
        print(
            f"Provider: openai | Model: {model_id} | size={size} "
            f"quality={args.quality} format={args.output_format}"
        )
        generate_openai(
            api_key, model_id, args.prompt, args.output,
            size, args.quality, args.output_format, args.background,
        )
        return

    print(f"ERROR: 알 수 없는 provider '{provider}'", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
