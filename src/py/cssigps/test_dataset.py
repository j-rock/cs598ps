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
    templates.append('/test/a/nontemplate.wav')
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

class TestFinderMethods(unittest.TestCase):
    """
    Tests for the non-class methods that identify and find dataset files
    such as Templates, TestRecordings, and TestSamples.
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

        # check that a sample name with missing parts is invalid
        self.assertEqual(_is_testsample('sample_Q1_1_A1.wav'), False)
        self.assertEqual(_is_testsample('sample_Q1_.wav'), False)
        self.assertEqual(_is_testsample('sample_A1.wav'), False)

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
        self.assertEqual(m.y,'A1')

        s2 = TestSample('sample_Q1_0002_1_A1.wav')
        self.assertEqual(s2.path,'sample_Q1_0002_1_A1.wav')
        self.assertEqual(s2.recording_id,'0002')
        self.assertEqual(s2.env,'Q1')
        self.assertEqual(s2.sample_num,'1')
        self.assertEqual(s2.y,'A1')

        # test with long environment name
        m3 = TestSample('sample_Q100_0034_56_E32.wav')
        self.assertEqual(m3.env,'Q100')
        self.assertEqual(m3.recording_id,'0034')
        self.assertEqual(m3.sample_num,'56')
        self.assertEqual(m3.y,'E32')

class TestClassLabelMethods(unittest.TestCase):
    """
    Tests for the non-class methods that convert and handle
    class labels.
    """

    def test_extract_gen_class(self):
        """
        Test that the "extract_gen_class" method properly returns a
        short prefix summarizing the class to aid in histogram generation
        and dataset analysis.
        """
        # simple two letter cases
        self.assertEqual(extract_gen_class("A1"), "A")
        self.assertEqual(extract_gen_class("E1"), "E")
        self.assertEqual(extract_gen_class("I3"), "I")
        self.assertEqual(extract_gen_class("O2"), "O")
        self.assertEqual(extract_gen_class("U17"), "U")

        # test the pure text cases
        self.assertEqual(extract_gen_class("NONE"), "NONE")
        self.assertEqual(extract_gen_class("UNKNOWN"), "UNKNOWN")

        # test a longer class name
        self.assertEqual(extract_gen_class("CLICK1"), "CLICK")

        # test lowercase
        self.assertEqual(extract_gen_class("Click17"), "CLICK")

        # test an empty string
        self.assertEqual(extract_gen_class(""), "")

    def test_class_to_num(self):
        """
        Test that the "class_to_num" method properly returns a
        number for a class label
        """
        # simple yes/no case
        self.assertEqual(class_to_num("Y1"), 1)
        self.assertEqual(class_to_num("N1"), 0)

        # simple two letter cases
        self.assertEqual(class_to_num("A1"), 2)
        self.assertEqual(class_to_num("E1"), 3)
        self.assertEqual(class_to_num("I3"), 4)
        self.assertEqual(class_to_num("O2"), 5)
        self.assertEqual(class_to_num("U17"), 6)

        # test the pure text cases
        self.assertEqual(class_to_num("NONE"), -1)
        self.assertEqual(class_to_num("UNKNOWN"), -1)

        # test a longer class name
        self.assertEqual(class_to_num("CLICK1"), 10)

        # test lowercase
        self.assertEqual(class_to_num("Click17"), 10)

        # test an empty string
        self.assertEqual(class_to_num(""), -1)

    def test_num_to_class(self):
        """
        Test that the "num_to_class" method properly returns a
        class label for a num
        """
        # simple yes/no case
        self.assertEqual(num_to_class(1), "Y")
        self.assertEqual(num_to_class(0), "N")

        # simple two letter cases
        self.assertEqual(num_to_class(2), "A")
        self.assertEqual(num_to_class(3), "E")
        self.assertEqual(num_to_class(4), "I")
        self.assertEqual(num_to_class(5), "O")
        self.assertEqual(num_to_class(6), "U")

        # test the pure text cases
        self.assertEqual(num_to_class(-1), "")

        # test a longer class name
        self.assertEqual(num_to_class(10), "CLICK")

        # test lowercase
        self.assertEqual(num_to_class(10), "CLICK")

def prep_sample_set():
    samples = []
    samples.append(TestSample('sample_Q1_0002_1_A1.wav'))
    samples.append(TestSample('sample_Q1_0002_2_A1.wav'))
    samples.append(TestSample('sample_Q1_0002_3_A1.wav'))
    samples.append(TestSample('sample_Q1_0002_4_A1.wav'))
    samples.append(TestSample('sample_Q1_0002_5_A1.wav'))
    samples.append(TestSample('sample_Q1_0002_6_A1.wav'))
    samples.append(TestSample('sample_Q1_0002_7_A1.wav'))
    samples.append(TestSample('sample_Q1_0002_8_A1.wav'))
    samples.append(TestSample('sample_Q1_0002_9_A1.wav'))
    samples.append(TestSample('sample_Q1_0002_10_A1.wav'))

    return SampleSet(samples)

class TestSampleSet(unittest.TestCase):
    """
    Tests for the SampleSet class.
    """

    def test_sample_simple(self):
        """
        Test that the sample method returns the correct number
        of items.
        """
        sample_set = prep_sample_set()
        (train,test) = sample_set.sample()
        self.assertEqual(len(train)+len(test),len(sample_set))

    def test_sample_include_class_filter(self):
        """
        Test that the include_class filter works correctly
        by only including samples with that class.
        """
        samples = []
        samples.append(TestSample('sample_Q1_0002_1_A1.wav'))
        samples.append(TestSample('sample_Q1_0002_2_A2.wav'))
        samples.append(TestSample('sample_Q1_0002_3_A3.wav'))
        samples.append(TestSample('sample_Q1_0002_4_A4.wav'))
        samples.append(TestSample('sample_Q1_0002_5_E1.wav'))
        samples.append(TestSample('sample_Q1_0002_6_E1.wav'))
        samples.append(TestSample('sample_Q1_0002_7_E1.wav'))
        samples.append(TestSample('sample_Q1_0002_8_E1.wav'))
        samples.append(TestSample('sample_Q1_0002_9_E1.wav'))
        samples.append(TestSample('sample_Q1_0002_10_E1.wav'))
        samples.append(TestSample('sample_Q1_0002_11_NONE.wav'))
        samples.append(TestSample('sample_Q1_0002_12_NONE.wav'))

        all_samples = SampleSet(samples)
        self.assertEqual(len(all_samples),12)
        a_samples = SampleSet(samples,classes=["A"])
        self.assertEqual(len(a_samples),4)
        e_samples = SampleSet(samples,classes=["E"])
        self.assertEqual(len(e_samples),6)
        none_samples = SampleSet(samples,classes=["NONE"])
        self.assertEqual(len(none_samples),2)
        all_samples = SampleSet(samples,classes=["A","E","NONE"])
        self.assertEqual(len(all_samples),12)

    def test_sample_in_order(self):
        """
        Test that the sample method returns the same lists
        of training and testing data if the in_order argument
        is True. The method should be indempotent in this case.
        """
        sample_set = prep_sample_set()

        # take 1st sample from SampleSet and gather stats
        (train,test) = sample_set.sample(in_order=True)
        self.assertEqual(len(train)+len(test),len(sample_set))
        train1 = train[0]
        train2 = train[1]
        train3 = train[2]
        train_len = len(train)
        test1 = test[0]
        test2 = test[1]
        test3 = test[2]
        test_len = len(test)

        # take N samples and confirm that the results are the same
        for i in range(0,10):
            (train,test) = sample_set.sample(in_order=True)
            self.assertEqual(train_len,len(train))
            self.assertEqual(train1,train[0])
            self.assertEqual(train2,train[1])
            self.assertEqual(train3,train[2])
            self.assertEqual(test_len,len(test))
            self.assertEqual(train1,train[0])
            self.assertEqual(train2,train[1])
            self.assertEqual(train3,train[2])


    def test_sample_ratio_0_5(self):
        """
        Test that the sample method returns the proper ratio of
        TestSamples based on the ratio argument.
        """
        sample_set = prep_sample_set()
        self.assertEqual(len(sample_set),10)

        # test 0.5 ratio
        (train,test) = sample_set.sample(ratio=0.5)
        self.assertEqual(len(train),5)
        self.assertEqual(len(test),5)

    def test_sample_ratio_0_1(self):
        """
        Test that the sample method returns the proper ratio of
        TestSamples based on the ratio argument.
        """
        sample_set = prep_sample_set()
        self.assertEqual(len(sample_set),10)

        # test 0.1 ratio
        (train,test) = sample_set.sample(ratio=0.1)
        self.assertEqual(len(train),1)
        self.assertEqual(len(test),9)

    def test_sample_ratio_0_7(self):
        """
        Test that the sample method returns the proper ratio of
        TestSamples based on the ratio argument.
        """
        sample_set = prep_sample_set()
        self.assertEqual(len(sample_set),10)

        # test 0.7 ratio
        (train,test) = sample_set.sample(ratio=0.7)
        self.assertEqual(len(train),7)
        self.assertEqual(len(test),3)


    def test_sample_ratio_0_8(self):
        """
        Test that the sample method returns the proper ratio of
        TestSamples based on the ratio argument.
        """
        sample_set = prep_sample_set()
        self.assertEqual(len(sample_set),10)

        # test 0.8 ratio
        (train,test) = sample_set.sample(ratio=0.8)
        self.assertEqual(len(train),8)
        self.assertEqual(len(test),2)


    def test_sample_ratio_0_9(self):
        """
        Test that the sample method returns the proper ratio of
        TestSamples based on the ratio argument.
        """
        sample_set = prep_sample_set()
        self.assertEqual(len(sample_set),10)

        # test 0.9 ratio
        (train,test) = sample_set.sample(ratio=0.9)
        self.assertEqual(len(train),9)
        self.assertEqual(len(test),1)


    def test_sample_ratio_1_0(self):
        """
        Test that the sample method returns the proper ratio of
        TestSamples based on the ratio argument.
        """
        sample_set = prep_sample_set()
        self.assertEqual(len(sample_set),10)

        # test 0.7 ratio
        (train,test) = sample_set.sample(ratio=1.0)
        self.assertEqual(len(train),10)
        self.assertEqual(len(test),0)
