# Typography System for Commercial / Poem / Poster Images

This file is mandatory when the generated/edited image contains visible text. The current image generation quality is acceptable; the weak point is typography and layout. Treat text-heavy images as layout/design tasks, not only image-generation tasks.

## Core principle

For any image with Chinese text:

```text
visual generation/editing → typography design system → visual QA → delivery
```

Never assume that placing text on top of a generated picture is enough.

## Font tiers

### Tier A — currently available and safe

Use these when no extra font has been installed:

- `Noto Sans CJK SC` — clean body, labels, commercial/product copy.
- `Noto Serif CJK SC` — poems, cultural material, elegant long text.
- Avoid WenQuanYi/Unifont for final commercial posters unless no other choice.

### Tier B — should be installed for better design range

Recommended display/style fonts:

- 得意黑 / SmileySans — youthful, poster titles, social covers.
- 阿里妈妈数黑体 / Alimama ShuHeiTi — strong commercial title, product posters.
- 阿里巴巴普惠体 / Alibaba PuHuiTi — modern commercial body/title.
- HarmonyOS Sans SC — clean digital/product UI style.
- 霞鹜文楷 / LXGW WenKai — poem, cultural, warm humanistic scenes.

If a poster feels “字体不高级/不自然/像系统字”, switch font family and layout style, not just size/color.

## Type hierarchy rules

### Product/commercial poster

- Kicker/label: 20–26px, generous pill padding, not tight.
- Main title: 72–120px depending on canvas; no bulky default stroke.
- Subtitle: 34–48px, max 1–2 lines.
- Selling points: 24–32px, split into chips/cards; never cram long copy into one line.
- Bottom info: 24–32px, consumer-facing only; no process notes.

### Poem / 古诗配图

- Prefer text integrated with scene: sky, mist, wall, silk, paper texture already in the image.
- Do not default to hard white/parchment cards unless user wants teaching-material readability.
- For natural poem images:
  - Use `Noto Serif CJK SC` or a calligraphic/wenkai font when available.
  - Use opacity 0.68–0.86, soft shadow/highlight only.
  - Add a very subtle mist/sky wash behind text, not a visible box.
  - Keep line spacing wide enough for reading.
- If full poem is long and vertical text becomes cramped, either use horizontal poem block integrated into a natural surface, or make the image larger/less dense.

### Social / 小红书 style

- One sharp headline; do not overfill.
- Use bold display title + 2–4 short chips.
- Keep mobile readability: small text must remain readable at phone size.
- Avoid generic four-card SaaS layouts unless the requested style is explicitly tech/product briefing.

## Text integration modes

Choose one intentionally:

1. **Natural inscription** — poem/quote appears as ink in sky, mist, wall, scroll, paper, stone, or water reflection.
2. **Editorial overlay** — magazine-style title and neat supporting text, no heavy frames.
3. **Commercial poster system** — strong title, subtitle, selling chips, CTA/info panel.
4. **Teaching material card** — highly readable panel, allowed to be less natural.
5. **Sticker/Y2K style** — playful thick outlines and labels, only for trendy youth poster requests.

Do not mix modes accidentally.

## Hard failure cases

Reject and redo when:

- Text looks pasted on rather than belonging to the scene.
- Font choice is visibly system/default/cheap for the image style.
- A label/chip frame touches or is exceeded by text.
- Title has heavy stroke/bevel that does not match the style.
- Generated background contains fake characters or pseudo-calligraphy near real text.
- Prompt wording such as “poster”, “invitation”, “calligraphy”, “text area”, or “Chinese typography” caused the background model to create fake text; regenerate using physical-scene-only wording and a blank wall/sky/negative-space description.
- Poem text is correct but too cramped to read naturally.
- A poem/classical text is placed on a hard card when the desired feel is natural scene integration; switch to subtle ink over mist/sky/wall unless readability/worksheet format is the explicit goal.
- The poster contains workflow/provenance notes meant for the assistant report.

## QA checklist before sending

1. Read every character aloud against the intended copy.
2. Check title, author, punctuation, and line breaks.
3. Inspect at full size and phone-scale.
4. Check no card/pill/frame overflow.
5. Check text/background contrast.
6. Ask: “Does this text feel designed into the image, or merely placed on top?” If placed on top, redesign.
7. If user criticized typography once in the current thread, create at least one more distinct typography route before final delivery.
