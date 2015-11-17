
import numpy as np

def calc_padding(array,n):
    """
    Calculate the padding necessary for an array.

    Parameters:
    -----------
    array : array
        Numpy array that needs to be divided into equal segments.
    n : int
        The number of segments to divide the array
    """
    return (-len(array))%n

def split_padded(array,n):
    """
    Split a numpy array into n segments with padding if necessary.
    Inspired by http://stackoverflow.com/questions/9922395/python-numpy-split
    -array-into-unequal-subarrays

    Parameters:
    -----------
    array : array
        Numpy array that needs to be divided into equal segments.
    n : int
        The number of segments to divide the array
    """
    padding = calc_padding(array,n)
    print('array shape: '+str(array.shape))
    temp = np.concatenate((array,np.zeros((padding,2),dtype=array.dtype)))
    return np.split(temp,n)
