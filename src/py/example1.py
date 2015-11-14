# This contains a collection of short examples about how to use the new
# classes in the "dataset" Python module. Recall that a Python module is simply
# a collection of classes and functions within a single file.

from dataset import *
from get_dropbox_path import *

if __name__ == '__main__':
    print('Running example1\n')

    # return a list of the audio templates
    templates = find_templates(get_dropbox_path())
    print('Found '+str(len(templates))+' templates')
    for template in templates:
        print('\t'+str(template))

    # return a list of the audio test recordings
    recordings = find_testrecordings(get_dropbox_path())
    print('Found '+str(len(recordings))+' recordings')
    for recording in recordings:
        print('\t'+str(recording))
