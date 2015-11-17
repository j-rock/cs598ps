import unittest
import numpy as np
from numpyutils import *


def create_1d_array(len):
    return np.zeros(len)

def create_2d_array(len):
    return np.zeros((len,2))

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
        self.assertEqual(calc_padding(arr1000,1000),0)
        self.assertEqual(calc_padding(arr1000,100),0)
        self.assertEqual(calc_padding(arr1000,10),0)

        # test 1d array with n segments where n is not a factor of length
        self.assertEqual(calc_padding(arr1000,24),8)
        self.assertEqual(calc_padding(arr1000,3),2)
        self.assertEqual(calc_padding(arr1000,12),8)

        # test 2d array with n segments where n is a factor of length
        arr1000 = create_2d_array(1000)
        self.assertEqual(calc_padding(arr1000,1000),0)
        self.assertEqual(calc_padding(arr1000,100),0)
        self.assertEqual(calc_padding(arr1000,10),0)

        # test 2d array with n segments where n is not a factor of length
        self.assertEqual(calc_padding(arr1000,24),8)
        self.assertEqual(calc_padding(arr1000,3),2)
        self.assertEqual(calc_padding(arr1000,12),8)
