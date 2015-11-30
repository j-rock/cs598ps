# This contains a collection of short examples about how to use the new
# classes in the "dataset" Python module. Recall that a Python module is simply
# a collection of classes and functions within a single file.

from cssigps.dataset import *
from cssigps.feature import *
from get_dropbox_path import *

if __name__ == '__main__':
    print('Running example4 - generates features for each test sample')

    path=get_dropbox_path()

    # return a list of the audio test samples
    samples = find_testsamples(path)
    print('\nFound '+str(len(samples))+' samples')

    # generate features
    print("\nGenerating FreqBinFeatures")
    for sample in samples:
        if sample.env == 'Q1':
            sample.check()
            print('\t'+str(sample))
            feature = FreqBinFeature(sample)
            feature.stats()
