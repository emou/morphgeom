"""
A module containing morphological operators.
"""

class MorphologicalOperator(object):
    def __call__(self, image):
        if image.mode != 'grayscale':
            raise TypeError('%s only works on grayscale images' % self.__class__)
        res = []
        for i in xrange(image.height):
            res.append(
                [self.compute_pixel((i,j), image) for j in xrange(image.width)])
        assert len(res)==image.height, 'Wrong height'
        assert len(res[0])==image.width, 'Wrong width'
        return image.__class__(data=res, width=image.width, height=image.height)

    def compute_pixel(self, px, original):
        raise NotImplementedError()

class ComposedMorphologicalOperator(MorphologicalOperator):

    operationsList = []
    
    def __call__(self, original):
        if original.mode != 'grayscale':
            raise TypeError('%s only works on grayscale images' % self.__class__)
        image = original.copy()
        res = []
        for operation in self.operationsList:
            instance = operation(self.structuralElement)
            print(self.structuralElement)
            for i in xrange(image.height):
                res.append(
                    [instance.compute_pixel((i,j), image) for j in xrange(image.width)])
            assert len(res)==image.height, 'Wrong height'
            assert len(res[0])==image.width, 'Wrong width'
            image = image.__class__(data = res, width=image.width, height=image.height)
            res = []

        return image


class Erosion(MorphologicalOperator):
    """
    The erosion operator.
    """
    def __init__(self, structuralElement):
        self.structuralElement = structuralElement

    def compute_pixel(self, px, original):
        i, j = px
        neighbourhood = self.structuralElement.get_neighbourhood(original, px)
        return min(original[p][q] for p,q in neighbourhood)


class Dilation(MorphologicalOperator):
    """
    The dilation operator.
    """
    def __init__(self, structuralElement):
        self.structuralElement = structuralElement

    def compute_pixel(self, px, original):
        i, j = px
        neighbourhood = self.structuralElement.get_neighbourhood(original, px)
        return max(original[p][q] for p,q in neighbourhood)


class GeodesicDilation(Dilation):
    """
    Geodesic dilation operator.
    """
    def __init__(self, structuralElement, mask):
        super(GeodesicDilation, self).__init__(structuralElement)
        if mask is not None and mask.mode != 'grayscale':
            raise TypeError('%s only works with grayscale mask' % self.__class__)
        self.mask = mask

    def __call__(self, original):
        if self.mask is not None \
           and (original.width > self.mask.width \
                or original.height > self.mask.height):
            raise ValueError('Mask too small %r for image %r' % (
                self.mask.size, original.size))
        return super(GeodesicDilation, self).__call__(original)

    def compute_pixel(self, px, original):
        i, j = px
        gd = super(GeodesicDilation, self).compute_pixel(px, original)
        if self.mask is None:
            return gd
        return min(self.mask[i][j], gd)


class ReconstructionByDilation(GeodesicDilation):
    # Mainly for debugging.
    ITERATIONS_LIMIT = 100

    def __call__(self, original):
        i = 0
        result = original.copy()

        changed = True
        while True:
            if not changed:
                return result
            changed = False
            i += 1
            if i > self.ITERATIONS_LIMIT:
                return result
            for i in xrange(result.height):
                for j in xrange(result.width):
                    old = result[i][j]
                    result[i][j] = GeodesicDilation.compute_pixel(self, (i,j), result)
                    if old != result[i][j]:
                        changed = True
        return 'joo'


class OpeningByReconstruction(MorphologicalOperator):
    """
    TBD
    """
    pass


class AreaOpening(MorphologicalOperator):
    """
    TBD
    """
    pass


class CloseHoles(MorphologicalOperator):
    """
    Closes-holes operator.
    As defined in M.A. Luengo-Oroz et al. / Image and Vision Computing 28 (2009) 278-284.
    """
    def __call__(self, original):
        # Used as a marker
        inv = original.invert()
        border = original.border()
        reconstruct = ReconstructionByDilation(
            StructuralElement.predefined('circle'),
            inv
        )
        return reconstruct(border).invert()


class Opening(ComposedMorphologicalOperator):
    """
    Opening operator. Basically, this is an erosion followed by a dilation
    """

    operationsList = [Erosion, Dilation]
    
    def __init__(self, structuralElement):
        self.structuralElement = structuralElement 


class Closing(ComposedMorphologicalOperator):
    """
    Opening operator. Basically, this is a dilation followed by an erosion
    """

    operationsList = [Dilation, Erosion]
    
    def __init__(self, structuralElement):
        self.structuralElement = structuralElement
        

class StructuralElement(object):
    """
    Represents a structural element.
    Basically this must be a matrix with 1/0 values only.
    """

    PREDEFINED = {
        'octagon': [[1, 1, 1],
                    [1, 1, 1],
                    [1, 1, 1]],

        'rhombus': [[0, 1, 0],
                    [1, 1, 1],
                    [0, 1, 0]
                   ],

        'diagonal': [[0, 0, 1],
                     [0, 1, 0],
                     [1, 0, 0],
                    ],
        'circle': [[0, 1, 1, 1, 0],
                   [1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1],
                   [0, 1, 1, 1, 0],
                  ],
    }

    def __init__(self, matrix_list, center=None):
        if not all(x in [0, 1] for row in matrix_list for x in row):
            raise TypeError("Structured element should be initialized with a matrix "
                            " containing only zeros and ones")
        elif not all(len(row) == len(matrix_list[0]) for row in matrix_list):
            raise TypeError(
                "Malformed structured element matrix: %r" % matrix_list)
        self.matrix = list(matrix_list)
        if center is None:
            self.center = (len(self.matrix) / 2, len(self.matrix[0]) / 2)
        else:
            self.center = center

    @classmethod
    def predefined(cls, key):
        """
        A factory for predefined structural elements.
        """
        return cls(cls.PREDEFINED[key])

    def get(self, i, j):
        return self.matrix[i][j]

    def get_neighbourhood(self, image, pixel):
        """
        Return the neighbourhood of pixels for a pixel in an image defined by
        the structural element
        """
        res = []
        pi, pj = pixel
        for i, row in enumerate(self.matrix):
            for j, value in enumerate(row):
                ci, cj = self.center
                ni, nj = pi + (ci - i), pj + (cj - j)
                if value and ni < image.height and nj < image.width:
                    # In bounds and covered by structural element.
                    res.append((ni, nj))
        return res
