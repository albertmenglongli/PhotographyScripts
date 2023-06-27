import os
from pathlib import Path
from typing import Union

import PIL
import numpy as np
import tqdm
from PIL import Image

from utils import parse_input_paths

SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'}

if not hasattr(PIL.Image, 'Resampling'):  # Pillow<9.0
    PIL.Image.Resampling = PIL.Image


def histeq(im, nbr_bins=256):
    # get image histogram
    imhist, bins = np.histogram(im.histogram(), nbr_bins, normed=True)
    print(bins)
    cdf = imhist.cumsum()  # cumulative distribution function
    cdf = 255 * cdf / cdf[-1]  # normalize
    return cdf


# a cache decorator to store already calculated histograms, and save cache into file under tmp folder
def cache(func):
    def wrapper(*args, **kwargs):
        # load cache from file using numpy
        cache_path = Path('/tmp') / (func.__name__ + '.npy')
        if os.path.exists(cache_path):
            cache_dict = np.load(cache_path, allow_pickle=True).item()
        else:
            cache_dict = {}
        if args in cache_dict:
            return cache_dict[args]
        else:
            result = func(*args, **kwargs)
            cache_dict[args] = result
            np.save(cache_path, cache_dict)
            return result

    return wrapper


# generate histograms of image passed in
@cache
def generate_histograms(input_path: Union[str, Path]):
    img = Image.open(input_path)
    # convert to grayscale
    img_gray = img.convert(mode='L')

    # convert to NumPy array
    img_array = np.asarray(img_gray)

    # STEP 1: Normalized cumulative histogram
    # flatten image array and calculate histogram via binning
    histogram_array = np.bincount(img_array.flatten(), minlength=256)

    # normalize
    num_pixels = np.sum(histogram_array)
    histogram_array = histogram_array / num_pixels

    return histogram_array


# calculate L1 for two histograms
@cache
def calculate_L1_distance_of_histogram(img_path1, img_path2):
    histogram_array1 = generate_histograms(img_path1)
    histogram_array2 = generate_histograms(img_path2)
    return np.sum(np.abs(histogram_array1 - histogram_array2))


# calculate L2 for two histograms
@cache
def calculate_L2_distance_of_histogram(img_path1, img_path2):
    histogram_array1 = generate_histograms(img_path1)
    histogram_array2 = generate_histograms(img_path2)
    return np.sum(np.square(histogram_array1 - histogram_array2))
