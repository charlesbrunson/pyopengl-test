
import numpy
from OpenGL.GL import *

from transform import Transform

class Pyramid:
  vertices = numpy.array([
    [ 0.0, -0.5,  0.0, 1.0, 0.0, 0.0],
    [ 0.5,  0.5,  0.5, 1.0, 1.0, 0.0], 
    [-0.5,  0.5,  0.5, 0.0, 0.0, 1.0],
    [-0.5,  0.5, -0.5, 0.0, 1.0, 0.0],
    [ 0.5,  0.5, -0.5, 1.0, 0.0, 1.0], 
  ], dtype=numpy.float32)

  elements = numpy.array([
    0, 1, 2, # front
    0, 1, 4, # right
    0, 3, 2, # left
    0, 3, 4, # back
    1, 2, 3, # bottom 1
    3, 4, 1, # bottom 2
  ], dtype=numpy.ubyte)

  def __init__(self):

    self.transform = Transform()

    self.vao = glGenVertexArrays(1)
    glBindVertexArray(self.vao)

    self.vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
    glBufferData(GL_ARRAY_BUFFER, Pyramid.vertices, GL_STATIC_DRAW)

    self.ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, Pyramid.elements, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(0, 3, GL_FLOAT, False, 6*4, ctypes.c_void_p(0)) # position
    glVertexAttribPointer(1, 3, GL_FLOAT, False, 6*4, ctypes.c_void_p(3*4))  # color

    glBindVertexArray(0)
    glDisableVertexAttribArray(0)
    glDisableVertexAttribArray(1)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

  def draw(self):
    glBindVertexArray(self.vao)
    glDrawElements(GL_TRIANGLES, 18, GL_UNSIGNED_BYTE, ctypes.c_void_p(0))
    glBindVertexArray(0)