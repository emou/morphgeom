class Image(object):
    """
    An image abstraction
    """

    def __init__(self, width, height, data):
        self._width = width
        self._height = height
        self._data = data

    @classmethod
    def load(cls, filepath):
        """
        Loads image into memory and returns the Image object representing it.
        """
        # PIL is used for image import/export only.
        import PIL.Image
        pil_image=PIL.Image.open(filepath)
        width, height = pil_image.size
        # Get the pixel list
        pixel_list = list(pil_image.getdata())
        data = []
        # The pixel list is flat, so we need to make it into a matrix for more
        # convinient processing.
        for i in xrange(0, len(pixel_list), width):
            data.append(RGBImageRow(pixel_list[i:i+width]))
        assert len(data) == height, \
                'Image data height mismatch: %s instead of %s.' % (len(data), height)
        return cls(width=width, height=height, data=data)

    def save(self, filepath):
        """
        Saves an image to disk.
        """
        raise NotImplementedError()

    def copy(self):
        """
        Return a copy of the image.
        """
        raise NotImplementedError()

    @property
    def size(self):
        """
        Return the size of the image as a tuple (width, height).
        """
        return (self.width, self.height)

    @property
    def width(self):
        """
        Return the width of the image in pixels.
        """
        try:
            return self._width
        except AttributeError:
            self.load()
            return self._width

    @property
    def height(self):
        """
        Return the height of the image in pixels.
        """
        try:
            return self._width
        except AttributeError:
            self.load()
            return self._width

    def __getitem__(self, i):
        """
        Return a row of pixels
        """
        try:
            return self._data[i]
        except AttributeError:
            self.load()
            return self._data[i]
    
    def __setitem__(self, i, row):
        """
        Set a row of pixels
        """
        self._data[i] = self._check_row(row)

    def append(self, i, row):
        """
        Append a row of pixels
        """
        self._data.append(self._check_row(row))

    def _check_row(self, row):
        row = list(row)
        if len(row) != self.width:
            raise ValueError(
                "All rows in image should have lenght %s. Got %s instead" % (
                    self.width, len(row)
                ))
        return row

class RGBImageRow(object):
    VALUES_PER_PIXEL=3

    def __init__(self, lst):
        self.lst = list(lst)
    
    def __setitem__(self, i, x):
        if not isinstance(x, tuple) or \
           len(x) != self.VALUES_PER_PIXEL:
            raise TypeError('Invalid RGB row value: %r' % x)
        self.lst[i] = x

    def __getitem__(self, i):
        return self.lst[i]
