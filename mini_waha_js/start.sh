#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
if command -v python3 >/dev/null 2>&1; then PY=python3; else PY=python; fi
$PY -m pip install -r python/requirements.txt >/dev/null
$PY python/app.py
