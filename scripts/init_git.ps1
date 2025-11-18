<#
.SYNOPSIS
  init_git.ps1 - Initialize git repo and create commits/branches.
.PARAMETER Remote
  Remote URL to add as origin (optional).
#>
param(
    [string]$Remote = ""
)

if (-Not (Test-Path ".git")) {
    git init
}

# Ensure user config exists (prompt if missing)
$userName = (git config user.name) -ne $null
if (-not $userName) {
    git config --global user.name "Your Name"
}
$userEmail = (git config user.email) -ne $null
if (-not $userEmail) {
    git config --global user.email "you@example.com"
}

git add .
git commit -m "Initial import: project + docs + Dockerfile" -q 2>$null

# Create branches
git checkout -B main
git checkout -B docs
git add docs
git commit -m "Add generated docs" -q 2>$null || Write-Host "Docs commit may be empty"
git checkout main
git checkout -B container
git add Dockerfile
git commit -m "Add Dockerfile" -q 2>$null || Write-Host "Dockerfile commit may be empty"
git checkout main

if ($Remote -ne "") {
    git remote remove origin -ErrorAction SilentlyContinue
    git remote add origin $Remote
    Write-Host "Remote set to $Remote. Push with: git push -u origin main --force"
}

Write-Host "Git init complete."
