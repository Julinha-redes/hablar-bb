#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
python3 utils/instagram_dm_helper_app.py
