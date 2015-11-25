import unittest
import numpy as np
from numpyutils import split_padded, _calc_padding


def create_1d_array(l):
    return np.ones(l)

def create_2d_array(l):
    return np.ones((l,2))

class TestNonClassMethods(unittest.TestCase):
    """
    Tests for the methods in the "numpyutils" module not within a class.
    """

    def test_calc_padding_simple(self):
        """
        The calc_padding method simply checks whether the array can be divided
        evenly or needs to be padded or not.
        """

        # test 1d array with n segments where n is a factor of length
        arr1000 = create_1d_array(1000)
        self.assertEqual(_calc_padding(arr1000,1000),0)
        self.assertEqual(_calc_padding(arr1000,100),0)
        self.assertEqual(_calc_padding(arr1000,10),0)

        # test 1d array with n segments where n is not a factor of length
        self.assertEqual(_calc_padding(arr1000,24),8)
        self.assertEqual(_calc_padding(arr1000,3),2)
        self.assertEqual(_calc_padding(arr1000,12),8)

        # test 2d array with n segments where n is a factor of length
        arr1000 = create_2d_array(1000)
        self.assertEqual(_calc_padding(arr1000,1000),0)
        self.assertEqual(_calc_padding(arr1000,100),0)
        self.assertEqual(_calc_padding(arr1000,10),0)

        # test 2d array with n segments where n is not a factor of length
        self.assertEqual(_calc_padding(arr1000,24),8)
        self.assertEqual(_calc_padding(arr1000,3),2)
        self.assertEqual(_calc_padding(arr1000,12),8)

    def test_split_padded_simple(self):
        """
        Test split_padded method with simple arrays that divide evenly
        into the segments without any padding.
        """
        arr1000 = create_1d_array(1000)
        samplesize=500
        arrays = split_padded(arr1000,samplesize)
        for a in arrays:
            self.assertEqual(len(a),samplesize)
        self.assertEqual(len(arrays),2)

    def test_split_padded_array_needs_padding(self):
        """
        Test split_padded method with 1d array and samplesize that needs
        padding.
        """
        arr1000 = create_1d_array(1000)
        samplesize=300
        arrays = split_padded(arr1000,samplesize)
        for a in arrays:
            self.assertEqual(len(a),samplesize)
        self.assertEqual(len(arrays),4)

        # verify that the padding is done at the following range
        for i in range(100,300):
            self.assertEqual(arrays[3][i],0)
