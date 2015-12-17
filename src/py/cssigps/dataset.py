import time
import os
import re
import string
import os.path
import json
import random

import scipy.io.wavfile as wav

from utils import *
from utils import _split_padded

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
            try:
                samples.append(TestSample(file))
            except AssertionError:
                pass
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
    name_parts = file_name.split('_')
    if len(name_parts) != 5:
        return False
    return file_name.startswith('sample_') and file_name.endswith('.wav')

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
        assert len(name_parts) == 4
        self.key=name_parts[1]


def process_live_recording(audio,env,id,samplerate,directory="./temp"):
    """
    Store and create a TestRecording for a single
    live session and generate TestSamples for
    classification.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    recording_path = directory+os.sep+"rec_"+env+"_"+id+".wav"
    if os.path.exists(recording_path):
        raise ValueError("Recording path already exists: "+recording_path)
    save_sample(recording_path,audio,samplerate=samplerate)
    recording = TestRecording(recording_path)
    return recording.generate_classless_samples()

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
        assert len(name_parts) ==3
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
            assert self.name == obj["filename"]
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

    def _create_sample_name(self,num,default_key='NONE'):
        sample_key=default_key
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
            segments = _split_padded(audio,rate)
            samples = []
            for s in range(0,len(segments)):
                root = self.path.replace(self.name,'')
                sample_path = root+relative_path+self._create_sample_name(s)
                save_sample(sample_path,segments[s],rate)
                samples.append(TestSample(sample_path))
            return samples

    def generate_classless_samples(self,relative_path=''):
        """
        TestSamples are derived from TestRecordings. Typically each TestRecording
        is annotated with an associated json file, but this is not the case for
        live test recordings. This method will generate TestSamples without knowing
        the class of each audio segment within it.
        """
        (rate,audio) = wav.read(self.path)
        segments = _split_padded(audio,rate)
        samples = []
        for s in range(0,len(segments)):
            root = self.path.replace(self.name,'')
            sample_path = root+relative_path+self._create_sample_name(s,default_key='UNKNOWN')
            save_sample(sample_path,segments[s],rate)
            samples.append(TestSample(sample_path))
        return samples

    def __str__(self):
        return self.name

class TestSample():
    """
    Sound sample derived from test recordings. These samples were generated
    from test recordings to simplify training/testing. The length of test samples
    should be the same. A testsample name is supposed to follow the pattern:


    sample_<ENVIRONMENT>_<RECORDINGID>_<SAMPLENUMBER>_<CLASS>.<FORMAT>

    e.g.   sample_Q1_0001_1_A1.wav
    """

    def __init__(self,path):
        self.path=path
        parts = path.split(os.sep)
        self.name=parts[len(parts)-1]
        name_parts = self.name.split('_')
        assert len(name_parts) == 5
        self.env=name_parts[1]
        self.recording_id=name_parts[2]
        self.sample_num=name_parts[3]
        self.y=name_parts[4].replace('.wav','')
        self.samples=0
        self.samplerate=0

    def classname(self):
        """
        Convenience method to clarify the properties of the object.
        """
        return self.y

    def sec(self):
        """
        Convenience method to return the length of the sample
        in seconds.
        """
        if self.samples != 0 and self.samplerate != 0:
            return float(self.samples)/float(self.samplerate)
        return 0.0

    def __str__(self):
        string = "<sample name='"+self.name+"' y='"+self.y+"' "
        if self.sec() != 0.0:
            string=string+"length='"+str(self.sec())+"sec' "
        return string+">"


    def check(self):
        """
        Load the wav file sample rate, length. Currently this is done
        by reading the file directly, which can likely be improved in the future.
        """
        if self.samples == 0 or self.samplerate == 0:
            (rate,audio) = wav.read(self.path)
            self.samples=len(audio)
            self.samplerate=rate

def extract_gen_class(class_label):
    """
    Convert a specific class label (e.g. A1) to a
    generic class label (e.g. A).
    """
    matchObj = re.match(r'([a-zA-Z]+)([0-9]*)',class_label)
    if matchObj:
        return string.upper(matchObj.group(1))
    return ""

def class_to_num(class_label):
    """
    Convert a class label to a number to aid in classification
    tasks.
    """
    gen_class = extract_gen_class(class_label)
    if gen_class == "N":
        return 0
    elif gen_class =="Y":
        return 1
    elif gen_class =="A":
        return 2
    elif gen_class =="E":
        return 3
    elif gen_class =="I":
        return 4
    elif gen_class =="O":
        return 5
    elif gen_class =="U":
        return 6
    elif gen_class =="CLICK":
        return 10
    return -1

def num_to_class(num):
    """
    Convert a number after classification back to a class label.
    """
    if num == 0:
        return "N"
    elif num ==1:
        return "Y"
    elif num ==2:
        return "A"
    elif num ==3:
        return "E"
    elif num ==4:
        return "I"
    elif num ==5:
        return "O"
    elif num ==6:
        return "U"
    elif num ==10:
        return "CLICK"
    return ""

class SampleSet():
    """
    Generate sample sets of TestSample objects for
    training and testing classifiers.
    """

    def __init__(self,samples,envs=None,classes=None):
        """
        Constructor for the SampleSet class. Filtering available for both
        classes and environments of TestSamples.

        Parameters:
        -----------

        samples - list of TestSample
            List of samples to include in the sample set.
        envs - list of string
            List of environment strings to filter the list of samples.
            (e.g. envs=["Q"] will only include samples with
            environment Q)
        classes - list of string
            List of class strings to filter the list of samples.
            (e.g. classes=["A"] will only include samples with
            class A)
        """
        s=[]
        for sample in samples:
            sample_class = extract_gen_class(sample.y)
            sample_env = sample.env
            if classes and not sample_class in classes:
                continue
            if envs and not sample_env in envs:
                continue
            s.append(sample)
        self.samples = s

    def sample(self,in_order=False,ratio=0.5):
        """
        Create training and testing sample sets.

        Parameters:
        -----------

        in_order - bool
           If True, no random sorting will be performed. The
           training and testing datasets will be non-changing
           if the ratio remains the same. By default, this is
           False.
        ratio - float
           The training/testing data ratio. This number must be
           in the range (0.0,1.0]
        """
        assert ratio > 0.
        assert ratio <= 1.
        train=[]
        test=[]

        n = len(self.samples)
        sequence = range(n)
        if not in_order:
            # generate random sequence
            sequence = random.sample(sequence,n)

        for s in sequence:
            if (float(len(train)/float(n))) < float(ratio):
                # add to training set
                train.append(self.samples[s])
            else:
                # add to testing set
                test.append(self.samples[s])
        return (train,test)

    def class_rep(self):
        """
        Return an array of samples with one from each class type.
        """
        classes=[]
        rep=[]
        for sample in self.samples:
            sample_class = extract_gen_class(sample.y)
            if sample_class not in classes:
                rep.append(sample)
                classes.append(sample_class)
        return rep

    def stats(self):
        """
        Print out basic statistics about the sample set.
        """
        classes=[]
        class_histogram={}
        for sample in self.samples:
            sample_class = extract_gen_class(sample.y)
            classes.append(sample_class)
            if class_histogram.has_key(sample_class):
                class_histogram[sample_class]=class_histogram[sample_class]+1
            else:
                class_histogram[sample_class]=0
        self.classes=set(classes)
        self.class_histogram = class_histogram
        print("Num samples: "+str(len(self.samples)))
        print("Num classes: "+str(len(self.classes)))
        for key in self.class_histogram.iterkeys():
            print("\t'"+key+"' : "+str(self.class_histogram[key]))

    def __len__(self):
        return len(self.samples)
