import pyglet
from pyglet import gl
from math import sqrt, cos, sin, pi

# Use circle verts with tirangle fan to get unit circle
_CIRCLE_POINTS = [0,0]
for i in range(0,101):
  _CIRCLE_POINTS.extend([cos(2*i*pi/100), sin(2*i*pi/100)])
CIRCLE_VERTS = pyglet.graphics.vertex_list(
    102, ('v2f', _CIRCLE_POINTS))


class Square:
  def __init__(self, width, height, xpos, ypos):
    self.xpos = xpos
    self.ypos = ypos
    self.angle = 0
    self.size = 1
    self.rgb = [1,1,1]
    x = width/2.0
    y = height/2.0
    self.vlist = pyglet.graphics.vertex_list(4, ('v2f', [-x,-y, x,-y, -x,y, x,y]))

  def draw(self):
    gl.glPushMatrix()
    gl.glTranslatef(self.xpos, self.ypos, 0)
    gl.glRotatef(self.angle, 0, 0, 1)
    gl.glScalef(self.size, self.size, self.size)
    gl.glColor3f(*self.rgb)
    self.vlist.draw(gl.GL_TRIANGLE_STRIP)
    gl.glPopMatrix()

class Circle:
  def __init__(self, width, height, xpos, ypos):
    self.xpos = xpos
    self.ypos = ypos
    self.angle = 0
    self.size = max(width, height)
    self.rgb = [1,1,1]
    x = width/2.0
    y = height/2.0
    self.vlist = CIRCLE_VERTS

  def draw(self):
    gl.glPushMatrix()
    gl.glTranslatef(self.xpos, self.ypos, 0)
    gl.glRotatef(self.angle, 0, 0, 1)
    gl.glScalef(self.size, self.size, self.size)
    gl.glColor3f(*self.rgb)
    self.vlist.draw(gl.GL_TRIANGLE_FAN)
    gl.glPopMatrix()