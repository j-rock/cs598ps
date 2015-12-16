
import numpy as np
import scipy.io.wavfile as wav
import scipy.fftpack
from scipy import signal

from features import mfcc
from features import logfbank
from dataset import *

def _extract_single_channel(audio):
    """
    Extract a single channel from the audio input.
    """
    if len(audio.shape) > 1:
        return audio[:,0]
    return audio

class BaseFeature():
    """
    Base feature class for generating features from testsamples.
    """

    def __init__(self):
        self.window_size=1024
        self.overlap=32

    def __str__(self):
        self.stats()

    def stats(self):
        """
        Print out basic statistics about the feature.
        """
        print("Window size: "+str(self.window_size))
        print("Window Overlap: "+str(self.overlap))

    def generate(self,testsample):
        print("BaseFeature.generate - not implemented")

class MagnitudeFeature(BaseFeature):
    """
    Simple magnitude based feature for testsamples.
    NOTE - only meant to be used for initial testing.
    """

    def __init__(self):
        BaseFeature.__init__(self)

    def stats(self):
        BaseFeature.stats(self)

    def generate(self,testsample):
        (rate,audio) = wav.read(testsample.path)

        # grab first channel
        one_channel = _extract_single_channel(audio)
        N = len(audio)
        T = 1.0 / float(rate)

        # run fft on single channel
        yf = scipy.fftpack.fft(one_channel)

        # create simple sum of all frequency bands
        single_sum=(2.0/N * np.abs(yf[0:N/2])).sum()
        return  np.asarray([single_sum])

class MultiTemplateFeature(BaseFeature):
    """
    Feature that convolves multiple templates with the input audio to
    derive the features.
    """

    def __init__(self,template_paths):
        BaseFeature.__init__(self)
        self.templates=[]
        self.template_rates = []
        for i in range(0,len(template_paths)):
            path = template_paths[i].path
            (template_rate, template_raw) = wav.read(path)
            template = _extract_single_channel(template_raw)
            self.templates.append(template)
            self.template_rates.append(template_rate)

    def stats(self):
        BaseFeature.stats(self)
        print("Num Bins: "+str(self.num_bins))
        print("Feature: "+str(self.feature))

    def generate(self,testsample):
        audio_rate, audio_raw = wav.read(testsample.path)
        audio = _extract_single_channel(audio_raw)
        feature = []

        for i in range(0,len(self.templates)):
            template = self.templates[i]
            # convolution
            result = signal.fftconvolve(audio, template)

            # scale and take absolute value
            result = result ** 2

            # low-pass filter
            a = 1
            b = signal.firwin(999, cutoff = 1e-9, window = 'hamming')
            result = signal.lfilter(b, a, result, axis = 0)

            feature.append(result.max())
        return np.asarray(feature)

class FreqBinFeature(BaseFeature):
    """
    Feature for test samples that includes a value
    for each frequency bin. Frequency bins are 100Hz
    wide and are only generated for 0-1000Hz. This equates
    to 10 features.
    """

    def __init__(self,bin_width=100,num_bins=10):
        BaseFeature.__init__(self)
        assert bin_width > 1
        assert num_bins >= 1
        self.bin_width=bin_width
        self.num_bins = num_bins

    def stats(self):
        BaseFeature.stats(self)
        print("Num Bins: "+str(self.num_bins))

    def generate(self, testsample):
        (rate,audio) = wav.read(testsample.path)

        # grab first channel
        one_channel = _extract_single_channel(audio)
        N = len(audio)
        T = 1.0 / float(rate)

        # run fft on single channel
        yf = scipy.fftpack.fft(one_channel)
        yf = (2.0/N * np.abs(yf[0:N/2]))

        # construct bins for each frequency channel
        feature = []
        for i in range(0,self.num_bins):
            feature.append((yf[(i*self.bin_width):((i+1)*self.bin_width-1)]).sum())
        return np.asarray(feature)

class MFCCFeature(BaseFeature):
    """
    Mel Frequency Cepstral Coefficients features as implmented
    by third-party library provided by:
    https://github.com/jameslyons/python_speech_features
    """

    def __init__(self):
        BaseFeature.__init__(self)

    def stats(self):
        BaseFeature.stats(self)

    def generate(self,testsample):
        (rate,audio) = wav.read(testsample.path)

        # grab first channel
        one_channel = _extract_single_channel(audio)
        N = len(audio)
        mfcc_feat = mfcc(one_channel,rate)
        cols=mfcc_feat.shape[0]*mfcc_feat.shape[1]
        return mfcc_feat.reshape((1,cols))[0]

class FBankFeature(BaseFeature):
    """
    FilterBank features as implmented
    by third-party library provided by:
    https://github.com/jameslyons/python_speech_features
    """

    def __init__(self):
        BaseFeature.__init__(self)

    def stats(self):
        BaseFeature.stats(self)

    def generate(self,testsample):
        (rate,audio) = wav.read(testsample.path)

        # grab first channel
        one_channel = _extract_single_channel(audio)
        N = len(audio)
        fbank_feat = logfbank(one_channel,samplerate=rate) #winlen=1.0
        cols=fbank_feat.shape[0]*fbank_feat.shape[1]
        return fbank_feat.reshape((1,cols))[0]
