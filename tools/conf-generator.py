#!/usr/bin/env python3
import os
import shutil
import yaml
from render_config import render_config

# Folders
DEVICE_DIR = "snapshots/ci_net/device-yaml"
GENERATED_DIR = "snapshots/ci_net/configs/generated"


if os.path.exists(GENERATED_DIR):
    shutil.rmtree(GENERATED_DIR)
os.makedirs(GENERATED_DIR, exist_ok=True)

# YAML
yaml_files = [f for f in os.listdir(DEVICE_DIR) if f.endswith(".yaml")]

if not yaml_files:
    print("No YAML files found in", DEVICE_DIR)

for file in yaml_files:
    path = os.path.join(DEVICE_DIR, file)
    with open(path) as f:
        content = yaml.safe_load(f)

    devices = content if isinstance(content, list) else [content]

    for data in devices:
        if not isinstance(data, dict) or "hostname" not in data:
            print(f"Skipping invalid entry in {file}")
            continue

        try:
            cfg = render_config(data)
        except Exception as e:
            print(f"Error rendering {data.get('hostname')}: {e}")
            continue

        hostname = data["hostname"]
        out_path = os.path.join(GENERATED_DIR, f"{hostname}_gen.cfg")

        with open(out_path, "w") as out:
            out.write(cfg)

        print(f"Rendered: {hostname}_gen.cfg")
