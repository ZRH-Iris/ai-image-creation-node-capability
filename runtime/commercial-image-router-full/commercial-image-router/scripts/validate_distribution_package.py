#!/usr/bin/env python3
from __future__ import annotations
import json
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path


def run(cmd: list[str], cwd: Path | None = None) -> tuple[int, str]:
    p = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300)
    return p.returncode, p.stdout


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_distribution_package.py <tar.gz>", file=sys.stderr)
        return 2

    tar_path = Path(sys.argv[1]).resolve()
    if not tar_path.exists():
        print(f"missing_tar:{tar_path}")
        return 2

    checks: list[dict] = []

    def add(name: str, ok: bool, detail: str = "") -> None:
        checks.append({"name": name, "ok": bool(ok), "detail": detail})

    with tempfile.TemporaryDirectory(prefix="commercial-image-router-pkg-") as tmpdir:
        tmp = Path(tmpdir)
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall(tmp)

        root = next((p for p in tmp.iterdir() if p.is_dir()), tmp)
        if (root / "commercial-image-router-full").exists():
            root = root / "commercial-image-router-full"

        # Required top-level files
        required = [
            "README.md",
            "TECHNICAL.md",
            "setup_runtime.sh",
            "一键安装.sh",
            "runtime_manifest.json",
            "commercial-image-router/SKILL.md",
            "comfy-helpers/workflows/sdxl_txt2img.json",
            "comfy-helpers/workflows/sdxl_img2img.json",
            "comfy-helpers/workflows/sdxl_inpaint.json",
            "comfy-helpers/workflows/upscale_4x.json",
        ]
        for rel in required:
            add(f"required:{rel}", (root / rel).exists())

        readme = (root / "README.md").read_text()
        tech = (root / "TECHNICAL.md").read_text()

        # README must stay ordinary-user friendly
        technical_terms = ["ComfyUI", "SAM", "Juggernaut", "SDXL", "manifest", "checkpoint", "PyTorch", "HuggingFace"]
        for term in technical_terms:
            add(f"readme_hide:{term}", term not in readme)

        add("readme_one_click", "bash 一键安装.sh" in readme)
        add("tech_dry_run_doc", "--dry-run" in tech)

        nested = root / "commercial-image-router/commercial-image-router"
        add("no_nested_skill_dir", not nested.exists())

        pycache = list(root.rglob("__pycache__"))
        add("no_pycache", not pycache)

        # Syntax checks
        shell = run(["bash", "-n", str(root / "setup_runtime.sh")])
        add("shell_syntax_setup", shell[0] == 0)
        shell2 = run(["bash", "-n", str(root / "一键安装.sh")])
        add("shell_syntax_entry", shell2[0] == 0)

        node = run(["node", "--check", str(root / "commercial-image-router/scripts/compose_product_poster.js")])
        add("node_syntax", node[0] == 0)

        manifest = json.loads((root / "runtime_manifest.json").read_text())
        models = manifest.get("models", manifest)
        for key in ["juggernaut_xl_v9", "sdxl_base", "sam_vit_b", "upscale_4x_ultrasharp"]:
            add(f"manifest:{key}", key in models and bool(models[key].get("url")) and bool(models[key].get("path")))

    failed = [c for c in checks if not c["ok"]]
    report = {
        "tarball": str(tar_path),
        "ok": not failed,
        "failed_count": len(failed),
        "checks": checks,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
