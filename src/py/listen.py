import sys
import time

from cssigps.offlineclassifier import *
from cssigps.dataset import *
from cssigps.feature import *
from cssigps.experiments import *
from get_dropbox_path import *

def feature_factory(sample):
    return FBankFeature(sample).feature

def class_factory(sample):
    return class_to_num(sample.y)

def train_offline_svm_test_live(path=get_dropbox_path()):
    """
    Train the offline version of the SVM classifier on all
    samples found in the path. Then run the classifier on
    1 second inputs live.

    Parameters
    ----------
    path - string
      The directory to search for TestSamples
    """
    print('Training SVM classifier')

    # return a list of the audio test samples
    samples = find_testsamples(path)

    sample_set = SampleSet(samples)
    sample_set.stats()
    (train,test) = sample_set.sample(in_order=False)

    # generate features and classes from TestSamples
    train_features = []
    train_classes = []
    for sample in train:
        train_features.append(feature_factory(sample))
        train_classes.append(class_factory(sample))

    # train the classifier
    classifier = SVMClassifier()
    classifier.train(train_features,train_classes)

    prompt ='Would you like to record a 3-sec sample to test?'
    if raw_input(prompt) == 'y':
        print('Recording now...')
        live_recording = record_sample(samplerate=22050,blocking=True)
        new_recording = live_recording.astype('int16')
        print("dtype: "+str(new_recording.dtype))
        #quit()

        # process the recording into test samples
        test_samples = process_live_recording(new_recording,"UChiApt",str(time.time()),22050)

        print('Testing...')
        for sample in test_samples:
            feature = feature_factory(sample)
            print("Prediction: "+str(classifier.predict(feature)))
    else:
        print('Exiting...')

if __name__ == '__main__':
    print("Training the classifier against the Yes/No dataset")
    path = get_dropbox_path()+"yes-no-test/"
    train_offline_svm_test_live(path)
