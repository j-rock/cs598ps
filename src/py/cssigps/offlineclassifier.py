import timeit

from sklearn import svm
from scipy import signal
import scipy.io.wavfile as wavfile

from dataset import *

class TemplateClassifier():

    def __init__(self):
        self._raw_result = None
        self._raw_test_times = []
        self._raw_read_times = []
        self.template=None
        self.template_rate = None

    def train(self,template_path):
        (template_rate, template) = wavfile.read(template_path)
        self.template = template
        self.template_rate = template_rate

    def test_recording(self,audio_path):
        """
        Run the classification on a testrecording input.
        """
        start = timeit.timeit()
        assert self.template != None
        audio_rate, audio = wavfile.read(audio_path)
        print("Testing recording with samplerate: "+str(audio_rate))
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
        self._raw_read_times.append(end_read - start)
        self._raw_test_times.append(timeit.timeit() - start)

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

class BaseClassifier():
    """
    BaseClassifier providing common functionality.
    """

    def __init__(self):
        """
        Base constructor.
        """

    def train(self,X,y):
        """
        Train the classifier with X, a set of instances,
        and y, a set of class labels
        """

    def test(self,X,y):
        """
        Test the classifier against X, a set of instances,
        and y, a set of class labels
        """

    def predict(self,x):
        """
        Predict the class of a single instance.
        """

class BestGuessClassifier(BaseClassifier):
    """
    Baseline classifier that uses the probabilities of the
    different class labels during training, and simply guesses
    the most probably class each time during predict/test stages.
    This is meant to give a baseline of performance that can be
    achieved with trivial solutions.
    """

    def __init__(self):
        BaseClassifier.__init__(self)
        self.most_probable_class=-1

    def train(self,X,y):
        """
        Train the classifier with X, a set of instances,
        and y, a set of class labels.
        """
        classes={}
        for class_ in y:
            if str(class_) in classes:
                classes[str(class_)]=classes[str(class_)]+1
            else:
                classes[str(class_)]=1

        max_val=0
        for c in classes:
            if classes[c] > max_val:
                max_val = classes[c]
                self.most_probable_class = int(c)

    def test(self,X,y):
        """
        Test the classifier against X, a set of instances,
        and y, a set of class labels.
        """
        # convert to numpy arrays
        Xtest = np.asarray(X)
        Ytest = np.asarray(y)
        score = 0
        for i in range(0,len(Xtest)):
            if self.most_probable_class == Ytest[i]:
                print('correct classification')
                score=score+1
            else:
                print('incorrect classification - true class: '+str(self.most_probable_class))
        print('Classification score: '+str(score)+'/'+str(len(Xtest)))
        print('Classification score: '+str(float(score)/float(len(Xtest))))

    def predict(self,x):
        """
        Predict the class of a single instance.
        """
        return self.most_probable_class


class SVMClassifier(BaseClassifier):
    """
    SVM Classifier that uses the sklearn SVM implementation
    to train/test with TestSample objects.
    """

    def __init__(self):
        BaseClassifier.__init__(self)
        self.clf = svm.SVC()

    def train(self,X,y):
        """
        Train the classifier with X, a set of instances,
        and y, a set of class labels.
        """
        self.clf.fit(np.asarray(X),np.asarray(y))


    def test(self,X,y):
        """
        Test the classifier against X, a set of instances,
        and y, a set of class labels.
        """
        # convert to numpy arrays
        Xtest = np.asarray(X)
        Ytest = np.asarray(y)
        Yclass = self.clf.predict(Xtest)
        score = 0
        for i in range(0,len(Xtest)):
            if Yclass[i] == Ytest[i]:
                print('correct classification')
                score=score+1
            else:
                print('incorrect classification - true class: '+str(Ytest[i]))
        print('Classification score: '+str(score)+'/'+str(len(Xtest)))
        print('Classification score: '+str(float(score)/float(len(Xtest))))

    def predict(self,x):
        """
        Predict the class of a single instance.
        """
        return self.clf.predict(np.asarray([x]))
