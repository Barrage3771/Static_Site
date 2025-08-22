import os
import sys
import shutil
from textnode import *
from copystatic import *
from generate_page import generate_pages_recursively

default_basepath = "/"

def main():
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    source_dir = "static"
    dest_dir = "docs"
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    copy_files_recursive(source_dir, dest_dir)
    path1 = "content"
    path2 = "template.html"
    path3 = "docs"
    generate_pages_recursively(path1, path2, path3, basepath)
main()