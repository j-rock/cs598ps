import math
import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt


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

def sine(frequency, length, rate,dtype='int16',amplitude=0.5):
    length = int(length * rate)
    factor = float(frequency) * (math.pi * 2) / rate
    return np.sin(np.arange(length,dtype=dtype) * factor)

def loadnplot(wavfile):
    """
    Utility method for loading and displaying wav file content transformed
    from the time domain to the frequency domain.
    """
    (rate,audio) = wav.read(wavfile)
    freq_domain = np.fft.fft(audio)
    #plt.plot(audio)
    #plt.show()
    plt.plot(freq_domain.real)
    plt.show()
