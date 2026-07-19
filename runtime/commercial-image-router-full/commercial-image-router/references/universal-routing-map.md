# Universal Image Routing Map

This reference expands `commercial-image-router` from poster/product/avatar into a full image-processing router. It does not mean every backend is already installed; it means every user request must be classified into a known route with a quality gate and an honest fallback.

## Route 0 — Intake contract

For every image task, determine:

1. **Input assets**: none / one image / multiple images / reference style / reference person / product photo / screenshot.
2. **Output type**: photo-real image, illustration, cartoon/avatar, poster/graphic, collage, transparent PNG, social cover, print file.
3. **Must preserve**: person identity, product/logo, original photo uncropped, exact text, style, ratio.
4. **Allowed changes**: background, style, color grade, pose, text, crop, cleanup, upscale.
5. **Risk**: copyrighted character/IP, face identity, child/minor likeness, brand/logo, medical/legal/official document.
6. **Publishing level**: quick draft / user evaluation / public-facing / paid commercial.

If the route has obvious defaults, act. Ask only when missing information changes the tool chain or can cause irreversible drift.

## Capability matrix

| User need | Route | Primary tools | QA gate |
|---|---|---|---|
| Text-to-image / 创意生图 | Generate 2+ variants, choose best | ComfyUI JuggernautXL/SDXL/FLUX when installed; image_generate if auth works | prompt intent visible, no watermark/text, no anatomy/artifact failures |
| Poster / 宣传图 / 封面图 | Generate no-text visual → deterministic typography template | ComfyUI + SVG/Satori/Figma/Canva route | exact Chinese text, no overflow, mobile-readable |
| Product poster | Preserve product → segment → scene → composite → template | SAM/Grounded-SAM + JuggernautXL/RealVisXL + SVG | product fidelity, clean cutout, contact shadow, no AI-redrawn product |
| Change background | Segment subject → generate/inpaint new background → blend | SAM/rembg/Grounded-SAM + ComfyUI inpaint/img2img | subject unchanged, edge/no halo, lighting plausible |
| Existing image text edit / 图片改字 | Locate old text → erase → re-typeset exact text | OCR/manual region + inpaint/LaMA/BrushNet + SVG/AnyText | old text gone, new text exact, no background scars |
| Remove object | Mask object → inpaint → texture QA | ComfyUI inpaint/IOPaint/LaMA/BrushNet | removed object invisible, structure preserved |
| Extend/outpaint | Expand canvas → outpaint margins → crop/export | ComfyUI outpaint/inpaint | no seams, subject not distorted |
| Repair blurry/low-res | upscale/deblur/face restore | Real-ESRGAN/Upscale/CodeFormer/GFPGAN when available | sharper but not plastic; face/product identity preserved |
| Transparent cutout | Segment + edge cleanup + alpha review | SAM/rembg + checkerboard review | no fringe/holes; alpha clean at actual size |
| Avatar from real photo | square prep → img2img/identity model → QA | ComfyUI img2img; InstantID/IPAdapter/PuLID when installed | likeness, glasses/hair/age, circular-crop safe |
| Pet/animal image | generate/modify directly | ComfyUI text2img/img2img | animal type/action clear, no extra limbs/watermarks |
| Collage/photo wall | deterministic contain-mode layout | SVG/HTML/Pillow layout | no image cropped unless allowed; spacing/style consistent |
| Screenshot/UI cleanup | crop/annotate/blur/redact/resize | deterministic local tools | no sensitive info leak; labels readable |
| Format conversion | convert, compress, resize | sharp/Pillow/ffmpeg/ImageMagick if installed | dimensions, filesize, color mode verified |
| Print-ready export | high-res layout and margins | SVG/PDF route, 300dpi raster if needed | bleed/safe margins/size verified |
| Series/brand pack | fixed template + seed/style presets | SVG templates + model seed/LoRA if installed | consistency across all outputs |

## Route selection rules

### A. If exact Chinese text appears in final output

Use deterministic text layer unless the user explicitly wants text baked into a natural image. Commercial posters must use SVG/Figma/Satori/Canva-like layout, not model-generated Chinese.

### B. If a real product appears

The real product photo is the source of truth. Never let a diffusion model redraw the product as final unless the user explicitly wants a concept illustration. Segment/composite; do not hallucinate packaging, logo, pattern, or product color.

### C. If a real person appears

Preserve identity only through a route designed for references. For avatar stylization, use img2img/identity models and QA against reference traits. Do not report success if eyes/glasses/hair/age are wrong.

### D. If user asks for protected named IP

Do not make a 1:1 replica. Create an original character with high-level traits and relationship/scene, or ask for proof/licensed assets if they need brand work. Keep the refusal short and still be useful.

### E. If user says “不好/不够好/字体不行/还是不对”

Treat this as a method failure, not a parameter tweak. Change route: different model, template, font family, segmentation approach, or composition concept.

## Honest capability states

Use these labels in internal reasoning and, when needed, user-facing status:

- **Verified**: actually ran in this environment and produced a checked file.
- **Installed, not verified**: package/model exists but no successful output yet.
- **Configured externally**: requires API key/MCP/template service.
- **Planned**: known route, but not connected here.
- **Blocked**: attempted and failed; include the real error.

Do not claim “can do” as if verified when the route is only planned.
