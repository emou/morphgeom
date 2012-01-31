"""
Putting it all together ...
"""
import os
import unittest
from os.path import abspath, basename, dirname, exists, join

from morphlib.image import GrayscaleImage
from morphlib.operator import Dilation, StructuralElement

class ImageObjectTest(unittest.TestCase):
    TEST_IMAGE={
        'path': join(dirname(abspath(__file__)), 'images', 'pict.png'),
        # Validated using an external program (gimp)
        'size': (100, 100),
        'topleftpixel': (255, 253, 244),
    }
    # Directory for test output
    TEST_OUT='test_out'

    def setUp(self):
        assert exists(self.TEST_IMAGE['path']), \
                'Test picture missing: %s' % self.TEST_IMAGE['path']
        self.i = GrayscaleImage.load(filepath=self.TEST_IMAGE['path'])

    def test_dilation_on_test_image(self):
        name, ext = os.path.splitext(self.TEST_IMAGE['path'])
        try:
            os.mkdir(self.TEST_OUT)
        except OSError:
            # Hope it just already exists
            pass
        test_out = join(self.TEST_OUT,
                        '%s%s%s' % (basename(name), '_dilation_test', ext))
        test_intermediate = join(self.TEST_OUT,
                                 '%s%s%s' % (basename(name), '_grayscale', ext))
        try:
            self.i.save(test_intermediate)
            dilate = Dilation(StructuralElement.predefined('rhombus'))
            i = dilate(self.i)
            i.save(test_out)
        finally:
            try:
                pass
                #os.unlink(test_out)
                #os.unlink(test_intermidiate)
            except EnvironmentError:
                pass
