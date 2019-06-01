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

# dicom image standards: ftp://dicom.nema.org/MEDICAL/dicom/2016a/output/chtml/part03/sect_C.7.6.html
# Series Number indicates scan type (i.e., perfusion vs flair)
# Patient ID has been anonymized, but the data he has given us is already organized by patient
# Instance Number uniquely identifies an image within a given series
# Acquisition number indicates which scan we're doing --> this is the one that will vary with time, then. Have 25 slices per acquisition number.
# Slice location indicates which slice we're looking at, so we can consistently add a value
# Creation time will allow for sorting of pixel values within a sllsice via time, though instance number ought to anyway

print ("Patient No: FLAIR_COUNT PERFUSION_COUNT")
for patient_no in range(1,19):
    direc1 = "./Patients/{0}/Perfusion".format(patient_no)
    # acquisition_dict = {} # maps acquistion # to slices corresponding to that acqusition # 
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

'''
        acquisition_number = dcm.AcquisitionNumber
        if acquisition_number not in acquisition_dict.keys():
            acquisition_dict[acquisition_number] = 0
        acquisition_dict[acquisition_number] += 1

for key, value in acquisition_dict.items():
    print (key, value)
    #if value != 26:
    #    print (key)
'''
        


'''
        print("-----")
        print("Reading file: {}".format(os.path.join(direc, file)))
        dcm = pydicom.dcmread(os.path.join(direc, file))
        # print(dcm)
        print("Patient ID: {}".format(dcm.PatientID))
        print("Acquisition Number: {}".format(dcm.AcquisitionNumber))
        print("Acquisiton Time: {}".format(dcm.AcquisitionTime))
        print("Instance Number: {}".format(dcm.InstanceNumber))
        print("Rows, Cols: {}".format((dcm.Rows, dcm.Columns)))
        print("Series Number: {}".format(dcm.SeriesNumber))
        print("Creation Time: {}".format(dcm.InstanceCreationTime))
        print("Slice Location: {}".format(dcm.SliceLocation))
'''

# result_acquisitionNum_sliceLoc_creationTime


# {0: {(34, 43): [(0, 221), (2, 3212), (-1, 3421), (1, 1234), (10, 123432)],
#     (52, 12): [(-2, 421), (21, 412), (5, 2321)]}, 
# 1: {(0, 2): [(54, 12123), (55, 12123)]}}