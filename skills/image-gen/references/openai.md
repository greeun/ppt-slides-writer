# OpenAI 이미지 생성 — 모델별 상세

`gpt-image` 시리즈는 OpenAI의 이미지 생성 모델 라인업이다. 2026년 출시된 `gpt-image-2`가 한국어 텍스트 렌더링과 인포그래픽 정확성에서 SOTA로 평가되며, 이 스킬에서 인포그래픽/슬라이드 용도의 1순위 모델이다.

> 가격 출처: OpenAI 공식 image-generation guide (`developers.openai.com/api/docs/guides/image-generation`) 및 pricing 페이지 (`developers.openai.com/api/docs/pricing`), 2026-08-17 확인.

## 모델 라인업 (2026-08 기준)

| 단축키 | model_id | 출시 | 핵심 강점 |
|--------|----------|------|-----------|
| `gpt2` | `gpt-image-2` | 2026 | 다국어 텍스트 95~99%, 인포그래픽/슬라이드/지도/만화, 멀티턴 편집, reference image, transparency |
| `gpt2-mini` | `gpt-image-1-mini` | 2025 | 비용 최저, 같은 멀티모달 입출력 |
| `gpt1.5` | `gpt-image-1.5` | 2025 후반 | 직전 플래그십, LM Arena Elo 1264 |
| `dalle3` | `dall-e-3` | 2023 | 구세대 (사실상 deprecated) |

> Batch API 사용 시 모든 모델 50% 할인.

## 정확한 per-image 가격 (USD, 2026-08)

### gpt-image-2 (`gpt2`)

| Quality | 1024×1024 | 1024×1536 (portrait) | 1536×1024 (landscape) |
|---------|-----------|----------------------|------------------------|
| low     | $0.006    | $0.005               | $0.005                 |
| medium  | $0.053    | $0.041               | $0.041                 |
| **high**| **$0.211**| **$0.165**           | **$0.165**             |

> 16:9 슬라이드(1536×1024) high가 정사각(1024²)보다 싸다는 점 주목 — 슬라이드 용도가 비용·품질 양쪽으로 유리.

### gpt-image-1-mini (`gpt2-mini`)

| Quality | 1024×1024 | 1024×1536 | 1536×1024 |
|---------|-----------|-----------|-----------|
| low     | $0.005    | $0.006    | $0.006    |
| medium  | $0.011    | $0.015    | $0.015    |
| **high**| **$0.036**| **$0.052**| **$0.052**|

### gpt-image-1.5 (`gpt1.5`)

| Quality | 1024×1024 | 1024×1536 | 1536×1024 |
|---------|-----------|-----------|-----------|
| low     | $0.009    | $0.013    | $0.013    |
| medium  | $0.034    | $0.050    | $0.050    |
| high    | $0.133    | $0.200    | $0.200    |

> gpt-image-1.5는 정사각(1024²)이 16:9보다 싸다 — gpt2와 반대 패턴. 1.5는 1024²만 강점.

### Token 기반 가격 (정확값, 1M tokens 기준)

| 모델 | text input | cached input | image input | output image |
|------|-----------|--------------|-------------|--------------|
| gpt-image-2 | $5.00 | $1.25 | $8.00 | $30.00 |
| gpt-image-1.5 | $5.00 | $1.25 | $8.00 | $32.00 |
| gpt-image-1-mini | $2.00 | $0.20 | $2.50 | $8.00 |

OpenAI는 image generation cost calculator를 image-generation guide에 제공한다. 위 per-image 표가 가장 명확한 기준.

### dall-e-3, gpt-image-1

OpenAI 신규 가격 페이지에서 deprecated 처리되었다. 신규 프로젝트 사용 비권장.

## API 기본 동작

- 엔드포인트: `POST https://api.openai.com/v1/images/generations`
- 인증: `Authorization: Bearer $OPENAI_API_KEY`
- 응답: `gpt-image` 시리즈는 항상 `b64_json` 반환 (URL 아님). `dall-e-3`만 URL 기본.

```python
from openai import OpenAI
client = OpenAI()

resp = client.images.generate(
    model="gpt-image-2",
    prompt="...",
    size="1536x1024",
    quality="high",
    output_format="png",
    n=1,
)
# resp.data[0].b64_json  → base64 디코드 후 저장
```

이 스킬은 SDK 의존을 피하기 위해 `urllib`로 직접 호출한다.

## 핵심 파라미터

### size

- `gpt-image-2`: **flex 지원**, 8의 배수 폭/높이로 임의 지정 가능 (최대 2048px). 다만 표준 사이즈에서 가장 잘 작동한다. 2560×1440 초과는 실험적.
- `gpt-image-1-mini`: **1024×1024 / 1024×1536 / 1536×1024 3종만 허용**. 이 외 사이즈는 거부된다.
- `dall-e-3`: 1024×1024 / 1792×1024 / 1024×1792 3종.

`generate.py`의 `aspect_to_openai_size()`가 비율과 해상도를 자동 매핑한다. 강제 지정은 `--size 1536x1024`.

### quality

`low` / `medium` / `high` / `auto` (gpt-image 시리즈 전용). 가격은 quality에 비례.

- low: 빠르고 싸지만 텍스트 정확도 떨어짐
- medium: 일반 일러스트 적합
- **high (기본)**: 인포그래픽/슬라이드용 권장
- auto: 모델이 프롬프트 복잡도 보고 자동 선택

### output_format

`png` / `jpeg` / `webp`. 투명 배경이 필요하면 `png` 또는 `webp` + `--background transparent`.

### background

`transparent` / `opaque` / `auto`. 슬라이드 위에 얹을 아이콘/일러스트는 `transparent`.

## 멀티턴 편집 (참고)

본 스킬은 단일 호출만 지원하지만, gpt-image-2의 강력한 기능 중 하나는 **멀티턴 편집**이다.
같은 캐릭터/스타일을 유지하며 점진적으로 수정할 때 `client.images.edit(image=..., prompt=...)`를 사용하면 일관성이 유지된다.

스트리밍 partial image는 partial당 100 tokens 추가 비용이 발생한다.

## Gemini 대비 강점

| 항목 | gpt-image-2 강점 |
|------|-----------------|
| 한글/CJK 텍스트 | 작은 폰트, 곡면, 밀집 레이아웃에서도 95~99% 정확 |
| 정형 다이어그램 | 워크플로우, 박스 다이어그램, 지도, 슬라이드 레이아웃 표준화 |
| 멀티턴 일관성 | 동일 캐릭터, 동일 스타일 유지 우수 |
| transparency | 투명 PNG 네이티브 지원 |

## Gemini가 나은 경우

| 상황 | 이유 |
|------|------|
| 사진풍 인물·풍경 | 나노바나나(네이티브 이미지 생성) 계열이 자연스러움 (Imagen 4 계열은 2026-08-17 서비스 종료) |
| 일러스트풍 배경 | 더 부드러운 색상, 빠른 추론 |
| 비용 우선 대량 생성 (정사각) | Gemini 2.5 $0.039 (해상도 무관) |
| 21:9 등 극단 비율 | Gemini는 비율 네이티브 지원(3.1 계열 10종, 2.5 레거시 14종), OpenAI는 flex로 근사 |

## Gemini 정확 가격 (2026-08, 비교용)

| 모델 | 해상도 | 표준 | Batch |
|------|--------|------|-------|
| gemini-2.5-flash-image | ≤1024² | $0.039 | $0.0195 |
| gemini-3.1-flash-image | 512px | $0.045 | $0.022 |
| gemini-3.1-flash-image | 1K | $0.067 | $0.034 |
| gemini-3.1-flash-image | 2K | $0.101 | $0.050 |
| gemini-3.1-flash-image | 4K | $0.151 | $0.076 |
| gemini-3-pro-image | 1K~2K | $0.134 | $0.067 |
| gemini-3-pro-image | 4K | $0.240 | $0.120 |

> Imagen 4 계열(imagen-4.0-*)은 2026-08-17 서비스 종료되어 표에서 제외.

## 비용 시나리오 — 슬라이드 1세트(10장, 1536×1024)

| 전략 | 비용 |
|------|------|
| Gemini 3.1 1K 일괄 | 10 × $0.067 = **$0.67** |
| Gemini 2.5 일괄 (정사각만 가능) | 10 × $0.039 = **$0.39** |
| gpt-image-1-mini high 일괄 | 10 × $0.052 = **$0.52** |
| gpt-image-2 high 일괄 | 10 × $0.165 = **$1.65** |
| 혼합 (핵심 2장 gpt2 + 8장 mini high) | 2×$0.165 + 8×$0.052 = **$0.75** |
| 혼합 (핵심 2장 gpt2 + 8장 Gemini 3.1) | 2×$0.165 + 8×$0.067 = **$0.87** |

**권장**: 한글이 들어가는 핵심 슬라이드 표지·인포그래픽은 gpt2 high(16:9), 보조 이미지는 gpt2-mini high 또는 Gemini 3.1.

## 트러블슈팅

| 에러 | 원인 | 해결 |
|------|------|------|
| 400 invalid size | mini에 비표준 사이즈 전달 | `gpt2-mini`는 1024×1024/1024×1536/1536×1024만 사용 |
| 400 too large | 2560×1440 초과 | 사이즈를 표준 범위로 |
| 401 unauthorized | `OPENAI_API_KEY` 미설정 또는 만료 | 환경변수 확인, 키 재발급 |
| 429 rate limit | 분당 요청 한도 초과 | 백오프 대기 또는 Tier 상향 |
| 콘텐츠 거부 | safety filter | 프롬프트에서 인물 묘사·민감 표현 완화 |

## 참고

- 가격: https://openai.com/api/pricing/ , https://developers.openai.com/api/docs/pricing
- 이미지 가이드 (per-image 표 출처): https://developers.openai.com/api/docs/guides/image-generation
- 모델 카드: https://developers.openai.com/api/docs/models/gpt-image-2
- Cookbook: https://cookbook.openai.com/examples/generate_images_with_gpt_image
- Gemini 가격: https://ai.google.dev/gemini-api/docs/pricing
