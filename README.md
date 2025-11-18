
# news_capstone - Capstone (enhanced)

This repository has been prepared for the capstone submission. The assistant has added helpful files: `.gitignore`, `requirements.txt`, a `docs/` Sphinx skeleton and prebuilt HTML, a `Dockerfile`, `README.md`, and `capstone.txt`.

## Install and run locally (venv)

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows use: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
# Configure your DATABASE settings (e.g. in settings.py or via env vars)
python manage.py migrate
python manage.py runserver
```

## Build and run with Docker

```bash
docker build -t news_capstone:latest .
docker run -p 8000:8000 news_capstone:latest
```

> Note: ensure you edit the Dockerfile `CMD` to point to your Django project's wsgi module (it currently uses `news_capstone.wsgi:application`).

## Regenerating Sphinx docs locally

Install Sphinx and run (from repo root):

```bash
pip install sphinx
sphinx-quickstart docs
# or use sphinx-apidoc:
sphinx-apidoc -o docs/source /mnt/data/news_capstone_work/news_capstone_bundle/news_capstone
make -C docs html
```

---

**Security note:** Do not commit secrets like `.env` files, API keys, or database passwords to public repos. Use `.gitignore` to exclude them.



---

# Helper scripts included

I added convenience scripts under the `scripts/` folder to **generate full Sphinx HTML docs locally** and to **initialize a Git repo with commits and branches** so you can create a GitHub-ready repository.

## Generate full Sphinx docs (Linux/macOS)
```
./scripts/generate_docs.sh <python_package_name>
# e.g.
./scripts/generate_docs.sh newsapp
```

## Generate full Sphinx docs (Windows PowerShell)
```
.\scripts\generate_docs.ps1 -Package newsapp
```

These scripts will:
- create/activate a virtual environment (default `.venv`),
- install `sphinx` and `sphinx-rtd-theme` (and your `requirements.txt`),
- run `sphinx-quickstart` non-interactively,
- run `sphinx-apidoc` for your package (e.g. `newsapp`),
- build HTML into `docs/_build/html`.

## Initialize git and create commits/branches (Linux/macOS)
```
./scripts/init_git.sh <optional_remote_url>
# e.g.
./scripts/init_git.sh https://github.com/youruser/yourrepo.git
```

## Initialize git (Windows PowerShell)
```
.\scripts\init_git.ps1 -Remote "https://github.com/youruser/yourrepo.git"
```

Notes:
- Review `scripts/init_git.sh` before running; it will set a global git user.name/user.email if missing – you may prefer to set them manually first.
- After running `init_git`, push to GitHub with `git push -u origin main` (it may ask for credentials or use your ssh agent).

