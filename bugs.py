import shapes
from environment import Tile
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
  MAX_EATING = 10
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
      self.x = environment.width/2
      self.y = environment.height/2
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
    try:
      tile = self.environment.get_tile(self.x, self.y)
    except IndexError:
      tile = Tile(h=0, s=0, v=0)


    if self.isAlive:
      # Do living things now
      action = self.brain.decide(tile.hsv[0],
                                 tile.hsv[1],
                                 tile.hsv[2],
                                 self.mass)
      if True: #action[0] > .5:
        # Eat
        self.mass += tile.eat(action[0]*self.MAX_EATING)

      if True: #action[1] > 1:
        # Move forward
        speed = self.move_speed*action[1]
        self.x = min(max(self.x + cos(self.direction)*speed, 0), self.environment.width)
        self.y = min(max(self.y + sin(self.direction)*speed,0), self.environment.height)


        self.mass -= .1*speed * .05*self.mass
      if action[2]:
        # Turn
        self.direction += action[2] * self.turn_speed

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
    Neural net method taken from https://medium.com/technology-invention-and-more/how-to-build-a-simple-neural-network-in-9-lines-of-python-code-cc8f23647ca1

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
      self.layer1 = []
      
      self.layer1.append([random(), random(), random(), random()])
      self.layer1.append([random(), random(), random(), random()])
      self.layer1.append([random(), random(), random(), random()])
      self.layer1.append([random(), random(), random(), random()])

      self.layer2 = []
      self.layer2.append([random(), random(), random(), random()])
      self.layer2.append([random(), random(), random(), random()])
      self.layer2.append([random(), random(), random(), random()])
    else:
      print 'Warning: brain inheritance not yet implemented'

  def decide(self, h, s, v, mass):
    inputs = [h,s,v,mass]

    outs1 = [self.__tanh(dot(inputs, self.layer1[0])),
             self.__tanh(dot(inputs, self.layer1[0])),
             self.__tanh(dot(inputs, self.layer1[0])),
             self.__tanh(dot(inputs, self.layer1[0]))]


    return (self.__tanh(dot(outs1,self.layer2[0])),
            self.__tanh(dot(outs1,self.layer2[1])),
            self.__tanh(dot(outs1,self.layer2[2])))

  # The Sigmoid function, which describes an S shaped curve.
  # We pass the weighted sum of the inputs through this function to
  # normalise them between 0 and 1.
  def __sigmoid(self, x):
    return 1 / (1 + exp(-x))
  
  # The derivative of the Sigmoid function.
  # This is the gradient of the Sigmoid curve.
  # It indicates how confident we are about the existing weight.
  def __sigmoid_derivative(self, x):
    return x * (1 - x)

  def __tanh(self,x):
    return (exp(x) - exp(-x)) / (exp(x) + exp(-x))