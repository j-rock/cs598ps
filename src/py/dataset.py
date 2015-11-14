
import os

def _get_abs_files(path):
    """
    Get a list of the files within a root directory.

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
            recordings.append(file)
    return recordings

def _is_testrecording(filepath):
    """
    Determine whether a filename corresponds to a testrecording or not.
    """
    parts = filepath.split(os.sep)
    file_name = parts[len(parts)-1]
    return file_name.startswith('testrecording_') and file_name.endswith('.wav')

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
    or more templates.
    """
    def __init__(self,path):
        self.path=path
        self.key=""

class TestSample():
    """
    Sound sample derived from test recordings. These samples were pre-processed
    from test recordings to simplify training/testing. The length of test samples
    should be the same.
    """

    def __init__(self,path):
        self.path=path
        self.key=""

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
