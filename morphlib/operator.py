"""
A module containing image operators.
"""

class MorphologicalOperator(object):
    def __call__(self, image):
        if not image.mode == 'greyscale':
            raise TypeError('%s only works on greyscale images' % self.__class__)
        res = []
        for i in xrange(image.height):
            res.append(
                [self.compute_pixel(i,j, image) for j in xrange(image.width)])
        return image.__class__(data=res, width=image.width, height=image.height)

    def compute_pixel(self, i, j, original):
        raise NotImplementedError()


class Erosion(MorphologicalOperator):
    """
    The erosion operator.
    """
    def __init__(self, structuralElement):
        self.structuralElement = structuralElement

    def compute_pixel(self, i, j, original):
        return original[i][j]


class Dilation(MorphologicalOperator):
    """
    The dilation operator.
    """
    def __init__(self, structuralElement):
        self.structuralElement = structuralElement

    def compute_pixel(self, i, j, original):
        return original[i][j]


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
        """
        A factory for predefined structural elements.
        """
        return cls(cls.PREDEFINED[key])
