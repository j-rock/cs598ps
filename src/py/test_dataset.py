import unittest
import os
import time
from dataset import _get_abs_files, _is_template, _is_testsample, _is_testrecording
from dataset import *

def create_dummy_file(path):
    """
    utility method for creating test files with dummy contents.

    Parameters
    ----------
    path : string
       The path to create the file at.
    """
    f = open(path, 'w')
    try:
        f.write('test file')
    finally:
        f.close()

def get_mock_templates(path):
    templates=[]
    templates.append('template_A1_16bit_48000.wav')
    templates.append('/test/template_A2_16bit_48000.wav')
    templates.append('/test/a/template_A3_16bit_48000.wav')
    return templates

def get_mock_testrecordings(path):
    testrecordings=[]
    testrecordings.append('rec_Q1_0001.wav')
    testrecordings.append('/test/a/rec_Q2_0003.wav')
    testrecordings.append('/test/a/b/rec_Q1_0002.wav')
    return testrecordings

def get_mock_testsamples(path):
    testrecordings=[]
    testrecordings.append('sample_Q1_0001_1_A1.wav')
    testrecordings.append('/test/a/sample_Q1_0001_2_A1.wav')
    testrecordings.append('/test/a/b/sample_Q1_0001_3_A1.wav')
    return testrecordings

valid_template_name='template_A1_16bit_48000.wav'
valid_testrecording_name='rec_Q1_0001.wav'
valid_testsample_name='sample_Q1_0001_1_A1.wav'
valid_abs_template_name='/lib/template_A1_16bit_48000.wav'
valid_abs_testrecording_name='/lib/a/rec_Q1_0001.wav'
valid_abs_testsample_name='/lib/a/b/sample_Q1_0001_1_A1.wav'

class TestNonClassMethods(unittest.TestCase):
    """
    Tests for the methods not within a class.
    """

    def test_is_template_method(self):
        """
        Test that the "_is_template" methods properly evaluate template names.
        """
        # simple positive checks
        self.assertEqual(_is_template(valid_template_name), True)
        self.assertEqual(_is_template(valid_abs_template_name), True)

        # simple negative checks
        self.assertEqual(_is_template('tempalte_A1_16bit_48000.wav'), False)

        # ensure that no valid name of one type is valid for the other types
        # (these names need to correlate with a single type)
        self.assertEqual(_is_template(valid_testrecording_name), False)
        self.assertEqual(_is_template(valid_testsample_name), False)

    def test_is_testrecording_method(self):
        """
        Test that the "_is_testrecording" methods properly evaluate testrecording names.
        """

        # simple positive checks
        self.assertEqual(_is_testrecording(valid_testrecording_name), True)
        self.assertEqual(_is_testrecording(valid_abs_testrecording_name), True)

        # simple negative checks
        self.assertEqual(_is_testrecording('re__Q1_0001.wav'), False)

        # ensure that no valid name of one type is valid for the other types
        # (these names need to correlate with a single type)
        self.assertEqual(_is_testrecording(valid_template_name), False)
        self.assertEqual(_is_testrecording(valid_testsample_name), False)

    def test_is_testsample_method(self):
        """
        Test that the "_is_testsample" methods properly evaluate testsample names.
        """

        # simple positive checks
        self.assertEqual(_is_testsample(valid_testsample_name), True)
        self.assertEqual(_is_testsample(valid_abs_testsample_name), True)

        # simple negative checks
        self.assertEqual(_is_testsample('samle___Q1_0001_1_A1.wav'), False)

        # ensure that no valid name of one type is valid for the other types
        # (these names need to correlate with a single type)
        self.assertEqual(_is_testsample(valid_template_name), False)
        self.assertEqual(_is_testsample(valid_testrecording_name), False)

    def test_get_abs_files(self):
        temp_dir = 'test_'+str(time.time())
        temp_dir2 = temp_dir+os.sep+'a'
        temp_dir3 = temp_dir+os.sep+'a'+os.sep+'b'
        os.makedirs(temp_dir)
        os.makedirs(temp_dir2)
        os.makedirs(temp_dir3)
        create_dummy_file(temp_dir2+os.sep+'text.txt')
        create_dummy_file(temp_dir3+os.sep+'text.txt')

        files=_get_abs_files(temp_dir)
        self.assertEqual(len(files),2)

        # cleanup test files
        os.remove(temp_dir2+os.sep+'text.txt')
        os.remove(temp_dir3+os.sep+'text.txt')
        os.rmdir(temp_dir3)
        os.rmdir(temp_dir2)
        os.rmdir(temp_dir)

    def test_find_templates(self):
        templates = find_templates('mock_path',get_mock_templates)
        self.assertEqual(len(templates),3)

    def test_find_testrecordings(self):
        testrecordings = find_testrecordings('mock_path',get_mock_testrecordings)
        self.assertEqual(len(testrecordings),3)

    def test_find_testsamples(self):
        testsamples = find_testsamples('mock_path',get_mock_testsamples)
        self.assertEqual(len(testsamples),3)

class TestTemplate(unittest.TestCase):
    """
    Tests for the Template class
    """

    def test_init_sets_requiredprops(self):
        """
        Test that the init method sets the appropriate properties
        within the class object.
        """
        m = Template(valid_template_name);
        self.assertEqual(m.path,valid_template_name)
        self.assertEqual(m.key,'A1')

class TestTestRecording(unittest.TestCase):
    """
    Tests for the TestRecording class
    """

    def test_init_sets_requiredprops(self):
        """
        Test that the init method sets the appropriate properties
        within the class object.
        """
        m = TestRecording(valid_testrecording_name);
        self.assertEqual(m.path,valid_testrecording_name)


        m2 = TestRecording('rec_Q1_0002.wav')
        self.assertEqual(m2.path,'rec_Q1_0002.wav')
        self.assertEqual(m2.metapath,'rec_Q1_0002.json')
        self.assertEqual(m2.id,'0002')
        self.assertEqual(m2.env,'Q1')

        # test with long environment name
        m3 = TestRecording('rec_Q100_0002.wav')
        self.assertEqual(m3.env,'Q100')

class TestTestSample(unittest.TestCase):
    """
    Tests for the TestSample class
    """

    def test_init_sets_requiredprops(self):
        """
        Test that the init method sets the appropriate properties
        within the class object.
        """
        m = TestSample(valid_testsample_name);
        self.assertEqual(m.path,valid_testsample_name)
        self.assertEqual(m.template,'A1')

        s2 = TestSample('sample_Q1_0002_1_A1.wav')
        self.assertEqual(s2.path,'sample_Q1_0002_1_A1.wav')
        self.assertEqual(s2.recording_id,'0002')
        self.assertEqual(s2.env,'Q1')
        self.assertEqual(s2.sample_num,'1')
        self.assertEqual(s2.template,'A1')

        # test with long environment name
        m3 = TestSample('sample_Q100_0034_56_E32.wav')
        self.assertEqual(m3.env,'Q100')
        self.assertEqual(m3.recording_id,'0034')
        self.assertEqual(m3.sample_num,'56')
        self.assertEqual(m3.template,'E32')

default_key = 'A1'

def init_throws_exception(min,sec):
    """
    utility method for testing invalid argument values
    for TemplateMarker.
    """
    try:
        m = TemplateMarker(default_key,min,sec);
    except ValueError:
        return True
    return False

class TestTemplateMarker(unittest.TestCase):
    """
    Tests for the TemplateMarker class
    """

    def test_string(self):
        m = TemplateMarker(default_key,3,4);
        self.assertEqual(str(m), '03:04')
        m = TemplateMarker(default_key,13,4);
        self.assertEqual(str(m), '13:04')

    def test_init_invalidvalues(self):
        """
        TemplateMarker should only be created with min and sec in range
        [0,59]
        """
        self.assertEqual(init_throws_exception(0,59), False)
        self.assertEqual(init_throws_exception(-13,4), True)
        self.assertEqual(init_throws_exception(13,-4), True)
        self.assertEqual(init_throws_exception(-13,-4), True)
        self.assertEqual(init_throws_exception(0,60), True)
        self.assertEqual(init_throws_exception(60,0), True)
        self.assertEqual(init_throws_exception(60,60), True)

    def test_init_validvalue(self):
        m = TemplateMarker('A1',3,4);
        self.assertEqual(m.key, 'A1')
        self.assertEqual(m.min, 3)
        self.assertEqual(m.sec, 4)
