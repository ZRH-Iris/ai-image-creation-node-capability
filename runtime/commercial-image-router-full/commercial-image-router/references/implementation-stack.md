# Commercial Image Implementation Stack

This reference exists because the user explicitly rejected ad-hoc/manual poster attempts. For high-quality images, do the stack, not improvisation.

## Mandatory Production Stack

### 1. High-quality generation/editing models

Install/use the best available route before claiming a serious result:

- Product/lifestyle backgrounds: FLUX.1-dev, FLUX.1-schnell, JuggernautXL, RealVisXL, SD3.5, Qwen-Image.
- Image editing / preserving source: FLUX.1-Kontext, Qwen-Image-Edit, GPT/Gemini image editing APIs if auth is working.
- Image text/editing: AnyText2 / ComfyUI_Anytext, or erase + deterministic re-typeset.

SDXL Base is only a compatibility/fallback route. SD1.5 is removed from formal AI图片制作 routes.

### 2. Product/subject preservation

For product images, do not hand-cut with rough polygon masks. Use proper segmentation/background-removal:

- GroundingDINO + SAM / Grounded-SAM
- Segment Anything / SAM2 where available
- rembg/U2Net only if it works in the current Python environment and output is visually clean
- IOPaint/LaMa/BrushNet for background cleanup and old-text/object removal

Always inspect the cutout alone on a checkerboard/solid background before composing.

### 3. Professional layout/template layer

For public/commercial posters and product images, route typography through a template system:

1. Figma API/MCP if configured.
2. Canva/Bannerbear/Placid if credentials/templates exist.
3. Satori/SVG/HTML template system if no external design API is available.
4. Pillow only for emergency fallback or helper assets.

If no Figma/Canva/Bannerbear/Placid integration exists, build or use an HTML/SVG template first rather than placing text manually each time.

### 4. Font rules

If the user dislikes a font, replace it immediately. Do not keep the same font with minor tweaks.

Recommended Chinese font roles:

- Body/UI: 思源黑体 / Noto Sans CJK SC, 阿里巴巴普惠体, HarmonyOS Sans.
- Youthful display: 得意黑 / SmileySans, 优设标题黑, Alimama ShuHeiTi.
- Warm/cultural/lifestyle: 霞鹜文楷, LXGW WenKai.
- Avoid weak system fallback fonts for commercial images.

### 5. QA gates

Before delivery:

- Product preserved: logo/pattern/shape/color unchanged unless user requested edits.
- Cutout inspected; no ragged/white/gray background residue.
- Typography inspected at full size and phone-scale; no bad fonts, clipping, low contrast, or fake/garbled text.
- If user rejected a route twice, change method/tool, not parameters.

## Product Poster Route

1. Analyze product image and key visual features.
2. Create clean mask/cutout using segmentation, not manual polygon fallback.
3. Generate or choose a compatible lifestyle/product scene with high-quality model.
4. Composite product with realistic contact shadow and color matching.
5. Apply professional template layout; use exact copy and good fonts.
6. QA cutout, product fidelity, text, final ratio.
7. Send file directly.

## Existing Image Text Edit Route

1. Identify text region and exact replacement copy.
2. Remove old text with inpainting/cleanup.
3. Recreate text using matching font/style or AnyText2 if text must be baked into the scene.
4. QA old text removal, new text exactness, and local background artifacts.
