# Skill Maintenance and Regression Protocol

Use this protocol whenever this image skill itself is changed, expanded, or repaired. The user's expectation is not just better documentation: every claimed capability must be grounded in a run, a visible artifact, or an explicit limitation.

## When to run

Run this protocol after:

- Adding a new route, model, workflow, template, or script.
- Fixing a failure discovered during image generation/editing.
- User criticism about quality, typography, cropping, layout, cutout, or delivery.
- Any claim that a capability is now "ready", "跑通", "可测试", or "已解决".

## Required sequence

1. **Patch the class-level skill, not a one-off note**
   - Update `SKILL.md` only for durable router rules.
   - Put detailed commands, artifacts, and session-specific evidence into `references/`.
   - Put reusable probes/renderers into `scripts/`.

2. **Separate verified vs planned**
   - Verified means: a command/workflow ran successfully and produced an inspectable artifact.
   - Planned means: researched or designed but not yet executed.
   - Never let planned integrations read like available capabilities.

3. **Run a real smoke/regression test**
   - For generation: create at least one fresh image with the intended route.
   - For edit/inpaint/upscale: run the actual workflow on a small fixture or recent artifact.
   - For layout/template changes: render an output that contains realistic Chinese text and inspect for overflow/cropping.

4. **Visual QA before claiming success**
   - Use vision inspection or browser visual inspection as appropriate.
   - Specifically check: text overflow, garbled Chinese, watermarks, subject drift, edge artifacts, product fidelity, identity similarity, and platform crop safety.
   - If QA reveals an issue, fix and rerun; do not call the route solved.

5. **Audit the skill from the top**
   - Run:
     ```bash
     ${HERMES_IMAGE_RUNTIME:-$HOME/.hermes-image-runtime}/comfy-venv/bin/python ${HERMES_HOME:-$HOME/.hermes}/skills/creative/commercial-image-router/scripts/audit_skill.py
     ```
   - Expected result: `ok: true`, `failed_count: 0`.
   - If audit fails, fix the skill/reference/script mismatch and rerun.

6. **Record evidence concisely**
   - Update `references/local-runtime-status.md` with:
     - workflow/script used;
     - output artifact path;
     - what visual QA confirmed;
     - remaining limitation, if any.
   - Do not store credentials, tokens, or transient process IDs.

7. **Report honestly**
   - Tell the user what is verified, what still needs stronger tooling, and what was inspected.
   - If the final image/document is the deliverable, send it directly as a file attachment.

## Quality lessons from this session

- A text-safe template is mandatory: long Chinese copy must wrap, split into chips/cards, or shrink inside measured safe areas. Never place long copy as a single fixed SVG `<text>` line.
- Product-poster routes must inspect the cutout alone before compositing. White/gray edge residues are not acceptable.
- For image-skill improvements, a passing document update is insufficient. The skill must have a runnable audit plus at least one current smoke artifact.
- If the user says overall quality is "not enough", treat it as a system/template/method issue, not a minor color/font tweak.
