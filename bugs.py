import shapes
from pyglet import gl
from math import cos, sin, pi
from numpy import exp, array, random, dot
from random import random, randrange

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
      isDead - True if alive


    Methods:
      __init__(mom, dad) - Creates a bug from the two
        parent bugs.
      draw() - Draws the bug as it is at the moment
  """
  DEATH_WEIGHT = 15
  MAX_TURN_SPEED = pi/4
  MAX_MOVEMENT_SPEED = 50
  SCALE = .5

  def __init__(self, environment, mom=None, dad=None, name='TODO'):
    """
      Creates a bug from two parents.

      mom - bugs.Bug
      dad - bugs.Bug
    """
    if mom is None or dad is None:
      # Default constructor
      print 'Constructing default bug.'
      self.brain = Brain()
      self.x = 300
      self.y = 200
      self.brain = Brain()
      self.turn_speed = random() * self.MAX_TURN_SPEED
      self.direction = random() * 2*pi
      self.move_speed = random() * self.MAX_MOVEMENT_SPEED
      self.name = name
      self.antennae = Antennae()
      self.color = [random(),random(),random()]
    else:
      # Inherited constructor
      self.brain = brain
      self.x = (mom.x + dad.x)/2
      self.y = (mom.y + dad.y)/2

      self.brain = Brain(mom.brain, dad.brain)
      name = 'TODO'
      antennae = Antennae(mom.antennae, dad.antennae)
      self.color = [0,1,0]
      
    self.mass = 60
    self.age = 0
    self.isAlive = True
    self.environment = environment

  def update(self):
    self.age += 1
    self.mass -= 1
    self.isAlive = (self.mass > self.DEATH_WEIGHT)

    if self.isAlive:
      # Do living things now
      action = self.brain.decide()
      if action[0]:
        # Eat
        try:
          tile = self.environment.get_tile(self.x, self.y)
          self.mass += tile.eat(9)
        except IndexError:
          print 'Error: bug offscreen trying to eat.'

      if action[1]:
        # Move forward
        self.x += cos(self.direction)*self.move_speed
        self.y += sin(self.direction)*self.move_speed

        self.mass -= self.move_speed
      if action[2]:
        # Turn
        self.direction += self.turn_speed

    else:
      # Do dying things now
      pass

  def draw(self):
    """
      Draws the Bug.
    """
    gl.glPushMatrix()
    gl.glTranslatef(self.x, self.y, 0)
    gl.glRotatef(self.direction*180/pi, 0, 0, 1)
    gl.glScalef(self.SCALE, self.SCALE, 1)
    shapes.draw_circle(0, 0, self.mass, self.color)
    self.antennae.draw(0,0)
    gl.glPopMatrix()




class Antennae:
  """
    Main sensory organs of a Bug.

    Attributes:
      theta1 - Angle from x+ of first antenna (radians)
      theta2 - Angle from x+ of second antenna (radians)
      l1 - Length of antenna 1 
      l2 - Length of antenna 2
  """
  _MAX_LENGTH = 160
  _MIN_LENGTH = 20

  def __init__(self, antenae1=None, antenae2=None):
    if antenae1 is None or antenae2 is None:
      self.theta1 = 2*pi*random()
      self.theta2 = 2*pi*random()
        
      self.l1 = randrange(Antennae._MIN_LENGTH, Antennae._MAX_LENGTH)
      self.l2 = randrange(Antennae._MIN_LENGTH, Antennae._MAX_LENGTH)
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

    Senses that can be detected at any antenna 
    point or under the center of the bug:
      HSV at location
      Is another bug there?

    Internal senses that are not location dependent:
      Mass
      
    Actions:
      Eat
      Move forward
      Turn
  """
  def __init__(self, brain1=None, brain2=None):
    if brain1 is None or brain2 is None:
      pass
    else:
      print 'Warning: brain inheritance not yet implemented'

  def decide(self):
    return (1,1,1)
