import os
import shutil

def copy_files_recursive(source_dir, dest_dir):
    #Step 1: Clean the destination first
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir, ignore_errors=True)
    
    os.mkdir(dest_dir)
    #Step 2: Get a list of all the items in the source directory
    for item_name in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item_name)
        dest_path = os.path.join(dest_dir, item_name)
        
        print(f"Looking at: {source_path}")
        #Step 3: determine if its a file or directory(*ehem* folder)
        if os.path.isfile(source_path):
            #Step 4: if file we copy it
            print(f"Copying file: {source_path} -> {dest_path}")
            shutil.copy(source_path, dest_path)
            #Step 5: if subdirectory we reccursively call into it and start from step2 again.
        else:
            print(f"Found directory: {source_path}")
            copy_files_recursive(source_path, dest_path)
