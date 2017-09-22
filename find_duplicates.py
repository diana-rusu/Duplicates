u"""
Write a program that outputs the file_names of duplicate files.
"""
__author__ = "Diana Rusu"
__email__ = "diana.russu.87@gmail.com"

import os
import sys
from collections import defaultdict
import hashlib


def find_files_with_same_size(folder_to_check):
    """Find files that have the same size."""
    file_size_to_names = defaultdict(list)
    files = [f for f in os.listdir(
                    folder_to_check) if os.path.isfile(folder_to_check+f)]

    for file_name in files:
        file_size = os.path.getsize(os.path.join(folder_to_check, file_name))
        file_size_to_names[file_size].append(file_name)

    duplicate_size_to_name = {file_size: file_size_to_names[file_size]
                              for file_size in file_size_to_names.keys() if
                              len(file_size_to_names[file_size]) > 1}

    return list(duplicate_size_to_name.values())


def find_duplicates(folder_to_check_duplicates):
    """Calculate hash for files with same size."""
    file_hash_to_names = defaultdict(list)

    files_with_same_size_list = find_files_with_same_size(
                                folder_to_check_duplicates)

    if len(files_with_same_size_list) == 0:
        print('''___________________________________
              \n No duplicates found. Will exit now. \n  ''')
        sys.exit()
    else:
        for files_with_same_size in files_with_same_size_list:
            for file_name in files_with_same_size:
                file_hash = compute_hash_sha256(
                            folder_to_check_duplicates+file_name)
                file_hash_to_names[file_hash].append(file_name)

    duplicate_hash_to_names = {file_hash: file_hash_to_names[file_hash]
                               for file_hash in file_hash_to_names.keys() if
                               len(file_hash_to_names[file_hash]) > 1}

    return duplicate_hash_to_names


def compute_hash_sha256(filename, block_size=65536):
    """Since MD5 is known to have weaknesses, will use SHA1 256."""
    hash_sha256 = hashlib.sha256()

    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            hash_sha256.update(block)

    return hash_sha256.hexdigest()


def find_original_file(duplicate_hash_to_names, folder_to_check):
    """Find the original file from which the others duplicates are copied."""
    original_files = {}

    for file_names in duplicate_hash_to_names.values():
        min_mtime = sys.maxsize
        file_name_min = None
        for file_name in file_names:
            file_mtime = os.stat(folder_to_check+file_name).st_mtime
            if(file_mtime < min_mtime):
                min_mtime = file_mtime
                file_name_min = file_name
        original_files[file_name_min] = [
                    file_name for file_name in file_names
                    if file_name != file_name_min]

    return original_files


def check_directory_exist(directory):
    """Verify validity of the user input."""
    if (os.path.exists(directory) &
            os.path.isdir(directory)):
        return True
    else:
        print("That is an invalid path. Try again")
        return False


if __name__ == '__main__':
    while(True):
        folder_to_check_duplicates = input(
            "Enter the folder path you want to check for duplicates: "
            )
        if(check_directory_exist(folder_to_check_duplicates)):
            break
    duplicate_hash_to_names = find_duplicates(folder_to_check_duplicates)
    print("=========================================================\n")
    print("Hash of the duplicate files with corresponding file names")
    print("_________________________________________________________\n")
    for file_hash, file_names in duplicate_hash_to_names.items():
        print(file_hash, file_names)
    print("=========================================================\n")
    print("Original File", "  |\t", "Duplicates")
    print("_________________________________________________________\n")
    originals = find_original_file(
                duplicate_hash_to_names, folder_to_check_duplicates)
    for original_file, duplicate_files in originals.items():
        print(original_file, "\t\t|\t", duplicate_files)
    print("=========================================================\n")
