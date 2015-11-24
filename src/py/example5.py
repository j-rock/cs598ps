# This contains a collection of short examples about how to use the new
# classes in the "dataset" Python module. Recall that a Python module is simply
# a collection of classes and functions within a single file.

from dataset import *
from get_dropbox_path import *
from feature import *
from offlineclassifier import *

def feature_factory(sample):
    return FreqBinFeature(sample).feature

def class_factory(sample):
    if sample.y == "A1":
        return 1
    else:
        return 0

if __name__ == '__main__':
    print('Running example1 - generates features for each test sample')

    path=get_dropbox_path()

    # return a list of the audio test samples
    samples = find_testsamples(path)
    print('\nFound '+str(len(samples))+' samples')

    # extract quiet samples
    quiet_samples = []
    for sample in samples:
        if sample.env == 'Q1' or sample.env == 'Q2':
            quiet_samples.append(sample)

    # generate MagnitudeFeatures
    print("\nGenerating MagnitudeFeatures")
    for sample in samples:
        sample.check()
        print('\t'+str(sample))
        print(str(feature_factory(sample)))

    # run SVM classifier
    classifier = SVMClassifier(samples)
    classifier.stats()

    classifier.run(feature_factory,class_factory)
