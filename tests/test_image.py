import os
import unittest
from os.path import abspath, dirname, exists, join

from morphlib.image import Image, GrayscaleImage

class ImageObjectTest(unittest.TestCase):
    TEST_IMAGE={
        'path': join(dirname(abspath(__file__)), 'images', 'pict.png'),
        # Validated using an external program (gimp)
        'size': (110, 153),
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

    def test_Image_equality(self):
        p = self.TEST_IMAGE['path']
        i1, i2 = Image.load(filepath=p), Image.load(filepath=p)
        self.assertTrue(i1 == i2)
        self.assertEquals(i1, i2)
        i1[0][0] = (0, 0, 0)
        self.assertTrue(i1 != i2)

    def test_Image_object_pixel_values(self):
        self.assertEqual(self.i[0][0], self.TEST_IMAGE['topleftpixel'])

    def test_required_filepath(self):
        self.assertRaises(TypeError, Image)

    def test_save(self):
        name, ext = os.path.splitext(self.TEST_IMAGE['path'])
        test_out = '%s%s%s' % (name, '_test', ext)
        try:
            changed_pixel = (1, 2, 3)
            self.i[0][0] = changed_pixel
            self.i.save(test_out)
            self.assertTrue(exists(test_out))

            # Load it back
            i = Image.load(filepath=test_out)
            self.assertTrue(i.width, self.TEST_IMAGE['size'][0])
            self.assertTrue(i.height, self.TEST_IMAGE['size'][1])
            self.assertEquals(i[0][1], self.i[0][1])
            self.assertEquals(i[0][0], changed_pixel)
        finally:
            try:
                os.unlink(test_out)
            except EnvironmentError:
                pass

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

    def test_GrayscaleImage_invert(self):
        i = GrayscaleImage.load(filepath=self.TEST_IMAGE['path'])
        inv = i.invert()
        self.assertEquals(inv.size, i.size)
        self.assertEquals(inv[0][0] + i[0][0], 255)
