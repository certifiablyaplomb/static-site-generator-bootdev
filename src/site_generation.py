import os

from helpers import markdown_to_blocks, block_to_html, markdown_to_html_node

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_info = block_to_html(block)
        if block_info[0] == 'h1':
            return block_info[1]
    raise Exception("no <h1> element was found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ''
    with open(from_path, 'r') as markdown_file:
        for line in markdown_file:
            markdown += line
    template = ''
    with open(template_path, 'r') as template_file:
        for line in template_file:
            template += line
    title = extract_title(markdown)
    htmlnode = markdown_to_html_node(markdown)
    html = htmlnode.to_html()

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    
    if not os.path.exists(dest_path): ##really shouldn't be possible, but hey why not
        os.mkdir(dest_path)
    
    html_file_path = os.path.join(dest_path, "index.html")
    with open(html_file_path, 'w') as file:
        file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    branches = os.listdir(dir_path_content)
    
    for branch in branches:
        branch_dir = os.path.join(dir_path_content, branch)
        new_dest_dir_path = os.path.join(dest_dir_path, branch)
        if not os.path.isfile(branch_dir):
            if not os.path.exists(new_dest_dir_path):
                os.mkdir(new_dest_dir_path)
            generate_pages_recursive(branch_dir, template_path, new_dest_dir_path)
        else:
            generate_page(branch_dir, template_path, dest_dir_path.replace('.md', '.html'))