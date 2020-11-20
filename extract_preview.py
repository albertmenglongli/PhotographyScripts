#!/usr/bin/env python3
import os
import shutil
from pathlib import Path
from typing import Optional, Set
import argparse
import sys

from utils import convert_cr2_to_jpg


def analyze_files_to_convert(file_paths: Optional[Set[Path]]):
    files_to_convert = set()
    all_file_names = set()

    for fp in file_paths:
        file_name = fp.name
        all_file_names.add(file_name)

    for fp in file_paths:
        if fp.name.endswith('CR2'):
            if fp.stem + '.JPG' in all_file_names:
                pass
            else:
                files_to_convert.add(fp)
    return files_to_convert


def parse_args():
    description = ("Extract JPG to another directory, convert to JPG for CR2 without preview")

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(dest='dir_path', type=str, help='dir')
    parser.add_argument(dest='output_dir', type=str, help='dir')

    args = parser.parse_args()
    return args


def entry(dir_path: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    for root, sub_dirs, file_names in os.walk(dir_path):
        file_paths = set([Path(root) / file for file in file_names])

        file_to_copy_directly = list(filter(lambda fp: fp.name.endswith('.JPG'), file_paths))
        for fp in file_to_copy_directly:
            shutil.copy(fp, output_dir)
        file_paths_to_convert = analyze_files_to_convert(file_paths)
        file_paths_converted = convert_cr2_to_jpg(file_paths_to_convert, output_dir)
        print(f'{len(file_to_copy_directly) + len(file_paths_converted)} extracted! '
              f'({len(file_to_copy_directly)} files copied directly,'
              f' {len(file_paths_converted)} files converted)')


if __name__ == '__main__':
    args = parse_args()
    dir_path = args.dir_path
    dir_path = Path(dir_path)
    output_dir = args.output_dir
    output_dir = Path(output_dir)
    if not dir_path.exists():
        print(f'Invalid dir_path {dir_path}')
        sys.exit(1)
    if not dir_path.is_dir():
        print(f'Invalid dir_path {dir_path}')
        sys.exit(1)
    entry(dir_path=dir_path, output_dir=output_dir)
