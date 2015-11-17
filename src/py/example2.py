# This contains a collection of short examples about how to use the new
# classes in the "dataset" Python module. Recall that a Python module is simply
# a collection of classes and functions within a single file.

from dataset import *
from get_dropbox_path import *

if __name__ == '__main__':
    print('Running example2 - shows how to record/play/save a new audio file \n')

    # record a new sound
    print('Recording...')
    sample = record_sample(blocking=True)

    # print stats
    print('Recorded sample of length: '+str(len(sample)))

    # play the audio back
    print('Replaying the recorded sample...')
    play_sample(sample)

    # write the file
    filename='sample-'+str(time.time())+'.wav'
    print('Writing the sample to local file: '+filename)
    save_sample(filename,sample)
