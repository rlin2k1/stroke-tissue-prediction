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

_INSTANCE_NUMBER = (0x0020, 0x0013)
_ACQUISITION_NUMBER = (0x0020, 0x0012)

# dicom image standards: ftp://dicom.nema.org/MEDICAL/dicom/2016a/output/chtml/part03/sect_C.7.6.html
# Series Number indicates scan type (i.e., perfusion vs flair)
# Patient ID has been anonymized, but the data he has given us is already organized by patient
# Instance Number uniquely identifies an image within a given series
# Acquisition number indicates which scan we're doing --> this is the one that will vary with time, then. Have 25 slices per acquisition number.
# Slice location indicates which slice we're looking at, so we can consistently add a value
# Creation time will allow for sorting of pixel values within a slice via time, though instance number ought to anyway


for file in os.listdir("./ep2d_perf_35"):
    if file.endswith(".dcm"):
        print("-----")
        print("Reading file: {}".format(os.path.join("./ep2d_perf_35", file)))
        dcm = pydicom.dcmread(os.path.join("./ep2d_perf_35", file))
        print("Patient ID: {}".format(dcm.PatientID))
        print("Acquisition Number: {}".format(dcm.AcquisitionNumber))
        print("Instance Number: {}".format(dcm.InstanceNumber))
        print("Rows, Cols: {}".format((dcm.Rows, dcm.Columns)))
        print("Series Number: {}".format(dcm.SeriesNumber))
        print("Creation Time: {}".format(dcm.InstanceCreationTime))
        print("Slice Location: {}".format(dcm.SliceLocation))


# {0: {(34, 43): [(0, 221), (2, 3212), (-1, 3421), (1, 1234), (10, 123432)],
#     (52, 12): [(-2, 421), (21, 412), (5, 2321)]}, 
# 1: {(0, 2): [(54, 12123), (55, 12123)]}}