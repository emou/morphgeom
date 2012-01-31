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
        self.i = Image(filepath=self.TEST_IMAGE['path'])

    def test_Image_object(self):
        self.assertEquals(self.i.filepath, self.TEST_IMAGE['path'])
        self.i.load()
        self.assertTrue(self.i.size[0]==self.i.width)
        self.assertTrue(self.i.size[1]==self.i.height)
        self.assertEqual(self.i.width, self.TEST_IMAGE['size'][0])
        self.assertEqual(self.i.height, self.TEST_IMAGE['size'][1])

    def test_Image_object_pixel_values(self):
        self.assertEqual(self.i[0][0], self.TEST_IMAGE['topleftpixel'])

    def test_required_filepath(self):
        self.assertRaises(TypeError, Image)
