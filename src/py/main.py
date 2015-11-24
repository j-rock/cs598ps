from offlineclassifier import *
from get_dropbox_path import *
from dataset import *
from matplotlib import pyplot as plt
from feature import *

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

def run_offline_svm(quiet_env=True,path=get_dropbox_path()):
    """
    Run the offline version of the SVM classifier on all
    samples found in the path.

    Parameters
    ----------
    path - string
      The directory to search for TestSamples
    """
    print('Running SVM classifier')

    if quiet_env == True:
        # return a list of the audio test samples
        samples = find_testsamples(path)

        # extract quiet samples
        quiet_samples = []
        for sample in samples:
            if sample.env == 'Q1' or sample.env == 'Q2':
                quiet_samples.append(sample)

        classifier = SVMClassifier(quiet_samples)
        classifier.stats()
        classifier.run(feature_factory,class_factory)
    else:
        classifier = SVMClassifier(find_testsamples(path))
        classifier.stats()
        classifier.run(feature_factory,class_factory)

if __name__ == '__main__':
    run_offline_svm(quiet_env=False)
