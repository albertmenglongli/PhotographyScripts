# combine 9 images of same size all together
import os
import random
from functools import partial
from pathlib import Path
from typing import List, Union

import PIL
import tqdm
from PIL import Image

from color_histogram import calculate_L1_distance_of_histogram
from utils import parse_input_paths

if not hasattr(PIL.Image, 'Resampling'):  # Pillow<9.0
    PIL.Image.Resampling = PIL.Image

SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'}
already_selected_images = set()


def combine_images(input_paths: Union[str, Path, List[Union[Path, str]]], output_path=None):
    global already_selected_images
    input_paths = parse_input_paths(input_paths, SUPPORTED_IMAGE_FORMATS)
    input_paths = [input_path for input_path in input_paths if input_path not in already_selected_images]

    input_paths = input_paths[:9 * 4]
    input_paths = random.sample(input_paths, k=9)
    already_selected_images.update(input_paths)

    if not output_path:
        # if output path is not specified, use the directory of input path
        output_path = os.path.dirname(input_paths[0])
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)

    images = [Image.open(input_path) for input_path in input_paths]
    # get the size of the first image
    width, height = images[0].size

    # make sure all images are of same size
    images = [image.resize((width, height), resample=Image.Resampling.LANCZOS) for image in images]

    new_image_path = Path(output_path) / (input_paths[0].stem + '_combo' + input_paths[0].suffix)
    new_image = Image.new('RGB', (width * 3, height * 3))
    # paste images together
    for index, image in enumerate(images):
        new_image.paste(image, (width * (index % 3), height * (index // 3)))
    new_image = new_image.resize((width, height), resample=Image.Resampling.LANCZOS)
    new_image.save(new_image_path)
    return new_image_path


if __name__ == '__main__':
    input_dir = '/Volumes/Samsung_T5/develop'
    output_dir = '/Volumes/Samsung_T5/develop_output'

    input_paths = parse_input_paths(Path(input_dir), SUPPORTED_IMAGE_FORMATS)
    kol_each_group = random.choices(list(input_paths), k=18)

    for candidate in tqdm.tqdm(kol_each_group):
        sorted_input_paths = sorted(input_paths, key=partial(calculate_L1_distance_of_histogram, candidate))
        combine_images(sorted_input_paths, output_dir)
