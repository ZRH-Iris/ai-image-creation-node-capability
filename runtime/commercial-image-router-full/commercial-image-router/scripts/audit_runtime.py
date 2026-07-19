#!/usr/bin/env python3
"""Audit local runtime for AI图片制作.
Checks ComfyUI server, LayerStyle nodes, official workflow templates, and key local model files.
"""
from __future__ import annotations
import json, os, sys, urllib.request, pathlib

HOST=os.environ.get('COMFYUI_HOST','http://127.0.0.1:8188')
RUNTIME_ROOT=pathlib.Path(os.environ.get('HERMES_IMAGE_RUNTIME', str(pathlib.Path.home()/'.hermes-image-runtime')))
VENV=RUNTIME_ROOT/'comfy-venv'
TEMPLATE_DIR=next(iter((VENV/'lib').glob('python*/site-packages/comfyui_workflow_templates_json/templates')), VENV/'lib/python3.12/site-packages/comfyui_workflow_templates_json/templates')
MODEL_BASE=RUNTIME_ROOT/'comfy-workspace/models'

def get_json(url):
    with urllib.request.urlopen(url, timeout=10) as r:
        return json.load(r)

result={'ok': False, 'host': HOST, 'checks': {}, 'missing': []}
try:
    stats=get_json(HOST+'/system_stats')
    result['checks']['comfyui_running']=True
    result['checks']['comfyui_version']=stats.get('system',{}).get('comfyui_version')
except Exception as e:
    result['checks']['comfyui_running']=False
    result['missing'].append(f'ComfyUI not reachable: {e}')

try:
    obj=get_json(HOST+'/object_info')
    required_nodes=['LayerStyle: GradientOverlay','LayerStyle: Stroke','LayerStyle: DropShadow','LayerStyle: OuterGlow','LayerUtility: ColorImage','LoadImage','SaveImage']
    miss=[n for n in required_nodes if n not in obj]
    result['checks']['layerstyle_nodes_loaded']=not miss
    result['checks']['layerstyle_missing_nodes']=miss
    if miss: result['missing'].append('LayerStyle missing nodes: '+', '.join(miss))
except Exception as e:
    result['checks']['layerstyle_nodes_loaded']=False
    result['missing'].append(f'object_info failed: {e}')

important_templates=['image_qwen_Image_2512.json','image_qwen_image_edit_2511.json','flux_kontext_dev_basic.json','api_openai_gpt_image_2_t2i.json','api_google_nano_banana2_text_to_image.json','templates-product_ad-v2.0.json','template_product_placement.json','templates-product_scene_relight.json']
existing=[t for t in important_templates if (TEMPLATE_DIR/t).exists()]
result['checks']['official_templates_found']=existing
missing_templates=[t for t in important_templates if t not in existing]
if missing_templates: result['missing'].append('missing templates: '+', '.join(missing_templates))

model_files={
 'qwen_text_encoder': MODEL_BASE/'text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors',
 'qwen_vae': MODEL_BASE/'vae/qwen_image_vae.safetensors',
 'qwen_2512_unet': MODEL_BASE/'diffusion_models/qwen_image_2512_fp8_e4m3fn.safetensors',
 'qwen_2512_lightning_lora': MODEL_BASE/'loras/Qwen-Image-2512-Lightning-4steps-V1.0-fp32.safetensors',
}
models={}
for k,p in model_files.items():
    models[k]={'exists':p.exists(), 'size_gb': round(p.stat().st_size/1e9,3) if p.exists() else 0, 'path':str(p)}
result['checks']['qwen_2512_models']=models
if not all(v['exists'] and v['size_gb']>0.001 for v in models.values()):
    result['missing'].append('Qwen-Image-2512 model set incomplete')

result['ok']=not result['missing']
print(json.dumps(result, ensure_ascii=False, indent=2))
sys.exit(0 if result['checks'].get('comfyui_running') and result['checks'].get('layerstyle_nodes_loaded') else 1)
