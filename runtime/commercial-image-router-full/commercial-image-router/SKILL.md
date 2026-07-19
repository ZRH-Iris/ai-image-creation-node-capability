---
name: commercial-image-router
description: "Use when the user wants AI图片制作: generate, edit, repair, upscale, or design images such as 商品图、宣传图、海报、封面图、头像、图片改字、换背景、拼图、修复放大. Routes each request to the right image model, ComfyUI workflow, template/layout layer, title-art typography system, and QA path."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ai-image-creation, image-generation, image-editing, poster, product-image, comfyui, typography, title-art, layout, qa]
    related_skills: [visual-media-generation, comfyui, html-design]
---

# AI图片制作

## Overview

Use this Skill as the default router for public-facing image tasks. The goal is not to pick one model for everything; the goal is to classify the job, preserve what must not change, choose the correct generation/editing/layout chain, verify the exported image visually, and deliver the actual file.

Core principle:

> Hermes is the director and QA layer; use the best available specialized tools for the job. ComfyUI/image models generate or edit visual material; product/subject segmentation preserves real assets; a professional layout/template layer handles commercial Chinese typography and information hierarchy; repair/upscale tools polish the result.

Mandatory references before producing text-bearing images:

- `references/implementation-stack.md` — model/tool/layout stack.
- `references/quality-gates.md` — visual QA and rejection rules.
- `references/typography-system.md` — font, hierarchy, poem inscription, and text-in-scene rules.
- `references/text-bearing-image-pitfalls.md` — session-tested pitfalls for fake model text, poem integration, invitation posters, and consumer-facing copy.

Hard rule from user feedback: do **not** improvise commercial image production by hand when better tools exist. Do not hand-arrange posters with ad-hoc Pillow layouts as the main route. For serious outputs, use or install the right stack: high-quality models, segmentation/background removal, inpainting/editing models, and a professional template/layout layer. Pillow is only an emergency fallback for simple deterministic assembly or inspection helpers.

## When to Use

Use when the user asks to:

- generate an image / 做一张图 / 生图
- generate character images, including animal/person/cartoon-style prompts; if the prompt names a living/active copyrighted character or franchise IP, do not make a 1:1 replica. Route to an original character with similar high-level traits/relationship/scene and tell the user briefly.
- make 商品图、公众号封面、朋友圈图、宣传图、活动海报、招生海报、社交平台配图
- make 商品图、商品海报、电商主图、产品宣传图
- edit an existing image, including 换背景、改风格、局部修改、扩图
- change text inside an existing image / 图片改字 / 替换海报文字
- make or iterate avatars / 头像 / IP形象
- repair, upscale, sharpen, restore, or clean up images
- produce a commercial/public-facing image that must be suitable for external publishing

Do not use this Skill for purely textual writing, PPT decks, or ordinary web pages unless the final deliverable is an exported image.

## Runtime Environment Notes

This Skill can be installed with the bundled full-runtime installer. In a distributed install, paths are controlled by environment variables rather than hardcoded machine paths:

- `HERMES_IMAGE_RUNTIME` — runtime root for ComfyUI, models, helper workflows, and outputs. Default: `~/.hermes-image-runtime`.
- `COMFY_HELPERS_DIR` — helper workflow/script directory. Default: `$HERMES_IMAGE_RUNTIME/comfy-helpers`.
- `COMFY_WORKSPACE` — ComfyUI checkout. Default: `$HERMES_IMAGE_RUNTIME/comfy-workspace`.
- ComfyUI local endpoint: `http://127.0.0.1:8188`.
- Expected installed checkpoints/support models after full setup:
  - `models/checkpoints/Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors` — verified high-quality SDXL-compatible route for product backgrounds/posters/cartoon-style visuals.
  - `models/checkpoints/sd_xl_base_1.0.safetensors` — SDXL base, acceptable fallback/preview model.
  - `image-models/sam/sam_vit_b_01ec64.pth` — SAM product segmentation.
  - `models/upscale_models/4x-UltraSharp.pth` — verified 4× poster upscaler.
- When a shareable runtime package is produced, validate it with the tarball validator script and also with a full `bash setup_runtime.sh --dry-run` rehearsal before claiming the package is ready.
- GPT image generation via Hermes `image_generate` may fail if OpenAI/Codex auth returns 401. If that happens, do not keep retrying the same route; fall back to ComfyUI or repair the credential separately.

For this machine's historical verification evidence, see `references/local-runtime-status.md`. For distribution packaging rules, see `references/runtime-distribution-packaging.md`.

## Current Composition

This Skill is intentionally split into a small router plus supporting references/scripts:

- `SKILL.md` — trigger conditions, routing matrix, tool priority, typography rules, verification checklist, and delivery rules.
- `references/universal-routing-map.md` — full coverage map for text-to-image, posters, product images, background replacement, image text edits, object removal, outpainting, repair/upscale, avatars, collages, screenshots, conversion, print export, and series graphics.
- `references/quality-gates.md` — strict QA rules for text/layout, product fidelity, posters, avatars, animals/characters, repair/upscale, and iteration.
- `references/implementation-stack.md` — mandatory model/segmentation/template/font stack for serious public-facing work.
- `references/ai-image-creation-sota-stack.md` — current high-quality model/workflow priority list for AI图片制作: Qwen-Image, FLUX/Kontext, Step1X-Edit, HunyuanImage, AnyText2/Glyph, LayerStyle, and official ComfyUI product/poster templates. Load this before trying to improve visual quality or when the user says the result is not good enough.
- `references/local-runtime-status.md` — what is actually installed and verified in this environment.
- `references/qwen2512-layerstyle-route.md` — verified local route: Qwen-Image-2512 text-to-image + ComfyUI_LayerStyle Chinese title-art + ComfyUI mask compositing. Load this before poster/creative visual POCs when no GPT/Gemini image API is available.
- `references/poster-typography-and-style-lessons.md` — session lessons for commercial poster typography/style: safe-width text pills, avoiding heavy title outlines for enterprise/product graphics, rejecting model-generated fake background text, and making “换个风格” a true visual-system change.
- `references/comfyui-layerstyle-compositing-pitfalls.md` — practical pitfalls from real poster runs: ComfyUI input overwrite, stale title layers, LayerStyle black-background/alpha loss, mask compositing fix, and mandatory intermediate QA.
- `references/executable-workflows.md` — verified product-poster commands and scripts.
- `references/avatar-cartoon-workflow.md` — verified real-photo to anime/cartoon avatar route.
- `references/text-edit-inpaint-workflow.md` — verified inpaint smoke test plus honest text-edit workflow/limitations.
- `references/upscale-repair-workflow.md` — verified 4× upscaling route and QA rules for high-res/print outputs.
- `references/product-poster-routing-lessons.md` — corrections from failed product-poster attempts.
- `references/product-poster-mouse-lessons.md` — product poster lessons from a real mouse photo: reject generated backgrounds with fake text/products, keep process language off consumer posters, run SAM on a free GPU after OOM, and inspect cutout review before composition.
- `references/poem-poster-workflow.md` — poem/classical-literature poster workflow: generate no-text scene, reject or cover hallucinated calligraphy, render exact poem text deterministically, and QA poem completeness/readability.
- `references/capability-backlog.md` — upgrade plan separating verified routes from planned integrations.
- `references/skill-maintenance-and-regression.md` — mandatory protocol for updating this Skill: patch class-level rules, run a real smoke test, visually QA, audit from the top, and record evidence before claiming readiness.
- `references/runtime-distribution-packaging.md` — how to package this Skill for other Hermes/Harness users as a non-technical one-click full runtime, not just a small Skill archive; includes installer shape, portability rules, and package QA checks.
- `references/github-node-capability-packaging.md` — how to publish this Skill as a GitHub node-capability repository modeled after shareable capability repos: README, AUTO_INSTALL_FOR_HERMES, MANIFEST, installer, runtime, user guide, dry-run test, and GitHub push handoff.
- `references/ai-image-creation-positioning-and-typography.md` — user-approved positioning/naming rule: public-facing name is **AI图片制作**; do not make it look 小红书-specific; use deliberate title-art typography rather than plain system text; locally QA and get user confirmation before pushing GitHub packaging updates.
- `scripts/sam_product_extract.py` — SAM product extraction with foreground/background points and review outputs.
- `scripts/compose_product_poster.js` — Node/sharp/SVG product poster compositing with deterministic CJK typography.
- `scripts/make_inpaint_smoke_test.py` — deterministic smoke-test source/mask generator for inpaint/text removal.
- `scripts/audit_skill.py` — end-to-end skill audit: frontmatter, links, required references/scripts, ComfyUI workflow deps, and verified artifacts.
- `scripts/validate_distribution_package.py` — extract-level package validator for distribution tarballs: checks required files, ordinary-user README wording, nesting/cache defects, shell/node syntax, and manifest completeness.

## Intake: Classify Before Acting

Before choosing tools, load `references/universal-routing-map.md` when the request is not a simple already-verified product/avatar/poster route. Then classify the request along these axes:

1. **Input state**
   - No image supplied: generate new visual.
   - Image supplied: edit, preserve, composite, repair, or use as reference.

2. **Asset type**
   - Product photo / 商品
   - Person / avatar / portrait
   - Poster or graphic with existing text
   - Scenic/photo background
   - Screenshot/UI
   - Multiple photos for collage

3. **Operation**
   - Generate from scratch
   - Change background
   - Change text in image
   - Add Chinese title/layout
   - Product ad composition
   - Inpaint/remove object
   - Outpaint/extend canvas
   - Upscale/repair
   - Style transfer
   - Series/brand consistency

4. **Preservation constraints**
   - Product/logo/package must not change
   - Person identity must stay similar
   - Original photo must not be cropped
   - Existing brand style must be preserved
   - Text must be exact

5. **Publishing context**
   - 平台封面图: if the user explicitly names 小红书/公众号/朋友圈/电商, adapt ratio, reading distance, and style to that platform; otherwise keep the Skill positioned as general AI image creation.
   - 商品图/电商: product accuracy first.
   - 宣传图/海报: information hierarchy and typography matter most.
   - 头像: square, centered, safe for circular crop.

## Routing Matrix

| Task | Default route | Critical rule |
|---|---|---|
| New image / 宣传图 / 海报 / 封面图 | Generate no-text visual with ComfyUI/API → apply professional layout template → export PNG | Do not trust diffusion models for Chinese typography. |
| Product image poster | Preserve real product → segment/cut out product → generate/choose background → composite → template typography | Never hallucinate/redraw product logo, packaging, color, or shape. |
| Change text inside image | Locate/erase old text → restore/inpaint background → add exact new text with matching font/style or AnyText route | Do not regenerate the whole image unless user accepts major drift. |
| Change background | Mask subject/product/person → generate or inpaint new background → blend edges/shadows | Preserve subject. |
| Person/avatar | Use references + identity-preserving route (InstantID/PhotoMaker/IP-Adapter/PuLID when available) → QA similarity | Inspect eyes/glasses/hair/age/crop. |
| Collage/social photo wall | Deterministic layout (Pillow/HTML/SVG) with contain mode | Default: never crop original photos. |
| Repair/upscale | Real-ESRGAN/CodeFormer/GFPGAN/Topaz-like route | Do not over-sharpen or alter product/face identity. |
| Series/brand graphics | Use fixed template + fixed fonts + model/style seed/LoRA where available | Consistency beats one-off novelty. |
| Poem/classical-literature image with text | Generate no-text poem scene → inspect for hallucinated calligraphy → cover/regenerate contaminated areas → render exact poem text with deterministic template | Never let the model write the poem; if fake background text remains visible through a translucent card, use an opaque poem panel. |
| Named copyrighted character/IP request | Create an original character scene using high-level traits only, or ask for user-owned/licensed reference if they need exact brand assets | Do not promise or attempt 1:1 replication of protected characters. |
| Ordinary animal/pet image | Generate directly with the best available photoreal/cartoon route → QA anatomy, action clarity, no watermark | Run 2+ variations when quick; choose the clearest action/least artifacts before delivery. |

## Tool Priority

### Generation / visual material

Prefer in this order when available:

1. GPT/Gemini/OpenAI image editing API for high-level instruction-following and image edits, if auth is valid.
2. ComfyUI with FLUX/JuggernautXL/RealVisXL/SDXL/Qwen routes, depending on installed models.
3. SDXL base for acceptable previews and medium-quality tests.
4. SD1.5 only for smoke tests or rough drafts.

### Layout / typography

Prefer in this order:

1. **Figma template/API/MCP** — best long-term commercial typography and reusable design templates. If unavailable, explicitly try to set it up or report the missing credential/tool; do not silently fall back to hand layout for commercial work.
2. **Canva/Bannerbear/Placid or similar template API** — good commercial output when credentials/templates exist.
3. **Satori/SVG/HTML template system** — best open-source automated layout route. Build reusable templates; do not ad-hoc hand-place every poster.
4. **ComfyUI LayerStyle** — useful for Photoshop-like compositing, strokes, shadows, masks, and layer effects, but not enough for information hierarchy by itself.
5. **Pillow** — emergency fallback only: simple deterministic assembly, batch crops, contact sheets, or when all professional template routes are unavailable and the user accepts a rough draft.

**Font rule:** never keep using a rejected font. If the user says the font is bad, immediately switch font family/style and preferably switch the entire template. For Chinese commercial images, first try a proper font set (e.g. 阿里巴巴普惠体 / HarmonyOS Sans / 思源黑体 for body; 得意黑/SmileySans/优设标题黑 for youthful display; 霞鹜文楷 for warm/cultural scenes). If the required font is not installed, download/install it before rendering or choose a verified available substitute.

### Text inside images

Use when text must be generated/edited as part of the image texture:

- AnyText / AnyText2 / ComfyUI_Anytext
- GlyphDraw / Glyph-ByT5 / JoyType routes if installed and verified
- Inpaint/BrushNet/Lama style erasing + deterministic re-typesetting when possible

For flat posters, deterministic re-typesetting is usually more reliable than text-generation models.

### Repair / polish

Use when available:

- Real-ESRGAN for general upscale
- CodeFormer/GFPGAN for face repair
- ComfyUI upscalers / Ultimate SD Upscale for generated images
- Manual color/contrast/sharpening only after visual QA

## Standard Workflows

Reference: `references/implementation-stack.md` is mandatory for serious/high-quality work. It lists the required stack: high-quality models, segmentation/background-removal, image editing/inpainting, professional template layout, font rules, and QA gates. Follow it before producing product posters, creative images, or image edits.

Reference: `references/universal-routing-map.md` is the broad coverage map for all image-processing needs: text-to-image, posters, product images, background replacement, image text edits, object removal, outpainting, repair/upscale, avatars, collages, screenshots, conversions, print exports, and series graphics.

Reference: `references/quality-gates.md` is the mandatory pre-delivery QA checklist. Load it for any public-facing, edited, or user-criticized output.

Reference: `references/ai-image-creation-sota-stack.md` is mandatory when the user asks for better image quality, says the current result is bad, asks to compare with GPT/Gemini/Gemini 生图/GPT 生图, or asks to find popular/open-source/high-liked ready-made routes. Use it before making a new sample. The default upgrade path is: Qwen-Image/FLUX/Hunyuan for generation; Qwen-Image-Edit/FLUX Kontext/Step1X-Edit/OmniGen2 for editing; ComfyUI official product/poster templates, Yolain workflows, ProductFix, PosterCraft, LayerStyle, AnyText2/Glyph routes for product/poster/text quality. Do not continue with low-quality hand-made SVG/Pillow samples after the user rejects quality.

Reference: `references/local-runtime-status.md` records the tools actually installed and verified on this machine, including the Node/sharp SVG template renderer and model/segmentation setup. Check it before choosing routes.

Reference: `references/capability-backlog.md` separates verified routes from planned upgrades and defines what counts as a solved capability.

Reference: `references/skill-maintenance-and-regression.md` is mandatory when improving this Skill itself. It requires a real smoke/regression run, visual QA, `scripts/audit_skill.py`, and concise evidence in `local-runtime-status.md` before saying a capability is ready.

Reference: `references/runtime-distribution-packaging.md` is mandatory when sharing this Skill with other Hermes/Harness users. If the expected promise is "others install it and get our image quality," create a full runtime package: Skill + ComfyUI helper workflows/scripts + installer + model manifest + font/layout/SAM/upscale setup + smoke test. Do not share only the Skill directory unless the recipient already has equivalent image infrastructure.

Reference: `references/github-node-capability-packaging.md` is mandatory when the user wants a GitHub link that others can forward to Hermes for installation. Use the shareable capability repo shape (`README.md`, `AUTO_INSTALL_FOR_HERMES.md`, `MANIFEST.yaml`, `installer/`, `runtime/`, `docs/`, `card/`) and dry-run the installer from a clean temp `HERMES_HOME`/`HERMES_IMAGE_RUNTIME` before claiming readiness. If the user provides another capability repo as an example, study its structure; do not install that unrelated capability unless explicitly requested.

Reference: `references/ai-image-creation-positioning-and-typography.md` is mandatory when the user comments on naming, scope, 小红书 over-emphasis, typography quality, title effects, or GitHub publication timing. It records the user-approved public name **AI图片制作**, the requirement for stronger artistic title treatments, and the rule to visually QA/get user confirmation before pushing packaging changes.

Reference: `references/executable-workflows.md` contains verified commands and scripts for real product-poster execution: JuggernautXL background generation, SAM product extraction, SVG typography compositing, and QA. Use it when the user asks to actually make a product poster.

Reference: `references/avatar-cartoon-workflow.md` contains the verified real-photo-to-anime/cartoon WeChat avatar workflow: square reference prep, ComfyUI img2img prompt/settings, denoise-strength choices, and QA for likeness plus circular-crop safety. Use it for 真人照片转动漫头像/卡通头像.

Reference: `references/text-edit-inpaint-workflow.md` contains the verified local inpaint smoke test and the workflow for 图片改字/旧字擦除/局部去物. It also records the current limitation: basic SDXL/Juggernaut inpaint can remove text but may leave a soft panel/scar, so commercial text edits need stronger cleanup or deliberate template reconstruction.

Reference: `references/upscale-repair-workflow.md` contains the verified 4× upscaling route using ComfyUI and `4x-UltraSharp.pth`, including command, artifact paths, and QA rules for 高清/印刷/大图 delivery.

Reference: `references/product-poster-routing-lessons.md` captures a correction from a real product-poster attempt: manual polygon/color-mask product cutouts are not reliable enough for commercial output; use proper segmentation/background-removal, inspect the cutout alone, and only then build the poster.

Reference: `references/poem-poster-workflow.md` is mandatory when creating 古诗配图/诗词海报 or any image that must include exact poem/literary text. It records the verified pattern: generate a no-text scene, reject or fully cover hallucinated calligraphy, render the poem with deterministic template text, and QA the exact characters/readability before delivery.

### 1. AI image creation / poster / 宣传图 / 封面图

1. Clarify or infer: purpose, audience, title, key facts, required ratio.
2. Generate a **no-text** background or main visual using the best available image model.
3. Choose a professional layout route:
   - existing Figma/template if available;
   - Satori/SVG/HTML template if open-source route;
   - only use Pillow for simple layout or emergency fallback.
4. Add exact Chinese copy via deterministic text layer.
5. Export platform size: 1080×1350, 1080×1440, 1242×1660, 1080×1920, square, etc.
6. Visually inspect final image.
7. Send the actual exported image file directly.

### 2. Product poster / 商品图

1. Treat the provided product photo as ground truth.
2. Segment or mask the product; preserve logo/package/colors.
3. Generate or select background separately.
4. Composite with correct shadow/contact/reflection.
5. Add promotional copy through template layout.
6. QA product drift: compare original and final product shape, logo, color, label placement.
7. Deliver final image and optionally a comparison/contact sheet.

### 3. Change text in an existing image

1. Identify target text region(s). If OCR is available, use it; otherwise inspect visually.
2. Mask and remove old text with inpainting/background reconstruction.
3. Add exact replacement text via deterministic layout, matching font/color/angle/shadow as closely as possible.
4. If text must blend into a natural scene, consider AnyText/AnyText2 route.
5. QA: old text fully gone; new text exact; no artifacts/residue; no unrelated image drift.

### 4. Background replacement

1. Mask foreground subject/product/person.
2. Preserve the subject pixels when possible.
3. Generate/inpaint background.
4. Composite with edge feathering, color matching, shadow/contact correction.
5. QA subject drift and edge artifacts.

### 5. Avatar/person image

1. Collect 2–4 references when possible.
2. Extract stable visible traits and current user correction notes.
3. Use identity-preserving route when available.
4. Generate square, centered, text-free output.
5. QA for face similarity, eyes/glasses, hair, age, extra fingers/limbs, circular crop.

### 6. Collage/photo wall

1. Preserve every input image with contain mode unless user explicitly permits cropping.
2. Use deterministic layout: white borders, subtle shadow, warm textured background when appropriate.
3. QA every source image is fully visible.

### 7. Named IP / character crossover images

1. If the user names protected characters/franchises and asks for a 1:1 replica, do not reproduce them exactly.
2. Preserve the user's intent at a high level: relationship, pose, mood, scene, broad archetype, species, colors, and age-appropriate tone.
3. Prompt for an **original** version, e.g. “black cat police captain” instead of a named IP character, and “pink piglet girl” instead of a named franchise character.
4. Keep the explanation short. Do not over-lecture; if delivering an image, mention it is an original cartoon version.
5. QA character clarity: correct species, clear interaction such as hand-holding/eating/running, no extra limbs, no watermarks or stray text.

## Typography Rules for AI Image Creation

- Do not ask diffusion models to render the final Chinese text for flat posters.
- Use design/template layout for titles, dates, prices, locations, badges, and selling points.
- **Title-art rule:** for any poster/cover/promotional graphic, plain black/white system text is not enough. Create at least one deliberate title treatment: display font + gradient fill, subtle shadow/glow, highlight underline, sticker/label shape, thin outline, or brush/calligraphy style when appropriate. Do **not** default to thick outlines, heavy bevels, or bulky strokes for enterprise/product posters; reserve those for playful sticker/Y2K styles only.
- Prefer modern Chinese fonts: 思源黑体/Noto Sans CJK, 阿里巴巴普惠体, HarmonyOS Sans, 得意黑/SmileySans/优设标题黑/阿里妈妈数黑 for display titles, 霞鹜文楷 for warm/cultural scenes when appropriate.
- Do not use weak system fallback fonts for public images unless no alternative exists.
- Use 2-font hierarchy at most: display title + readable body.
- Keep mobile readability: large title, high contrast, no thin light text over busy backgrounds.
- Do not over-emphasize 小红书. Treat it as one optional platform style only when the user explicitly requests it; otherwise present this Skill as general AI 图片制作.
- Avoid scattering many stickers/cards unless the requested style is explicitly Y2K/sticker collage.
- If the user says typography/layout is bad, treat it as a layout-system failure. Switch to a professional template route and a stronger title-art treatment; do not only change font size/color.

## Current Known Research Findings

Useful projects found for this routing system:

- `tyxsspa/AnyText` — multilingual visual text generation and editing.
- `tyxsspa/AnyText2` — visual text generation/editing with customizable attributes.
- `zmwv823/ComfyUI_Anytext` — ComfyUI custom node supporting AnyText v1/v2, Glyph-ByT5, JoyType routes.
- `chflame163/ComfyUI_LayerStyle` — Photoshop-like compositing in ComfyUI.
- `chflame163/ComfyUI_LayerStyle_Advance` — advanced layer-style nodes.
- `vercel/satori` — HTML/CSS to SVG rendering; useful for open-source automated template layouts.
- `OPPO-Mente-Lab/GlyphDraw` — Chinese character text-to-image direction; experimental compared with template layout.

## Degradation / Fallback Rules

- If GPT image auth fails with 401, do not claim GPT image output was generated. Switch to ComfyUI or fix auth.
- If ComfyUI server is down, start it and verify `/system_stats` before running workflows.
- If only SD1.5 is available, label it as a rough/test route and recommend SDXL/FLUX/JuggernautXL/RealVisXL for commercial quality.
- If no professional template engine is connected, produce a functional draft but clearly treat typography as draft quality. For user-facing delivery, prioritize building/reusing a template first.
- If the user rejects layout twice, stop iterating ad-hoc; switch method.

## Verification Checklist

Before final delivery:

- [ ] Correct task route chosen and preservation constraints respected.
- [ ] If product/person supplied, original identity/shape/logo is preserved.
- [ ] If text requested, every character is exact.
- [ ] No garbled Chinese, residual old text, unwanted watermark, or stray letters.
- [ ] No text clipping, low contrast, overlap, or overflow beyond cards/panels; long Chinese copy must be wrapped, split into chips, or resized inside a measured safe area.
- [ ] Overall composition is commercial-grade, not merely technically valid; if it looks like a rough template or "能看但不够好", iterate layout/background before delivery.
- [ ] Image ratio and size match the platform/use.
- [ ] Important content is mobile-readable.
- [ ] Faces/hands/products checked for obvious AI artifacts.
- [ ] Final file opened/visually inspected.
- [ ] Finished image is delivered directly as a file/attachment, not only a local path or UI link.

## Delivery Rules

For this user, when a final image file is made, send it directly through Feishu with `MEDIA:/absolute/path`. Do not only report the path. Do not send a ComfyUI link as the primary deliverable unless the user explicitly wants to operate ComfyUI manually.
