# distutils: language = c++
# distutils: sources = ./pybug/rasterize/matlabcpp/MM3DRenderer.cpp ./pybug/rasterize/matlabcpp/GLRFramework.cpp
# distutils: libraries = GLU GL glut GLEW
from libcpp.vector cimport vector
from libc.stdint cimport uint8_t
from libcpp cimport bool
import numpy as np
cimport numpy as np


# externally declare the C++ classes
cdef extern from "./matlabcpp/MM3DRenderer.h":

    cdef cppclass MM3DRenderer:
        MM3DRenderer(double* tpsCoord_in, float* coord_in, size_t numCoords_in,
                     unsigned int* coordIndex_in, size_t numTriangles_in,
                     float* texCoord_in, uint8_t* textureImage_in,
                     size_t textureWidth_in, size_t textureHeight_in,
                     bool INTERACTIVE_MODE)
        void returnFBPixels(int argc, char **argv, uint8_t* pixels,
                            float* coords, int width,
                            int height)


cdef class OpenGLRasterizer:
    cdef MM3DRenderer* thisptr
    cdef unsigned t_width
    cdef unsigned t_height
    cdef unsigned n_coords

    def __cinit__(self,
                  np.ndarray[double, ndim=2, mode="c"] tpsCoords not None ,
                  np.ndarray[float, ndim=2, mode="c"] coords not None,
                  np.ndarray[unsigned, ndim=2, mode="c"] trilist not None,
                  np.ndarray[float, ndim=2, mode="c"] tcoords not None,
                  np.ndarray[uint8_t, ndim=3, mode="c"] texture not None):
        self.thisptr = new MM3DRenderer(&tpsCoords[0,0], &coords[0,0],
                                         coords.shape[0], &trilist[0,0],
                                         trilist.shape[0],
                                         &tcoords[0,0], &texture[0,0,0],
                                         texture.shape[0], texture.shape[1],
                                         False)
        self.t_width = texture.shape[0]
        self.t_height = texture.shape[1]
        self.n_coords = coords.shape[0]

    def __dealloc__(self):
        print "Is this going to cause an issue?\n"
        del self.thisptr

    @property
    def pixels(self):
        # cdef np.ndarray[uint8_t, ndim=3, mode='c'] pixels = \
        #     np.empty((self.t_width, self.t_height, 4), dtype=np.uint8)
        cdef np.ndarray[uint8_t, ndim=1, mode='c'] pixels = \
             np.empty((self.t_width * self.t_height * 4), dtype=np.uint8)
        cdef np.ndarray[float, ndim=3, mode='c'] coords = \
            np.empty((self.t_width, self.t_height, 3), dtype=np.float32)
        print self.t_width
        print self.t_height
        cdef pystring = 'hello'.encode('UTF-8')
        cdef char* b = pystring
        self.thisptr.returnFBPixels(1, &b, &pixels[0], &coords[0,0,0],
                                    self.t_width, self.t_height)
        return pixels, coords
