# :: benji_playground.py
#####################################################
# Place to mess around with and figure out python code.
#####################################################
# :: Created By: Benji Brandt <benjibrandt@ucla.edu>
# :: Creation Date: 15 May 2019

import sys
sys.path.append("..")

import os
import pydicom
from src import image_processing as ip

ds = pydicom.dcmread("IM-0008-0024.dcm")
pixels = ds.pixel_array
d = ip.map_pixel_data(pixels)


print(ip.random_sample_pixel_map(d, 5))

