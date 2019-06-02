# :: data_processing.py
#####################################################
# Functions to handle processing the data created
# via the functions in image_processing.py
#####################################################
# :: Created By: Benji Brandt <benjibrandt@ucla.edu>, 
#                Roy Lin <rlin2k1@gmail.com>, 
#                David Macaraeg <dmacaraeg@g.ucla.edu>
# :: Creation Date: 26 May 2019

# Standard Library, specific imports
from random import sample
from math import floor

# Dependency Imports
from scipy import interpolate
import numpy as np

# ----------------------------------------------------------------------------
#  Functions
# ----------------------------------------------------------------------------

def generate_interpolations_per_slice(slice_dict):
    """
    Takes the data from a slice dictionary in the form {slice_id: {pixel_coordinate: array_of_pixel_values_over_time}}
    and generates interpolations in place of the array_of_pixel_values_over_time.

    :param dict slice_dict: a dict of the form: {slice_id: {pixel_coordinate: array_of_pixel_values_over_time}}
    :return: a dict of the form: {slice_id: {pixel_coordinate: pixel_intensity_interp_func}}
    :rtype: dict
    """
    return (
            {slice_id: 
                {
                    coord: interpolate.interp1d(np.array([t for (t, _) in intensity_arr]).astype("float64"),
                                                [i_val for (_, i_val) in intensity_arr], 
                                                kind = "cubic") 
                    for (coord, intensity_arr) in coord_dict.items()
                } 
                for (slice_id, coord_dict) in slice_dict.items()
            }
    )


def sample_interp_intensity(interp_func, count):
<<<<<<< HEAD
    """
    Takes the interp_function, and samples it to obtain count values evenly-spaced across its domain

    :param <func> interp_func: an interpolation function generated from data via scipy
    :param int count: the number of samples to obtain
    :return: a list of length count, with values obtained at evenly-spaced intervals across interp_func to obtain count total
    """
    times = interp_func.x
    t_start = times[0]
    t_end = times[len(times)-1]
    step = (t_end - t_start) / count
    l = []
    for t in np.arange(t_start, t_end, step):
        l.append(interp_func(t))
=======
    """
    Takes the interp_function, and samples it to obtain count values evenly-spaced across its domain

    :param <func> interp_func: an interpolation function generated from data via scipy
    :param int count: the number of samples to obtain
    :return: a list of length count, with values obtained at evenly-spaced intervals across interp_func to obtain count total
    """
    times = interp_func.x
    t_start = float(times[0])
    t_end = float(times[len(times)-1])
    step = (t_end - t_start) / float(count)
    l = []
    for t in np.arange(t_start, t_end-1, step):
        l.append(float(interp_func(t).item()))
>>>>>>> 46a4c19023d09fc6a835fe3d3351236698cded5f
    return l


def generate_resampled_slice_dict(interpolation_dict, n_intensity_vals):
<<<<<<< HEAD
    """
    Takes the data from a slice dictionary in the form {slice_id: {pixel_coordinate: array_of_pixel_values_over_time}}
    and generates intensity arrays by evenly sampling each coordinate's interpolation function.

    :param dict slice_dict: a dict of the form: {slice_id: {pixel_coordinate: array_of_pixel_values_over_time}}
    :param int n_intensity_vals: the number of intensity values to put in the list replacing the interpolations.
    :return: a dict of the form: {slice_id: {pixel_coordinate: [evenly_sampled_array_of_intensities]}}
    :rtype: dict
    """
    return (
            {slice_id: 
                {
                    coord: sample_interp_intensity(interp_func, n_intensity_vals)
                    for (coord, interp_func) in coord_dict.items()
                } 
                for (slice_id, coord_dict) in interpolation_dict.items()
            }
    )

=======
    """
    Takes the data from a slice dictionary in the form {slice_id: {pixel_coordinate: array_of_pixel_values_over_time}}
    and generates intensity arrays by evenly sampling each coordinate's interpolation function.
>>>>>>> 46a4c19023d09fc6a835fe3d3351236698cded5f

    :param dict slice_dict: a dict of the form: {slice_id: {pixel_coordinate: array_of_pixel_values_over_time}}
    :param int n_intensity_vals: the number of intensity values to put in the list replacing the interpolations.
    :return: a dict of the form: {slice_id: {pixel_coordinate: [evenly_sampled_array_of_intensities]}}
    :rtype: dict
    """
    return (
            {slice_id: 
                {
                    coord: sample_interp_intensity(interp_func, n_intensity_vals)
                    for (coord, interp_func) in coord_dict.items()
                } 
                for (slice_id, coord_dict) in interpolation_dict.items()
            }
    )
