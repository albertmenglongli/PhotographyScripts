#!/usr/bin/env python3
import argparse
import os
import random
from pathlib import Path

from PIL import Image

WATERMARK_FILEPATHS = [
    './data/watermark_1.png', './data/watermark_2.png',
    './data/watermark_3.png', './data/watermark_4.png'
]

SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']
DOWNSAMPLING_STR = 'downsampling'


def add_watermark(image_path, ratio=4):
    """
    Add watermark to an image
    """
    image = Image.open(image_path)
    width, height = image.size
    watermarks = [Image.open(watermark_filepath) for watermark_filepath in WATERMARK_FILEPATHS]
    watermarks = [watermark.resize((width // ratio, height // ratio), resample=Image.Resampling.LANCZOS)
                  for watermark in watermarks]

    layer = Image.new('RGBA', image.size, (0, 0, 0, 0))

    # add watermark in four corners of the image
    layer.paste(random.choice(watermarks), (0, 0))
    layer.paste(random.choice(watermarks), (0, height - height // ratio))
    layer.paste(random.choice(watermarks), (width - width // ratio, 0))
    layer.paste(random.choice(watermarks), (width - width // ratio, height - height // ratio))

    # add watermark in the center of the image
    layer.paste(random.choice(watermarks), (width // 2 - width // ratio // 2, height // 2 - height // ratio // 2))

    return Image.composite(layer, image, layer)


def downsampling_n_save_image(input_path, output_path=None, quality=50, force=False):
    input_path = Path(input_path)
    if not output_path:
        # if output path is not specified, use the directory of input path
        output_path = os.path.dirname(input_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)
    # appending new image with watermark, the new generated filename has '_downsampling' as suffix
    new_image_path = Path(output_path) / (input_path.stem + f'_{DOWNSAMPLING_STR}_{quality}' + input_path.suffix)
    if new_image_path.exists() and not force:
        print(f'already exists output image with quality {quality}: {new_image_path}')
        return
    new_image = add_watermark(input_path)
    # resize new_image to smaller image
    new_image = new_image.resize(
        (new_image.width // 2, new_image.height // 2),
        resample=Image.Resampling.LANCZOS)
    print(f'new image with quality {quality} generated: {new_image_path}')
    new_image.save(new_image_path, quality=quality)


def dfs_handle(input_path, output_path, quality, force=False):
    input_path: Path = Path(input_path)
    if input_path.is_dir():
        for file_name in os.listdir(input_path):
            file_path = os.path.join(input_path, file_name)
            dfs_handle(file_path, output_path, quality, force)
    elif input_path.is_file() and input_path.suffix in SUPPORTED_IMAGE_FORMATS:
        if DOWNSAMPLING_STR not in input_path.name:
            if not output_path:
                # if output path is not specified, use the directory of input path
                output_path = os.path.dirname(input_path)
            downsampling_n_save_image(input_path, output_path, quality, force)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='input image path')
    parser.add_argument('--output', type=str, default='', help='input image path')
    parser.add_argument('--quality', type=int, default=30, help='quality of the output image')
    # parser get bool value from command line, if the value is not specified, the default value is False
    parser.add_argument('--force', action='store_true', default=False,
                        help='force to overwrite the existing output image')

    args = parser.parse_args()
    input_path = Path(args.input)
    output_path = args.output or None
    quality = args.quality
    force = args.force

    if not input_path:
        raise ValueError('input path is empty')

    if not os.path.exists(input_path):
        raise ValueError('input path is not exists')

    dfs_handle(input_path, output_path, quality, force)
