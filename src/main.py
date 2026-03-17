import os
import shutil
import sys

from site_generation import generate_pages_recursive

if len(sys.argv) > 1:
    BASE_PATH = sys.argv[1]
else:
    BASE_PATH = '/'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(BASE_DIR, "../public")
DOCS_DIR = os.path.join(BASE_DIR, "../docs")
STATIC_DIR = os.path.join(BASE_DIR, "../static")
TEMPLATE_PATH = os.path.join(BASE_DIR, "../template.html")
CONTENT_DIR = os.path.join(BASE_DIR, "../content")
CONTENT_FILE = os.path.join(CONTENT_DIR, "./index.md")

def main():
    #write_to_public()
    write_to_docs()
    generate_pages_recursive(CONTENT_DIR, TEMPLATE_PATH, DOCS_DIR, BASE_PATH)
    


def write_to_docs():
    if os.path.exists(DOCS_DIR):
        shutil.rmtree(DOCS_DIR)
    shutil.copytree(STATIC_DIR, DOCS_DIR)

def write_to_public():
    if os.path.exists(PUBLIC_DIR):
        shutil.rmtree(PUBLIC_DIR)
    shutil.copytree(STATIC_DIR, PUBLIC_DIR)

if __name__ == "__main__":
    main()