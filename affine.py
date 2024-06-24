import numpy
import math

def scale(sx, sy, sz):
  return numpy.array([
    [sx, 0.0, 0.0, 0.0],
    [0.0, sy, 0.0, 0.0],
    [0.0, 0.0, sz, 0.0],
    [0.0, 0.0, 0.0, 1.0],
  ], dtype=numpy.float32)

def translation(tx, ty, tz):
  return numpy.array([
    [1.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0],
    [ tx,  ty,  tz, 1.0],
  ], dtype=numpy.float32)

def rotatex(ang):
  cos = numpy.cos(ang)
  sin = numpy.sin(ang)
  return numpy.array([
    [1.0, 0.0, 0.0, 0.0],
    [0.0, cos, -sin, 0.0],
    [0.0, sin, cos, 0.0],
    [0.0, 0.0, 0.0, 1.0],
  ], dtype=numpy.float32)

def rotatey(ang):
  cos = numpy.cos(ang)
  sin = numpy.sin(ang)
  return numpy.array([
    [cos, 0.0, sin, 0.0],
    [0.0, 1.0, 0.0, 0.0],
    [-sin, 0.0, cos, 0.0],
    [0.0, 0.0, 0.0, 1.0],
  ], dtype=numpy.float32)

def rotatez(ang):
  cos = numpy.cos(ang)
  sin = numpy.sin(ang)
  return numpy.array([
    [cos, -sin, 0.0, 0.0],
    [sin, cos, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 1.0],
  ], dtype=numpy.float32)

def rotate(xang, yang, zang):
  return rotatex(xang) @ rotatey(yang) @ rotatez(zang)

def identity():
  return numpy.array([
    [1.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 1.0],
  ], dtype=numpy.float32)

def projection(fovy_degrees, ratio, z_near, z_far): 

  tangent = numpy.tan(math.radians(fovy_degrees / 2.0))
  top     = tangent
  right   = top * ratio

  mat = identity()
  mat[0][0] = -1.0 / right
  mat[1][1] = -1.0 / top
  mat[2][2] = -(z_far + z_near) / (z_far - z_near)
  mat[2][3] = -1.0
  mat[3][2] = -(2.0 * z_far * z_near) / (z_far-z_near)
  mat[3][3] = 0.0
  return mat