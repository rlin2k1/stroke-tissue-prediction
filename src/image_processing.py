# :: image_processing.py
#####################################################
# Functions to handle processing the raw DCM images.
#####################################################
# :: Created By: Benji Brandt <benjibrandt@ucla.edu>, 
#                Roy Lin <rlin2k1@gmail.com>, 
#                David Macaraeg <dmacaraeg@g.ucla.edu>
# :: Creation Date: 15 May 2019

import pydicom
import numpy as np
from random import sample

def random_sample_pixel_map(pixel_map, number_of_samples):
    """
    Randomly samples the provided pixel map to obtain number_of_samples coordinates.

    :param dict pixel_map: a key-value storage of coordinates to pixel values.
    :param int number_of_samples: the number of samples we wish to obtain.
    :return: a dictionary comprised of number_of_samples randomly-selected key-value pairs from pixel_map.
    :rtype: dict
    """
    keys = sample(pixel_map.keys(), number_of_samples)
    return {k:v for (k, v) in pixel_map.items() if k in keys}

def map_pixel_data(pixels, ignore_zero_intensity = True):
    """
    Creates a dictionary of pixel coordinates to pixel values.

    :param arr pixels: the 2-d array of pixels generated by pydicom's pixel_array.
    :param bool ignore_zero_intensity: if true, mappings won't be created for pixels which have 0 as their value.
    :return: a dictionary of image coordinates as the key, matched with pixel values as the value.
    :rtype: dict
    """
    sto = {}
    for x in range(len(pixels)):
        for y in range(len(pixels[x])):
            if ignore_zero_intensity and pixels[x][y] == 0: 
                continue
            sto[(x, y)] = pixels[x][y]
    return sto

import os
def three_dimensional_representation(folder_name):
    for filename in os.listdir(folder_name):
        pass