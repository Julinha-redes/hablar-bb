#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 -m pip install --user pyinstaller
python3 -m PyInstaller --onefile --windowed --name saminho_dm_helper utils/instagram_dm_helper_app.py

if [ -f "dist/saminho_dm_helper.exe" ]; then
  echo "✅ Executável gerado em: dist/saminho_dm_helper.exe"
else
  echo "✅ Executável gerado em: dist/saminho_dm_helper"
fi
