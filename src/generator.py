import os
from document import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("#") and not line.startswith("##"):
            return line[1:].strip()
    raise Exception("No top-level header found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        md = file.read()
    with open(template_path, "r") as file:
        template = file.read()

    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    directory = os.path.dirname(dest_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(dest_path, "w") as file:
        file.write(page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    contents = os.listdir(dir_path_content)
    for content in contents:
        from_path = os.path.join(dir_path_content, content)
        dest_path = os.path.join(dest_dir_path, content)
        if os.path.isfile(from_path) and content.endswith(".md"):
            generate_page(
                from_path, template_path, dest_path.removesuffix(".md") + ".html"
            )
        else:
            generate_pages_recursive(from_path, template_path, dest_path)
