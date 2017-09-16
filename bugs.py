import shapes
from environment import Tile
from pyglet import gl
from math import cos, sin, pi, fabs
from numpy import exp, array, random, dot
from random import random, randrange
import math


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
  MAX_MASS = 100
  MAX_EATING = 10
  SCALE = .5

  def __init__(self, environment, mating, mom=None, dad=None, name='TODO'):
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
      self.turn_speed = random() * self.MAX_TURN_SPEED
      self.direction = random() * 2*pi
      self.move_speed = random() * self.MAX_MOVEMENT_SPEED
      self.name = name
      self.antennae = Antennae()
      self.color = [random(),random(),random()]
    else:
      # Inherited constructor
      self.brain = Brain(mom.brain, dad.brain)
      self.x = (mom.x + dad.x)/2
      self.y = (mom.y + dad.y)/2

      # TODO make these inherited
      self.turn_speed = (mom.turn_speed + dad.turn_speed)/2
      self.direction = (mom.direction + dad.direction)/2
      self.move_speed = (mom.move_speed + dad.move_speed)/2


      self.name = 'TODO'
      self.antennae = Antennae(mom.antennae, dad.antennae)
      self.color = [(mom.color[0] + dad.color[0])/2,
                    (mom.color[1] + dad.color[1])/2,
                    (mom.color[2] + dad.color[2])/2]
      
    self.mass = 60
    self.age = 0
    self.isAlive = True
    self.environment = environment
    self.mates = mating

  def update(self):
    self.age += 1
    self.mass -= 1
    self.isAlive = (self.mass > self.DEATH_WEIGHT)
    try:
      tile = self.environment.get_tile(self.x, self.y)
      (tile_a1, tile_a2) = self.antennae.sense(self.x, self.y, self.environment)
    except IndexError:
      tile = Tile(h=0, s=0, v=0)


    if self.isAlive:
      # Do living things now
      action = self.brain.decide(tile.hsv[0],
                                 tile.hsv[1],
                                 tile.hsv[2],
                                 self.mass,
                                 tile_a1.hsv[0],
                                 tile_a1.hsv[1],
                                 tile_a1.hsv[2],
                                 tile_a2.hsv[0],
                                 tile_a2.hsv[1],
                                 tile_a2.hsv[2],)
      eat_weight = action[0] #min(max(action[0], 1), -1)
      move_weight = action[1] #min(max(action[1], 1), -1)
      turn_weight = action[2] #min(max(action[2], 1), -1)
      mate_weight = action[3] #min(max(action[3], 1), -1)
      if action == 0 or True:
        # Eat 
        print 'eating'
        self.mass += tile.eat(fabs(eat_weight)*self.MAX_EATING)

      speed = 0
      if action == 1 or True:
        # Move forward
        print 'move'
        speed = self.move_speed*move_weight

      self.x += cos(self.direction)*speed
      self.y += sin(self.direction)*speed
      # Keep in bounds
      self.x = min(max(self.x,0), self.environment.width)
      self.y = min(max(self.y,0), self.environment.height)

      self.mass -= .05*speed * .05*self.mass

      if action == 2 or True:
        # Turn
        print 'turn'
        self.direction += self.turn_speed * turn_weight

      if mate_weight > 0 and self.mass > 50:
        #self.mates.add(self)
        print 'mate'
        self.mates.add(self)
      else:
        self.mates.discard(self)

    else:
      # Do dying things now
      pass

    self.mass = min(self.mass, self.MAX_MASS)

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

  def mate(self):
    self.mass -= 30



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
      # TODO: make a little random
      self.theta1 = (antenae1.theta1 + antenae2.theta1)/2
      self.theta2 = (antenae1.theta2 + antenae2.theta2)/2

      self.l1 = (antenae1.l1 + antenae2.l1)/2
      self.l2 = (antenae1.l2 + antenae2.l2)/2

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

  def sense(self, origx, origy, env):
    x = origx + self.l1*cos(self.theta1)
    y = origy + self.l1*sin(self.theta1)
    t1 = env.get_tile(x,y)
    
    x = origx + self.l2*cos(self.theta2)
    y = origy + self.l2*sin(self.theta2)
    t2 = env.get_tile(x,y)
    return (t1, t2)




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
      Mate
  """
  
  counter = 0
  inc = .01
  def __init__(self, brain1=None, brain2=None):
    counter = Brain.counter
    inc = Brain.inc
    if brain1 is None or brain2 is None:
      self.layertest = []
      self.layertest.append([myrand(), myrand(), myrand(), 0, myrand(), myrand(), myrand(), myrand(), myrand(), myrand()])
      self.layertest.append([myrand(), myrand(), myrand(), 0, myrand(), myrand(), myrand(), myrand(), myrand(), myrand()])
      self.layertest.append([myrand(), myrand(), myrand(), 0, myrand(), myrand(), myrand(), myrand(), myrand(), myrand()])
      self.layertest.append([myrand(), myrand(), myrand(), 0, myrand(), myrand(), myrand(), myrand(), myrand(), myrand()])
      self.layertest.append([myrand(), myrand(), myrand(), 0, myrand(), myrand(), myrand(), myrand(), myrand(), myrand()])
      self.layertest.append([myrand(), myrand(), myrand(), 0, myrand(), myrand(), myrand(), myrand(), myrand(), myrand()])
      self.layertest.append([myrand(), myrand(), myrand(), 0, myrand(), myrand(), myrand(), myrand(), myrand(), myrand()])

      self.layer2 = []
      self.layer2.append([myrand(),myrand(),myrand(),myrand(),myrand(),myrand(),myrand()])
      self.layer2.append([myrand(),myrand(),myrand(),myrand(),myrand(),myrand(),myrand()])
      self.layer2.append([myrand(),myrand(),myrand(),myrand(),myrand(),myrand(),myrand()])
      self.layer2.append([myrand(),myrand(),myrand(),myrand(),myrand(),myrand(),myrand()])


    else:
      self.layertest = []
      self.layertest.append([myrand(), myrand(), myrand(), 0, myrand(), myrand(), myrand(), myrand(), myrand(), myrand()])
      self.layertest.append([myrand(), myrand(), myrand(), 0, myrand(), myrand(), myrand(), myrand(), myrand(), myrand()])
      self.layertest.append([myrand(), myrand(), myrand(), 0, myrand(), myrand(), myrand(), myrand(), myrand(), myrand()])
      self.layertest.append([myrand(), myrand(), myrand(), 0, myrand(), myrand(), myrand(), myrand(), myrand(), myrand()])
      self.layertest.append([myrand(), myrand(), myrand(), 0, myrand(), myrand(), myrand(), myrand(), myrand(), myrand()])
      self.layertest.append([myrand(), myrand(), myrand(), 0, myrand(), myrand(), myrand(), myrand(), myrand(), myrand()])
      self.layertest.append([myrand(), myrand(), myrand(), 0, myrand(), myrand(), myrand(), myrand(), myrand(), myrand()])

      self.layer2 = []
      self.layer2.append([myrand(),myrand(),myrand(),myrand(),myrand(),myrand(),myrand()])
      self.layer2.append([myrand(),myrand(),myrand(),myrand(),myrand(),myrand(),myrand()])
      self.layer2.append([myrand(),myrand(),myrand(),myrand(),myrand(),myrand(),myrand()])
      self.layer2.append([myrand(),myrand(),myrand(),myrand(),myrand(),myrand(),myrand()])
      print 'Warning: brain inheritance not yet implemented'

  def decide(self, h, s, v, mass, ah1, as1, av1, ah2, as2, av2):
    inputs = [h,s,v,mass, ah1, as1, av1, ah2, as2, av2]

    layer1 = [self.__activation(inputs,self.layertest[0]),
                 self.__activation(inputs,self.layertest[1]),
                 self.__activation(inputs,self.layertest[2]),
                 self.__activation(inputs,self.layertest[3]),
                 self.__activation(inputs,self.layertest[4]),
                 self.__activation(inputs,self.layertest[5]),
                 self.__activation(inputs,self.layertest[6])]

    layer2 = [self.__activation(layer1, self.layer2[0]),
              self.__activation(layer1, self.layer2[1]),
              self.__activation(layer1, self.layer2[2]),
              self.__activation(layer1, self.layer2[3])]


    decisions = layer2
    _max = max([abs(i) for i in decisions])
    decisions = [i/_max for i in decisions]


    return decisions#.index(max(decisions))

  def __activation(self, inputs, weights):
    dot_out = dot(inputs, weights)
    out = dot_out
    return out

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

  def __softmax(self, values ):
    values_exp = [math.exp(val) for val in values]
    sum_exps = sum(values_exp)
    result = [round(i / sum_exps, 3) for i in values_exp]
    return result


def myrand():
  return 2*random() - 1

