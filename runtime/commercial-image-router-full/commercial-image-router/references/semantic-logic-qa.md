# Semantic and Logic QA for Generated Images

Use this before delivering generated or edited images. Many AI images look beautiful but fail because the scene is logically wrong. QA must inspect meaning, relationships, physics, anatomy, and factual consistency — not only artifacts.

## Core rule

Before delivery, ask:

```text
Does the image actually depict the requested scene, in a way that makes real-world/common-sense sense?
```

If the answer is no, regenerate or change route. Do not deliver a beautiful but illogical image.

## Mandatory logic checklist

### 1. Requirement fulfillment

- Does the subject match exactly? e.g. dragonfly vs butterfly, baby banquet vs wedding, product poster vs generic beauty image.
- Does the requested action happen clearly? e.g. tail touching water for 蜻蜓点水, hand-holding, eating, pouring, opening, presenting.
- Are all required entities present? e.g. product + background + text; time + venue + event name for invitations.
- Are there extra entities that change meaning? e.g. fake second product, extra baby/name, extra signage, fake logo.

### 2. Spatial and physical logic

- Do objects sit on surfaces instead of floating?
- Are shadows/contact points consistent with placement?
- Is scale plausible? e.g. baby, furniture, insects, products, hands.
- Are reflections/water/ripples consistent with the action?
- Does perspective make sense? no impossible table/product/body angles.

### 3. Anatomy and object structure

- Humans: hands, fingers, arms, eyes, glasses, face symmetry, extra limbs, broken joints.
- Animals/insects: correct body plan, legs/wings/tail, action-specific pose.
- Products: bottle/cap/dropper/package geometry, logo/label placement, no melted edges.
- Vehicles/tools/food: recognizable object structure, no fused or duplicated parts.

### 4. Factual and text consistency

- Text exactly matches requested facts: event, date, venue, name, price, phone, address, poem.
- No model-generated fake text, pseudo Chinese/English, fake watermark, fake signage.
- If date/time/location appears multiple times, all instances match.
- The image context matches the text: a 百日宴 invite should not look like a wedding poster unless intended.

### 5. Narrative and audience logic

- Is the tone appropriate for the audience? baby invitation = warm/clean; principal/investor training = professional; child image = safe and gentle.
- Does the visual metaphor support the message, or just look pretty?
- Is the main message immediately understandable without reading an assistant explanation?

## Category-specific logic gates

### Invitation / event card

- Event type is visually and textually clear.
- Date and venue are present and readable.
- Decorations match the event: baby banquet should avoid loud wedding red/gold unless requested.
- Card area remains calm; decorations do not compete with text.
- No extra fake names, fake QR codes, fake venue signage, or generated invitation text.

### Product image / product poster

- If user supplied a product, the visible product must come from the real photo, not AI re-creation.
- No second fake product in background.
- Product sits naturally with contact shadow/reflection.
- Scale and perspective are plausible.
- Product label/logo/package details are not altered or covered by text.
- Selling points must match what is shown; do not imply unavailable functions/effects.

### Animal / idiom / action scene

- Verify the action, not only the noun. For example:
  - 蜻蜓点水: dragonfly abdomen/tail touches water and ripples appear.
  - 鱼跃龙门: fish clearly leaps through/over a dragon gate, not just near a gate.
  - 鹏程万里: bird/roc visual should communicate flight and vast distance.
- Reject if creature anatomy is ambiguous or wrong.
- Reject if the action is only implied by title but not visible.

### People / portrait / avatar

- No extra fingers, fused hands, crossed/unnatural arms, distorted ears/glasses.
- If based on a real person, preserve stable traits.
- If for avatar, crop-safe and not too close.
- Age/tone must match request.

### Education / training / concept poster

- Visual should express the concrete teaching/training scenario, not generic AI icons.
- Avoid abstract floating UI unless requested.
- If the target is principals/bosses/investors, avoid hobbyist/tech-fan aesthetics.

## QA prompt template for vision inspection

When using `vision_analyze`, ask category-specific questions. Example:

```text
Strictly inspect this image for semantic/logical correctness before delivery.
Request: <paste user request/facts>.
Check: required subject/action/entities; factual text; spatial physics; anatomy/object structure; extra or missing objects; tone/audience fit; watermarks/fake text. List pass/fail and any reason to regenerate.
```

Do not ask vague questions like “is it good?” Ask about the exact requested logic.

## Regeneration rules

Regenerate or change route if:

- the required action is not clearly visible;
- object anatomy/structure is wrong;
- factual text is missing/wrong;
- background contains fake text/logos/watermarks;
- scene meaning contradicts the request;
- the image would require a long explanation to justify.

If the same logic failure happens twice, change route:

- add stronger spatial/action wording to prompt;
- generate a composition sketch or layout first;
- use reference/control image;
- use deterministic compositing instead of pure generation;
- switch model/tool.

## Delivery rule

Do not deliver a generated image until the final artifact has passed both:

1. visual artifact/layout QA;
2. semantic/logical QA.

For this user, if there is any doubt, make another variant or explicitly say the route is draft-quality rather than sending an unverified image.
