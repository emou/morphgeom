"""
A module containing image operators.
"""

class Erosion(object):
    """
    The erosion operator.
    """
    def __init__(self, structuralElement):
        self.structuralElement = structuralElement

    def __call__(self, image):
        raise NotImplementedError()

class Dilation(object):
    """
    The dilation operator.
    """
    def __init__(self, structuralElement):
        self.structuralElement = structuralElement

    def __call__(self, image):
        raise NotImplementedError()
