import png
import os
import sys
import pydicom
import numpy as np

ROOT_DIR = os.getcwd()
IN_DIR = ROOT_DIR + "/data"
PNG_IN_DIR = ROOT_DIR + "output/pix2pix/inputs"
PNG_OUT_DIR = ROOT_DIR + "output/pix2pix/outputs"
INPUT = "Features"
OUTPUT = "Labels"

def convert(mri_path, mri_filename):
    """ Function to convert a DICOM MRI file to PNG
    @param mri_path: The absolute path to the dicom file
    @param mri_filename: The name of the file without the path
    """

    # Read Dicom file
    mri_file = open(mri_path, "rb")
    ds = pydicom.read_file(mri_file)
    mri_file.close()

    # Get dicom data
    shape = ds.pixel_array.shape
    # Convert to float to avoid overflow or underflow losses.
    image_2d = ds.pixel_array.astype(float)
    # Rescaling grey scale 
    normalize_factor = 2000.0 if INPUT not in mri_filename else image_2d.max()
    if INPUT not in mri_filename:
        image_2d[image_2d==5000.0] = normalize_factor
    for row in range(len(image_2d)):
        for col in range(len(image_2d[0])):
            image_2d[row][col] = (image_2d[row][col] / normalize_factor) * 255.0
            
    # Convert to uint8 
    image_2d_scaled = np.uint8(image_2d)

    if INPUT in mri_filename:
        new_filename = mri_filename.replace(INPUT+'_', '')
        png_fn = os.path.join(PNG_IN_DIR, new_filename + '.png')
    elif OUTPUT in mri_filename:
        new_filename = mri_filename.replace(OUTPUT+'_', '')
        png_fn = os.path.join(PNG_OUT_DIR, new_filename + '.png')
        
    print('Writing {}...'.format(png_fn))
    # Create PNG file
    png_file = open(png_fn, "wb")
    # Write to png file
    w = png.Writer(shape[1], shape[0], greyscale=True)
    w.write(png_file, image_2d_scaled)
    png_file.close()

def getFiles(root_dir, files):
    for r, s, f in os.walk(root_dir):
        if f == []:
            for sn in s:
                curr_path = os.path.join(r, sn)
                getFiles(curr_path, files)
        else:
            for fn in f:
                if os.path.splitext(fn)[1] == '.dcm':
                    curr_path = os.path.join(r, fn)
                    dirs = r.split('/')
                    pre = dirs[-2] + '_' + dirs[-1] + '_'
                    files.add((curr_path, pre + fn[:-4]))

def rename_and_generate(IN_DIR):


def main():
    # Create png directory
    if not os.path.exists(PNG_IN_DIR):
        os.makedirs(PNG_IN_DIR)
    if not os.path.exists(PNG_OUT_DIR):
        os.makedirs(PNG_OUT_DIR)

    rename_and_generate(IN_DIR)
    
    files = set()
    # Get all files recursively in dicom directory
    getFiles(IN_DIR, files)
    # Convert all dicom files to pngs
    for f, fn in files:
        convert(f, fn)

if __name__ == '__main__':
    main()