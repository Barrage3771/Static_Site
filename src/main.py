import os
import shutil
from textnode import *
from copystatic import *
from generate_page import generate_pages_recursively

def main():

    source_dir = "static"
    dest_dir = "public"
    if os.path.exists("public"):
        shutil.rmtree("public")
    copy_files_recursive(source_dir, dest_dir)
    path1 = "content"
    path2 = "template.html"
    path3 = "public"
    generate_pages_recursively(path1, path2, path3)
main()