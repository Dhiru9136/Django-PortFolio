
import os
import shutil
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio.settings")

import django
django.setup()

from django.test import Client

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "docs"

# Purana build folder remove karo
if OUTPUT_DIR.exists():
    shutil.rmtree(OUTPUT_DIR)

OUTPUT_DIR.mkdir(parents=True)

# Django pages render karo
client = Client()

pages = {
    "": "index.html",
    "about": "about.html",
    "contact": "contact.html",
    "skills": "skills.html",
    "projects": "projects.html",
}

for url, filename in pages.items():
    response = client.get("/" + url if url else "/")

    if response.status_code != 200:
        raise Exception(
            f"Page failed: /{url} - Status {response.status_code}"
        )

    html = response.content.decode("utf-8")

    # Django links ko static HTML links mein convert karo
    for name in ["about", "contact", "skills", "projects"]:
        html = html.replace(f'href="/{name}"', f'href="./{name}.html"')
        html = html.replace(f'href="/{name}/"', f'href="./{name}.html"')

    html = html.replace('href="/"', 'href="./index.html"')

    (OUTPUT_DIR / filename).write_text(html, encoding="utf-8")
    print(f"Created: {filename}")

# Static files copy karo
static_source = BASE_DIR / "static"
static_destination = OUTPUT_DIR / "static"

if static_source.exists():
    shutil.copytree(static_source, static_destination)

print("\nPortfolio build complete! Files are inside the docs folder.")
