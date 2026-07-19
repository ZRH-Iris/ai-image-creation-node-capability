# AI图片制作定位与标题字效规则

Use this reference when maintaining, packaging, or using the image-making Skill after user feedback about naming, platform positioning, typography, or layout quality.

## Naming / positioning

- User-approved public-facing name: **AI图片制作**.
- Avoid public names such as “商业图片生成”, “商业图片处理能力”, or “图片处理增强”; they either sound too narrow, too abstract, or not immediately understandable.
- The plain-language promise should be: **用 AI 生成、修改和制作图片**.
- Keep the Skill broad: generation, editing, product images, posters, covers, avatars, background replacement, text edits, upscale/repair, and layout.
- Do **not** position the capability as a 小红书-specific tool. 小红书 is only one optional platform style; mention it only when the user explicitly asks for that platform or when listing examples in a low-emphasis way.

## Typography / art title quality

User rejected plain, monotonous typography. For posters, covers, promotional graphics, product graphics, and capability cards:

1. Do not use plain system CJK text as the main title treatment.
2. Use a deliberate title-art treatment, combining at least two of:
   - display/heavy CJK font;
   - gradient fill;
   - thick outline/stroke;
   - drop shadow or glow;
   - sticker/label shape;
   - underline/highlight sweep;
   - 3D/extruded layer;
   - brush/calligraphy/title-display font when the scene fits.
3. Body text can remain clean and readable, but the main title must carry visual energy.
4. If the user says typography/layout is bad, treat it as a template/design-system failure. Switch template and title-art style; do not merely adjust font size/color.
5. QA must include “aesthetic typography” checks, not only technical checks such as no overflow/no garbled text.

## Pre-GitHub deployment rule

When packaging this Skill for GitHub distribution:

1. Update the local Skill and bundled runtime copy together.
2. Generate or update a visual sample that exercises the new visual/typography rule.
3. Run visual QA and installer dry-run locally.
4. Show the sample to the user for confirmation.
5. Only after user approval, commit and push to GitHub.

## Installer dry-run pitfall

If an installer wrapper supports `COMMERCIAL_IMAGE_RUNTIME_DRY_RUN=1`, it must pass `--dry-run` through to `setup_runtime.sh`; otherwise tests may unexpectedly clone/install/download large models instead of doing a safe package rehearsal.
