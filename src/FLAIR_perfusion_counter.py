# :: FLAIR_perfusion_counter.py
#####################################################
# Functions to handle processing the raw DCM images.
#####################################################
# :: Created By: Benji Brandt <benjibrandt@ucla.edu>, 
#                Roy Lin <rlin2k1@gmail.com>, 
#                David Macaraeg <dmacaraeg@g.ucla.edu>
# :: Creation Date: May 29, 2019

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
# from src import image_processing as ip

_INSTANCE_NUMBER = (0x0020, 0x0013)
_ACQUISITION_NUMBER = (0x0020, 0x0012)

print ("Patient No: FLAIR_COUNT PERFUSION_COUNT")
for patient_no in range(1,19):
    direc1 = "./Patients/{0}/Perfusion".format(patient_no)
    slice_locations = []
    for file in os.listdir(direc1):
        if file.endswith(".dcm"):
            dcm = pydicom.dcmread(os.path.join(direc1, file))
            slice_locations.append(dcm.SliceLocation)
    slice_locations = set(slice_locations)

    direc2 = "./Patients/{0}/FLAIR".format(patient_no)
    FLAIR_count = 0
    for file in os.listdir(direc2):
        if file.endswith(".dcm"):
            FLAIR_count += 1

    print (str(patient_no) + ": ", FLAIR_count, len(slice_locations))

