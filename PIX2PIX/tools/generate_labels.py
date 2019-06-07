import png
import os, shutil
import sys
import pydicom
import numpy as np

from os.path import dirname, abspath
ROOT_DIR = dirname(dirname(abspath(__file__)))
IN_DIR = ROOT_DIR + "/data/"
PNG_IN_DIR = ROOT_DIR + "/output/pix2pix/inputs"
PNG_OUT_DIR = ROOT_DIR + "/output/pix2pix/outputs"
INPUT = "Perfusion"
OUTPUT = "RegisteredFlair"

from shutil import copyfile
def rename_and_generate(IN_DIR, ignore_folders):
    remove = '.DS_Store'
    for i in range(1, 19): #HARD CODED NUMBER OF FOLDERS IN DATA
        if (i in ignore_folders):
            continue

        flair_files = sorted(os.listdir(IN_DIR + str(i) + '/RegisteredFlair/'))
        if remove in flair_files:
            flair_files.remove(remove)
        print(flair_files)
        flair_length = len(flair_files)
        print(flair_length)
        perfusion_files = sorted(os.listdir(IN_DIR + str(i) + '/Perfusion'))
        if remove in perfusion_files:
            perfusion_files.remove(remove)

        output_dir = IN_DIR + str(i) + '/CleanedFlair/'
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.mkdir(output_dir)

        if(len(perfusion_files) % flair_length != 0):
            print("MRI DOES NOT LINE UP. CHECK FOLDER: " + str(i))
        else:
            print("Done Processing Folder: " + str(i))

        for counter, file in enumerate(perfusion_files):
            copyfile(IN_DIR + str(i) + '/RegisteredFlair/' + flair_files[counter%(flair_length)], output_dir + file)

def main():
    ignore_folders=[6, 11]

    rename_and_generate(IN_DIR, ignore_folders)

if __name__ == "__main__":
    main()