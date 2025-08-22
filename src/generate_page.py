import os
from markdown_to_html_node import *
from extract_markdown import *
from copystatic import *

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    file1 = open(from_path, "r")
    content1 = file1.read()
    file1.close()
    
    file2 = open(template_path, "r")
    content2 = file2.read()
    file2.close()
    
    new_content1 = markdown_to_html_node(content1)
    html_code = new_content1.to_html()
    title = extract_title(content1)
    
    content2 = content2.replace("{{ Title }}", title)
    content2 = content2.replace("{{ Content }}", html_code)
    
    name = os.path.dirname(dest_path)
    
    if name != "":
        os.makedirs(name, exist_ok=True)
    
    file3 = open(dest_path, "w")
    file3.write(content2)
    file3.close()
    

def generate_pages_recursively(content_root, template_path, public_root, from_path=None, dest_path=None):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    if from_path is None:
        from_path = content_root
    if dest_path is None:
        dest_path = public_root
    
    for entry in os.listdir(from_path):
        src_entry_path = os.path.join(from_path, entry)
        rel_path = os.path.relpath(src_entry_path, content_root)
        dest_entry_path = os.path.join(public_root, rel_path)
        
        if os.path.isdir(src_entry_path):
            
            os.makedirs(dest_entry_path, exist_ok=True)
            
            generate_pages_recursively(content_root, template_path, public_root, src_entry_path, dest_entry_path)
        elif os.path.isfile(src_entry_path) and src_entry_path.endswith(".md"):
            html_output_path = dest_entry_path.replace(".md", ".html")
            os.makedirs(os.path.dirname(html_output_path), exist_ok=True)
            with open(src_entry_path, "r") as f:
                content = f.read()
                new_content = markdown_to_html_node(content)
                html_code = new_content.to_html()
                title = extract_title(content)
                
            with open(template_path, "r") as f:
                template_html = f.read()
            
            output_html = template_html.replace("{{ Title }}", title)
            output_html = output_html.replace("{{ Content }}", html_code)
            
            with open(html_output_path, "w") as f:
                f.write(output_html)