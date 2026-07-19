# Poem and Classical-Literature Image Posters

Use when the user asks for 古诗配图 / 诗词海报 / a poem image that must include the poem text plus a matching scene.

## Durable lesson from real runs

Diffusion models often hallucinate fake calligraphy when prompted with Chinese poetry, even when the prompt says `no text`. Treat this as a common failure mode, not a surprise. The final poem text must be rendered by the deterministic layout/template layer.

## Recommended workflow

1. **Generate a no-text scene background**
   - Prompt for the poem's imagery and mood, not the exact Chinese text.
   - Add strong negatives: `text, Chinese characters, calligraphy, letters, watermark, signature, logo`.
   - For 《登高》-type scenes, include concrete visual anchors: late autumn, high cliff/terrace, scholar looking into distance, falling leaves, broad river/江水, birds, misty mountains.

2. **Inspect the raw background before layout**
   - If the model produced fake Chinese/calligraphy/watermark marks, do not deliver it.
   - Either regenerate, crop away the fake text, or cover it with an opaque designed poem card.
   - Translucent covers are risky: fake characters may remain visible through the panel. Use an opaque parchment/paper card or hard cover strip when hiding model text.

3. **Render the poem deterministically**
   - Use SVG/HTML/Satori/sharp/Pillow text layers, never the image model, for the final poem text.
   - Use exact public-domain poem text and author. Verify every character manually or against a trusted source when uncertain.
   - For readability, prefer horizontal lines in a parchment card unless vertical calligraphy is specifically requested and has been visually validated.
   - Vertical layouts are easy to make unreadable or visually jumbled; if visual QA says the poem is hard to read, switch to horizontal text rather than tweaking spacing only.

4. **Composition guidance**
   - Keep the scenery and poem panel clearly separated: scene on one side, poem card on the other, or poem card floating over a low-detail area.
   - Avoid placing long poem text over busy trees, rocks, water, or high-contrast sky.
   - For classical poetry, good visual systems include parchment cards, ink-like serif CJK fonts, warm paper gradients, subtle seals, and restrained borders.

5. **QA before delivery**
   - Poem title and author are present if requested.
   - Full poem text is complete, no wrong characters, no missing punctuation when punctuation is used.
   - No clipping, overlap, out-of-frame text, or cramped lines.
   - Any model-generated fake calligraphy/text from the background is fully invisible, not merely faded.
   - The scene actually matches the poem's concrete imagery, not just a generic pretty landscape.

## Example: 《登高》

Final text used in the verified poster:

```text
登高
杜甫

风急天高猿啸哀，
渚清沙白鸟飞回。
无边落木萧萧下，
不尽长江滚滚来。
万里悲秋常作客，
百年多病独登台。
艰难苦恨繁霜鬓，
潦倒新停浊酒杯。
```

The first background run contained hallucinated calligraphy in the upper-right. The successful fix was to cover the entire contaminated right/top area with an opaque parchment region plus a poem card, then render clear horizontal poem text on top. The final QA gate checked both the poem text and that the fake background characters were completely hidden.
