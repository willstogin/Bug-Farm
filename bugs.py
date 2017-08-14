import shapes
from math import cos, sin, pi

class Bug:
  """
    The first creature for our farm.

    Attributes:
      x - float position of the bug
      y - float position of the bug
      brain - bugs.Brain
      name - Name inherited from parents' names
      antennae - bugs.Antenna
      mass - Amount of substance to the bug
      age - Number of ticks since birth
      color - (r,g,b) value of bug (may determine diet in the future)


    Methods:
      __init__(mom, dad) - Creates a bug from the two
        parent bugs.
      draw() - Draws the bug as it is at the moment
  """

  def __init__(self, mom=None, dad=None, name='TODO'):
    """
      Creates a bug from two parents.

      mom - bugs.Bug
      dad - bugs.Bug
    """
    if mom is not None and dad is not None:
      self.brain = brain
      self.x = (mom.x + dad.x)/2
      self.y = (mom.y + dad.y)/2

      self.brain = Brain(mom.brain, dad.brain)
      name = 'TODO'
      antennae = Antennae(mom.antennae, dad.antennae)
    else:
      # Default constructor
      print 'Constructing default bug.'
      self.brain = Brain()
      self.x = 300
      self.y = 200
      self.brain = Brain()
      self.name = name
      self.antennae = Antennae()
    
    self.color = [0,1,0]
    self.mass = 60
    self.age = 0

  def update(self):
    self.age += 1
    self.mass -= 1

  def draw(self):
    """
      Draws the Bug.
    """
    shapes.draw_circle(self.x, self.y, self.mass, self.color)
    self.antennae.draw(self.x, self.y)




class Antennae:
  """
    Main sensory organs of a Bug.

    Attributes:
      theta1 - Angle from x+ of first antenna (radians)
      theta2 - Angle from x+ of second antenna (radians)
      l1 - Length of antenna 1 
      l2 - Length of antenna 2
  """
  def __init__(self, antenae1=None, antenae2=None):
    if antenae1 is None or antenae2 is None:
      self.theta1 = pi/8
      self.theta2 = -pi/8
        
      self.l1 = 80
      self.l2 = 80
    else:
      print 'Warning: antennae inheritance not implemented'

  def draw(self, origx, origy):
    x = origx + self.l1*cos(self.theta1)
    y = origy + self.l1*sin(self.theta1)
    shapes.draw_circle(x,
                       y,
                       10,
                       [0,0,0])
    shapes.draw_line(origx, origy, x, y, [0,0,0])
    
    x = origx + self.l2*cos(self.theta2)
    y = origy + self.l2*sin(self.theta2)
    shapes.draw_circle(x,
                       y,
                       10,
                       [0,0,0])
    shapes.draw_line(origx, origy, x, y, [0,0,0])



class Brain:
  """
    Dictates the bug's senses and actions
  """
  def __init__(self, brain1=None, brain2=None):
    print 'Warning: brain not yet implemented.'
