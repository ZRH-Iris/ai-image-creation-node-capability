# AI图片制作：高质量模型与现成工作流优先栈

本参考用于避免继续“本地手搓低质样张”。当用户要求高质量 AI 图片制作、生成图片、修改图片、商品图、宣传图、海报、图片改字或对标 GPT/Gemini 生图效果时，优先寻找并使用现成高质量模型、工作流和模板，不要从零手写粗糙样式。

## 核心结论

高质量 AI 图片制作不是“换一个字体”或“手写几个 SVG 效果”。应按以下顺序处理：

1. 先选强模型/现成工作流生成或编辑画面；
2. 再用专业排版/LayerStyle/模板系统处理文字和标题字效；
3. 商品图必须保留真实商品或用专门 product-preservation workflow；
4. 最后做放大、修复、视觉 QA；
5. 如果效果像技术 demo、粗糙海报、普通黑体模板，不得称为通过。

## 对标 GPT/Gemini 的开源/开放权重模型优先级

### 1. Qwen-Image / Qwen-Image-Edit / Qwen-Image-2512 / Qwen-Image-Edit-2511

- Repo: https://github.com/QwenLM/Qwen-Image
- HF: https://huggingface.co/Qwen/Qwen-Image
- 强项：中文/英文文字渲染、提示词理解、真实感、图片编辑、多图编辑。
- 适用：AI 图片生成、图片改图、中文语境视觉、带文字的视觉生成。
- 优先级：最高。若目标是中文用户可用的 AI 图片制作，应优先尝试 Qwen-Image 系列。
- 注意：模型重，需要 ComfyUI/diffusers/SGLang/WaveSpeed/ModelScope 等合适运行方式。

### 2. FLUX / FLUX Kontext / FLUX Fill / FLUX Krea

- Repo: https://github.com/black-forest-labs/flux
- 强项：审美、写实、商业质感、instruction editing、局部重绘/扩图。
- 适用：高质量主视觉、产品氛围图、海报背景、改图。
- 注意：dev/Kontext/Fill/Krea 多数不是商用友好 license；商用前查 license。若只是本机测试可优先试效果。

### 3. Step1X-Edit / ReasonEdit-S

- Repo: https://github.com/stepfun-ai/Step1X-Edit
- 强项：指令式图片编辑，对标 GPT-4o/Gemini 风格的“按话改图”。
- 适用：用户上传图片后要求“别变主体，帮我改成……”。
- 优先用于图片编辑，不作为纯文生图主力。

### 4. HunyuanImage-2.1

- Repo: https://github.com/Tencent-Hunyuan/HunyuanImage-2.1
- 强项：2K 高质量生成、中文/英文提示词、电影感画面。
- 适用：高质量纯生成、海报主视觉背景。
- 注意：偏 T2I，不是通用改图。

### 5. OmniGen2 / BAGEL

- OmniGen2: https://github.com/VectorSpaceLab/OmniGen2
- BAGEL: https://github.com/ByteDance-Seed/Bagel
- 强项：统一多模态理解、参考图/in-context 生成与编辑。
- 适用：需要多图参考、场景一致性、人物/物体参考的任务。
- 注意：生产稳定性需实测。

### 6. SD3.5 / SDXL / JuggernautXL / RealVisXL

- 强项：生态成熟、ComfyUI 支持广、适合作为 fallback 和背景生成。
- 适用：本地可控流程、商品背景、一般海报背景。
- 注意：不要把基础 SDXL 当成质量上限。

### 7. Seedream

- 现状：未确认有官方开放权重，更多是平台/API 方式。
- 适用：如果未来接入 API，可作为高质量闭源/平台路线候选。

## 文字、艺术字、标题效果路线

### 1. ComfyUI_LayerStyle

- Repo: https://github.com/chflame163/ComfyUI_LayerStyle
- 作用：Photoshop-like layer effects，包括描边、投影、内阴影、外发光、渐变叠加、颜色叠加、混合模式。
- 结论：这是提升“标题字效”的首选 ComfyUI 方案。不要只用普通字体；标题应经过 LayerStyle 或等价的 SVG/CSS/Canvas 字效层。

### 2. ComfyUI_LayerStyle_Advance

- Repo: https://github.com/chflame163/ComfyUI_LayerStyle_Advance
- 作用：更高级图层/蒙版/效果节点。

### 3. AnyText / AnyText2 / ComfyUI_Anytext

- AnyText: https://github.com/tyxsspa/AnyText
- AnyText2: https://github.com/tyxsspa/AnyText2
- ComfyUI node: https://github.com/zmwv823/ComfyUI_Anytext
- 作用：多语言视觉文字生成/编辑，可让文字自然融入图片。
- 使用原则：如果文字必须成为图像纹理，用 AnyText2/Glyph 路线；如果是平面海报标题，仍优先确定性排版 + LayerStyle。

### 4. Glyph-ByT5 / GlyphDraw / JoyType

- Glyph-ByT5: https://github.com/AIGText/Glyph-ByT5
- GlyphDraw: https://github.com/OPPO-Mente-Lab/GlyphDraw
- JoyType: https://github.com/jdh-algo/JoyType
- 作用：提高文字生成准确性与多语言 glyph 表现。
- 适用：实验性艺术字/海报字生成；需要实测，不要默认宣称生产级。

### 5. 稳定排版层

优先级：

1. Figma/Canva/Bannerbear/Placid 模板 API（若有授权）；
2. Satori/SVG/resvg/sharp 模板系统；
3. Fabric.js/Konva/Polotno 做 Canva-like 可编辑对象；
4. Pillow 只用于简单处理和 fallback。

标题必须至少有一种设计处理：艺术字体、描边、渐变、投影、发光、标签形、局部高亮、纹理填充、立体层、手写/书法风。单纯 Noto/黑体白字不合格。

## 现成 ComfyUI 产品/海报工作流优先尝试

### 官方 ComfyUI workflow_templates

Repo: https://github.com/Comfy-Org/workflow_templates

优先找这些模板：

- `image_flux2_fp8` — Product Mockup (Flux.2 Dev FP8)
- `templates-9grid_social_media-v2.0` — 3x3 Grid For Product Ads
- `templates-poster_product_integration` — Generate Poster/Ad Asset with your Product
- `templates-poster_to_2x2_mockups-v2.0` — Poster Scene Mockups
- `templates-subject_product_swap.app` — Swap Product in Character’s Hand, UGC Style
- `templates-subject_holding_product.app` — Add Product to Character’s Hand, AI UGC
- `templates-product_scene_relight` — Composite your Product + Scene and Relight
- `gsl_starter_1_3` — Starter – Product Photography

这些是最应该先试的“现成模板”，不要继续从零写粗糙样张。

### Yolain ComfyUI Workflows

Repo: https://github.com/yolain/ComfyUI-Yolain-Workflows

重点：`workflows/3_awesome/3-2/3-2-1电商产品主图.json`

适用：电商产品主图、商品图。

### ComfyUI-productfix

Repo: https://github.com/MiddleKD/ComfyUI-productfix

重点：`productfix_text.json`, `productfix_adapter.json`

适用：保留商品包装、logo、文字和细节的商品图生成。

### PosterCraft-ComfyUI

Repos:
- https://github.com/AIFSH/PosterCraft-ComfyUI
- https://github.com/Yuan-ManX/ComfyUI-PosterCraft

适用：模型级海报生成和版式探索。依赖重，需实测，不要空口承诺效果。

### FLUX All-in-One / SDXL Mature Workflows

- https://github.com/Ling-APE/ComfyUI-All-in-One-FluxDev-Workflow
- https://github.com/SytanSD/Sytan-SDXL-ComfyUI
- https://github.com/SeargeDP/SeargeSDXL

适用：高质量背景/主视觉生成，再接排版层。

## 更新后的执行规则

1. 用户说“效果不好/别瞎干/对标 GPT/Gemini”时，立即停止自制 SVG/Pillow 方案，先查/用现成强模型或现成工作流。
2. 如果任务是图片生成：优先 Qwen-Image、FLUX、HunyuanImage、SD3.5/SDXL 高质量模型。
3. 如果任务是图片编辑：优先 Qwen-Image-Edit、FLUX Kontext、Step1X-Edit、OmniGen2。
4. 如果任务是商品图：优先 ComfyUI 官方产品模板、ProductFix、Yolain 电商主图 workflow；商品主体必须保留。
5. 如果任务有中文标题/海报文字：优先 LayerStyle/AnyText2/Glyph/模板系统，不允许只用普通黑体。
6. 如果没有实际跑通强模型或模板，只能说“方案已筛选/待安装验证”，不能发低质样张假装完成。

## 验收标准

- 画面质量：接近主流闭源模型/热门 AI 作品，而不是技术 demo。
- 字体效果：标题有明确艺术化处理，不单调、不土、不像默认黑体。
- 排版：信息层级清楚，有留白、焦点和视觉节奏。
- 文字：准确、无乱码、无裁切、无拥挤。
- 定位：AI图片制作是通用做图工具，不是任何单一平台专用工具。
