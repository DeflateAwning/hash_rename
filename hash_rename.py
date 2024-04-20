# ChatGPT Prompt:
# Write a Python script which takes one argument (using argparse): a path to either a file or a directory.
# If it's a file, then it should read that file, calculate the md5 hash as base16 lowercase,
# and then rename that file to: <first 6 md5 characters>_<old filename>. 
# If it's a folder, then it should perform that operation recursively on all files in the folder.
# Prompt the user to press enter for each rename.

import argparse
import os
import hashlib

def get_md5_hash(file_path):
    """Calculate the md5 hash of a file and return the first 6 characters."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        buffer = file.read(8192)
        while len(buffer) > 0:
            hasher.update(buffer)
            buffer = file.read(8192)
    return hasher.hexdigest()[:6]

def rename_file(file_path):
    """Rename a file to include the first 6 characters of its md5 hash."""
    dir_name, file_name = os.path.split(file_path)
    hash_prefix = get_md5_hash(file_path)
    new_file_name = f"{hash_prefix}_{file_name}"
    new_file_path = os.path.join(dir_name, new_file_name)
    
    input(f"Press Enter to rename the file {file_path}...")
    os.rename(file_path, new_file_path)
    print(f"Renamed '{file_path}' to '{new_file_path}'")

def process_path(path):
    """Process a path, recursively renaming files if it's a directory."""
    if os.path.isfile(path):
        rename_file(path)
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                rename_file(file_path)

def main():
    parser = argparse.ArgumentParser(description="Process a file or directory to rename files based on md5 hashes.")
    parser.add_argument("path", type=str, help="Path to the file or directory to process.")
    # TODO: add a "--no-prompt" (aka "-y") flag to skip the prompt
    # TODO: add a hash_length arg
    # TODO: add a hash_func arg (to select md5, etc.)

    args = parser.parse_args()

    # Check if the path exists
    if not os.path.exists(args.path):
        print(f"The path {args.path} does not exist.")
        return

    process_path(args.path)

if __name__ == "__main__":
    main()
