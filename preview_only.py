#!/usr/bin/env python3
import os
from pathlib import Path
from typing import Optional, Set
import argparse
import sys

from utils import convert_cr2_to_jpg, delete_file_paths


def analyze_files_to_delete(file_paths: Optional[Set[Path]]):
    files_to_delete = set()
    all_file_names = set()

    for fp in file_paths:
        file_name = fp.name
        all_file_names.add(file_name)

    for fp in file_paths:
        if fp.name.endswith('CR2') and fp.stem + '.JPG' in all_file_names:
            files_to_delete.add(fp)

    return files_to_delete


def parse_args():
    description = ("keep only preview file JPGs:"
                   "\t1. remove CR2 if JPG exists;"
                   "\t2. convert CR2 to JPG then remove CR2;")

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(dest='dir_path', type=str, help='dir')

    args = parser.parse_args()
    return args


def entry(dir_path: Path):
    for root, sub_dirs, file_names in os.walk(dir_path):
        file_paths = set([Path(root) / file for file in file_names])
        file_paths_to_delete = analyze_files_to_delete(file_paths)
        file_paths_to_convert = set(filter(lambda __: __.name.endswith('CR2'),
                                           file_paths.difference(file_paths_to_delete)))
        file_paths_converted = convert_cr2_to_jpg(file_paths_to_convert)
        print(f'{len(file_paths_to_convert)} CR2 files converted!')
        file_paths_to_delete |= file_paths_converted
        delete_file_paths(file_paths_to_delete)
        print(f'{len(file_paths_to_delete)} CR2 files deleted!')


if __name__ == '__main__':
    args = parse_args()
    dir_path = args.dir_path
    dir_path = Path(dir_path)
    if not dir_path.exists():
        print(f'Invalid dir_path {dir_path}')
        sys.exit(1)
    if not dir_path.is_dir():
        print(f'Invalid dir_path {dir_path}')
        sys.exit(1)
    entry(dir_path=dir_path)
