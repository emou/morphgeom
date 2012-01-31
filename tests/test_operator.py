import unittest

from morphlib.operator import ImageOperator

class OperatorObjectTest(unittest.TestCase):

    def test_base_not_implemented(self):
        op = ImageOperator()
        self.assertRaises(NotImplementedError, op, None, None)

    def test_erosion(self):
        """ TBD """

    def test_dilation(self):
        """ TBD """

    def test_opening(self):
        """ TBD """

    def test_closing(self):
        """ TBD """
