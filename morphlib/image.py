class Image(object):
    """
    An image abstraction
    """

    def __init__(self, filepath):
        """
        Initialize a new image from the given filepath.
        """
        self.filepath = filepath

    def load(self):
        """
        Loads image into memory and returns a list representing each pixel.

        Return value: None.
        """
        # PIL is used for image import/export only.
        import PIL.Image
        pil_image=PIL.Image.open(self.filepath)
        self._width, self._height = pil_image.size
        # Get the pixel list
        pixel_list = list(pil_image.getdata())
        data = []
        # The pixel list is flat, so we need to make it into a matrix for more
        # convinient processing.
        for i in xrange(0, len(pixel_list), self._width):
            data.append(tuple(pixel_list[i:i+self._width]))
        assert len(data) == self._height, \
                'Image data height mismatch: %s instead of %s.' % (len(data), self._height)
        self.data=data

    def save(self, filepath):
        """
        Saves an image to disk.
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

    def __getitem__(self, x):
        """
        Return row at position x as a tuple (rows are immutable)
        """
        try:
            return self.data[x]
        except AttributeError:
            self.load()
            return self.data[x]
