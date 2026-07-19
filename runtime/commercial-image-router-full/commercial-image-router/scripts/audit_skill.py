#!/usr/bin/env python3
"""Audit commercial-image-router for structure, linked files, runtime deps, and known quality rules."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except Exception:
    yaml = None

BASE = Path(__file__).resolve().parents[1]
OS = __import__('os')
RUNTIME_ROOT = Path(OS.environ.get('HERMES_IMAGE_RUNTIME', str(Path.home() / '.hermes-image-runtime')))
COMFY_HELPERS = Path(OS.environ.get('COMFY_HELPERS_DIR', str(RUNTIME_ROOT / 'comfy-helpers')))
if not (COMFY_HELPERS / 'scripts' / 'check_deps.py').exists():
    for candidate in [
        BASE.parent / 'comfy-helpers',
    ]:
        if (candidate / 'scripts' / 'check_deps.py').exists():
            COMFY_HELPERS = candidate
            break
COMFY_WORKSPACE = Path(OS.environ.get('COMFY_WORKSPACE', str(RUNTIME_ROOT / 'comfy-workspace')))
REQUIRED_REFS = [
    'implementation-stack.md',
    'ai-image-creation-sota-stack.md',
    'universal-routing-map.md',
    'quality-gates.md',
    'local-runtime-status.md',
    'capability-backlog.md',
    'executable-workflows.md',
    'avatar-cartoon-workflow.md',
    'text-edit-inpaint-workflow.md',
    'upscale-repair-workflow.md',
    'product-poster-routing-lessons.md',
]
REQUIRED_SCRIPTS = [
    'sam_product_extract.py',
    'compose_product_poster.js',
    'make_inpaint_smoke_test.py',
    'audit_skill.py',
]
REQUIRED_PHRASES = [
    'No text overflow',
    'Product pixels come from the real user photo',
    'QA',
    '4x-UltraSharp.pth',
    'SAM ViT-B',
    'Noto CJK',
    'do not reproduce them exactly',
]
COMFY_WORKFLOWS = [
    'workflows/sdxl_txt2img.json',
    'workflows/sdxl_img2img.json',
    'workflows/sdxl_inpaint.json',
    'workflows/upscale_4x.json',
]


def add(results: list[dict], name: str, ok: bool, detail: str = '') -> None:
    results.append({'name': name, 'ok': bool(ok), 'detail': detail})


def run(cmd: list[str], cwd: Path | None = None) -> tuple[bool, str]:
    p = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
    return p.returncode == 0, p.stdout[-4000:]


def main() -> int:
    results: list[dict] = []
    skill_path = BASE / 'SKILL.md'
    content = skill_path.read_text()
    add(results, 'SKILL.md starts with frontmatter', content.startswith('---'))
    m = re.search(r'\n---\s*\n', content[3:])
    add(results, 'frontmatter closes', m is not None)
    if m:
        if yaml is not None:
            fm = yaml.safe_load(content[3:m.start()+3])
        else:
            fm = {}
            for line in content[3:m.start()+3].splitlines():
                if ':' in line and not line.startswith(' '):
                    k, v = line.split(':', 1)
                    fm[k.strip()] = v.strip().strip('"\'')
        add(results, 'frontmatter is mapping', isinstance(fm, dict))
        add(results, 'name is commercial-image-router', fm.get('name') == 'commercial-image-router')
        add(results, 'description present <=1024', bool(fm.get('description')) and len(fm.get('description')) <= 1024, str(len(fm.get('description', ''))))
    add(results, 'SKILL.md <=100k chars', len(content) <= 100_000, str(len(content)))

    for ref in REQUIRED_REFS:
        p = BASE / 'references' / ref
        add(results, f'reference exists: {ref}', p.exists(), str(p.stat().st_size) if p.exists() else 'missing')
        add(results, f'SKILL links reference: {ref}', f'references/{ref}' in content)
    for script in REQUIRED_SCRIPTS:
        p = BASE / 'scripts' / script
        add(results, f'script exists: {script}', p.exists(), str(p.stat().st_size) if p.exists() else 'missing')

    all_text = content + '\n'.join((BASE / 'references' / r).read_text() for r in REQUIRED_REFS if (BASE / 'references' / r).exists())
    for phrase in REQUIRED_PHRASES:
        add(results, f'quality phrase present: {phrase}', phrase in all_text)

    for wf in COMFY_WORKFLOWS:
        check_script = COMFY_HELPERS / 'scripts' / 'check_deps.py'
        if check_script.exists():
            ok, out = run([sys.executable, str(check_script), wf], cwd=COMFY_HELPERS)
            add(results, f'Comfy workflow dependency ready: {wf}', ok, out.splitlines()[0] if out else '')
        else:
            add(results, f'Comfy workflow helper present: {wf}', False, f'missing {check_script}')

    files = [
        RUNTIME_ROOT / 'comfy-workspace/models/checkpoints/Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors',
        RUNTIME_ROOT / 'image-models/sam/sam_vit_b_01ec64.pth',
        RUNTIME_ROOT / 'comfy-workspace/models/upscale_models/4x-UltraSharp.pth',
    ]
    optional_artifacts = [
        RUNTIME_ROOT / 'commercial-image-runtime-tests/product-poster/final_product_poster_v5_no_overflow.png',
        RUNTIME_ROOT / 'commercial-image-runtime-tests/upscale/winter_poster_4x_ultrasharp_00001_.png',
    ]
    for f in files:
        p = Path(f)
        add(results, f'required runtime model exists: {p.name}', p.exists(), str(p.stat().st_size) if p.exists() else 'missing')
    for f in optional_artifacts:
        p = Path(f)
        # Smoke/sample artifacts are useful regression evidence on the origin machine but should not fail a fresh install.
        add(results, f'optional sample artifact exists: {p.name}', True, str(p.stat().st_size) if p.exists() else 'not present on this machine')

    failed = [r for r in results if not r['ok']]
    report = {'ok': not failed, 'failed_count': len(failed), 'results': results}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not failed else 1


if __name__ == '__main__':
    raise SystemExit(main())
