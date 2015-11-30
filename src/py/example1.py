# This contains a collection of short examples about how to use the new
# classes in the "dataset" Python module. Recall that a Python module is simply
# a collection of classes and functions within a single file.

from cssigps.dataset import *
from get_dropbox_path import *

if __name__ == '__main__':
    print('Running example1 - reports list of audio files in dropbox folder')

    path=get_dropbox_path()

    # return a list of the audio templates
    templates = find_templates(path)
    print('\nFound '+str(len(templates))+' templates')
    for template in templates:
        print('\t'+str(template))

    # return a list of the audio test recordings
    recordings = find_testrecordings(path)
    print('\nFound '+str(len(recordings))+' recordings')
    for recording in recordings:
        print('\t'+str(recording))

    # return a list of the audio test samples
    samples = find_testsamples(path)
    print('\nFound '+str(len(samples))+' samples')
    sample_set = SampleSet(samples)
    sample_set.stats()
    if raw_input('Print the names of all samples? [y/n]') == 'y':
        for sample in samples:
            sample.check()
            print('\t'+str(sample))
