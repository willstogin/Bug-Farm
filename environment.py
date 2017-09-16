from random import random
from math import pi
from shapes import draw_square

class World:
  _BOXES_WIDE = 30
  _BOXES_TALL = 15

  def __init__(self, width, height):
    """
      Initializes the background.

      width - Number of pixels wide the world is
      height - Number of pixels tall the world is
    """
    self.width =width
    self.height = height
    self.box_width = width/self._BOXES_WIDE
    print 'box width: ', self.box_width
    self.box_height = height/self._BOXES_TALL

    self.tiles = []
    self.changes = set()
    y = 0
    for i in range(World._BOXES_TALL):
      y += self.box_height
      x = 0
      self.tiles.append([])
      for j in range(World._BOXES_WIDE):
        x += self.box_width
        tile = Tile(self.changes, x, y, self.box_width, self.box_height)
        self.tiles[i].append(tile)

  def draw(self):
    y = 0
    for i in range(World._BOXES_TALL):
      y += self.box_height
      x = 0
      for j in range(World._BOXES_WIDE):
        tile = self.tiles[i][j]
        tile.draw()

  def update(self):
    for tile in self.changes:
      tile.grow()

  def get_tile(self, x, y):
    """
      Gets the tile at location x,y

      Returns Tile instance
    """
    row = int(x/self.box_width)
    col = int(y/self.box_height)

    try:
      return self.tiles[col][row]
    except IndexError:
      return Tile(None, 0,0,0,0, h=0,s=0,v=0)
    
  
_TYPE = 0 
_AMOUNT = 1
_RATE = 2
class Tile:
  """
    Class representing a food-bearing tile

    HUE indicates the type of food being grown
    VAL indicates the growth rate of the food
    SAT indicates the amount of food available
  """

  def __init__(self, change_list, x, y, width, height, h=None, s=None, v=None):
    self.hsv = []
    if h is None:
      self.hsv.append(random())  #hue
    else:
      self.hsv.append(h)
      
    if s is None:
      self.hsv.append(random())  #value
    else:
      self.hsv.append(s)

    if v is None:
      self.hsv.append(random())  #saturation
    else:
      self.hsv.append(v)
      
    self.change_list = change_list
    if change_list is not None:
      change_list.add(self)

    self.x = x
    self.y = y
    self.width = width
    self.height = height

  def draw(self):
    draw_square(self.x, self.y, self.width, self.height, self.hsv)

  def grow(self):
    """ 
      Increases the SAT as indicated by the VAL
    """
    change = self.hsv[_RATE]/15
    self.hsv[_AMOUNT] = min(1, self.hsv[_AMOUNT] + change)
    if self.hsv[2] == 1:
      self.change_list.remove(self)

  def eat(self, amount):
    """
      Removes up to amount of food from the tile.

      returns - how much food is actually eaten. I.e. amount or how much was left.
    """
    food = self.hsv[_AMOUNT] * 7
    eaten = min(amount, food)
    change = eaten/7
    self.hsv[_AMOUNT] -= change


    if (self.change_list is not None 
        and self not in self.change_list):
      self.change_list.add(self)
    return eaten