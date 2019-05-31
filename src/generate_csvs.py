# :: generate_csvs.py
#####################################################
# Generates the CSV files necessary to train
#####################################################
# :: Created By: Benji Brandt <benjibrandt@ucla.edu>, 
#                Roy Lin <rlin2k1@gmail.com>, 
#                David Macaraeg <dmacaraeg@g.ucla.edu>
# :: Creation Date: 26 May 2019

import os
import argparse
import csv

from random import sample

import data_processing as dp
import image_processing as ip
from utilities import represents_int

parser = argparse.ArgumentParser(description="Generates CSV training data from a set of perfusion and labeled flair images.")

parser.add_argument("directory_name", action="store", help="The directory containing information for all patients.")
parser.add_argument("sample_count", action="store", help="The number of intensity values to obtain for interpolation.")
parser.add_argument("nlive", action="store", help="The number of intensity arrays which represent surviving pixels to sample.")
parser.add_argument("ndie", action="store", help="The number of intensity arrays which represent dying pixels to sample.")

_PERFUSION = "Perfusion"
_FLAIR = "FLAIR-COREG"

def sample_pixel_array(pixel_array, nlive, ndie):
    """
    Samples a pixel array for nlive and ndie coordinates of pixels which live and die, respectively.

    :param list_of_list pixel_array: a 2D array of pixels, representing an image
    :param int nlive: roughly how many pixel coordinates we wish to obtain for living pixels
    :param int ndead: roughly how many pixel coordinates we wish to obtain for dead pixels
    :return: a list of coordinates which point to roughly nlive pixels, and ndie pixels, combined
    :rtype: dict
    """
    l = []
    d = []
    ndie = int(ndie)
    nlive = int(nlive)
    for y in range(len(pixel_array)):
        for x in range(len(pixel_array[0])):
            if pixel_array[y][x] > 0:
                l.append((x, y))
            else:
                d.append((x, y))
    dead_sample = sample(d, ndie) if len(d) >= ndie else d
    if len(dead_sample) < ndie:
        nlive += ndie - len(dead_sample)
    live_sample = sample(l, nlive) if len(l) >= nlive else l
    return (live_sample, dead_sample)

def sample_labeled_flairs(flair_dict, nlive, ndie):
    """
    Samples a dictionary of the form: {flair_slice_locs: pixel_arrays} for nlive and ndie coordinates of pixels which live and die, respectively.
    Does this for each slice in the dict.

    :param dict flair_dict: a dict of the form: {flair_slice_locs: pixel_arrays}
    :param int nlive: roughly how many pixel coordinates we wish to obtain for living pixels
    :param int ndead: roughly how many pixel coordinates we wish to obtain for dead pixels
    :return: a dict of the form: {slice_loc: [(living_coords, dead_coords)]}.
    :rtype: dict
    """
    return(
        {
            slc: sample_pixel_array(pixel_array, nlive, ndie)
            for (slc, pixel_array) in flair_dict.items()
        }
    )

def generate_normalized_slice_loc_map(slice_dict):
    """
    Normalize the slice locations presented in slice_dict, such that the most negative is 0, and the largest is N, where N is the number of slices.

    :param dict slice_dict: a dictionary of some form: {slice_location: some_value}
    :return: two dictionarys, one of the form: {slice_location: normalized_slice_location}, and one of the form: {normalized_slice_location: slice_location}
    :rtype: dict
    """
    slices = sorted(slice_dict.keys())
    unorm_to_norm = {}
    norm_to_unorm = {}
    for i in range(len(slices)):
        unorm_to_norm[slices[i]] = i
        norm_to_unorm[i] = slices[i]
    return unorm_to_norm, norm_to_unorm

def parse_structured_dcm_data(structured_directory, sample_count, nlive, ndie, use_arr_storage=False):
    """
    Parses DCM data that has been structured in the following format:
        Patients <-- structured_directory_root
        |--- 1 <-- must be an integer
             |--- FLAIR
             |--- Perfusion
        |--- 2
             |--- FLAIR
             |--- Perfusion
        |--- ...
        |--- N
             |--- FLAIR
             |--- Perfusion

    :param str structured_directory: the name of a directory with DCM files, structured as above.
    :param int nlive: roughly how many pixel coordinates we wish to obtain for living pixels
    :param int ndead: roughly how many pixel coordinates we wish to obtain for dead pixels
    :param bool use_arr_storage: affects form of return value. See below.
    :return: a dictionary in one of the following forms: 
        if use_arr_storage is True: {slice_id: [(time_stamp, pixel_array), (time_stamp, pixel_array)...]}
        if use_arr_storage is False: {slice_id: {pixel_coordinate: array_of_pixel_values_over_time}}
    :rtpye: dict
    """
    for root, dirs, _ in os.walk(structured_directory):
        for id_num, directory in enumerate(dirs):
            if represents_int(directory):
                print("Parsing directory: {}".format(directory))
                print("Parsing perfusion data...")
                dd = ip.parse_perfusion_data(os.path.join(root, directory, _PERFUSION), use_arr_storage)
                print("Done!\nGenerating interpolations per slice...")
                df = dp.generate_interpolations_per_slice(dd)
                print("Done!\nGenerating resampled arrays per slice...")
                dfd = dp.generate_resampled_slice_dict(df, sample_count)
                # with the above, we now have voxels mapped to intensity arrays
                # now, we want to sample individual pixels per slice, 50% of which live, 50% of which die
                print("Done!\nParsing flair data...")
                labeled_flairs = ip.parse_flair_data(os.path.join(root, directory, _FLAIR))
                print("Done!\nSampling flair data...")
                perf_to_nrom, norm_to_perf = generate_normalized_slice_loc_map(dfd)
                flair_to_norm, norm_to_flair = generate_normalized_slice_loc_map(labeled_flairs)
                lfd = sample_labeled_flairs(labeled_flairs, nlive, ndie)
                print("Done!\nWriting training CSV file...")
                # Then grab the intensity arrays of those from dfd, generate the csvs
                with open("patient_{}_training.csv".format(directory), mode="a+") as tracsv, open("patient_{}_test.csv".format(directory), mode="a+") as tstcsv:
                    training_csv = csv.writer(tracsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    training_csv.writerow(["Healthy", "PixelDensity"])
                    for unorm_flair_slice, (live_coords, dead_coords) in lfd.items():
                        norm_flair_slice = flair_to_norm[unorm_flair_slice]
                        unorm_perf_slice = norm_to_perf[norm_flair_slice]
                        for coord in live_coords:
                            pv = dfd[unorm_perf_slice].get(coord)
                            if pv is not None: # some coordinates may still not carry over even with coregistration, such is a fact of life
                                training_csv.writerow([0, *pv])
                        for coord in dead_coords:
                            pv = dfd[unorm_perf_slice].get(coord)
                            if pv is not None: # some coordinates may still not carry over even with coregistration, such is a fact of life
                                training_csv.writerow([1, *pv])
                print("Done!\nWriting testing CSV file...")
                with open("patient_{}_test.csv".format(directory), mode="a+") as tstcsv:
                    test_csv = csv.writer(tstcsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    test_csv.writerow(["X", "Y", "Z", "PixelDensity"])
                    for perf_slice, coord_dict in dfd.items():
                        for coord, intensity_arr in coord_dict.items():
                                test_csv.writerow([0, *coord, perf_slice])
                print("Done!")


if __name__ == '__main__':
    args = parser.parse_args()
    print("Processing DCMs in directory: {}".format(args.directory_name))
    parse_structured_dcm_data(str(args.directory_name), args.sample_count, args.nlive, args.ndie)
