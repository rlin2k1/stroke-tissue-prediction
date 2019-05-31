# :: image_processing.py
#####################################################
# Functions to handle processing the raw DCM images.
#####################################################
# :: Created By: Benji Brandt <benjibrandt@ucla.edu>, 
#                Roy Lin <rlin2k1@gmail.com>, 
#                David Macaraeg <dmacaraeg@g.ucla.edu>
# :: Creation Date: 15 May 2019


import os
from random import sample
from collections import defaultdict
from operator import itemgetter
import argparse
import re

import pydicom

parser = argparse.ArgumentParser(description="Processes DCM files into python data structures.")

parser.add_argument("directory_name", action="store")
parser.add_argument("-r", "--recursive", action="store_true", dest="recursive", default=False, help="Examine all subdirectories within directory_name, assuming each subdirectory corresponds to a patient. Ignores DCM files within the immediate directory.")


def random_sample_pixel_map(pixel_map, number_of_samples):
    """
    Randomly samples the provided pixel map to obtain number_of_samples coordinates.

    :param dict pixel_map: a key-value storage of coordinates to pixel values.
    :param int number_of_samples: the number of samples we wish to obtain.
    :return: a dictionary comprised of number_of_samples randomly-selected key-value pairs from pixel_map.
    :rtype: dict
    """
    keys = sample(pixel_map.keys(), number_of_samples)
    return {k: v for (k, v) in pixel_map.items() if k in keys}


def _clean_slice_dict(slice_dict):
    """
    Uses dictionary comprehension to remove the time data from pixel_arrs, turning [(time, val), (time, val)] into [val, val]

    :param dict slice_dict: a dict of the form {slice_id: {coord: pixel_arr}}.
    :return: the same dictionary, but with the (time, val) tuples in pixel_arrs replaced just by their values.
    :rtpye: dict
    """
    return {slice_id: {coord: [i_val for (_, i_val) in intensity_arr] for (coord, intensity_arr) in coord_dict.items()} for (slice_id, coord_dict) in slice_dict.items()}


def _sort_slice_dict(slice_dict, use_arr_storage):
    """
    Sorts the nested pixel arrays within {slice_id: {coord: pixel_arr}}-type dictionaries in order of ascending time.
    Assumes items in a pixel_arr are in the form (timestamp, pixel_value)

    :param dict slice_dict: a dict of the form {slice_id: {coord: pixel_arr}}.
    :param bool use_arr_storage: assumes dict in the following forms based on this value:
        if use_arr_storage is True: {slice_id: [(time_stamp, pixel_array), (time_stamp, pixel_array)...]}
        if use_arr_storage is False: {slice_id: {pixel_coordinate: array_of_pixel_values_over_time}}
    :return: the same dictionary, but with each given pixel intensity array sorted via the time slice the data corresponds to.
    :rtpye: dict
    """
    if use_arr_storage:
        for timestamped_pixelmaps in slice_dict.values():
            timestamped_pixelmaps.sort(key=itemgetter(0))
    else:
        for coordinate_dict in slice_dict.values():
            for pixel_arr in coordinate_dict.values():
                pixel_arr.sort(key=itemgetter(0))


def parse_perfusion_data(directory_name, use_arr_storage=False):
    """
    Parses all DCMs within directory_name, creating a mapping between slice_id, pixel coordinates, and pixel intensity over time.
    Will not look at subdirectories.

    :param str directory_name: the name of a directory with DCM files to examine.
    :param bool use_arr_storage: affects form of return value. See below.
    :return: a dictionary in one of the following forms: 
        if use_arr_storage is True: {slice_id: [(time_stamp, pixel_array), (time_stamp, pixel_array)...]}
        if use_arr_storage is False: {slice_id: {pixel_coordinate: array_of_pixel_values_over_time}}
    :rtpye: dict
    """
    slice_dict = defaultdict(list) if use_arr_storage else {}
    for file in os.listdir(directory_name):
        if file.endswith(".dcm"):
            dcm = pydicom.dcmread(os.path.join(directory_name, file))
            if use_arr_storage:
                slice_dict[dcm.SliceLocation].append((dcm.AcquisitionTime, dcm.pixel_array))
            else:
                if dcm.SliceLocation in slice_dict.keys():
                    map_pixel_data(dcm.pixel_array, dcm.AcquisitionTime, slice_dict[dcm.SliceLocation])
                else:
                    slice_dict[dcm.SliceLocation] = map_pixel_data(dcm.pixel_array, dcm.AcquisitionTime)
    _sort_slice_dict(slice_dict, use_arr_storage)
    return slice_dict


def parse_perfusion_data_recursively(root_directory_name, use_arr_storage=False):
    """
    Parses all DCMs contained within subdirectories inside root_directory_name, creating a mapping between patient_id, slice_id, pixel coordinates, and pixel intensity over time.
    patient_id is taken from an arbitrary number assigned to the patient's directory.

    :param str root_directory_name: the name of a directory with DCM files to examine.
    :param bool use_arr_storage: affects form of return value. See below.
    :return: a dictionary in one of the following forms: 
        if use_arr_storage is True: {slice_id: [(time_stamp, pixel_array), (time_stamp, pixel_array)...]}
        if use_arr_storage is False: {slice_id: {pixel_coordinate: array_of_pixel_values_over_time}}
    :rtpye: dict
    """
    patient_dict = {}
    for root, dirs, _ in os.walk(root_directory_name):
        for id_num, directory in enumerate(dirs):
            patient_dict[id_num] = parse_perfusion_data(os.path.join(root, directory), use_arr_storage)
    return patient_dict


def parse_flair_data(directory_name):
    """
    Parses all coregistered flair images in directory name.
    Assumes files are named like: result_img-id_acqui-num_acqui-time_slice-loc

    :param str directory_name: the name of a directory with DCM files to examine.
    :return: a dictionary of the form {slice_id: pixel_array}
    :rtpye: dict
    """
    slice_dict = {}
    match_flair_slice_loc = re.compile(r"_([+-]*[0-9]+\.*[0-9]*).dcm")
    for file in os.listdir(directory_name):
        if file.endswith(".dcm"):
            dcm = pydicom.dcmread(os.path.join(directory_name, file))
            slice_loc = match_flair_slice_loc.search(file).group(1)
            slice_dict[slice_loc] = dcm.pixel_array
    return slice_dict

def map_pixel_data(pixels, creation_time, slice_data=None, ignore_zero_intensity=True):
    """
    Creates a dictionary of pixel coordinates to pixel values.

    :param list pixels: a list of lists, where each sublist is a 2-d array of pixels generated by pydicom's pixel_array for a specific time slice.
    :param bool ignore_zero_intensity: if true, mappings won't be created for pixels which have 0 as their value.
    :return: a dictionary of image coordinates as the key, matched with pixel values as the value.
    :rtype: dict
    """
    if slice_data is None: slice_data = defaultdict(list)
    pixel_sz_x = len(pixels)
    for x in range(pixel_sz_x):
        for y in range(len(pixels[x])):
            if ignore_zero_intensity and pixels[x][y] == 0: 
                continue
            slice_data[(x, y)].append((creation_time, pixels[x][y]))
    return slice_data


# if __name__ == '__main__':
#     args = parser.parse_args()
#     print("Processing DCMs in directory: {}".format(args.directory_name))
#     if args.recursive:
#         print(parse_perfusion_data_recursively(str(args.directory_name)))
#     else:
#         print(parse_perfusion_data(str(args.directory_name)))
