
import numpy as np

def _calc_padding(array,n):
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

def split_padded(array,samplesize):
    """
    Split a numpy array into segments based on the samplesize.
    Inspired by http://stackoverflow.com/questions/9922395/python-numpy-split
    -array-into-unequal-subarrays
    If the array can't be evenly divided into the samplesize, then it must be
    padded.

    Parameters:
    -----------
    array : array
        Numpy array that needs to be divided into equal segments.
    samplesize : int
        The num of elements to include in each segment.
    """
    padding = _calc_padding(array,samplesize)
    print('split_padded.padding: '+str(padding))
    if len(array.shape) == 1:
        temp = np.concatenate((array,np.zeros(padding,dtype=array.dtype)))
        return np.split(temp,(len(temp)/samplesize))
    elif len(array.shape) == 2:
        temp = np.concatenate((array,np.zeros((padding,2),dtype=array.dtype)))
        return np.split(temp,(len(temp)/samplesize))
    else:
        raise ValueError('Higher dimensional arrays not yet supported.')
