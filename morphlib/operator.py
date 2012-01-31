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

class StructuralElement(object):
    """
    Represents a structural element.
    Basically this must be a matrix with 1/0 values only.
    """

    PREDEFINED = {
        'octagon': [[0, 1, 1, 0],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [0, 1, 1, 0],
                   ],

        'diagonal': [[0, 0, 0, 1],
                     [0, 0, 1, 0],
                     [0, 1, 0, 0],
                     [1, 0, 0, 0],
                    ],
    }

    def __init__(self, matrix_list):
        if not all(x in [0, 1] for row in matrix_list for x in row):
            raise TypeError("Structured element should be initialized with a matrix containing only zeros and ones")
        elif not all(len(row) == len(matrix_list[0]) for row in matrix_list):
            raise TypeError("Malformed structured element matrix: %r" % matrix_list)
        self.matrix = list(matrix_list)

    @classmethod
    def predefined(cls, key):
        return cls(cls.PREDEFINED[key])
