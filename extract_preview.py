#!/usr/bin/env python3
import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import Optional, Set

from tqdm import tqdm

from utils import convert_cr2_to_jpg, extract_image_seq_num


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


def entry(dir_path: Path, output_dir: Path, start, end, force=False):
    my_start = start or 0
    my_end = end or float('inf')

    if my_start > my_end:
        raise ValueError(f'start {start} must less equal than end {end}')

    output_dir.mkdir(parents=True, exist_ok=True)
    for root, sub_dirs, file_names in os.walk(dir_path):
        file_paths = set([Path(root) / file for file in file_names])
        # ignore files starts with '._'
        file_paths = set(filter(lambda fp: not fp.name.startswith('._'), file_paths))
        if not (start is None and end is None):
            file_paths = set(filter(lambda fp: my_start <= extract_image_seq_num(fp) <= my_end, file_paths))
        else:
            pass

        file_to_copy_directly = set(filter(lambda fp: fp.name.endswith('.JPG'), file_paths))
        file_paths_to_convert = analyze_files_to_convert(file_paths)
        total = len(file_to_copy_directly) + len(file_paths_to_convert)

        with tqdm(total=total) as pbar:
            for fp in file_to_copy_directly:
                if not force and (output_dir / fp.name).exists():
                    pass
                else:
                    shutil.copy(fp, output_dir)
                pbar.update(1)

            file_paths_converted = set()
            for fp in file_paths_to_convert:
                if not force and (output_dir / (fp.stem + '.JPG')).exists():
                    pass
                else:
                    file_paths_converted |= convert_cr2_to_jpg(fp, output_dir)
                pbar.update(1)

        print(f'{len(file_to_copy_directly) + len(file_paths_converted)} extracted! '
              f'({len(file_to_copy_directly)} files copied directly,'
              f' {len(file_paths_converted)} files converted)')


def parse_args():
    description = ("Extract JPG to another directory, convert to JPG for CR2 without preview")

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(dest='dir_path', type=str, help='dir')
    parser.add_argument(dest='output_dir', type=str, help='dir')
    parser.add_argument('-s', '--start', dest='start', type=int, help='start', required=False, default=None)
    parser.add_argument('-e', '--end', dest='end', type=int, help='start', required=False, default=None)

    args = parser.parse_args()
    return args


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
    entry(dir_path=dir_path, output_dir=output_dir, start=args.start, end=args.end)
