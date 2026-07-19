#!/usr/bin/env python3
from pathlib import Path
import json
import hashlib
import shutil

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "build-manifest.json").read_text(encoding="utf-8"))
DEPLOY = ROOT / "custom-html-block"
DIST = ROOT / "dist"

DEPLOY.mkdir(exist_ok=True)
DIST.mkdir(exist_ok=True)

def combine(paths):
    return "\n".join(
        (ROOT / path).read_text(encoding="utf-8").rstrip()
        for path in paths
    ) + "\n"

outputs = {
    "HTML.html": combine(MANIFEST["html"]),
    "CSS.css": combine(MANIFEST["css"]),
    "JAVASCRIPT.js": combine(MANIFEST["javascript"])
}

checksums = {}
for name, content in outputs.items():
    deploy_path = DEPLOY / name
    dist_path = DIST / name
    deploy_path.write_text(content, encoding="utf-8")
    shutil.copyfile(deploy_path, dist_path)
    checksums[name] = hashlib.sha256(deploy_path.read_bytes()).hexdigest()

(DIST / "checksums.json").write_text(
    json.dumps(checksums, indent=2) + "\n",
    encoding="utf-8"
)

for name in outputs:
    print(f"{name}: {(DEPLOY / name).stat().st_size:,} bytes")
