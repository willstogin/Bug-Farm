import pyglet
from pyglet import gl

from shapes import Square, Circle
from bugs import Bug
from environment import World


class Farm(pyglet.window.Window):
  MIN_BUGS = 1

  def __init__(self):
    super(Farm, self).__init__()

    # Set up window
    self.keyboard = pyglet.window.key.KeyStateHandler()
    self.push_handlers(self.keyboard)

    # Set up environment
    self.living_bugs = []
    
    self.world = World(self.width, self.height)
    print 'width: ', self.width
    print 'height: ', self.height

    # Populate world
    bug = Bug(self.world)
    self.living_bugs.append(bug)

  def run(self):
    # Start simulation
    pyglet.clock.schedule_interval(self.update,1/20.0)
    pyglet.app.run()
    
  def update(self, dummy):
    if self.keyboard[pyglet.window.key.H]:
      print 'Help requested... sorry.'
    if self.keyboard[pyglet.window.key.SPACE]:
      self.living_bugs.append(Bug(self.world))
      
  def on_draw(self):
    #gl.glClearColor(0, 0.3, 0.5, 0)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
  
    # Grow (TODO)
    self.world.update()
    self.world.draw()
  
    # Update and kill
    for bug in self.living_bugs:
      bug.update()
      if not bug.isAlive:
        self.living_bugs.remove(bug)
  
    # Repopulate
    while len(self.living_bugs) < self.MIN_BUGS:
      self.living_bugs.append(Bug(self.world))
  
    # Draw
    for bug in self.living_bugs:
      bug.draw()





def main():
  """ Main function for running world """
  Farm().run()
  


if __name__ == "__main__":
  print 'Running...'
  main()