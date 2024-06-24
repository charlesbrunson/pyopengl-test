import pygame
from pygame.locals import *
from OpenGL.GL import *

import affine
from shader import Shader
from pyramid import Pyramid

vertex_shader_src = """#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;
out vec3 ourColor;

uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;

void main() 
{
  gl_Position = projection * view * model * vec4(aPos, 1.0f);
  ourColor = aColor;
}
"""

fragment_shader_src = """#version 330 core

in vec3 ourColor;
out vec3 outputColor;

void main()
{
  outputColor = ourColor;
}
"""

def render(drawable, shader, uniforms):
  glClearColor(0.2, 0.3, 0.3, 1.0)
  glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
  shader.bind()
  for uniform, mat in uniforms.items():
    glUniformMatrix4fv(shader.get_loc(uniform), 1, False, mat)
  drawable.draw()
  shader.unbind()

def main():
  global model_mat
  pygame.init()
  width, height = (800, 600)
  pygame.display.set_mode((width, height), DOUBLEBUF|OPENGL)
  glEnable(GL_DEPTH_TEST)

  shader = Shader(
    vertex_shader_src,
    fragment_shader_src,
    uniforms=['projection', 'model', 'view']
  )

  pyramid = Pyramid()

  counter = 0

  projection_mat = affine.projection(80.0, width/height, 1.0, 10000.0)
  view_mat       = affine.translation(0, 0, -50)

  class Input:
    def __init__(self, key, dir):
      self.key = key
      self.dir = dir
      self.state = False
    
  move = {
    'forward':  Input(pygame.K_w,     ( 0,  0,  1)),
    'backward': Input(pygame.K_s,     ( 0,  0, -1)),
    'right':    Input(pygame.K_d,     ( 1,  0,  0)),
    'left':     Input(pygame.K_a,     (-1,  0,  0)),
    'up':       Input(pygame.K_SPACE, ( 0,  1,  0)),
    'down':     Input(pygame.K_LCTRL, ( 0, -1,  0))
  }

  # hide & lock mouse
  pygame.event.set_grab(True)
  pygame.mouse.set_visible(False)

  while True:
    for event in pygame.event.get():
      if   event.type == pygame.QUIT:
        return
      elif event.type == pygame.KEYDOWN:
        for i in move:
          if event.key == move[i].key:
            move[i].state = True
            continue
        if event.key == pygame.K_ESCAPE:
          return
      elif event.type == pygame.KEYUP:
        for i in move:
          if event.key == move[i].key:
            move[i].state = False
            continue
      elif event.type == pygame.MOUSEMOTION:
          relx, rely = pygame.mouse.get_rel()
          view_mat @= affine.rotatey(relx / 200) @ affine.rotatex(rely / 200)

    for i in move:
      if move[i].state:
        view_mat @= affine.translation(*move[i].dir)

    pyramid.transform.scale  = [10, 10, 10]
    pyramid.transform.rot    = [0, counter/50.0, 0]
    pyramid.transform.pos[0] = 10

    render(
      pyramid,
      shader,
      uniforms={
        'projection': projection_mat,
        'view':       view_mat,
        'model':      pyramid.transform.matrix(),
      }
    )

    counter += 1
    pygame.display.flip()
    pygame.time.wait(10)

try:
  main() 
finally:
  pygame.quit()