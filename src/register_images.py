""" register_images.py
This module is used to perform a registration upon a moving image onto the 
coordinate axis of the fixed image.

Image Registration with SimpleITK

USAGE: python2 register_images.py MAPPINGCSV
Export Function: register_images

Author(s):
    Roy Lin

Date Created:
    May 25th, 2019
"""

# ---------------------------------------------------------------------------- #
# Import Statements for the Necessary Packages
# ---------------------------------------------------------------------------- #
from __future__ import print_function # Python3 Printing
import SimpleITK as sitk # Image Registration
from matplotlib import pyplot as plt # Plot Images
import sys # Command Line Arguments
import matplotlib
import pydicom # For Acquisition Number, Slice Location, and Time
import os, shutil # Directory Manipulation

# Print Whole NumPy Array
import sys
import numpy
numpy.set_printoptions(threshold=sys.maxsize)

matplotlib.use('tkagg') # MacOS Support for Displaying Images

# ---------------------------------------------------------------------------- #
# Image Registration Function
# ---------------------------------------------------------------------------- #
def register_images(fixed_image_path, directory_path, moving_image_path, number):
    """
    Takes one fixed image, a directory of moving images, one moving image, and a
    number. Transforms all moving images in the directory to the coordinate 
    plane of the fixed image. Creates a New Directory called 'RESULT' and stores
    the registered Dicoms inside with file name: 
        result_DICOMFILENAME_AcquitionNumber_AcquitionTime_SliceLocation.dcm
    
    Args:
        fixed_image_path (string): Path to the Fixed Image.
        directory_path (string): Path to the Directory Containing Moving Images.
            Directory pointed to by directory_path must have at least ONE Image 
            File inside. Can Specify Which Image (moving.dcm) to Use as the 
            Image to Make the Transformation Matrix.
        moving_image_path (string): Path to the Moving Image.
        number (string): Number of the Patient.

    Returns:
        (Void): None.
    """
    
    # ------------------------------------------------------------------------ #
    # Load the Inputted Images from Command Line
    # ------------------------------------------------------------------------ #
    fixed = sitk.ReadImage(fixed_image_path)

    moving = sitk.ReadImage(os.path.join(directory_path, moving_image_path))

    # ------------------------------------------------------------------------ #
    # Translate 3-D DCM Images to 2-D Frame. Lose 3rd Dimension
    # ------------------------------------------------------------------------ #
    fixed = sitk.Extract(fixed, (fixed.GetWidth(), fixed.GetHeight(), 0), \
        (0, 0, 0))
    moving = sitk.Extract(moving, (moving.GetWidth(), moving.GetHeight(), 0), \
        (0, 0, 0))

    # ------------------------------------------------------------------------ #
    # Register the Moving Image to the Fixed Image Coordinate Plane
    # ------------------------------------------------------------------------ #
    # Parameter Map for Translation
    parameterMap = sitk.GetDefaultParameterMap('translation')

    # Create an Elastix Instance
    elastixImageFilter = sitk.ElastixImageFilter()
    elastixImageFilter.SetFixedImage(fixed)
    elastixImageFilter.SetMovingImage(moving)
    elastixImageFilter.SetParameterMap(parameterMap)
    elastixImageFilter.Execute()

    # Can Use Parameter Map for Future Images
    registeredImage = elastixImageFilter.GetResultImage()
    transformationMap = elastixImageFilter.GetTransformParameterMap()

    transformixImageFilter = sitk.TransformixImageFilter()
    transformixImageFilter.SetTransformParameterMap(transformationMap)

    dir = "RESULTS/" + number
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.mkdir(dir)

    fixed = sitk.GetArrayFromImage(fixed)

    for file in os.listdir('Labeled/' + number):
        if(file.endswith(".dcm")):
            filePath = os.path.join('Labeled/' + number, file)
            moving = sitk.ReadImage(filePath)
            moving = sitk.Extract(moving, (moving.GetWidth(), \
                moving.GetHeight(), 0), (0, 0, 0))
            transformixImageFilter.SetMovingImage(moving)
            transformixImageFilter.Execute()

            dcm = pydicom.dcmread(filePath)

            registeredImage = transformixImageFilter.GetResultImage()

            castFilter = sitk.CastImageFilter()
            castFilter.SetOutputPixelType(sitk.sitkInt16)
            # Convert floating type image (imgSmooth) to int type (imgFiltered)
            imgFiltered = castFilter.Execute(registeredImage)

            sitk.WriteImage(imgFiltered, dir + "/result_" + file[:-4] + '_' + str(dcm.AcquisitionNumber) + '_' + str(dcm.AcquisitionTime) + '_' + str(dcm.SliceLocation) + '.dcm')

            # ---------------------------------------------------------------- #
            # Show Image Translations
            # ---------------------------------------------------------------- #
            # moving = sitk.GetArrayFromImage(moving)

            # figure = plt.figure()
            # subplot = figure.add_subplot(1, 3, 1)
            # imgplot = plt.imshow(fixed)
            # subplot.set_title('Before Surgery. First MRI')
            # subplot = figure.add_subplot(1, 3, 2)
            # imgplot = plt.imshow(moving)
            # subplot.set_title('After Surgery. Second MRI')
            # subplot = figure.add_subplot(1, 3, 3)
            # imgplot = plt.imshow(registeredImage)
            # subplot.set_title('Moving Surgery Label to 1st MRI Coord System')
            # plt.show()

def main():
    # ------------------------------------------------------------------------ #
    # Constructs Argument Parser for Parsing Arguments
    # ------------------------------------------------------------------------ #
    if( (len(sys.argv) - 1) != 1):
        print("One Argument Needed.")
        print("USAGE: python2 register_images.py MAPPINGCSV")
        exit()
    
    csv_mapping = sys.argv[1]
    f = open(csv_mapping, 'r')

    for line in f:
        line = line.strip('\n')
        line = line.split(',')
        number = line[0]
        flair = line[1]
        perfusion = line[2]
        fixed_path = "Patients/" + number + "/Perfusion/" + perfusion
        directory_path = "Patients/" + number + "/FLAIR"
        register_images(fixed_path, directory_path, flair, number)

if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------- #
# Documentation
# ---------------------------------------------------------------------------- #
"""
Used SimpleElastix (https://simpleelastix.readthedocs.io/) as a medical image
registration library for image registration. I had a fixed image as the 'ground
truth' for the coordinate plane. I made a transformation matrix from the fixed
image and the moving image and applied this moving image to the other moving 
images in the directory to get the registered images. I write these image pixel
values to a text file in a new directory.
"""