# :: utilities.py
#####################################################
# Utility functions for usage in all modules.
#####################################################
# :: Created By: Benji Brandt <benjibrandt@ucla.edu>, 
#                Roy Lin <rlin2k1@gmail.com>, 
#                David Macaraeg <dmacaraeg@g.ucla.edu>
# :: Creation Date: 30 May 2019
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def represents_int(s):
    """
    Determines if the given string represents an integer.

    :param str s:
    :return: True if the string represents an int, else False.
    :rtype: bool
    """
    try: 
        int(s)
        return True
    except ValueError:
        return False

class Data:
    def __init__(self) :
        """
        Data class.
        
        Attributes
        --------------------
            X -- numpy array of shape (n,d), features
            y -- numpy array of shape (n,), targets
        """
                
        # n = number of examples, d = dimensionality
        self.X = None
        self.y = None
        
        self.Xnames = None
        self.yname = None

    def load(self, filename, header=0, predict_col=-1) :
        """Load csv file into X array of features and y array of labels."""
        
        # determine filename
        dir = os.path.dirname(__file__)
        f = os.path.join(dir, '..', 'data', filename)
        
        # load data
        with open(f, 'r') as fid :
            data = np.loadtxt(fid, delimiter=",", skiprows=header)
        
        # separate features and labels
        if predict_col is None:
            self.X = data[:,:]
            self.y = None
        else:
            if data.ndim > 1:
                self.X = np.delete(data, predict_col, axis=1)
                # self.y = data[:,predict_col]
                self.y = data[:,predict_col]
            else:
                self.X = None
                self.y = data[:]
        
        # load feature and label names
        if header != 0:
            with open(f, 'r') as fid :
                header = fid.readline().rstrip().split(",")
                
            if predict_col is None :
                self.Xnames = header[:]
                self.yname = None
            else :
                if len(header) > 1 :
                    self.Xnames = np.delete(header, predict_col)
                    self.yname = header[predict_col]
                else :
                    self.Xnames = None
                    self.yname = header[0]
        else:
            self.Xnames = None
            self.yname = None

    def load_test(self, filename, header=0, predict_col=-1):
        """Load csv file into X array of features and y array of labels."""
        
        # determine filename
        dir = os.path.dirname(__file__)
        f = os.path.join(dir, '..', 'data', filename)

        self.Xnames = None
        self.yname = None
        
        # load data
        with open(f, 'r') as fid:
            data1 = np.loadtxt(fid, delimiter=",", skiprows=header, usecols=(0,1,2))
            fid.close()
        with open(f, 'r') as fid:
            data = np.loadtxt(fid, delimiter=",", skiprows=header)


        l = range(0, predict_col + 1)
        self.X = np.delete(data, l, axis=1)
        self.y = data1
        

# helper functions
def load_model_data(filename, header=0, predict_col=-1):
    """Load csv file into Data class."""
    data = Data()
    data.load(filename, header=header, predict_col=predict_col)
    return data

def load_model_test(filename, header=0, predict_col=-1):
    """Load csv file into Data class."""
    data = Data()
    data.load_test(filename, header=header, predict_col=predict_col)
    return data