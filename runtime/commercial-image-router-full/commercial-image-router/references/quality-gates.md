# Quality Gates and Iteration Rules

Use this checklist before sending any image file. The user has repeatedly rejected unverified or rough outputs; therefore QA is part of production, not an optional afterthought.

## Global QA gate

Before delivery:

1. **Open the final file visually** with `vision_analyze` or browser screenshot.
2. **Check exact requirements**: subject, action, date, place, audience, copy, ratio.
3. **Check artifacts**: watermarks, random letters, extra limbs, broken hands, distorted eyes, fake text, strange objects.
4. **Check composition**: no important content cropped, no text collision, no unreadable contrast, no clutter.
5. **Check output file**: correct dimensions, file exists, can be opened.
6. **Send file directly** via Feishu using `MEDIA:/absolute/path`.

## Text and layout QA

Mandatory when final image contains text:

- If the image itself is good but typography/font/layout is weak, the output still fails. Text quality is part of the image, not a secondary decoration.

- Text content exactly matches user-provided copy.
- Chinese is rendered by deterministic font/layout layer, not hallucinated by the model, unless using a verified visual-text model intentionally.
- No text overflow, clipping, overlap, cropped descenders, or text outside its card/panel.
- Long Chinese copy is wrapped, split into multiple lines, or converted into chips/cards.
- Mobile readability: title large; body not too small; contrast high enough over background.
- If using SVG: avoid unmeasured long single-line `<text>` in fixed boxes. Prefer `<tspan>` wrapping or separate pill/card components.
- Top labels/pills/chips must be measured or given generous safe width. A text pill/frame must have at least 24–32px horizontal padding on each side and never let letters touch or exceed the border.
- Do not default to heavy title outlines or thick beveled strokes for enterprise/product posters. Use clean gradient fill, subtle shadow/glow, or thin dark stroke; reserve thick outlines for playful/Y2K/sticker styles only.
- Reject no-text model backgrounds that contain fake Chinese/English, pseudo-UI labels, watermark-like marks, or unreadable generated text; regenerate or switch background before layout.
- If the user asks to “换个风格”, change the visual system, not just the palette: composition, card language, title treatment, metaphor, and density should visibly differ.
- If the user says text “超格/出框/字体土/描边太粗/不好看”, patch the template and record the lesson.

## Poem/classical-literature poster QA

Mandatory when the final image includes a poem, quote, couplet, or classical text:

- The poem/quote is rendered by deterministic text layout, not by the image model.
- Title, author, poem text, and punctuation exactly match the intended source.
- If the generated background contains fake calligraphy/Chinese/letters, it must be regenerated, cropped away, or fully covered with an opaque designed panel. A translucent panel is not enough if fake characters remain visible.
- Prefer readable horizontal poem text unless vertical calligraphy was specifically requested and visually validated.
- The scene must match concrete imagery from the poem, not just a generic landscape.

## Product/commercial QA

Mandatory when the image contains a real product:

- Product shape/color/pattern/logo match the original.
- Product was not regenerated as an AI approximation.
- Cutout inspected alone on checkerboard or solid contrast background.
- No white/gray/black fringe, background scraps, holes, or jagged edge.
- Contact shadow and scale make product feel placed, not pasted.
- Background does not contain a second fake product competing with the real product.
- Model-generated backgrounds for product posters must be rejected if they contain fake readable text, pseudo-Chinese, watermarks, logos, or a hallucinated version of the product, even if the rest of the scene looks good.
- Product-poster copy must be consumer-facing. Do not place workflow/provenance/process notes such as “真实产品保留 / 场景合成 / 模板排版” on the final image; keep those in the assistant report.
- Product does not cover important text and text does not cover key product details.

If cutout is bad:

1. Add background/negative prompt points in SAM.
2. Try a tighter/looser box.
3. Try alternate segmentation route.
4. If still bad, use a designed photo-card layout preserving the original photo instead of pretending it is cleanly cut out.

## Poster/social QA

- For poem/古诗配图, text should feel integrated into the image, not pasted on a hard card by default. Prefer natural inscription treatments: mist/sky wash, wall/scroll texture already present in the scene, subtle vertical calligraphy/title marks, or low-opacity ink over negative space. Use a hard parchment/card only when the design intentionally calls for a teaching slide or readable worksheet.
- If a generated poem background contains fake calligraphy or model-made pseudo text, reject it and regenerate a clean no-text background before adding deterministic poem text.
- One visual focus and one primary message.
- Audience is reflected in tone/style.
- Dates, locations, prices, sign-up info are exact.
- Ratio is platform-appropriate.
- No busy background behind critical text.
- No cheap template feel: adjust hierarchy, spacing, and image crop until it looks intentional.

## Avatar/person QA

- Reference traits preserved: glasses, hair, face shape, age, gender presentation, expression, vibe.
- Clearly stylized if user requested cartoon/anime; not just a beautified photo.
- Square output with safe circular crop margin.
- Eyes/glasses are not broken; no extra face artifacts.
- Background supports avatar use and does not include distracting objects.

## Animal/character QA

- Species and action are clear.
- For animal actions with real-world anatomy/behavior, inspect biology, not just vibes. Example: “蜻蜓点水” must show a realistic dragonfly body plan, actual tail/abdomen contact with water, and visible ripples. If the result looks like a generic hovering insect, a standing pose, or a deformed creature, it fails.
- Interaction is visible, e.g. hand-holding, eating, tail touching water.
- No watermark/text.
- No scary or adult tone for child-friendly image requests.
- For copyrighted living/active characters or franchise IPs, do not create 1:1 replicas. Route to original character work with similar high-level traits.
- When the scene is a well-known action idiom (蜻蜓点水, 鱼跃龙门, 叶公好龙, etc.), verify the action is visually correct, not only the noun.

## Repair/upscale QA

- Sharpness improved without plastic overprocessing.
- Faces/products/logos not distorted.
- No tiling/seams after upscaling/outpainting.
- Compare before/after when the edit might be subtle.

## Iteration rules

- If one variant fails, generate at least one alternative before delivering if time permits.
- If the same failure happens twice, change route/tool/template/model, not just seed.
- User criticism overrides your confidence. Record recurring issues in the skill immediately.
- Do not hide limitations. If a route is only draft-quality, say so and propose/perform the stronger route.
