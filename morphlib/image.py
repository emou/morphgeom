class Image(object):
    """
    An RGB image abstraction
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
        # PIL used for image import/export only.
        import PIL.Image
        pil_image=PIL.Image.open(filepath).convert('RGB')
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
        # PIL used for image import/export only.
        import PIL.Image
        i = PIL.Image.new('RGB', (self._width, self._height))

        assert len(self._data) == self._height, 'Wrong height'
        assert len(self._data[0]) == self._width, 'Wrong width'
        assert len(self._data[0][0]) == 3, 'Wrong pixel'

        data = [px for r in self._data for px in r]

        assert all(isinstance(px, tuple) for px in data)
        assert self._data[0][0] == data[0]
        assert self._data[0][1] == data[1]
        assert self._data[1][0] == data[self._width]

        i.putdata(data, scale=1.0, offset=0.0)
        i.save(filepath)

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
           len(x) != self.VALUES_PER_PIXEL or \
           not all(isinstance(v, int) for v in x):
            raise TypeError('Invalid RGB row value: %r' % x)
        self.lst[i] = x

    def __getitem__(self, i):
        return self.lst[i]
    
    def __len__(self):
        return len(self.lst)
