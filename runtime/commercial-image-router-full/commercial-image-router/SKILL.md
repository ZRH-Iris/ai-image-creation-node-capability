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
- `references/text-and-product-poster-upgrade-rules.md` — mandatory upgraded route for text-bearing posters and real product posters: layout-first generation, safe negative space prompts, deterministic Chinese typography, product cutout QA, and asset-preserving compositing.
- `references/semantic-logic-qa.md` — mandatory semantic/common-sense QA: verify subject/action, spatial logic, anatomy/object structure, factual consistency, and audience fit before delivery.
- `references/typography-system.md` — font, hierarchy, poem inscription, and text-in-scene rules.
- `references/text-bearing-image-pitfalls.md` — session-tested pitfalls for fake model text, poem integration, invitation posters, and consumer-facing copy.

Hard rule from user feedback: do **not** improvise commercial image production by hand when better tools exist. Do not hand-arrange posters with ad-hoc Pillow layouts as the main route. For serious outputs, use or install the right stack: high-quality models, segmentation/background removal, inpainting/editing models, and a professional template/layout layer. Pillow is only an emergency fallback for simple deterministic assembly or inspection helpers.

## When to Use

Use when the user asks to:

- generate an image / 做一张图 / 生图
- generate character images, including animal/person/cartoon-style prompts; if the prompt names a living/active copyrighted character or franchise IP, do not make a 1:1 replica. Route to an original character with similar high-level traits/relationship/scene and tell the user briefly.
- make 商品图、公众号封面、朋友圈图、宣传图、活动海报、招生海报、社交平台配图
- make 请柬、邀请函、百日宴、满月宴、生日宴、婚礼请柬、升学宴、乔迁宴等带事实信息的宴会/活动卡片；优先生成空白卡片/留白底图，再确定性中文排版并逐字 QA
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
- Current install-profile policy:
  - Default shared install should be `core-generate`, not a giant full stack: install ComfyUI + PyTorch + `models/checkpoints/Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors` + the SDXL/JuggernautXL `txt2img` workflow + a smoke test.
  - Before downloading models, reuse existing user assets: honor `COMFY_WORKSPACE` for an existing ComfyUI checkout, honor colon-separated `COMFY_MODEL_DIRS`, search common ComfyUI/Hermes model roots, skip already-valid files, and symlink/copy valid existing models into the current runtime before downloading. For hash-known models such as JuggernautXL, require sha256 match.
  - Qwen is an on-demand profile for short Chinese copy, poem/culture images, direct model-written Chinese tests, and Qwen-Image-Edit style instruction editing. Do not default-install its 30GB+ model set for everyone.
  - SDXL Base is optional compatibility/fallback only.
  - SD1.5/legacy low-quality routes are removed from formal install, recommendation, and comparison workflows.
- When a shareable runtime package is produced, validate it with the package validator script, run a clean temp `--dry-run` install, run at least one real JuggernautXL/core smoke image on a machine that has the model, visually QA the smoke artifact, and only call GitHub deployment complete after `git push` and public/raw-link verification succeed.
- GPT image generation via Hermes `image_generate` may fail if OpenAI/Codex auth returns 401. If that happens, do not keep retrying the same route; fall back to ComfyUI or repair the credential separately.

For this machine's historical verification evidence, see `references/local-runtime-status.md`. For distribution packaging rules, see `references/runtime-distribution-packaging.md`.

## Current Composition

This Skill is intentionally split into a small router plus supporting references/scripts:

- `SKILL.md` — trigger conditions, routing matrix, tool priority, typography rules, verification checklist, and delivery rules.
- `references/text-and-product-poster-upgrade-rules.md` — mandatory upgraded route for text-bearing posters and real product posters: layout-first generation, safe negative space prompts, deterministic Chinese typography, product cutout QA, and asset-preserving compositing.
- `references/semantic-logic-qa.md` — mandatory semantic/common-sense QA for generated images: subject/action correctness, spatial physics, anatomy/object structure, factual text consistency, narrative/audience fit, and regeneration triggers.
- `references/session-20260720-text-product-poster-upgrade.md` — session evidence for the text/product poster upgrade: failed hard-paste smoke, reserved-space retry, verified artifact path, and remaining template/font/product-cutout gaps.
- `references/universal-routing-map.md` — full coverage map for text-to-image, posters, product images, background replacement, image text edits, object removal, outpainting, repair/upscale, avatars, collages, screenshots, conversion, print export, and series graphics.
- `references/quality-gates.md` — strict QA rules for text/layout, product fidelity, posters, avatars, animals/characters, repair/upscale, and iteration.
- `references/implementation-stack.md` — mandatory model/segmentation/template/font stack for serious public-facing work.
- `references/ai-image-creation-sota-stack.md` — current high-quality model/workflow priority list for AI图片制作: Qwen-Image, FLUX/Kontext, Step1X-Edit, HunyuanImage, AnyText2/Glyph, LayerStyle, and official ComfyUI product/poster templates. Load this before trying to improve visual quality or when the user says the result is not good enough.
- `references/local-runtime-status.md` — what is actually installed and verified in this environment.
- `references/model-selection-and-install-profiles.md` — 本轮实测后的模型选择与安装分层：默认 shared install 为 `core-generate`（ComfyUI + PyTorch + JuggernautXL + 基础 txt2img workflow + smoke test）；Qwen 作为中文/短文案/古诗/模型直写中文的按需 profile；SDXL Base 仅兼容兜底；SD1.5/旧版低质路线从正式安装与推荐中移除；并规定用户要求“单独用 Qwen”时不得偷偷后期排版或遮盖。
- `references/qwen2512-layerstyle-route.md` — verified local route: Qwen-Image-2512 text-to-image + ComfyUI_LayerStyle Chinese title-art + ComfyUI mask compositing. Load this before poster/creative visual POCs when no GPT/Gemini image API is available.
- `references/background-aware-product-ad-text-overlay.md` — session-tested pattern for turning a no-text product visual into a final Chinese promotional poster: infer text when appropriate, sample the background palette, match typography/material/light, QA for pasted-on text, and treat no-text visuals as intermediate unless explicitly requested.
- `references/comfyui-layerstyle-compositing-pitfalls.md` — practical pitfalls from real poster runs: ComfyUI input overwrite, stale title layers, LayerStyle black-background/alpha loss, mask compositing order.
- `references/node-engine-share-prompt.md` — user-approved concise `【节点引擎】AI图片制作能力安装包` forwarding text and deployment verification rules; use this instead of verbose model/profile install wording.
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
- `scripts/render_invitation_card.py` — deterministic Chinese invitation/card renderer for 百日宴、满月宴、婚礼、生日宴 and other event cards using blank-card backgrounds.
- `scripts/render_text_poster.py` — deterministic Chinese poster typography renderer: samples background palette, adds scene-matched title/subtitle/chips/CTA/footer, and prevents model-generated Chinese text from being final copy.
- `scripts/sam_product_extract.py` — SAM product extraction with foreground/background points and review outputs.
- `scripts/compose_product_poster.js` — Node/sharp/SVG product poster compositing with deterministic CJK typography.
- `scripts/make_inpaint_smoke_test.py` — deterministic smoke-test source/mask generator for inpaint/text removal.
- `scripts/audit_skill.py` — end-to-end skill audit: frontmatter, links, required references/scripts, ComfyUI workflow deps, and verified artifacts.
- `scripts/validate_distribution_package.py` — extract-level package validator for distribution tarballs: checks required files, ordinary-user README wording, nesting/cache defects, shell/node syntax, and manifest completeness.
- `scripts/publish_github_api.py` — fallback GitHub publisher for shareable capability repos when normal `git push` is blocked but a one-time `GITHUB_TOKEN` is available; uses GitHub REST/Git Database API and does not persist the token.

## Intake: Classify Before Acting

Do not treat previous smoke-test examples as default formal requirements. 百日宴、护肤品、邀请函等 examples are only route-validation samples unless the current user request explicitly asks for them. For formal image generation, first extract the current request's real purpose, audience, subject, action, facts, brand/product constraints, style references, output size, and success criteria; then generate and QA against those current requirements.

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
| Invitation / 宴会请柬 / 百日宴 / 满月宴 | Generate decorated blank invitation card background → deterministic Chinese invitation typesetting → character QA | Card area must be blank; decorations stay around edges; never let model write event facts. |
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
2. ComfyUI with **JuggernautXL v9 as the default local visual-quality model** for commercial backgrounds, posters, product atmosphere, lifestyle images, and general high-quality image generation.
3. Qwen-Image/Qwen-Image-2512/Qwen-Image-Edit as the Chinese/special-route model: short Chinese text, poem/culture images, direct model-written Chinese tests, Chinese instruction understanding, and image-editing routes when installed.
4. SDXL Base only for compatibility/fallback and workflow baseline testing.
5. Do not use SD1.5/legacy low-quality models for AI图片制作 outputs or formal comparisons unless the user explicitly asks to see a historical/lowest baseline.

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

Reference: `references/github-node-capability-packaging.md` is mandatory when the user wants a GitHub link that others can forward to Hermes for installation. Use the shareable capability repo shape (`README.md`, `AUTO_INSTALL_FOR_HERMES.md`, `MANIFEST.yaml`, `installer/`, `runtime/`, `docs/`, `card/`) and dry-run the installer from a clean temp `HERMES_HOME`/`HERMES_IMAGE_RUNTIME` before claiming readiness. If the user provides another capability repo as an example, study its structure; do not install that unrelated capability unless explicitly requested. Do not call the GitHub deployment complete until `git push` has succeeded and the public repo/raw installer URL can be accessed; if GitHub auth is missing, say it is blocked on auth and keep the local commit/package ready.

Reference: `references/ai-image-creation-positioning-and-typography.md` is mandatory when the user comments on naming, scope, 小红书 over-emphasis, typography quality, title effects, or GitHub publication timing. It records the user-approved public name **AI图片制作**, the requirement for stronger artistic title treatments, and the rule to visually QA/get user confirmation before pushing packaging changes.

Reference: `references/executable-workflows.md` contains verified commands and scripts for real product-poster execution: JuggernautXL background generation, SAM product extraction, SVG typography compositing, and QA. Use it when the user asks to actually make a product poster.

Reference: `references/avatar-cartoon-workflow.md` contains the verified real-photo-to-anime/cartoon WeChat avatar workflow: square reference prep, ComfyUI img2img prompt/settings, denoise-strength choices, and QA for likeness plus circular-crop safety. Use it for 真人照片转动漫头像/卡通头像.

Reference: `references/text-edit-inpaint-workflow.md` contains the verified local inpaint smoke test and the workflow for 图片改字/旧字擦除/局部去物. It also records the current limitation: basic SDXL/Juggernaut inpaint can remove text but may leave a soft panel/scar, so commercial text edits need stronger cleanup or deliberate template reconstruction.

Reference: `references/upscale-repair-workflow.md` contains the verified 4× upscaling route using ComfyUI and `4x-UltraSharp.pth`, including command, artifact paths, and QA rules for 高清/印刷/大图 delivery.

Reference: `references/product-poster-routing-lessons.md` captures a correction from a real product-poster attempt: manual polygon/color-mask product cutouts are not reliable enough for commercial output; use proper segmentation/background-removal, inspect the cutout alone, and only then build the poster.

Reference: `references/poem-poster-workflow.md` is mandatory when creating 古诗配图/诗词海报 or any image that must include exact poem/literary text. It records the verified pattern: generate a no-text scene, reject or fully cover hallucinated calligraphy, render the poem with deterministic template text, and QA the exact characters/readability before delivery.

### 1. AI image creation / poster / 宣传图 / 封面图

### 1. AI image creation / poster / 宣传图 / 封面图 with readable text

For any final image that contains Chinese text, use **layout-first generation**, not “generate a full pretty image and paste text later”.

1. Clarify or infer: purpose, audience, exact copy, required ratio, and reading distance.
2. Build a rough layout skeleton before image generation:
   - title zone;
   - product/person/scene zone;
   - subtitle/selling-point zone;
   - CTA/date/location zone if needed.
3. Generate a **no-text** background or main visual with explicit safe typography space:
   - `large clean negative space`;
   - `blank area for title`;
   - `empty wall/sky/panel`;
   - `product placed lower/right/left, leaving top/side blank`;
   - always include `no text, no logo, no watermark, no letters, no symbols`.
4. If the generated image does not contain enough safe blank area, reject it and regenerate. Do **not** force text on top of busy content.
5. Choose a professional layout route:
   - existing Figma/template if available;
   - reusable SVG/HTML/Satori template if open-source route;
   - `scripts/render_text_poster.py` for a local deterministic commercial draft;
   - only use ad-hoc Pillow for inspection helpers or emergency drafts.
6. Before rendering text, sample the background palette and choose title/body/chip colors that belong to the image. Match shadow/glow/panel opacity to the scene light.
7. Add exact Chinese copy via deterministic text layer. Text-bearing images must never rely on model-generated Chinese as final copy.
8. Export platform size: 1080×1350, 1080×1440, 1242×1660, 1080×1920, square, etc.
9. Visually inspect final image at full size and phone scale: exact characters, no overflow, no fake background text, no pasted-on feel.
10. Send the actual exported image file directly.

### 2. Product poster / 商品图

Treat real-product posters as **asset-preservation compositing**, not pure image generation.

1. If the user provides a real product photo, that photo is ground truth. Never redraw/reimagine the product, package, logo, label, color, or shape unless explicitly asked.
2. First isolate the product with a proper segmentation/background-removal route:
   - SAM / RMBG / rembg / BiRefNet / ComfyUI segmentation nodes when available;
   - if unavailable, install/use one or clearly mark the result as draft quality.
3. Inspect the cutout alone before poster design. Reject if edges are jagged, halos remain, background residue exists, or product texture/logo is damaged.
4. Generate/select the background separately, with planned negative space for copy and a scene that supports the product category. Do not let the image model invent extra products, fake packages, fake labels, or pseudo text.
5. Composite the real product onto the background with matched contact shadow, reflection, edge feathering, color balance, and scale/perspective.
6. Add promotional copy through a template/layout layer, not by asking the image model to write Chinese.
7. QA product fidelity against the original: silhouette, color, material, logo/label, package details, visible texture, and proportions.
8. QA commercial quality: product cutout must look good even on a plain cream/white background; text must not cover key product features; no workflow/provenance notes.
9. Deliver final image, and when useful include a comparison/contact sheet for product-fidelity review.

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
- If the local runtime has no JuggernautXL/Qwen/SDXL-compatible model installed, do not fall back to SD1.5 or another legacy low-quality route. Install the proper profile or use a configured external image API.
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
