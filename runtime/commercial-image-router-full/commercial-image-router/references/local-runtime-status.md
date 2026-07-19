# AI图片制作：当前本机高质量能力验收记录

更新时间：2026-07-19

## 已确认安装/可用

### 1. ComfyUI 服务

- 地址：`http://127.0.0.1:8188`
- 状态：已启动并可访问 `/system_stats` / `/object_info`
- ComfyUI：`0.28.0`
- 模板库：`comfyui-workflow-templates 0.11.11`
- GPU：ComfyUI 识别到 NVIDIA GeForce RTX 5090 × 2

### 2. ComfyUI_LayerStyle

已安装并成功加载到 ComfyUI object_info。

已确认节点包括：

- `LayerStyle: GradientOverlay`
- `LayerStyle: Stroke`
- `LayerStyle: DropShadow`
- `LayerStyle: OuterGlow`
- `LayerUtility: ColorImage`
- `LoadImage`
- `SaveImage`

### 3. 文字效果链路实跑结果

已实跑：

```text
可靠中文透明文字层 → LoadImage → LayerStyle GradientOverlay/Stroke/DropShadow/OuterGlow → SaveImage
```

输出：

```text
${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/qwen2512-layerstyle/layerstyle_svgtext_outputs/ai_image_creation_layerstyle_svgtext_00002_.png
```

视觉检查结果：

- 中文“AI图片制作”完整；
- 无乱码；
- 无裁切；
- 已有描边、阴影、金属/立体层；
- 仍只是文字效果链路验证，不是完整海报成品；
- 后续必须和成熟视觉模板/模型图结合，不能单独当成最终效果。

### 4. 官方 ComfyUI 模板库

已确认当前环境自带 179 个与 AI 图片制作相关的官方模板候选，包括：

- Qwen Image / Qwen Image Edit / Qwen Image 2512
- FLUX / FLUX Kontext / FLUX 2
- OpenAI GPT Image 2 / GPT Image 1
- Google Gemini / Nano Banana
- ByteDance Seedream
- Ideogram
- Recraft
- Product placement
- Product ad
- Product scene relight
- Product swap
- Image fix / product upscale

## 外部 API 型模板

这些效果上限接近 GPT/Gemini，但需要对应凭证：

- `api_openai_gpt_image_2_t2i.json`
- `api_openai_gpt_image_2_image_edit.json`
- `api_google_nano_banana2_text_to_image.json`
- `api_google_nano_banana2_image_edit.json`
- `templates-product_ad-v2.0.json`（Gemini）
- `templates-product_scene_relight.json`（Seedream）
- `api_recraft_v4_t2i.json`
- `api_ideogram_v4_t2i.json`

若没有这些 API 凭证，不要假装能跑。必须走本地模型路线。

## 本地模型路线

优先安装并测试：

### Qwen-Image-2512

下载中/待完成：

- `models/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors`
- `models/vae/qwen_image_vae.safetensors`
- `models/diffusion_models/qwen_image_2512_fp8_e4m3fn.safetensors`
- `models/loras/Qwen-Image-2512-Lightning-4steps-V1.0-fp32.safetensors`

目标：先跑通本地中文图像生成，再尝试和 LayerStyle 文字效果合成。

## Skill 执行规则更新

1. 用户说“效果不好 / 对标 GPT/Gemini / 找火的 / 找点赞高的”，不得继续本地手搓样张。
2. 优先使用官方模板库、Qwen/FLUX/Seedream/Gemini/GPT Image/Recraft/Ideogram 等成熟路线。
3. 没有 API 凭证时，明确说明外部 API 型模板不可跑，改用本地模型型模板。
4. 中文标题最终不得依赖扩散模型直接生成，应走可靠中文字体透明图层 + LayerStyle/Figma/SVG/Satori 的确定性排版。
5. 单独字效图不等于最终成品；必须和主视觉/商品/背景/版式一起验收。
