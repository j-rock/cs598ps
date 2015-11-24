from dataset import *
import scipy.io.wavfile as wav
import scipy.fftpack
import numpy as np

class BaseFeature():
    """
    Base feature class for generating features from testsamples.
    """

    def __init__(self,testsample):
        #print("Creating feature for testsample: "+testsample.name)
        self.sample = testsample
        (rate,audio) = wav.read(self.sample.path)
        #print("samplerate: "+str(rate))
        #print("len: "+str(len(audio)))
        self.rate=rate
        self.num_samples=len(audio)
        self.window_size=1024
        self.overlap=32
        self.generated=False

    def stats(self):
        """
        Print out basic statistics about the feature.
        """
        print("Num Samples: "+str(self.num_samples))
        print("Sample Rate: "+str(self.rate))
        print("Window size: "+str(self.window_size))
        print("Window Overlap: "+str(self.overlap))


class MagnitudeFeature(BaseFeature):
    """
    Simple magnitude based feature for testsamples.
    NOTE - only meant to be used for initial testing.
    """

    def __init__(self,testsample):
        BaseFeature.__init__(self,testsample)
        self.generate()

    def stats(self):
        BaseFeature.stats(self)
        print("Feature: "+str(self.feature))

    def generate(self):
        (rate,audio) = wav.read(self.sample.path)

        # grab first channel
        one_channel = audio[:,0]
        N = len(audio)
        T = 1.0 / float(rate)

        # run fft on single channel
        yf = scipy.fftpack.fft(one_channel)

        # create simple sum of all frequency bands
        single_sum=(2.0/N * np.abs(yf[0:N/2])).sum()
        self.feature = np.asarray([single_sum])

class FreqBinFeature(BaseFeature):
    """
    Feature for test samples that includes a value
    for each frequency bin. Frequency bins are 100Hz
    wide and are only generated for 0-1000Hz. This equates
    to 10 features.
    """

    def __init__(self,testsample,bin_width=100,num_bins=10):
        BaseFeature.__init__(self,testsample)
        assert bin_width > 1
        assert num_bins >= 1
        self.bin_width=bin_width
        self.num_bins = num_bins
        self.generate()

    def stats(self):
        BaseFeature.stats(self)
        print("Num Bins: "+str(self.num_bins))
        print("Feature: "+str(self.feature))

    def generate(self):
        (rate,audio) = wav.read(self.sample.path)

        # grab first channel
        one_channel = audio[:,0]
        N = len(audio)
        T = 1.0 / float(rate)

        # run fft on single channel
        yf = scipy.fftpack.fft(one_channel)
        yf = (2.0/N * np.abs(yf[0:N/2]))

        # construct bins for each frequency channel
        feature = []
        for i in range(0,self.num_bins):
            feature.append((yf[(i*self.bin_width):((i+1)*self.bin_width-1)]).sum())
        self.feature = np.asarray(feature)
