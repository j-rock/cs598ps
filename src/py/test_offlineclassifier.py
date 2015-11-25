import unittest
from offlineclassifier import TemplateClassifier
from sklearn import svm
import numpy as np

class TestTemplateClassifier(unittest.TestCase):
    """
    Tests for the TemplateClassifier class
    """

    def test_test_asserts(self):
        classifier = TemplateClassifier()
        # classifier.test_recording('')

class TestSklearnSVM(unittest.TestCase):
    """
    Tests for the linear SVM implementation provided
    by the sklearn library.
    """

    def test_simple(self):
        """
        Run the simple SVM test listed on their web page.
        """
        X = np.asarray([[0,0],[1,1]])
        y=[0,1]
        clf = svm.SVC()
        clf.fit(X,y)

        # predict point on side of 1 class
        self.assertEqual(clf.predict([2.,2.])[0],1)

        # predict point on side of 0 class
        self.assertEqual(clf.predict([-2.,-2.])[0],0)

    #def test_multi_class(self):
