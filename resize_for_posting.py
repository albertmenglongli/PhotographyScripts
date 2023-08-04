#!/usr/bin/env python3
import argparse
import os
from pathlib import Path

from PIL import Image
import PIL

SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'}

if not hasattr(PIL.Image, 'Resampling'):  # Pillow<9.0
    PIL.Image.Resampling = PIL.Image


def resize_image(image_path: Path, max_edge_length) -> PIL.Image:
    image = Image.open(image_path)
    width, height = image.size

    if width < height:
        # resize height to max_edge_length
        ratio = max_edge_length / height
        new_width = int(width * ratio)
        new_height = max_edge_length
    else:
        # resize width to max_edge_length
        ratio = max_edge_length / width
        new_width = max_edge_length
        new_height = int(height * ratio)

    new_image = image.resize((new_width, new_height), resample=Image.Resampling.LANCZOS)
    return new_image


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Resize image to max edge length')
    parser.add_argument('--input_dir', type=str, help='input path to image dir')
    parser.add_argument('--output_dir', type=str, help='output path to image dir', default=None)
    parser.add_argument('--max_edge_length', type=int, default=1706, help='max edge length of the output image')
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir) if args.output_dir else input_dir
    max_edge_length = args.max_edge_length

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):
        file_path = Path(input_dir) / file_name
        if (os.path.isfile(file_path)
                and file_path.suffix in SUPPORTED_IMAGE_FORMATS
                and f'-ds{str(max_edge_length)}' not in file_name):
            new_image_path = Path(output_dir) / (file_path.stem + f'-ds{str(max_edge_length)}' + file_path.suffix)
            if not new_image_path.exists():
                new_image = resize_image(file_path, max_edge_length=max_edge_length)
                # appending like'-ds1706' to the filename
                new_image.save(new_image_path)
                print(f'{file_path} resized to {new_image.size}')
