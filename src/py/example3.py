# This contains a collection of short examples about how to use the new
# classes in the "dataset" Python module. Recall that a Python module is simply
# a collection of classes and functions within a single file.

from dataset import *
from get_dropbox_path import *

if __name__ == '__main__':
    print('Running example3 - process test recordings to generate new samples')

    # generate samples for all of the current recordings
    path=get_dropbox_path()
    recordings = find_testrecordings(path)
    print('\nFound '+str(len(recordings))+' recordings')
    prompt='This will generate new sample wav files for each test recording.\n Do you want to continue? (y/n)'
    if len(recordings) > 0 and raw_input(prompt) == 'y':
        for recording in recordings:
            print('\t'+str(recording))
            # recording.load_metadata()
            recording.generate_samples('..'+os.sep+'samples'+os.sep)
    else:
        print('aborting...')
