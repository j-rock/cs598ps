import sys
import time

from cssigps.offlineclassifier import *
from cssigps.dataset import *
from cssigps.feature import *
from cssigps.experiments import *
from get_dropbox_path import *

def feature_factory(sample):
    return FreqBinFeature(sample).feature

def class_factory(sample):
    return class_to_num(sample.y)

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
        print('class: '+str(class_factory(sample)))

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

def mag_factory(sample):
    return MagnitudeFeature(sample).feature

def fbank_factory(sample):
    return FBankFeature(sample).feature

def print_usage():
    """
    Print the usage for the main script.
    """
    print("USAGE: use the run.sh or the main.py directly.")
    print("")
    print("  run.sh <EXPERIMENT_NUMBER>")
    print("  python main.py <EXPERIMENT_NUMBER>")


if __name__ == '__main__':

    # decide which experiment to run based on the command line or user-input
    response = ""
    if len(sys.argv) >= 2:
        response=sys.argv[1]
        if response in ["-h","--help"]:
             print_usage()
             quit()
    else:
        prompt = "Which experiment would you like to run? [0-2]"
        response = raw_input(prompt)

    # run experiment
    if response == "0":
        path=get_dropbox_path()+"old-test/"
        run_experiment_0(path)
    elif response == "1":
        run_experiment_1(include_none=True)
    elif response == "2":
        run_experiment_2()
    elif response == "3":
        run_experiment_3()
    elif response == "4":
        run_experiment_4()
    elif response == "5":
        path=get_dropbox_path()+"vowels-test/"
        run_offline_svm(path)
    elif response == "S":
        # run single class classifier
        c = sys.argv[2]
        f = sys.argv[3]
        classes=["NONE"]
        path=get_dropbox_path()+"yes-no-test/"
        factory = fbank_factory

        # select the class
        if c == "Y":
            path=get_dropbox_path()+"yes-no-test/"
            classes.append("Y")
        elif c=="N":
            path=get_dropbox_path()+"yes-no-test/"
            classes.append("N")
        elif c=="A":
            path=get_dropbox_path()+"vowels-test/"
            classes=["A","NONE"]
        elif c=="E":
            path=get_dropbox_path()+"vowels-test/"
            classes=["E","NONE"]
        elif c=="I":
            path=get_dropbox_path()+"vowels-test/"
            classes=["I","NONE"]
        elif c=="O":
            path=get_dropbox_path()+"vowels-test/"
            classes=["O","NONE"]
        elif c=="U":
            path=get_dropbox_path()+"vowels-test/"
            classes=["U","NONE"]
        else:
            print("class argument invalid")
            quit()

        # select the feature
        if f == "fbank":
            factory=fbank_factory
        else:
            print("feature argument invalid")


        samples = find_testsamples(path)
        sample_set = SampleSet(samples,classes=classes)
        sample_set.stats()
        run_sample_experiment(sample_set,feat_factory=fbank_factory)
    elif response == "M":
        # run multi class classifier
        c = sys.argv[2]
        f = sys.argv[3]
        classes=["NONE"]
        path=get_dropbox_path()+"yes-no-test/"
        factory = fbank_factory

        # select the class
        if c == "Y":
            path=get_dropbox_path()+"yes-no-test/"
            classes=["Y","N","NONE"]
        elif c=="A":
            path=get_dropbox_path()+"vowels-test/"
            classes=["A","E","I","O","U","NONE"]
        else:
            print("class argument invalid")
            quit()

        # select the feature
        if f == "fbank":
            factory=fbank_factory
        else:
            print("feature argument invalid")


        samples = find_testsamples(path)
        sample_set = SampleSet(samples,classes=classes)
        sample_set.stats()
        run_sample_experiment(sample_set,feat_factory=fbank_factory)
    else:
        print("Invalid option. Aborting..")
