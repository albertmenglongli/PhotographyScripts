from collections import deque
import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Set, Union

import imageio
import rawpy  # "brew install libraw" required in MacOS


def convert_cr2_to_jpg(file_paths: Union[Set[Path], Path], output_dir: Optional[Path] = None):
    if isinstance(file_paths, Path):
        file_paths = {file_paths}
    file_paths_converted = set()

    for file_path in file_paths:
        output_dir = output_dir or file_path.parent
        new_file_path = output_dir / (file_path.stem + '.JPG')
        try:
            with rawpy.imread(str(file_path)) as raw:
                try:
                    thumb = raw.extract_thumb()
                except rawpy.LibRawNoThumbnailError:
                    print('no thumbnail found')
                    continue
                except rawpy.LibRawUnsupportedThumbnailError:
                    print('unsupported thumbnail')
                    continue
                else:
                    if thumb.format == rawpy.ThumbFormat.JPEG:
                        # thumb.data is already in JPEG format, save as-is
                        with open(str(new_file_path), 'wb') as f:
                            f.write(thumb.data)
                    elif thumb.format == rawpy.ThumbFormat.BITMAP:
                        # thumb.data is an RGB numpy array, convert with imageio
                        imageio.imsave(str(new_file_path), thumb.data)
                    file_paths_converted.add(file_path)
        except Exception as e:
            print(str(e), file_path)
            continue
    return file_paths_converted


def remove(path: Path):
    path = Path(path)
    path = str(path)
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))


def identity(x):
    """Returns its argument."""
    return x


def copy_under_dir(dir_path: Path, dest: Path, pred=identity):
    file_paths = set()
    for root, sub_dirs, file_names in os.walk(dir_path):
        file_paths |= set([Path(root) / file for file in file_names])
    file_paths = filter(pred, file_paths)
    for fp in file_paths:
        shutil.copy(fp, dest)


def cmd_nouchg(file_path: Path):
    subprocess.run(f'chflags nouchg {str(file_path)}', shell=True, universal_newlines=True,
                   stdout=subprocess.PIPE, check=True)


def delete_file_paths(file_paths: Optional[Set[Path]]):
    for file_path in file_paths:
        try:
            remove(file_path)
        except PermissionError as e:
            cmd_nouchg(file_path)
            remove(file_path)


def extract_image_seq_num(file_path: Path):
    file_stem = file_path.stem

    seq_num_chars = deque()
    for c in file_stem[::-1]:
        if c.isdigit():
            seq_num_chars.appendleft(c)
        else:
            break

    seq_num = ''.join(seq_num_chars)
    seq_num = int(seq_num)
    return seq_num
