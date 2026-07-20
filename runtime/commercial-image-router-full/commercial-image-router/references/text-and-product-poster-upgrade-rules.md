# Text Poster and Product Poster Upgrade Rules

This reference exists because single-image generation can look acceptable while **text-bearing posters** and **real product posters** still fail commercially. Use it whenever the user asks for 带字海报、商品宣传图、产品图、主图、封面、招生图、活动图, or says the poster/product image is “差点意思”.

## A. Text-bearing images: layout first, image second

Never generate a visually full image first and then hunt for a place to paste text. The workflow must be:

```text
copy + ratio + platform
→ layout skeleton
→ no-text background with planned blank typography space
→ deterministic Chinese typography
→ full-size and phone-scale QA
```

### Required pre-generation layout skeleton

Before generating the background, decide:

1. Title zone — top/left/right/center.
2. Hero zone — product/person/scene position.
3. Supporting copy zone — subtitle, chips, features.
4. CTA/info zone — bottom or badge.
5. Forbidden zones — face, product label, logo, important texture.

If this skeleton is missing, the image will usually look like a pretty background with pasted-on text.

### Prompt rules for no-text backgrounds

The background prompt must describe safe typography space explicitly:

- `large clean negative space at the top`;
- `blank area on the left for title`;
- `empty warm wall surface`;
- `clean misty sky area with no calligraphy`;
- `product placed in lower right, leaving upper left blank`;
- `no text, no logo, no watermark, no letters, no symbols, no signage`.

For poem/culture scenes, avoid words like `calligraphy`, `inscription`, or `Chinese typography` in the image-generation prompt unless you also strongly say blank/no text; those words often cause fake characters.

### Typography rendering route

For local deterministic draft rendering, use:

```bash
/opt/hermes/.venv/bin/python scripts/render_text_poster.py \
  --background /path/to/no_text_bg.png \
  --output /path/to/final_poster.png \
  --mode luxury \
  --kicker 'LUMIÈRE SKINCARE' \
  --title '凝光焕颜' \
  --subtitle '奢宠精华礼盒' \
  --body '晨光凝露质感，点亮肌肤自然光泽' \
  --cta '新品上市 · 限时臻享' \
  --chips 深层润泽 柔光肤感 礼盒套装 \
  --footer '臻选礼赠 · 温柔开启护肤仪式'
```

Modes:

- `luxury` — skincare, jewelry, premium lifestyle, elegant commercial.
- `product` — general product poster.
- `editorial` — magazine/cover/lifestyle.
- `culture` — poem/cultural/warm humanistic.
- `tech` — digital/product/AI/enterprise.

This renderer is a baseline, not the ceiling. If a Figma/Canva/Satori template is available for the category, use that instead.

### Text QA rejection criteria

Reject and redo when:

- the background lacks enough safe blank space;
- text covers a face/product/logo/important visual;
- title color is unrelated to the image palette;
- cards/chips look like generic SaaS components on a commercial scene;
- Chinese characters overflow, touch borders, or are too small on a phone;
- the image contains fake background text or pseudo-calligraphy near the real text;
- typography feels pasted on rather than designed into the image.

If the user says “文字不搭/违和/像贴上去”, do not just change font size. Regenerate or relayout with a new skeleton and palette.

## B. Invitation / banquet / announcement cards: blank card first

For invitations such as 百日宴、满月宴、生日宴、婚礼请柬、升学宴、乔迁宴、活动邀请函, the successful route is a **decorated blank card plus deterministic Chinese typesetting**. Do not ask the image model to write the invitation text.

```text
event facts
→ centered/side blank invitation card area
→ no-text decorated background
→ deterministic Chinese invitation typography
→ character-by-character QA
```

### Required invitation facts

If user provides facts, use them exactly. If this is a sample and facts are incomplete, infer tasteful placeholders but do not invent names unless the user asks.

Typical fields:

- event name: e.g. 宝宝百日宴 / 满月宴 / 婚礼邀请 / 生日派对;
- date/time;
- venue/address;
- host/baby/couple/name if provided;
- blessing or invitation sentence.

### Invitation background prompt rules

Prompt the image model for a **blank physical invitation card area**:

- `large clean blank rounded invitation card in the center`;
- `card area completely empty, no letters, no symbols`;
- `decorations around the edges only`;
- `soft clouds / balloons / ribbons / flowers / stars` for baby banquet;
- `cream white, pale pink, champagne gold, warm bokeh` for 百日宴/满月宴;
- `no text, no logo, no watermark, no letters, no symbols, no fake characters`.

The most important quality rule from the verified 百日宴 run: **the card itself must be blank and calm; decoration belongs around the border, not behind the text.** The user explicitly said the result was much better after this route; treat that as the preferred baseline for future invitation/card work.

### Invitation typography rules

Use a gentle formal hierarchy:

1. small invitation mark: `诚邀莅临` / `INVITATION` only if English is appropriate;
2. main event title: e.g. `宝宝百日宴`;
3. short subtitle: e.g. `百日宴宴请 · 共赴成长之喜`;
4. blessing block, 2–4 centered lines;
5. time and venue as clear rounded info rows/cards;
6. closing invitation line.

For baby invitations, prefer warm brown/champagne-gold text, Noto Serif CJK or a soft Song/Ming-style font for title, Noto Sans CJK for details, and very soft shadows only. Avoid loud red/gold wedding style, cartoon clutter, cheap clip-art, and dense stickers.

### Local invitation renderer

Use `scripts/render_invitation_card.py` for deterministic local rendering when the background already has a blank card area:

```bash
/opt/hermes/.venv/bin/python scripts/render_invitation_card.py \
  --background /path/to/blank_invitation_bg.png \
  --output /path/to/final_invitation.png \
  --event '宝宝百日宴' \
  --subtitle '百日宴宴请 · 共赴成长之喜' \
  --date '8月2日' \
  --venue '世纪大酒店' \
  --blessing '愿宝贝健康成长' '平安喜乐，聪明可爱' '一生被爱与温柔环绕'
```

### Invitation QA rejection criteria

Reject and redo when:

- the card area contains fake text or decorative texture that competes with text;
- the event type is unclear;
- date or venue is missing/wrong;
- blessing lines are cramped or too small;
- text touches card edges;
- decorations cover text;
- the style is cheap, noisy, or too cartoonish for a family invitation.

## C. Product images: preserve real assets, do not redraw them

For real product images, the route is not pure text-to-image. It is asset-preserving compositing:

```text
real product photo
→ segmentation/cutout
→ cutout QA
→ background generation/selection with text space
→ product compositing with shadow/reflection/color match
→ deterministic typography
→ product-fidelity QA
```

### When product is supplied by user

Hard rules:

1. The real product photo is ground truth.
2. Do not ask an image model to redraw the product/package/logo/label.
3. Do not change product color, silhouette, material, label, logo placement, or visible texture.
4. If the product cutout is weak, fix segmentation before designing the poster.

### Cutout QA

Inspect the product on a plain light background before final composition. Reject if:

- halo/background residue remains;
- edges are jagged or melted;
- transparent holes cut into product texture;
- logo/label is damaged;
- color shifts from the source;
- fabric/metal/glass material is lost.

### Background and composition rules

- Generate/select background separately from the real product.
- Prompt the background with no products unless you intentionally want props; otherwise the model invents fake duplicate products.
- Match contact shadow and scale so the product sits naturally.
- Add a soft grounding shadow/reflection for cosmetics, bottles, cups, electronics, and packaging.
- Keep copy away from the product label and hero details.

### Commercial-quality rejection criteria

Do not call a product poster commercial-grade if:

- the product cutout would look bad on a plain cream/white background;
- the product is model-generated rather than the user’s actual product when the user supplied a photo;
- fake labels/products/text appear in the background;
- typography contains workflow notes, technical terms, or assistant-process language;
- the result is a nice generic image but no longer represents the actual product.

## D. If no real product photo is supplied

Then it is a generic product-style concept image, not a faithful product poster. Say or imply that honestly:

- okay: “无品牌护肤品概念海报 / generic skincare concept poster”;
- not okay: pretending it is the user’s actual商品图.

For generic product concepts, image generation may create the product, but final Chinese still goes through deterministic typography.

## E. Minimal smoke test after changing these routes

Use an existing no-text background and render a Chinese text poster:

```bash
/opt/hermes/.venv/bin/python scripts/render_text_poster.py \
  --background /opt/data/cache/images/openai_codex_gpt-image-2-high_20260720_055234_5646e1a2.png \
  --output /tmp/text_poster_smoke.png \
  --mode luxury \
  --kicker 'LUMIÈRE SKINCARE' \
  --title '凝光焕颜' \
  --subtitle '奢宠精华礼盒' \
  --body '晨光凝露质感，点亮肌肤自然光泽' \
  --cta '新品上市 · 限时臻享' \
  --chips 深层润泽 柔光肤感 礼盒套装 \
  --footer '臻选礼赠 · 温柔开启护肤仪式'
```

Then visually inspect for text correctness, overflow, product obstruction, color harmony, and pasted-on feeling.
