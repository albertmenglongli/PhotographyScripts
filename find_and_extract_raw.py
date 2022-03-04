#!/usr/bin/env python3
import multiprocessing
import os
import shutil
import sys
from pathlib import Path
import argparse

SELECTED_SUFFIXES = {'.JPG', '.jpeg', '.jpg'}
SRC_SUFFIXES = {'.CR2', '.CR3', '.ARW'}


def parse_args():
    description = ("Find and extract RAW to another directory")

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--selected_dir', dest='selected_dir', type=str, help='jpeg 等预览照片所在文件夹')
    parser.add_argument('--src_dir', dest='src_dir', type=str, help='源文件所在文件夹')
    parser.add_argument('--dst_dir', dest='dst_dir', type=str, help='输出文件夹')

    args = parser.parse_args()
    return args


def remove_suffix(v, s):
    return v[:-len(s)] if v.endswith(s) else v


def analyse_files_to_copy(selected_dir, src_dir, dst_dir):
    src_file_paths_to_copy = []
    not_found_src_file_names = []

    for root, sub_dirs, file_names in os.walk(selected_dir):
        for selected_file_name in file_names:
            selected_file_path = Path(root) / selected_file_name
            if selected_file_path.suffix in SELECTED_SUFFIXES:
                for src_suffix in SRC_SUFFIXES:
                    src_file_name = remove_suffix(selected_file_name, selected_file_path.suffix) + src_suffix
                    src_file_path = (src_dir / src_file_name)
                    if src_file_path.exists():
                        dst_file_path = (dst_dir / src_file_name)
                        if not dst_file_path.exists():
                            src_file_paths_to_copy.append(src_file_path)
                        break
                else:
                    not_found_src_file_names.append(selected_file_name)
    return src_file_paths_to_copy, not_found_src_file_names


def my_copy(src: Path, dst_dir):
    shutil.copy(src=src, dst=dst_dir)
    print(f'{src.name} copied')


if __name__ == '__main__':
    args = parse_args()
    selected_dir = args.selected_dir
    selected_dir: Path = Path(selected_dir)
    src_dir = args.src_dir
    src_dir: Path = Path(src_dir)
    dst_dir = args.dst_dir
    dst_dir: Path = Path(dst_dir)

    if not selected_dir.exists():
        print(f'SELECTED_DIR {selected_dir} 路径不存在')
        sys.exit(1)
    if not src_dir.exists():
        print(f'SRC_DIR {src_dir} 路径不存在')
        sys.exit(1)

    src_file_paths_to_copy, not_found_src_file_names = analyse_files_to_copy(selected_dir, src_dir, dst_dir)

    if not_found_src_file_names:
        print(f'以下照片对应源文件未找到:', ','.join(not_found_src_file_names))

    if src_file_paths_to_copy:
        if not dst_dir.exists():
            dst_dir.mkdir(parents=True, exist_ok=True)

        pool = multiprocessing.Pool()
        for src_file_path in src_file_paths_to_copy:
            pool.apply_async(my_copy, (src_file_path, dst_dir))
        pool.close()
        pool.join()
