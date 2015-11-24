
from scipy import signal
import scipy.io.wavfile as wavfile
from dataset import *
from dataset import TemplateMarker
import timeit
from sklearn import svm

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

class SVMClassifier():
    """
    SVM Classifier using only samples for training and testing. This uses
    a fixed-length input for both cases, which is ideal.
    """

    def __init__(self,samples,train_test_ratio=0.5):
        self.samples = samples
        self.ratio=train_test_ratio
        classes=[]
        class_histogram={}
        for sample in self.samples:
            classes.append(sample.y)
            if class_histogram.has_key(sample.y):
                class_histogram[sample.y]=class_histogram[sample.y]+1
            else:
                class_histogram[sample.y]=0
        self.classes=set(classes)
        self.class_histogram = class_histogram

    def stats(self):
        """
        Print out basic statistics about the classifier.
        """
        print("Num samples: "+str(len(self.samples)))
        print("Num classes: "+str(len(self.classes)))
        for key in self.class_histogram.iterkeys():
            print("\t'"+key+"' : "+str(self.class_histogram[key]))

    def run(self,feature_factory,class_factory):
        N = len(self.samples)
        Xtrain = []
        Ytrain = []
        Xtest = []
        Ytest = []
        for sample in self.samples:
            if len(Xtrain) >= int(float(N)/2.):
                Xtest.append(feature_factory(sample))
                Ytest.append(class_factory(sample))
            else:
                Xtrain.append(feature_factory(sample))
                Ytrain.append(class_factory(sample))

        # convert to numpy arrays
        Xtrain = np.asarray(Xtrain)
        Ytrain = np.asarray(Ytrain)
        Xtest = np.asarray(Xtest)
        Ytest = np.asarray(Ytest)

        print(str(len(Xtrain))+' training features generated')
        print(str(Xtrain.shape)+' feature shape')
        print(str(len(Xtest))+' testing features generated')
        print(str(len(Ytrain))+' training classes')
        print(str(len(Ytest))+' testing classes')

        # train classifier
        clf = svm.SVC()
        clf.fit(Xtrain,Ytrain)

        # test classifier
        Yclass = clf.predict(Xtest)
        score = 0
        for i in range(0,len(Xtest)):
            if Yclass[i] == Ytest[i]:
                print('correct classification')
                score=score+1
            else:
                print('incorrect classification')
        print('Classification score: '+str(score)+'/'+str(len(Xtest)))
        print('Classification score: '+str(float(score)/float(len(Xtest))))
