from OpenGL.GL import *

class Shader:
  def __init__(self, vert_src, frag_src, uniforms):
    vertShader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertShader, vert_src)
    glCompileShader(vertShader)
    result = glGetShaderiv(vertShader, GL_COMPILE_STATUS)
    if not(result):
      raise RuntimeError(glGetShaderInfoLog(vertShader))

    fragShader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragShader, frag_src)
    glCompileShader(fragShader)
    result = glGetShaderiv(fragShader, GL_COMPILE_STATUS)
    if not(result):
      raise RuntimeError(glGetShaderInfoLog(fragShader))

    self.program_id = glCreateProgram();
    glAttachShader(self.program_id, vertShader)
    glAttachShader(self.program_id, fragShader)
    glLinkProgram(self.program_id)
    result = glGetProgramiv(self.program_id, GL_LINK_STATUS)
    if not(result):
      raise RuntimeError(glGetProgramInfoLog(self.program_id))

    self.uniforms = {uniform_name: glGetUniformLocation(self.program_id, uniform_name) for uniform_name in uniforms }

    glDeleteShader(vertShader)
    glDeleteShader(fragShader)

  def bind(self):
    glUseProgram(self.program_id)

  def unbind(self):
    glUseProgram(0)

  def get_loc(self, uniform_name):
    return self.uniforms[uniform_name]
