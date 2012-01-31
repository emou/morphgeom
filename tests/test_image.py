import unittest
from os.path import abspath, dirname, exists, join

from morphlib.image import Image

class ImageObjectTest(unittest.TestCase):
    TEST_IMAGE={
        'path': join(dirname(abspath(__file__)), 'images', 'pict.jpg'),
        # Validated using an external program (gimp)
        'size': (110, 110),
        'topleftpixel': (255, 253, 244),
    }

    def setUp(self):
        assert exists(self.TEST_IMAGE['path']), \
                'Test picture missing: %s' % self.TEST_IMAGE['path']
        self.i = Image.load(filepath=self.TEST_IMAGE['path'])

    def test_Image_object(self):
        self.assertTrue(self.i.size[0]==self.i.width)
        self.assertTrue(self.i.size[1]==self.i.height)
        self.assertEqual(self.i.width, self.TEST_IMAGE['size'][0])
        self.assertEqual(self.i.height, self.TEST_IMAGE['size'][1])

    def test_Image_object_allows_assignment(self):
        try:
            self.i[0][0] = (0, 0, 0)
        except TypeError:
            raise AssertionError('Image does not allow RBG pixel assignment')

    def test_Image_object_doesnt_allow_invalid_assignemt(self):
        try:
            self.i[0][0] = ('foo', 0, 0)
        except TypeError:
            pass
        else:
            raise AssertionError(
                'Image does not catch junk pixel assignment (value)')

        try:
            self.i[0][0] = (0, 0, 0, 2)
        except TypeError:
            pass
        else:
            raise AssertionError(
                'Image does not catch junk pixel assignment (length)')

    def test_Image_object_pixel_values(self):
        self.assertEqual(self.i[0][0], self.TEST_IMAGE['topleftpixel'])

    def test_required_filepath(self):
        self.assertRaises(TypeError, Image)

    def test_save(self):
        self.assertRaises(NotImplementedError, self.i.save, 'foo')

    def test_copy(self):
        self.assertRaises(NotImplementedError, self.i.copy)

    def test_setrow(self):
        # Set a row to a new row with same width
        self.i[0] = [0,] * self.TEST_IMAGE['size'][0]
        # Set a row to a new row with wrong width
        self.assertRaises(ValueError,
                          self.i.__setitem__,
                          0,
                          [0,] * (self.TEST_IMAGE['size'][0] + 1))
