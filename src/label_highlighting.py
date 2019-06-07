# :: label_highlighting.py
#####################################################
# Functions to handle processing the raw DCM images.
#####################################################
# :: Created By: Benji Brandt <benjibrandt@ucla.edu>, 
#                Roy Lin <rlin2k1@gmail.com>, 
#                David Macaraeg <dmacaraeg@g.ucla.edu>
# :: Creation Date: May 29, 2019

import sys
sys.path.append("..")
import os
import pydicom
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
import png

# slice location

# grabbed from https://github.com/pydicom/pydicom/issues/352
def dicom2png(source_folder, output_folder):
    list_of_files = os.listdir(source_folder)
    for file in list_of_files:
        try:
            ds = pydicom.dcmread(os.path.join(source_folder,file))
            shape = ds.pixel_array.shape

            # Convert to float to avoid overflow or underflow losses.
            image_2d = ds.pixel_array.astype(float)

            # Rescaling grey scale between 0-255
            image_2d_scaled = (np.maximum(image_2d,0) / image_2d.max()) * 255.0

            # Convert to uint
            image_2d_scaled = np.uint8(image_2d_scaled)

            # Write the PNG file
            with open(os.path.join(output_folder, file.split(".")[0])+'.png' , 'wb') as png_file:
                w = png.Writer(shape[1], shape[0], greyscale=True)
                w.write(png_file, image_2d_scaled)
        except:
            print('Could not convert: ', file)

# works for if for if format is x,y,z,label and z represents slice_location
def main():
    stroke_output_dir = "./stroke_outputs"

    for csv_file in os.listdir(stroke_output_dir):
        if csv_file.endswith(".csv"):
            file_handler = open(os.path.join(stroke_output_dir, csv_file), "r")
            patient_no = int(csv_file.split("_")[0]) # assuming that the csv is named "<patient number>_stroke_output.csv"

            labels_data = [line.strip().split(",") for line in file_handler.readlines()]
            labels_data[0][0] = labels_data[0][0].replace(u'\ufeff', '') # remove the character that comes with excel csv

            slice_locations = sorted(set([float(label_data[2]) for label_data in labels_data])) # grabs all the unique slice_locations and orders them

            slice_pixels = {}
            for label_data in labels_data:
                
                x_coord = int(float(label_data[0]))
                y_coord = int(float(label_data[1]))
                z_coord = slice_locations.index(float(label_data[2])) # e.g. slice number
                label = int(float(label_data[3]))
                has_stroke_tissue = 1
                if label == has_stroke_tissue:
                    if z_coord not in slice_pixels.keys():
                        slice_pixels[z_coord] = []
                    slice_pixels[z_coord].append((y_coord, x_coord))

            dcm_dir = "./Patients/{0}/Perfusion".format(patient_no)
            one_brain = {}

            for dcm_file in os.listdir(dcm_dir):
                if dcm_file.endswith(".dcm"):
                    dcm = pydicom.dcmread(os.path.join(dcm_dir, dcm_file))
                    acquisition_no = dcm.AcquisitionNumber
                    slice_loc = dcm.SliceLocation
                    if acquisition_no == 1:
                        one_brain[slice_loc] = dcm_file
            
            ordered_one_brain_slices = []
            sorted_slice_locs = sorted(one_brain.keys())
            for slice_loc in sorted_slice_locs:
                if slice_loc in one_brain.keys():
                    ordered_one_brain_slices.append(one_brain[slice_loc])
            
            labeled_perfusions_dir = "./Patients/{0}/labeled_perfusions".format(patient_no)
            if not os.path.isdir(labeled_perfusions_dir):
                os.system("mkdir {0}".format(labeled_perfusions_dir))
            else: 
                os.system("rm -rf {0}".format(labeled_perfusions_dir))
                os.system("mkdir {0}".format(labeled_perfusions_dir))

            for dcm_file in ordered_one_brain_slices:
                os.system("cp {0} {1}".format(os.path.join(dcm_dir, dcm_file), os.path.join(labeled_perfusions_dir, dcm_file)))
            
            dicom2png(labeled_perfusions_dir, labeled_perfusions_dir)
            
            
            for z_coord, x_y_coords in slice_pixels.items():
                dcm_file_name = ordered_one_brain_slices[z_coord]

                dcm = pydicom.read_file(os.path.join(labeled_perfusions_dir, dcm_file_name))
                dcm_pixels = dcm.pixel_array

                png_file = dcm_file_name.split(".")[0] + ".png"
                picture = Image.open(os.path.join(labeled_perfusions_dir, png_file))
                width, height = picture.size
                if picture.mode != 'RGB':
                    picture = picture.convert('RGB')

                red = (255, 0, 0)
                green = (0, 255, 0)
                blue = (0, 0, 255)
                
                for x_y_coord in x_y_coords:
                    y_coord = x_y_coord[0]j
                    x_coord = x_y_coord[1]
                    if x_coord >= 0 and y_coord >= 0 and x_coord < width and y_coord < height and dcm_pixels[x_coord, y_coord] > 100:
                        picture.putpixel(x_y_coord, red)
                os.system("rm {0}".format(os.path.join(labeled_perfusions_dir, dcm_file_name)))
                picture.save(os.path.join(labeled_perfusions_dir, png_file))
            
            
            
            
        

if __name__ == "__main__":
    main()