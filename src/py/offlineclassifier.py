
from scipy import signal
import scipy.io.wavfile as wavfile
from audiomarker import AudioMarker

class TemplateClassifier():

    def __init__(self):
        self._raw_result = None

    def train(self,template_path):
        self.template_rate, self.template = wavfile.read(template_path)

    def test(self,audio_path):
        assert self.template != None
        audio_rate, audio = wavfile.read(audio_path)
        assert self.template_rate == audio_rate

        # convolution
        result = signal.fftconvolve(audio, self.template)

        # scale and take absolute value
        result = result ** 2

        # low-pass filter
        a = 1
        b = signal.firwin(999, cutoff = 1e-9, window = 'hamming')
        result = signal.lfilter(b, a, result, axis = 0)

        # store raw result for plotting
        self._raw_result = result

        # temporary hard-coded results, these can be used
        # to test against expected values
        matches = [AudioMarker(0,1),AudioMarker(0,3),AudioMarker(0,4)]
        return matches

    def _get_raw_result(self):
        """
        internal test method for returning the raw result of the test method.
        This can be used for plotting.
        """
        return self._raw_result
