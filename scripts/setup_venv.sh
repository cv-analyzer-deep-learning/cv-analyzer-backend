#!/usr/bin/env bash
set -euo pipefail

# Usage: ./scripts/setup_venv.sh [--recreate]
# Creates a Python virtualenv in ./venv, upgrades pip and installs requirements.

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV_DIR="$ROOT_DIR/venv"

RECREATE=0
if [ "${1-}" = "--recreate" ]; then
  RECREATE=1
fi

if [ $RECREATE -eq 1 ] && [ -d "$VENV_DIR" ]; then
  echo "Removing existing venv..."
  rm -rf "$VENV_DIR"
fi

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtualenv at $VENV_DIR"
  python3 -m venv "$VENV_DIR"
fi

echo "Activating virtualenv and upgrading pip..."
"$VENV_DIR/bin/python" -m pip install --upgrade pip setuptools wheel

echo "Installing runtime requirements..."
"$VENV_DIR/bin/python" -m pip install -r "$ROOT_DIR/requirements.txt"

if [ -f "$ROOT_DIR/requirements-dev.txt" ]; then
  echo "Installing dev requirements..."
  "$VENV_DIR/bin/python" -m pip install -r "$ROOT_DIR/requirements-dev.txt"
fi

echo "Done. Activate with: source venv/bin/activate"
