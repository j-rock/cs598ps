
import time
import os
import os.path
import json
import scipy.io.wavfile as wav
import sounddevice as sd
from numpyutils import *

def record_sample(duration=3,samplerate=11025,channels=1,blocking=False):
    """
    An optionally blocking method used to start the recording of a sample.

    Parameters:
    -----------
    duration : int
        The length in seconds to record
    samplerate : int
        The number of samplesa per second to record at
    channels : int
        The number of channels to be used during recording
    blocking : bool
        True if method should block until it completes. False otherwise.
    """
    sample=sd.rec(duration * samplerate, samplerate=samplerate, channels=channels)
    if blocking == True:
        sd.wait()
    return sample

def play_sample(sample,samplerate=11025,blocking=True):
    sd.play(sample, samplerate=samplerate,blocking=blocking)

def save_sample(filename,sample,samplerate=11025):
    wav.write(filename,samplerate,sample)

def _get_abs_files(path):
    """
    Utility method to return a list of the files within a root directory.

    Parameters
    ----------
    path : string
       The path to search for files and sub directories.
    """
    abs_files = []
    for root, subFolders, files in os.walk(path):
        for name in files:
            abs_files.append(os.path.join(root, name))
    return abs_files

def find_templates(path,get_files=_get_abs_files):
    """
    Recursively locate all of the templates within a root directory.

    Parameters
    ----------
    path : string
       The path to search for template files
    get_files : function
       The function to use for searching for files.
    """
    templates = []
    for file in get_files(path):
        if _is_template(file):
            templates.append(file)
    return templates

def _is_template(filepath):
    """
    Determine whether a filename corresponds to a template or not.

    Parameters
    ----------
    filepath : string
       The path of the file to check.
    """
    parts = filepath.split(os.sep)
    file_name = parts[len(parts)-1]
    return file_name.startswith('template_') and file_name.endswith('.wav')

def find_testrecordings(path,get_files=_get_abs_files):
    """
    Recursively locate all of the testrecordings within a root directory.
    """
    recordings = []
    for file in get_files(path):
        if _is_testrecording(file):
            recordings.append(TestRecording(file))
    return recordings

def _is_testrecording(filepath):
    """
    Determine whether a filename corresponds to a testrecording or not.

    Parameters
    ----------
    filepath : string
       The path of the file to check.
    """
    parts = filepath.split(os.sep)
    file_name = parts[len(parts)-1]
    return file_name.startswith('rec_') and file_name.endswith('.wav')

def find_testsamples(path,get_files=_get_abs_files):
    """
    Recursively locate all of the testsamples within a root directory.
    """
    samples = []
    for file in get_files(path):
        if _is_testsample(file):
            samples.append(file)
    return samples

def _is_testsample(filepath):
    """
    Determine whether a filename corresponds to a testsample or not.

    Parameters
    ----------
    filepath : string
       The path of the file to check.
    """
    parts = filepath.split(os.sep)
    file_name = parts[len(parts)-1]
    return file_name.startswith('testsample_') and file_name.endswith('.wav')

class Template():
    """
    Sound template that is used for detection. These instances represent the
    sounds that the classifier will train on.
    """

    def __init__(self,path):
        """
        Sound template that is used for detection. These instances represent the
        sounds that the classifier will train on. A template name is supposed
        to follow the pattern:

              template_<TEMPLATE>_<BITRATE>bit_<SAMPLING_RATE>.<FORMAT>

        e.g.  template_A1_16bit_48000.wav
        """
        self.path=path
        parts = path.split(os.sep)
        self.name=parts[len(parts)-1]
        name_parts = self.name.split('_')
        assert(len(name_parts),4)
        self.key=name_parts[1]


class TestRecording():
    """
    Sound recording that was made for training/testing. The length of the recording
    may be different between recordings. There may be several occurrances of one
    or more templates. A testrecording name is supposed to follow the pattern:

      rec_<ENVIRONMENT>_<ID>.<FORMAT>

      WHERE
            ENVIRONMENT:   Q1       - describes the sound environment
            ID:            0001     - describes the unique id of the environment recording
            FORMAT:        wav      - file format

       e.g.  rec_Q1_0001.wav
    """
    def __init__(self,path):
        self.path=path
        self.metapath=self.path.replace(".wav",".json",1)
        parts = path.split(os.sep)
        self.name=parts[len(parts)-1]
        name_parts = self.name.split('_')
        assert(len(name_parts),3)
        self.env = name_parts[1]
        self.id = name_parts[2].replace(".wav","")
        self.times = []
        self.templates = []
        self.valid = True
        self.loaded = False

    def load_metadata(self):
        """
        Method for accessing metadata. Metadata for testrecordings
        are stored within a json file located at the same location with the
        ".json" extension.
        """
        if (not os.path.isfile(self.metapath)):
            print('no file found')
            self.valid=False
            self.create_metadata()
        else:
            f = open(self.metapath,'r')
            obj = json.loads(f.read())

            # validate the metadata
            assert(self.name,obj["filename"])
            self.times = obj["times"]
            self.templates = obj["templates"]
        self.loaded = True

    def create_metadata(self):
        """
        Metadata for testrecordings are stored within a json file located at the
        same location with the ".json" extension. This creates a standard metadata
        file alongside the testrecording audiofile that can be populated by hand.
        """
        if (not os.path.isfile(self.metapath)):
            md = open(self.metapath,'w')
            obj = {}
            obj["filename"] = self.name
            obj["times"] = []
            obj["templates"] =[]
            md.write(json.dumps(obj, sort_keys=True,indent=4,separators=(',',': ')))
            md.close()

    def _create_sample_name(self,num):
        sample_key='NONE'
        # only set the template key of the sample if the template
        # occurred at this time.
        if num in self.times:
            sample_key=self.templates[self.times.index(num)]
        return "sample_"+self.env+"_"+str(self.id)+"_"+str(num)+"_"+sample_key+".wav"

    def generate_samples(self,relative_path=''):
        """
        TestSamples are derived from TestRecordings. This method will generate the
        actual sample wav files based on the test recording audio file. The metadata
        must exist and be valid in order for this method to succeed.
        """
        if not self.loaded:
            self.load_metadata()
        if not self.valid:
            raise ValueError('Cannot generate samples from invalid testrecording')
        else:
            (rate,audio) = wav.read(self.path)
            # divide the recordings into 1-sec samples
            num_segments = len(audio) / rate
            segments = split_padded(audio,num_segments)
            for s in range(0,len(segments)):
                root = self.path.replace(self.name,'')
                sample_path = root+relative_path+self._create_sample_name(s)
                save_sample(sample_path,segments[s],rate)

    def __str__(self):
        return self.name

class TestSample():
    """
    Sound sample derived from test recordings. These samples were pre-processed
    from test recordings to simplify training/testing. The length of test samples
    should be the same. A testsample name is supposed to follow the pattern:


    sample_<ENVIRONMENT>_<RECORDINGID>_<SAMPLENUMBER>_<TEMPLATE>.<FORMAT>

    e.g.   sample_Q1_0001_1_A1.wav
    """

    def __init__(self,path):
        self.path=path
        parts = path.split(os.sep)
        self.name=parts[len(parts)-1]
        name_parts = self.name.split('_')
        assert(len(name_parts),6)
        self.key=name_parts[3]

    def __str__(self):
        return self.name

class TemplateMarker():
    """
    Mark the time at which a specific template occurs within
    an audio file.
    """

    def __init__(self,key,min,sec):
        """
        Constructor method. Throws ValueError if min & sec are not in range
        [0,59].
        Parameters
        ----------
        key : string
           The template key
        min : int
           The minutes at which the event occurred.
        sec : int
           The seconds at which the event occurred.
        """
        self.key = key
        if min < 0 or min > 59 or sec < 0 or sec > 59:
            raise ValueError
        self.min = min
        self.sec = sec

    def __str__(self):
        """
        Return a string version of the instance.
        """
        return "{0:02d}:{1:02d}".format(self.min,self.sec)