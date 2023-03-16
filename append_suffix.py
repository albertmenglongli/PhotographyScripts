#!/usr/bin/env python3
import argparse
import os
import re
from pathlib import Path


def rename_files(folder_path, suffix):
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            if suffix not in filename and filename.endswith('.jpg'):
                new_filename = re.sub(r'\.(.*)$', rf'-{suffix}.\1', filename)
                if not Path(os.path.join(dirpath, new_filename)).exists():
                    os.rename(os.path.join(dirpath, filename), os.path.join(dirpath, new_filename))
                    print(f'{os.path.join(dirpath, filename)} -> {new_filename}')
                else:
                    print(f'Failed to rename {filename} -> {new_filename}, {new_filename} already exists')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Delete old and/or large files.")
    parser.add_argument("-d", "--dir", dest="folder_path")
    parser.add_argument("-s", "--suffix", default='ps', dest="suffix")
    args = parser.parse_args()
    folder_path = args.folder_path
    suffix = args.suffix
    rename_files(folder_path, suffix)
