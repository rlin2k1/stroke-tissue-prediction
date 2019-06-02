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

def main():
    stroke_output_dir = "./stroke_outputs"

    for csv_file in os.listdir(stroke_output_dir):
        if csv_file.endswith(".csv"):
            file_handler = open(os.path.join(stroke_output_dir, csv_file), "r")
            patient_no = int(csv_file.split("_")[0]) # assuming that the csv is named "<patient number>_stroke_output.csv"

        labels_data = [line.strip().split(",") for line in file_handler.readlines()]
        labels_data[0][0] = labels_data[0][0].replace(u'\ufeff', '') # remove the character that comes with excel csv

        slice_pixels = {}
        # print (labels_data)
        for label_data in labels_data:
            label = int(label_data[0])
            x_coord = int(label_data[1])
            y_coord = int(label_data[2])
            z_coord = int(label_data[3]) # e.g. slice number
            has_stroke_tissue = 1
            if label == has_stroke_tissue:
                if z_coord not in slice_pixels.keys():
                    slice_pixels[z_coord] = []
                slice_pixels[z_coord].append((x_coord, y_coord))

        dcm_dir = "./Patients/{0}/Perfusion".format(patient_no)
        one_brain = {}

        for dcm_file in os.listdir(dcm_dir):
            if dcm_file.endswith(".dcm"):
                dcm = pydicom.dcmread(os.path.join(dcm_dir, dcm_file))
                acquisition_no = dcm.AcquisitionNumber
                slice_loc = dcm.SliceLocation
                if acquisition_no == 1:
                    # one_brain[slice_loc] = (dcm, dcm_file)
                    one_brain[slice_loc] = dcm_file
        
        ordered_one_brain_slices = []
        sorted_slice_locs = sorted(one_brain.keys())
        for slice_loc in sorted_slice_locs:
            if slice_loc in one_brain.keys():
                ordered_one_brain_slices.append(one_brain[slice_loc])

        # print (ordered_one_brain_slices[0].pixel_array.shape)
        # print (ordered_one_brain_slices[0].pixel_array)
        
        labeled_perfusions_dir = "./Patients/{0}/labeled_perfusions".format(patient_no)
        if not os.path.isdir(labeled_perfusions_dir):
            os.system("mkdir {0}".format(labeled_perfusions_dir))
        else: 
            os.system("rm -rf {0}".format(labeled_perfusions_dir))
            os.system("mkdir {0}".format(labeled_perfusions_dir))

        for dcm_file in ordered_one_brain_slices:
            os.system("cp {0} {1}".format(os.path.join(dcm_dir, dcm_file), os.path.join(labeled_perfusions_dir, dcm_file)))
        
        dicom2png(labeled_perfusions_dir, labeled_perfusions_dir)
        
        os.system("rm {0}/*.dcm".format(os.path.join(labeled_perfusions_dir)))
        

        for z_coord, x_y_coords in slice_pixels.items():
            dcm_file = ordered_one_brain_slices[z_coord]
            png_file = dcm_file.split(".")[0] + ".png"
            picture = Image.open(os.path.join(labeled_perfusions_dir, png_file))
            width, height = picture.size
            if picture.mode != 'RGB':
                picture = picture.convert('RGB')
            
            red = (255, 0, 0)
            green = (0, 255, 0)
            blue = (0, 0, 255)
            '''
            pixels = picture.load()
            print (pixels)
            x_coord = x_y_coords[0]
            y_coord = x_y_coords[1]
            pixels[x_coord][y_coord] = red
            
            pixels.save(os.path.join(labeled_perfusions_dir, png_file))
            '''
            
            for x_y_coord in x_y_coords:
                x_coord = x_y_coord[0]
                y_coord = x_y_coord[1]
                # print (z_coord, x_y_coord)
                if x_coord >= 0 and y_coord >= 0 and x_coord < width and y_coord < height:
                    picture.putpixel(x_y_coord, green)
            
            picture.save(os.path.join(labeled_perfusions_dir, png_file))
            '''
            h,w,_ = np.shape(picture)
            print('height:',h,' width: ',w)
            plt.figure()
            plt.imshow(picture)
            plt.show()
            '''
            
            
            

        # print (labels)
        # print (ordered_one_brain_slices[0])
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

if __name__ == "__main__":
    main()