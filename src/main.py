import os
import shutil

from site_generation import generate_page, generate_pages_recursive

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(BASE_DIR, "../public")
STATIC_DIR = os.path.join(BASE_DIR, "../static")
TEMPLATE_PATH = os.path.join(BASE_DIR, "../template.html")
CONTENT_DIR = os.path.join(BASE_DIR, "../content")
CONTENT_FILE = os.path.join(CONTENT_DIR, "./index.md")

def main():
    write_to_public()
    generate_pages_recursive(CONTENT_DIR, TEMPLATE_PATH, PUBLIC_DIR)
    #generate_page(CONTENT_FILE, TEMPLATE_PATH, PUBLIC_DIR)



def write_to_public():
    if os.path.exists(PUBLIC_DIR):
        shutil.rmtree(PUBLIC_DIR)
    shutil.copytree(STATIC_DIR, PUBLIC_DIR)

if __name__ == "__main__":
    main()