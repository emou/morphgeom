import unittest

class ImageMock(object):
    """
    A mock Image object for testing purposes.
    """
    mode='grayscale'

    DATA = [
        [250] * 20,
    ] * 20

    def __init__(self, width=None, height=None, data=None):
        if data is None:
            self.data = self.DATA
            assert width is None
            assert height is None
            self.width = len(self.DATA[0])
            self.height = len(self.DATA)
        else:
            assert width is not None
            assert height is not None
            self.data = data
            self.width = width
            self.height = height
        self.size=(self.width, self.height)

    def __getitem__(self, i):
        return self.data[i]

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

        # Now a more realistic example
        b = StructuralElement([[0, 0, 1],
                               [0, 1, 1],
                               [1, 0, 0],
                              ])
        self.assertEqual(b.center, (1,1))

    def test_erosion(self):
        """ TBD """
        from morphlib.operator import Erosion, StructuralElement
        erode = Erosion(StructuralElement.predefined('octagon'))
        original = ImageMock()
        # Set the highest value to the pixel in the top left corner
        original[0][0] = 255
        # Set some low value to the second pixel on the second row
        original[1][1] = 1
        result = erode(original)
        self.assertEquals(result.size, original.size)
        # Make sure that the value of the second pixel on the second row is switched to 0
        # (erosion takes the minimum)
        self.assertEquals(result[0][0], original[0][1])
        self.assertEquals(result[1][1], original[0][1])

    def test_dilation(self):
        """ TBD """
        from morphlib.operator import Dilation, StructuralElement
        dilate = Dilation(StructuralElement.predefined('octagon'))
        original = ImageMock()
        # Set a high value to the second pixel to the right
        original[0][1] = 255
        result = dilate(original)
        self.assertEquals(result.size, original.size)
        # Make sure that the pixel left to the highest-valued pixel was switched to the bumped pixel's value
        # (since dilation takes the maximum)
        self.assertEquals(result[0][0], original[0][1])

    def test_opening(self):
        """ TBD """

    def test_closing(self):
        """ TBD """
