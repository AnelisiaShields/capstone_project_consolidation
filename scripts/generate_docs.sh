#!/usr/bin/env bash
set -euo pipefail
# generate_docs.sh
# Usage: ./scripts/generate_docs.sh [PY_PACKAGE_NAME]
# Example: ./scripts/generate_docs.sh newsapp
PKG=${1:-newsapp}
VENV_DIR=${VENV_DIR:-.venv}

echo "1) Creating/activating virtual environment at ${VENV_DIR} (if not exists)"
if [ ! -d "${VENV_DIR}" ]; then
  python -m venv "${VENV_DIR}"
fi
# shellcheck source=/dev/null
source "${VENV_DIR}/bin/activate"

echo "2) Installing project requirements + Sphinx"
pip install --upgrade pip
if [ -f requirements.txt ]; then
  pip install -r requirements.txt || true
fi
pip install sphinx sphinx-rtd-theme

echo "3) Running sphinx-quickstart (non-interactive) into docs/"
sphinx-quickstart -q -p "news_capstone" -a "Your Name" -v "1.0" --sep -l en docs

echo "4) Create docs/source/conf.py additions for Django"
# Append recommended Django config to conf.py
CONF=docs/source/conf.py
cat >> "${CONF}" <<'PYCONF'

# -- Django setup (added by helper script) -------------------------------
import os, sys, django
sys.path.insert(0, os.path.abspath('..' ))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsapp.settings')
try:
    django.setup()
except Exception:
    # If Django isn't fully configured yet, autodoc may still work for simple modules
    pass
# ------------------------------------------------------------------------
PYCONF

echo "5) Run sphinx-apidoc to generate module rst files"
sphinx-apidoc -o docs/source "${PKG}" || true

echo "6) Build HTML docs"
sphinx-build -b html docs/source docs/_build/html

echo "Docs built at: docs/_build/html/index.html"
echo "Done."
