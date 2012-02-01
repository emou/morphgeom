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
        """ Test the erosion operator """
        from morphlib.operator import Erosion, StructuralElement
        e = Erosion(StructuralElement.predefined('rhombus'))

    def test_dilation(self):
        """ Test the dilation operator """
        from morphlib.operator import Dilation, StructuralElement
        dilate = Dilation(StructuralElement.predefined('rhombus'))
        original = ImageMock()
        # Set a high value to the second pixel to the right
        original[0][1] = 255
        result = dilate(original)
        self.assertEquals(result.size, original.size)
        # Make sure that the pixel left to the highest-valued pixel was switched to the bumped pixel's value
        # (since dilation takes the maximum)
        self.assertEquals(result[0][0], original[0][1])

    def test_geodesic_dilation(self):
        """ Test geodesic dilation operator """
        from morphlib.operator import GeodesicDilation, StructuralElement
        original = ImageMock()
        mask = ImageMock()
        dilate = GeodesicDilation(StructuralElement.predefined('rhombus'), mask=mask)
        dilate(original)

    def test_opening(self):
        """ TBD """

    def test_closing(self):
        """ TBD """
