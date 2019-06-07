import os
from os.path import dirname, abspath

ROOT_DIR = dirname(dirname(abspath(__file__)))
IN_DIR = ROOT_DIR + "/data/"
remove = '.DS_Store'

def main():
    fix_folders=[12,14]
    for i in fix_folders:
        flair_files = sorted(os.listdir(IN_DIR + str(i) + '/Flair/'))
        if remove in flair_files:
            flair_files.remove(remove)
        flair_length = len(flair_files)
        
        perfusion_files = sorted(os.listdir(IN_DIR + str(i) + '/Perfusion'))
        if remove in perfusion_files:
            perfusion_files.remove(remove)

        for index, item in enumerate(perfusion_files):
            if (index + 1) % (flair_length + 1) == 0:
                os.remove(IN_DIR + str(i) + '/Perfusion/' + item)

if __name__ == "__main__":
    main()