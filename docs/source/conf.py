
import os
import sys
import django
sys.path.insert(0, os.path.abspath('..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'news_capstone.settings'  # Update if your project settings module differs
django.setup()

project = 'news_capstone'
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']
templates_path = ['_templates']
exclude_patterns = []
html_theme = 'alabaster'
