<#
.SYNOPSIS
  generate_docs.ps1 - Generate Sphinx docs for the project (Windows PowerShell).
.PARAMETER Package
  The Python package folder to document. Default: newsapp
.EXAMPLE
  .\scripts\generate_docs.ps1 -Package newsapp
#>
param(
    [string]$Package = "newsapp",
    [string]$Venv = ".venv"
)

Write-Host "1) Creating/activating virtual environment at $Venv (if not exists)"
if (-Not (Test-Path $Venv)) {
    python -m venv $Venv
}

$activate = Join-Path $Venv "Scripts\\Activate.ps1"
if (Test-Path $activate) {
    Write-Host "Activating venv..."
    & $activate
} else {
    Write-Host "Activate the venv manually: $Venv\\Scripts\\activate"
}

Write-Host "2) Installing requirements + Sphinx"
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt -q
}
pip install sphinx sphinx-rtd-theme -q

Write-Host "3) Running sphinx-quickstart (non-interactive) into docs/"
sphinx-quickstart -q -p "news_capstone" -a "Your Name" -v "1.0" --sep -l en docs

Write-Host "4) Appending Django setup to docs/source/conf.py"
$conf = "docs\\source\\conf.py"
Add-Content $conf "`n# -- Django setup (added by helper script) -------------------------------"
Add-Content $conf 'import os, sys, django'
Add-Content $conf "sys.path.insert(0, os.path.abspath('..'))"
Add-Content $conf "os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsapp.settings')"
Add-Content $conf "try:`n    django.setup()`nexcept Exception:`n    pass"
Add-Content $conf "# ------------------------------------------------------------------------`n"

Write-Host "5) Running sphinx-apidoc"
sphinx-apidoc -o docs/source $Package

Write-Host "6) Building HTML docs"
sphinx-build -b html docs/source docs/_build/html

Write-Host "Docs built at docs\\_build\\html\\index.html"
