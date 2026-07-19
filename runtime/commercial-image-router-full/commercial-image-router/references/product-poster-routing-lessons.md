# Product Poster Routing Lessons

## Context

A user supplied a real product photo of a warm yellow mountain-shaped cushion with subtle grey/silver Chinese landscape jacquard patterns and asked for a commodity宣传图. The important durable lesson is not the specific cushion, but the route for real-product posters.

## What Went Wrong

A fast deterministic poster was produced by manually tracing/cropping the product and composing a warm e-commerce-style layout. Even after QA fixes, this route had clear limitations:

- Manual polygon/color masks are too brittle for fabric/product edges.
- Color-threshold refinement can accidentally damage grey/silver embroidery or product texture.
- A decent poster layout is not enough if the product cutout looks visibly rough.
- Product posters need better extraction/compositing than a quick Pillow mask before being considered commercial-grade.

## Correct Future Route

For real product posters, use this priority order:

1. **Preserve original product as ground truth.** Never redraw the product/package/logo unless explicitly asked.
2. **Use a proper segmentation/background-removal route first**, not a hand-traced polygon:
   - SAM / RMBG / rembg / BiRefNet / ComfyUI segmentation nodes when available.
   - If automatic segmentation is not installed, install/use an appropriate segmentation tool or ask for a cleaner product photo before claiming commercial quality.
3. **Inspect the cutout alone** before designing the poster:
   - product silhouette intact;
   - no wall/bed/background residue;
   - embroidery/texture not cut out;
   - edges not jagged or haloed.
4. **Then generate or choose a scene/background** that supports the product, and composite with shadows/contact/reflection.
5. **Use a template/layout layer** for title, selling points, tags, price/date if needed.
6. **QA against the original photo** for product drift: color, shape, texture, logo/tag, package details.

## Practical QA Rule

For product posters, do not send the final image if either is true:

- the cutout would look bad on a plain white/cream background;
- the product’s original visible texture/pattern has been removed or punched through by the mask.

If the available source photo is too cluttered or low-quality, say so directly and request/produce a draft-level result, but do not describe it as commercial-grade.
