
from scipy import signal
import scipy.io.wavfile as wavfile
from dataset import TemplateMarker
import timeit


class TemplateClassifier():

    def __init__(self):
        self._raw_result = None
        self._raw_test_times = []
        self._raw_read_times = []

    def train(self,template_path):
        self.template_rate, self.template = wavfile.read(template_path)

    def test_recording(self,audio_path):
        """
        Run the classification on a testrecording input.
        """
        start = timeit.timeit()
        assert self.template != None
        audio_rate, audio = wavfile.read(audio_path)
        end_read = timeit.timeit()
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
        matches = [TemplateMarker('A1',0,1),TemplateMarker('A1',0,3),TemplateMarker('A1',0,4)]
        self._raw_read_times.append(end_read - start)
        self._raw_test_times.append(timeit.timeit() - start)
        return matches

    def _get_raw_result(self):
        """
        Internal test method for returning the raw result of the test method.
        This can be used for plotting.
        """
        return self._raw_result

    def _get_raw_test_times(self):
        return self._raw_test_times

    def _get_raw_read_times(self):
        return self._raw_read_times
