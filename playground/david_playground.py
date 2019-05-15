import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pydicom
import time
from pydicom.data import get_testdata_files

def main():
	#filename = get_testdata_files('IM-0006-0731.dcm')[0]
	ds = pydicom.dcmread('IM-0006-0731.dcm') 
	plt.imshow(ds.pixel_array, cmap=plt.cm.bone) 
	plt.show()

if __name__ == "__main__":
	main()
