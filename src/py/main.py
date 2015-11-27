from offlineclassifier import *
from get_dropbox_path import *
from dataset import *
from matplotlib import pyplot as plt
from feature import *
import time

def run_offline_template(path=get_dropbox_path()):
    """
    Run the offline version of the template classifier on all
    recordings found in the path.

    Parameters
    ----------
    path - string
      The directory to search for TestRecordings
    """
    print('Running template matching')
    classifier = TemplateClassifier()

    # train classifier
    templates = find_templates(path)
    if len(templates) < 1:
        raise ValueError('No templates found! aborting')

    # train on a single template for now
    classifier.train(templates[0])

    # test offline dataset with classifier
    recordings = find_testrecordings(get_dropbox_path())
    for test in recordings:
        matches = classifier.test_recording(test)
        print "Test: "+test
        print "Found "+str(len(matches))+" matches"

        # plot results
        plt.plot(classifier._get_raw_result())
        plt.show()

        print 'Classifier test times: '+str(classifier._get_raw_test_times())
        print 'Classifier read times: '+str(classifier._get_raw_read_times())


def feature_factory(sample):
    return FreqBinFeature(sample).feature

def class_factory(sample):
    if sample.y == "A1":
        return 1
    else:
        return 0

def run_offline_svm(path=get_dropbox_path()):
    """
    Run the offline version of the SVM classifier on all
    samples found in the path.

    Parameters
    ----------
    path - string
      The directory to search for TestSamples
    """
    print('Running SVM classifier')

    # return a list of the audio test samples
    samples = find_testsamples(path)

    # extract quiet samples
    quiet_samples = []
    for sample in samples:
        if sample.env == 'Q1' or sample.env == 'Q2':
            quiet_samples.append(sample)

    sample_set = SampleSet(quiet_samples)
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

    # generate features and classes from TestSamples
    test_features = []
    test_classes = []
    for sample in test:
        test_features.append(feature_factory(sample))
        test_classes.append(class_factory(sample))

    # test the classifier
    classifier.test(test_features,test_classes)

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

    # extract quiet samples
    quiet_samples = []
    for sample in samples:
        if sample.env == 'Q1' or sample.env == 'Q2':
            quiet_samples.append(sample)

    sample_set = SampleSet(quiet_samples)
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
        live_recording = record_sample(blocking=True)

        # process the recording into test samples
        test_samples = process_live_recording(live_recording,"UChiApt",str(time.time()))

        print('Testing...')
        for sample in test_samples:
            feature = feature_factory(sample)
            print("Prediction: "+str(classifier.predict(feature)))
    else:
        print('Exiting...')

if __name__ == '__main__':

    run_offline_svm()

    # Uncomment this line to run the classifier against new live recording
    #train_offline_svm_test_live()
