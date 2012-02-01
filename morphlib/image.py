class ImageRow(object):
    """
    RGB Image row
    """
    VALUES_PER_PIXEL=3

    def __init__(self, lst):
        self.lst = list(lst)
    
    def __setitem__(self, i, x):
        self.lst[i] = self.check_item(x)

    def __getitem__(self, i):
        return self.lst[i]
    
    def __len__(self):
        return len(self.lst)

    def check_item(self, x):
        if not isinstance(x, tuple) or \
           len(x) != self.VALUES_PER_PIXEL or \
           not all(isinstance(v, int) for v in x):
            raise TypeError('Invalid RGB pixel value: %r' % x)
        return x


class GrayscaleRow(ImageRow):
    def check_item(self, x):
        if not isinstance(x, int) or not 0<=x<=255:
            raise TypeError('Invalid grayscale pixel value: %r' % x)
        return x


class Image(object):
    """
    An RGB image abstraction
    """
    PIL_FORMAT='RGB'
    ROW_CLASS=ImageRow
    mode='rgb'

    def __init__(self, width, height, data):
        self.width = width
        self.height = height
        self._data = data

    @classmethod
    def load(cls, filepath):
        """
        Loads image into memory and returns the Image object representing it.
        """
        # PIL used for image import/export only.
        import PIL.Image
        pil_image=PIL.Image.open(filepath).convert(cls.PIL_FORMAT)
        width, height = pil_image.size
        # Get the pixel list
        pixel_list = list(pil_image.getdata())
        data = []
        # The pixel list is flat, so we need to make it into a matrix for more
        # convinient processing.
        for i in xrange(0, len(pixel_list), width):
            data.append(cls.ROW_CLASS(pixel_list[i:i+width]))
        assert len(data) == height, \
                'Image data height mismatch: %s instead of %s.' % (len(data), height)
        return cls(width=width, height=height, data=data)

    def save(self, filepath):
        """
        Saves an image to disk.
        """
        # PIL used for image import/export only.
        import PIL.Image
        i = PIL.Image.new(self.PIL_FORMAT, (self.width, self.height))

        assert len(self._data) == self.height, 'Wrong height'
        assert len(self._data[0]) == self.width, 'Wrong width'

        data = self.getdata()

        assert self._data[0][0] == data[0]
        assert self._data[0][1] == data[1]
        assert self._data[1][0] == data[self.width]

        i.putdata(data, scale=1.0, offset=0.0)
        i.save(filepath)

    def copy(self):
        """
        Return a copy of the image.
        """
        return self.__class__(
            width=self.width,
            height=self.height,
            data=map(list, self._data),
        )

    def invert(self):
        raise NotImplementedError("Not implemented for RGB yet!")

    def border(self, pixels=1):
        raise NotImplementedError("Not implemented for RGB yet!")

    @property
    def size(self):
        """
        Return the size of the image as a tuple (width, height).
        """
        return (self.width, self.height)

    def getdata(self):
        """
        Return a copy of the image data.
        """
        return [px for r in self._data for px in r]

    def __eq__(self, other):
        if self.size != other.size:
            return False
        for i in xrange(self.height):
            for j in xrange(self.width):
                if self[i][j] != other[i][j]:
                    print i, j, self[i][j], other[i][j]
                    return False
        return True

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


class GrayscaleImage(Image):
    # XXX: Should have an abstract class and not have Grayscale inherit Image
    # (which is actually RGBImage)
    PIL_FORMAT='L'
    ROW_CLASS=GrayscaleRow
    mode='grayscale'

    def invert(self):
        return GrayscaleImage(
            width=self.width,
            height=self.height,
            data=[map(lambda px: 255-px, r) for r in self._data]
        )

    def border(self, pixels=1):
        """
        Return the border of the image, which is a new image with BLACK inside.
        """
        assert 0 < pixels < self.width, "Invalid border size"
        assert 0 < pixels < self.height, "Invalid border size"

        compute_border_row = lambda i, r: list(r) if i<pixels or i>self.height-pixels \
                else [px if j<pixels or j>self.width-pixels else 0 for j, px in enumerate(r)]

        return GrayscaleImage(
            width=self.width,
            height=self.height,
            data=[compute_border_row(i, r) for i, r in enumerate(self._data)]
        )
