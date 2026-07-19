# Poster typography and style lessons

Updated: 2026-07-19

Use this reference when making product/Skill introduction posters, capability cards, and other public-facing graphics with Chinese text.

## What went wrong in the session

1. A small top label/pill had a fixed-width frame, but the English label text exceeded the frame.
2. The main title used a heavy LayerStyle stroke/beveled outline. It was technically readable, but visually too bulky for an enterprise/product poster.
3. A Qwen-generated light-style background included fake/generated text. It looked plausible at a glance but had to be rejected before layout.
4. The user asked for a new style after a polished dark-blue/gold version; the correct response was not a minor color tweak, but a materially different visual system.

## Durable rules

### 1. Measure or over-provision every framed text element

For top labels, chips, badges, and pills:

- Avoid fixed narrow boxes around unknown-length text.
- Give at least 24–32 px horizontal padding per side.
- For English all-caps labels with letter spacing, use more padding or make the pill substantially wider.
- Visually check that text does not touch, exceed, or visually crowd the border.
- If exact measurement is unavailable, remove the hard frame or use a wider translucent capsule.

### 2. Avoid heavy title outlines for enterprise/product posters

For enterprise, product, capability, or B2B posters, prefer:

- clean gradient fill;
- subtle shadow;
- thin dark stroke only when needed for contrast;
- small highlight line/accent;
- restrained glow.

Avoid by default:

- thick white outlines;
- chunky bevels;
- heavy metallic strokes;
- sticker-like borders;
- bulky 3D title effects.

Reserve heavy outlines for explicitly playful/Y2K/sticker/comic styles.

### 3. Never accept model-generated background text in no-text routes

When the final Chinese text will be rendered by the template layer, the image model should generate a no-text visual only. Reject and regenerate/switch background if the background contains:

- fake Chinese/English;
- pseudo UI labels;
- watermark-like marks;
- plausible but unreadable text.

Do not cover it with template text unless it is clearly outside the final crop or fully hidden.

### 4. “换个风格” means switch the visual system

When the user says “换个风格” after a poster iteration, do not just adjust colors. Change at least three of:

- palette, e.g. dark navy/gold → warm ivory/apricot/mint;
- composition, e.g. launch poster → editorial/magazine/workbench;
- card shape/layout, e.g. rigid panels → floating paper notes;
- title treatment, e.g. enterprise gradient → editorial display type;
- background metaphor, e.g. engine core → creative studio/toolbox;
- density and whitespace.

Keep the exact information architecture if it worked, but rebuild the visual language.

## QA checklist additions

Before sending:

- [ ] Top labels/chips have safe padding and no text-frame collision.
- [ ] Main title treatment matches the product style and is not overdecorated.
- [ ] No model-generated fake text remains in the background.
- [ ] If the user asked for a style change, the new version is visibly a different design direction, not a reskin.
