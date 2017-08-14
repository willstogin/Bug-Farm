import pyglet
from pyglet import gl

from shapes import Square, Circle

window = pyglet.window.Window()
keyboard = pyglet.window.key.KeyStateHandler()
window.push_handlers(keyboard)
square1 = Circle(120, 120, 300, 200)

@window.event
def on_draw():
  gl.glClearColor(0, 0.3, 0.5, 0)
  gl.glClear(gl.GL_COLOR_BUFFER_BIT)
  square1.draw()

def update(dummy):
  if keyboard[pyglet.window.key.A]:
    square1.xpos -= 5
  if keyboard[pyglet.window.key.D]:
    square1.xpos += 5
  if keyboard[pyglet.window.key.W]:
    square1.ypos += 5
  if keyboard[pyglet.window.key.S]:
    square1.ypos -= 5
  if keyboard[pyglet.window.key.UP]:
    square1.size *= 1.1
  if keyboard[pyglet.window.key.DOWN]:
    square1.size /= 1.1
  if keyboard[pyglet.window.key.LEFT]:
    square1.angle += 5
  if keyboard[pyglet.window.key.RIGHT]:
    square1.angle -= 5
  if keyboard[pyglet.window.key.SPACE]:
    square1.rgb = [0,1,0]

def main():
  """ Main function for running world """
  pyglet.clock.schedule_interval(update,1/60.0)
  pyglet.app.run()


if __name__ == "__main__":
  print 'Running...'
  main()