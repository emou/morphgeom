import unittest

class OperatorObjectTest(unittest.TestCase):


    def test_structured_element(self):
        from morphlib.operator import StructuredElement
        try:
            StructuredElement([1,2])
        except:
            pass
        else:
            raise AssertionError('StructuredElement lets a flat list in')

        try:
            StructuredElement([[1],[2]])
        except TypeError:
            pass
        else:
            raise AssertionError('StructuredElement lets a matrix with values not zero or one')

        try:
            StructuredElement([[1, 1],[0]])
        except TypeError:
            pass
        else:
            raise AssertionError('StructuredElement lets a matrix with variable row length')

        # These should work
        StructuredElement([[0],[0]])
        StructuredElement([[0],[1]])
        StructuredElement([[0, 0],[0, 1]])
        StructuredElement([[1, 1],[1, 1]])

    def test_erosion(self):
        """ TBD """
        from morphlib.operator import Erosion
        e = Erosion('Structured element?')

    def test_dilation(self):
        """ TBD """
        from morphlib.operator import Dilation
        d = Dilation('Structured element?')

    def test_opening(self):
        """ TBD """

    def test_closing(self):
        """ TBD """
