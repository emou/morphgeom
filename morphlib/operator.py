"""
A module containing image operators.
"""

class ImageOperator(object):
    """
    A binary Image operator
    """

    def __call__(self, imageA, imageB):
        raise NotImplementedError('Subclasses must provide implmentation.')


class Erosion(ImageOperator):
    """
    The erosion operator.
    """
    def __call__(self, imageA, imageB):
        raise NotImplementedError()

class Dilation(ImageOperator):
    """
    The dilation operator.
    """
    def __call__(self, imageA, imageB):
        raise NotImplementedError()
