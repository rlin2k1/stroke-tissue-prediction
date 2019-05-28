""" register_images.py
This module is a prototype module to perform a registration upon a moving image
onto the coordinate axis of the fixed image.

Image Registration with SimpleITK

USAGE: python2 register_images.py fixed.png moving.png

Author(s):
    Roy Lin

Date Created:
    May 25th, 2019
"""

# ---------------------------------------------------------------------------- #
# Import Statements for the Necessary Packages
# ---------------------------------------------------------------------------- #
from __future__ import print_function #Python3 Printing
import SimpleITK as sitk # Image Registration
from matplotlib import pyplot as plt # Plot Images
import sys # Command Line Arguments
import matplotlib

matplotlib.use('tkagg') # MacOS Support for Displaying Images

# ---------------------------------------------------------------------------- #
# Constructs Argument Parser for Parsing Arguments
# ---------------------------------------------------------------------------- #
if( (len(sys.argv) - 1) != 2):
    print("Two Arguments Needed.")
    print("USAGE: python2 register_images.py fixed.png moving.png")
    exit()

fixed = sys.argv[1]
moving = sys.argv[2]

# ---------------------------------------------------------------------------- #
# Load the Imputted Images from Command Line
# ---------------------------------------------------------------------------- #
fixed = sitk.ReadImage(fixed)
moving = sitk.ReadImage(moving)

# ---------------------------------------------------------------------------- #
# Translate 3 Dimentional DCM Images to 2 Dimentional Frame. Lose 3rd Dimension
# ---------------------------------------------------------------------------- #
fixed = sitk.Extract(fixed, (fixed.GetWidth(), fixed.GetHeight(), 0), (0, 0, 0))
moving = sitk.Extract(moving, (moving.GetWidth(), moving.GetHeight(), 0), \
    (0, 0, 0))

# ---------------------------------------------------------------------------- #
# Register the Moving Image to the Fixed Image Coordinate Plane
# ---------------------------------------------------------------------------- #
registeredImage = sitk.Elastix(fixed, moving, "translation")

# ---------------------------------------------------------------------------- #
# Plot the Fixed, Moving, and Registered Image
# ---------------------------------------------------------------------------- #
fixed = sitk.GetArrayFromImage(fixed)
moving = sitk.GetArrayFromImage(moving)
registeredImage = sitk.GetArrayFromImage(registeredImage)

figure = plt.figure()
subplot = figure.add_subplot(1, 3, 1)
imgplot = plt.imshow(fixed)
subplot.set_title('Before Surgery. First MRI')
subplot = figure.add_subplot(1, 3, 2)
imgplot = plt.imshow(moving)
subplot.set_title('After Surgery. Second MRI')
subplot = figure.add_subplot(1, 3, 3)
imgplot = plt.imshow(registeredImage)
subplot.set_title('Moving Surgery Label to 1st MRI Coord System')

plt.show()
# ---------------------------------------------------------------------------- #
# NOTES:
# ---------------------------------------------------------------------------- #

# EVEN THE SIZE AND AXES ARE CORRECT! YES :)
# STILL CONFUSED WHICH TWO IMAGES TO REGISTER!