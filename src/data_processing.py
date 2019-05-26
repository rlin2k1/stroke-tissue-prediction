# :: data_processing.py
#####################################################
# Functions to handle processing the data created
# via the functions in image_processing.py
#####################################################
# :: Created By: Benji Brandt <benjibrandt@ucla.edu>, 
#                Roy Lin <rlin2k1@gmail.com>, 
#                David Macaraeg <dmacaraeg@g.ucla.edu>
# :: Creation Date: 26 May 2019

from scipy import interpolate
import numpy as np


# TODO: Can use interp_func.x to get range of acceptable inputs, and then get fixed number of outputs
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
                    coord: interpolate.interp1d(np.array([t for (t, _) in intensity_arr]).astype('float64'),
                                                [i_val for (_, i_val) in intensity_arr], 
                                                kind = "cubic") 
                    for (coord, intensity_arr) in coord_dict.items()
                } 
                for (slice_id, coord_dict) in slice_dict.items()
            }
    )

