from textnode import *
from copystatic import *

def main():

    source_dir = "static"
    dest_dir = "public"

    copy_files_recursive(source_dir, dest_dir)

main()