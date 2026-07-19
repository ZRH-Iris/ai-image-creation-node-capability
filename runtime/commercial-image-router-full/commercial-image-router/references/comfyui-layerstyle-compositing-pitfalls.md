# ComfyUI LayerStyle compositing pitfalls

Use this when building poster/cover routes that combine a generated no-text visual with Chinese title art via ComfyUI_LayerStyle.

## Durable lessons from the Harness product-poster run

1. **Always upload/overwrite the current input layer before rerunning LayerStyle.**
   - ComfyUI `LoadImage` reads the server-side `input/` copy, not necessarily the local file path you just edited.
   - If the workflow still loads an old filename such as `text_layer_ai_image_creation.png`, manually upload the new PNG to ComfyUI input with `overwrite=true` before running the workflow.
   - QA symptom of missing upload: output title remains from the previous poster even though the local text-layer file changed.

2. **Do not trust LayerStyle output to preserve alpha.**
   - In the verified route, LayerStyle output saved as a black-background RGB image.
   - Direct `ImageCompositeMasked` with the LayerStyle image's own alpha/mask may produce either a black rectangle or no visible title.
   - Working pattern:
     ```text
     LoadImage(background)
     LoadImage(layerstyle_title)
     ImageColorToMask(layerstyle_title, color=black)
     InvertMask
     ImageCompositeMasked(destination=background, source=layerstyle_title, mask=non_black_title_mask)
     SaveImage
     ```

3. **Visually inspect every intermediate after compositing.**
   - A workflow can execute successfully while producing the wrong title, a black panel, or missing title.
   - Required checks before delivery:
     - title text exactly matches user request;
     - no old/stale title remains;
     - no black-background artifact;
     - Chinese characters complete and not garbled;
     - title not clipped;
     - background still visible and not overwritten.

4. **Separate responsibilities.**
   - Qwen/FLUX/etc. generate the no-text main visual.
   - Template/SVG/Sharp/Satori renders exact Chinese information hierarchy.
   - LayerStyle is for title-art effects only, not full poster layout.

5. **If the user asks for a product/promotional image, deliver the file directly after QA.**
   - Do not stop at a path or claim the model route works.
   - For this user, final images must be sent as a Feishu `MEDIA:/absolute/path` attachment.
