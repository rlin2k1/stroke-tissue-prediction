import os
import pydicom
from pydicom.data import get_testdata_files
import matplotlib.pyplot as plt
import time

ds = pydicom.dcmread('test.dcm')  # plan dataset
ds.PixelData
print(ds.pixel_array)
plt.imshow(ds.pixel_array, cmap=plt.cm.bone)
plt.show()
print(ds)