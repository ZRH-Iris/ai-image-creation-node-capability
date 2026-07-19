# Capability Backlog and Upgrade Plan

This file separates what is already verified from what still needs installation/API integration. The router should use verified routes first and continue improving toward full coverage.

## Verified now

- ComfyUI local server workflow execution.
- JuggernautXL checkpoint for high-quality SDXL-compatible backgrounds/illustrations.
- SDXL base fallback and SD1.5 smoke-test checkpoint.
- SAM ViT-B segmentation for product cutouts with foreground/background prompt points.
- Node/sharp/SVG deterministic layout templates.
- Noto CJK fonts installed for Chinese typography.
- Product poster full chain: generated background → SAM product cutout → SVG typography → QA → Feishu delivery.
- Real-photo to cartoon/anime avatar via ComfyUI img2img, with QA for glasses/hair/circular crop.
- Basic cartoon/animal text-to-image generation and variant selection.
- 4× high-resolution upscaling via ComfyUI `upscale_4x.json` + `4x-UltraSharp.pth`, verified on a 1080×1350 poster to produce 4320×5400 output with readable Chinese text.

## High-priority next capabilities

### 1. Inpainting / object removal / image text replacement

Need verified route for:

- Remove old text from a poster.
- Remove unwanted objects.
- Repair background after removal.
- Replace text with deterministic SVG layer.

Candidate stack:

- ComfyUI `sdxl_inpaint.json` if dependencies are ready.
- IOPaint/LaMA/BrushNet for robust background repair.
- AnyText2/ComfyUI_Anytext only when text must be integrated into image texture.

Verification target:

- Use a test poster with text; erase one text block; re-typeset exact Chinese; inspect for scars and text correctness.

### 2. Identity-preserving person/avatar route

Current img2img works, but likeness can drift. Add:

- InstantID / IP-Adapter / PhotoMaker / PuLID route for stronger identity preservation.
- Face-detail QA contact sheet.

Verification target:

- Same reference photo → 3 avatar styles, preserving glasses/hair/face vibe.

### 3. Grounded segmentation

SAM needs manual points. Add text-prompted boxes:

- GroundingDINO + SAM or Grounded-SAM.

Verification target:

- Product photo: prompt “pillow/cushion” and auto-produce cutout/review sheet without manually editing coordinates.

### 4. Advanced restoration and face/product repair

4× poster upscaling is verified. Still add/verify more specialized repair routes:

- CodeFormer/GFPGAN for face repair only when appropriate.
- Ultimate SD Upscale / tiled upscale for very large generated images.
- Product/logo-safe sharpening where labels must not warp.

Verification target:

- Face image repair without identity drift.
- Product package/logo upscale with no label hallucination.
- Large generated poster tiled upscale without seams.

### 5. Template library

Build reusable templates instead of one-off JS:

- Product poster: luxury/lifestyle, playful, tech, cultural.
- Camp/enrollment poster: winter/summer, school/training, travel/study.
- Xiaohongshu cover: big-title, listicle, comparison, quote card.
- Reminder/social card: Y2K/sticker, elegant note, bold poster.
- Avatar background: scenic, clean studio, illustrated.

Each template must define safe text boxes, max characters, wrapping rules, and QA examples.

### 6. External design/API integrations

Optional but high value if user provides credentials/templates:

- Figma MCP/API for professional design templates.
- Canva/Bannerbear/Placid for template-based social/ad graphics.
- OpenAI/Gemini image editing API if credentials fixed.

Credential rule: never store or echo raw tokens; record as `[REDACTED]`.

## Definition of “solves the need”

A capability is considered solved only when:

1. The route has a documented workflow and exact commands/scripts.
2. It has been executed at least once in this environment.
3. The output was visually QA’d.
4. The skill records limitations and fallback behavior.
5. The final output can be delivered directly as a file.

Anything else is only a planned route.
