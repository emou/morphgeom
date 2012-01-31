import unittest

class ImageMock(object):
    """
    A mock Image object for testing purposes.
    """
    pass

class OperatorObjectTest(unittest.TestCase):

    def test_structural_element(self):
        from morphlib.operator import StructuralElement
        try:
            StructuralElement([1,2])
        except:
            pass
        else:
            raise AssertionError('StructuralElement lets a flat list in')

        try:
            StructuralElement([[1],[2]])
        except TypeError:
            pass
        else:
            raise AssertionError('StructuralElement lets a matrix with values not zero or one')

        try:
            StructuralElement([[1, 1],[0]])
        except TypeError:
            pass
        else:
            raise AssertionError('StructuralElement lets a matrix with variable row length')

        # These should work
        StructuralElement([[0],[0]])
        StructuralElement([[0],[1]])
        StructuralElement([[0, 0],[0, 1]])
        StructuralElement([[1, 1],[1, 1]])

    def test_erosion(self):
        """ TBD """
        from morphlib.operator import Erosion, StructuralElement
        e = Erosion(StructuralElement.predefined('octagon'))
        e(ImageMock())

    def test_dilation(self):
        """ TBD """
        from morphlib.operator import Dilation
        d = Dilation('Structural element?')

    def test_opening(self):
        """ TBD """

    def test_closing(self):
        """ TBD """
