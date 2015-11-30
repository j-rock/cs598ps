import math
import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import sounddevice as sd


def record_sample(duration=3,samplerate=11025,channels=1,blocking=False):
    """
    An optionally blocking method used to start the recording of a sample.

    Parameters:
    -----------
    duration : int
        The length in seconds to record
    samplerate : int
        The number of samplesa per second to record at
    channels : int
        The number of channels to be used during recording
    blocking : bool
        True if method should block until it completes. False otherwise.
    """
    sample=sd.rec(duration * samplerate, samplerate=samplerate, channels=channels)
    if blocking == True:
        sd.wait()
    return sample

def play_sample(sample,samplerate=11025,blocking=True):
    sd.play(sample, samplerate=samplerate,blocking=blocking)

def save_sample(filename,sample,samplerate=11025):
    wav.write(filename,samplerate,sample)

def load_plot(wavfile):
    """
    Utility method for loading and displaying wav file content transformed
    from the time domain to the frequency domain via the FFT.

    Parameters:
    -----------
    wavfile : string
        absolute path to the wavfile
    """
    (rate,audio) = wav.read(wavfile)
    freq_domain = np.fft.fft(audio)
    plt.plot(freq_domain.real)
    plt.show()


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

def _split_padded(array,samplesize):
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
