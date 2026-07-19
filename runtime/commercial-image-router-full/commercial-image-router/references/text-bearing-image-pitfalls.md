# Text-Bearing Image Pitfalls and Better Routes

These notes capture recurring lessons from image tasks where the generated visual was acceptable but the final image failed or nearly failed because of typography, fake model text, or pasted-looking copy.

## Durable lesson

For images with visible text, the deliverable is judged as a single designed object. A strong generated background does not compensate for weak font choice, poor hierarchy, cramped labels, fake model text, or copy that looks pasted on.

Use this route by default:

```text
clean no-text visual scene → intentional typography mode → deterministic text rendering → visual QA → delivery
```

## Prompting no-text backgrounds

When the final image will contain deterministic text, do not ask the image model for a “poster”, “invitation”, “poem”, “calligraphy”, “title area”, or “text area” unless the model is explicitly being used for baked-in text. Those words often trigger fake Chinese/English.

Better prompt pattern:

- Describe only the physical scene and mood.
- Say “blank wall/sky/negative space” rather than “space for text”.
- Strongly negative prompt: `text, Chinese characters, English letters, calligraphy, inscription, sign, poster, banner, logo, watermark, readable marks, fake words`.
- Visually reject any background containing pseudo text, even if the rest is attractive.

Example correction:

- Bad: “birthday dinner invitation poster background, area for Chinese typography” → produced fake invitation text.
- Better: “warm private dining room birthday celebration scene, blank dark warm wall, no posters, no wall writing” → clean background suitable for deterministic layout.

## Poem / classical text integration

Problem seen: hard parchment cards can be readable but visually违和 when the user wants the poem naturally in the image.

Default natural route:

1. Generate a clean no-text scene using only concrete imagery from the poem.
2. Add poem as low-opacity ink/title inscription over sky, mist, wall, stone, silk, or another naturally occurring surface.
3. Use a subtle wash behind text, not a visible card/frame.
4. Avoid floating seals in the middle of the scene; only use seals if anchored near the inscription and visually intentional.
5. If the background has fake calligraphy, regenerate a clean background instead of trying to hide it with translucent mist.

Hard card route is acceptable only for teaching slides, worksheets, or when readability is explicitly more important than natural integration.

## Birthday / invitation posters

For invitations, model-generated text is especially tempting and especially bad. Generate a clean party/dining scene first, then typeset all invitation details.

Required content checks:

- Event/occasion is present.
- Time/date is exact.
- Location is exact.
- Invite sentence and blessing/warm copy are present.
- Typography is festive but not cheap; avoid generic party-template clutter.

Recommended layout:

- Top small English/Chinese label with measured safe padding.
- Large elegant Chinese title.
- One warm invitation sentence.
- Distinct time/location block.
- 1–2 blessing lines.
- Optional bottom closing line.

## Product/commercial copy

Never put assistant workflow/provenance copy on a consumer-facing poster, e.g. “真实产品保留 / 模板排版 / 场景合成”. Keep process notes in the assistant response, not inside the image.

## Visual QA questions

Before sending any text-bearing image, ask visually:

1. Is the background clean of fake text?
2. Does the text belong to the scene or merely sit on top of it?
3. Is the font appropriate to the genre: product, poem, invitation, youth/social, tech?
4. Are labels/chips safely padded?
5. Is every character exact and readable at phone scale?
6. If the user has criticized typography in this thread, did I try a genuinely different typography route rather than small tweaks?
