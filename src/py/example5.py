# This contains a simple method to generate empty json files for new
# TestRecordings.

import sys

from cssigps.dataset import *

def process_group(path):
    # generate json files for a group of TestRecordings
    print('Generate json files for group of TestRecording')
    recordings = find_testrecordings(path)
    for rec in recordings:
        rec.create_metadata()

def process_single(path):
    print('Generate json file for single TestRecording')
    recording_path = path
    recording = TestRecording(recording_path)
    recording.create_metadata()
    #recording.generate_classless_samples()

if __name__ == '__main__':
    if len(sys.argv) > 0:
        process_single(sys.argv[1])
