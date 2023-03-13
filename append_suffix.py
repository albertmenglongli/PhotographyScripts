#!/usr/bin/env python3
import os
import re
import argparse


def rename_files(folder_path, suffix):
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            if suffix not in filename and filename.endswith('.jpg'):
                new_filename = re.sub(r'\.(.*)$', rf'-{suffix}.\1', filename)
                os.rename(os.path.join(dirpath, filename), os.path.join(dirpath, new_filename))
                print(f'{os.path.join(dirpath, filename)} -> {new_filename}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Delete old and/or large files.")
    parser.add_argument("-d", "--dir", dest="folder_path")
    parser.add_argument("-s", "--suffix", default='ps', dest="suffix")
    args = parser.parse_args()
    folder_path = args.folder_path
    suffix = args.suffix
    rename_files(folder_path, suffix)
