import pyglet
from pyglet import gl
from math import sqrt, cos, sin, pi

# Use circle verts with tirangle fan to get unit circle
_CIRCLE_POINTS = [0,0]
for i in range(0,101):
  _CIRCLE_POINTS.extend([cos(2*i*pi/100), sin(2*i*pi/100)])
CIRCLE_VERTS = pyglet.graphics.vertex_list(
    102, ('v2f', _CIRCLE_POINTS))
SQUARE_VERTS = pyglet.graphics.vertex_list(4, ('v2f', [-1,-1, 1,-1, -1,1, 1,1]))


class Square:
  vlist = pyglet.graphics.vertex_list(4, ('v2f', [-1,-1, 1,-1, -1,1, 1,1]))
  def __init__(self, width, height, xpos, ypos):
    self.xpos = xpos
    self.ypos = ypos
    self.width = width
    self.height = height
    self.angle = 0
    self.rgb = [1,1,1]

  def draw(self):
    gl.glPushMatrix()
    gl.glTranslatef(self.xpos, self.ypos, 0)
    gl.glRotatef(self.angle, 0, 0, 1)
    gl.glScalef(self.size, self.size, self.size)
    gl.glColor3f(*self.rgb)
    self.vlist.draw(gl.GL_TRIANGLE_STRIP)
    gl.glPopMatrix()

class Circle:
  def __init__(self, xpos, ypos, scale=1):
    self.xpos = xpos
    self.ypos = ypos
    self.angle = 0
    self.size = scale
    self.rgb = [1,1,1]
    self.vlist = CIRCLE_VERTS

  def draw(self):
    gl.glPushMatrix()
    gl.glTranslatef(self.xpos, self.ypos, 0)
    gl.glRotatef(self.angle, 0, 0, 1)
    gl.glScalef(self.size, self.size, self.size)
    gl.glColor3f(*self.rgb)
    self.vlist.draw(gl.GL_TRIANGLE_FAN)
    gl.glPopMatrix()


def draw_square(xpos, ypos, height, width, rgb):
  gl.glPushMatrix()
  gl.glTranslatef(xpos, ypos, 0)
  gl.glScalef(height, width, 1)
  gl.glColor3f(*rgb)
  SQUARE_VERTS.draw(gl.GL_TRIANGLE_STRIP)
  gl.glPopMatrix()

def draw_circle(xpos, ypos, size, rgb):
  gl.glPushMatrix()
  gl.glTranslatef(xpos, ypos, 0)
  gl.glScalef(size, size, size)
  gl.glColor3f(*rgb)
  CIRCLE_VERTS.draw(gl.GL_TRIANGLE_FAN)
  gl.glPopMatrix()

def draw_line(x1, y1, x2, y2, rgb):
    vlist = pyglet.graphics.vertex_list(2, ('v2f', [x1,y1,x2,y2]))
    gl.glColor3f(*rgb)
    vlist.draw(gl.GL_LINES)
