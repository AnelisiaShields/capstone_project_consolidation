#!/usr/bin/env bash
set -euo pipefail
# init_git.sh
# Usage: ./scripts/init_git.sh [git_remote_url]
# Example: ./scripts/init_git.sh https://github.com/youruser/yourrepo.git
REMOTE=${1:-""}
# Configure user if missing
git config user.name >/dev/null 2>&1 || git config --global user.name "Your Name"
git config user.email >/dev/null 2>&1 || git config --global user.email "you@example.com"

if [ ! -d .git ]; then
  git init
fi

git add .
git commit -m "Initial import: project + docs + Dockerfile" || true
# create branches
git checkout -B main || git checkout main || true
git branch -f docs || true
git branch -f container || true

# Make separate commits for docs and Dockerfile if wanted
git add docs
git commit -m "Add generated docs" || true
git checkout main
git add Dockerfile
git commit -m "Add Dockerfile" || true
git checkout main

if [ -n "$REMOTE" ]; then
  git remote remove origin 2>/dev/null || true
  git remote add origin "$REMOTE"
  echo "Remote set to $REMOTE. Push with: git push -u origin main --force"
fi

echo "Git initialization complete. Use 'git log --oneline' to inspect commits."
