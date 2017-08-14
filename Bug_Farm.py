import pyglet
from pyglet import gl

from shapes import Square, Circle
from bugs import Bug

DEATH_WEIGHT = 30
MIN_BUGS = 1

window = pyglet.window.Window()
keyboard = pyglet.window.key.KeyStateHandler()
window.push_handlers(keyboard)

living_bugs = list()

@window.event
def on_draw():
  gl.glClearColor(0, 0.3, 0.5, 0)
  gl.glClear(gl.GL_COLOR_BUFFER_BIT)

  # Grow (TODO)

  # Update and kill
  for bug in living_bugs:
    bug.update()
    if bug.mass < DEATH_WEIGHT:
      living_bugs.remove(bug)

  # Repopulate
  while len(living_bugs) < MIN_BUGS:
    living_bugs.append(Bug())

  # Draw
  for bug in living_bugs:
    bug.draw()

def update(dummy):
  if keyboard[pyglet.window.key.H]:
    square1.xpos -= 5

def main():
  """ Main function for running world """
  bug = Bug()
  living_bugs.append(bug)
  pyglet.clock.schedule_interval(update,1/10.0)
  pyglet.app.run()


if __name__ == "__main__":
  print 'Running...'
  main()