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
            #print(self.structuralElement)
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
        it = 0
        result = original.copy()

        changed = True
        while changed:
            if it == self.ITERATIONS_LIMIT:
                print '%s: hit iteration limit (%d)' % (self.__class__, it)
                break
            it += 1
            changed = False

            for order_name, order in (('raster', lambda x: x),
                                      ('antiraster', reversed)):
                for i in order(xrange(result.height)):
                    for j in order(xrange(result.width)):
                        old = result[i][j]
                        result[i][j] = self.compute_pixel(
                            (i,j), result, order_name)
                        if old != result[i][j]:
                            changed = True

        if not changed:
            print '%s: Stability reached.' % self.__class__
        print '%s: took %s iterations.' % (self.__class__, it)
        return result

    def compute_pixel(self, px, image, order_name):
        offsets = self.structuralElement.offsets[order_name]
        pi, pj = px
        region = ((pi+i, pj+j) for i,j in offsets \
                  if pi+i<image.height and pj+j<image.width)
        if not region:
            return 0
        return min(max(image[i][j] for i,j in region), self.mask[pi][pj])


class OpeningByReconstruction(MorphologicalOperator):
    """
    TBD
    """
    pass


class AreaOpening(MorphologicalOperator):
    """
    Area opening operator.
    The same as standard morphological opening, but the connected components must have
    area that is smaller than some initially defined value.
    """

    def __init__(self, structuralElement, area, diffThreshold):
        self.structuralElement = structuralElement
        self.area = area
        self.diffThreshold = diffThreshold
        
    def __call__(self, original):
        if original.mode != 'grayscale':
            raise TypeError('%s only works on grayscale images' % self.__class__)
        result = []
        image = original.copy()
        
        opening = Opening(self.structuralElement)
        openedImage = opening(image)

        diffImage = self.__get_difference(image, openedImage)
        
        return diffImage
        

        
    def __get_difference(self, original, new):
        assert original.height == new.height, 'The height of the original image does not correspong to the height of the new image'
        assert original.width == new.width, 'The width of the original image does not correspong to the width of the new image'

        print 'Original image height: %d, width: %d' % (original.height, original.width)

        result = []
        
        #for row in xrange(original.height):
        #    result.append(
        #        map(self.__computeThreshold, [(abs(original[row][col] - new[row][col])) for col in xrange(original.width) ]))

        for i in xrange(original.height):
            row = []
            for j in xrange(original.width):
                diff = abs(original[i][j] - new[i][j])
                
                if diff > self.diffThreshold:
                    row.append(255)
                    #print (diff)
                else:
                    row.append(0)
            result.append(row)

        assert len(result)==original.height, 'Wrong height'
        assert len(result[0])==original.width, 'Wrong width'
        
        return original.__class__(data=result, width=original.width, height=original.height)


    def __computeThreshold(self, value):
        if value > self.diffThreshold:
            return value
        else:
            return 0


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

    #The order of the classes mathers. For example [Erosion, Dilation] would give morphological opening
    #but [Dilation, Erosion] would give morphological closing
    operationsList = [Erosion, Dilation]
    
    def __init__(self, structuralElement):
        self.structuralElement = structuralElement 


class Closing(ComposedMorphologicalOperator):
    """
    Opening operator. Basically, this is a dilation followed by an erosion
    """

    #The order of the classes mathers. For example [Erosion, Dilation] would give morphological opening
    #but [Dilation, Erosion] would give morphological closing
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
        'diagonal5': [[1, 0, 0, 0, 0],
                      [0, 1, 0, 0, 0],
                      [0, 0, 1, 0, 0],
                      [0, 0, 0, 1, 0],
                      [0, 0, 0, 0, 1],],
        'circle': [[0, 1, 1, 1, 0],
                   [1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1],
                   [0, 1, 1, 1, 0],
                  ],
        'big_circle': [[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                       [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                       [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                       [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                       [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                       [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                       [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                       [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                       [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                       [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],],
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
        ci, cj = self.center
        self.ones_offsets = set((i - ci, j - cj) for i in xrange(self.height) \
                                for j in xrange(self.width) \
                                if self.get(i, j))
        self.offsets = {
            'raster':     frozenset(
                (i,j) for i,j in self.ones_offsets if i<0 or (i==0 and j<=0)),
            'antiraster': frozenset(
                (i,j) for i,j in self.ones_offsets if i>0 or (i==0 and j>=0)),
        }

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

    @property
    def height(self):
        return len(self.matrix)

    @property
    def width(self):
        return len(self.matrix[0])


class SquaredStructuralElementBuilder(object):
    """
    Used to build squared structural elements of specific size
    """
    def __init__(self, size):
        self.size = size

    def get_struct_elem(self):
        structElem = []
        row = []
        
        for x in xrange(self.size):
            row.append(1)
        for y in xrange(self.size):
            structElem.append(row)

        return StructuralElement(structElem)















    
