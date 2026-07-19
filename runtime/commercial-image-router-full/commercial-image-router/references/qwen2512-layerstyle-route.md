# AI图片制作：Qwen-Image-2512 + LayerStyle 跑通链路

更新时间：2026-07-19

## 验收结论

本机已跑通一条不依赖 OpenAI/Gemini API 的高质量本地路线：

```text
Qwen-Image-2512 本地模型生成无文字主视觉
→ 可靠中文标题透明层
→ ComfyUI_LayerStyle 做描边/阴影/金属感字效
→ ComfyUI ImageColorToMask/InvertMask/ImageCompositeMasked 合成
→ 视觉验收
```

阶段性验收图：

```text
${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/qwen2512-layerstyle/composite_outputs/ai_image_creation_qwen_layerstyle_poc_00004_.png
```

视觉验收：

- 背景来自 Qwen-Image-2512 本地模型，不是 SDXL/SD1.5；
- 无文字主视觉质量明显高于前面临时样张；
- 中文标题完整，无乱码；
- 标题有 LayerStyle 节点生成的描边/阴影/金属感；
- ComfyUI 合成节点已修正黑底问题；
- 适合作为 Skill 跑通链路的阶段性证明，但不是最终模板库效果上限。

## 已安装模型

```text
models/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors      8.8G
models/vae/qwen_image_vae.safetensors                           243M
models/diffusion_models/qwen_image_2512_fp8_e4m3fn.safetensors  20G
models/loras/Qwen-Image-2512-Lightning-4steps-V1.0-fp32.safetensors 1.6G
```

HuggingFace 直连会 `Connection reset by peer`，已改用：

```text
https://hf-mirror.com
```

## 已跑通 API workflow

### 1. Qwen-Image-2512 文生图

```text
${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/qwen2512-layerstyle/qwen2512_t2i_api.json
```

关键节点：

- `UNETLoader`
- `CLIPLoader(type=qwen_image)`
- `VAELoader`
- `LoraLoaderModelOnly`
- `ModelSamplingAuraFlow(shift=3.1)`
- `EmptySD3LatentImage`
- `KSampler(euler/simple, steps=4, cfg=1.0)`
- `VAEDecode`
- `SaveImage`

### 2. LayerStyle 中文标题字效

```text
${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/qwen2512-layerstyle/layerstyle_svgtext_api.json
```

关键原则：

- 不能直接依赖 `LayerUtility: TextImage` 排中文，第一次实测中文/位置不稳定；
- 先用可靠中文透明文字层，再交给 LayerStyle 节点做效果；
- LayerStyle 输出默认会变成黑底 RGB，不能直接当透明图层使用。

### 3. Qwen 背景 + LayerStyle 标题合成

```text
${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/qwen2512-layerstyle/qwen_layerstyle_composite_api.json
```

最终修正链路：

```text
LoadImage(qwen_bg)
LoadImage(layerstyle_title)
ImageColorToMask(layerstyle_title, color=black)
InvertMask
ImageCompositeMasked(destination=qwen_bg, source=layerstyle_title, mask=non_black_title_mask)
SaveImage
```

注意：

- `LayerUtility: ImageBlend` 实测会导致只剩黑底标题，不适合这条链路；
- 直接用标题图自带 alpha mask 也不可靠，因为 LayerStyle Save 后 alpha 不保留；
- 必须用 `ImageColorToMask(black) → InvertMask` 从标题图反推出文字区域 mask。

## 下一步模板化

这条链路应被固化为 Skill 的标准 route：

```text
route: qwen2512_poster_visual_with_layerstyle_title
适用：创意图、宣传图、海报主视觉、封面图
不适用：商品保真改图、已有图片局部改字
```

后续要做：

1. 把 `${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}` 绝对路径改为安装包相对路径/环境变量；
2. 把标题位置、字号、字效参数模板化；
3. 支持多尺寸：1:1、4:5、3:4、16:9；
4. 接入商品图 route：product placement / product scene relight / segmentation；
5. 接入图片编辑 route：Qwen-Image-Edit / FLUX Kontext / GPT/Gemini API（有凭证时）。
