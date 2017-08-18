from random import random
from math import pi
from shapes import draw_square

class World:
  _BOXES_WIDE = 15
  _BOXES_TALL = 10

  def __init__(self, width, height):
    """
      Initializes the background.

      width - Number of pixels wide the world is
      height - Number of pixels tall the world is
    """
    self.box_width = width/self._BOXES_WIDE
    print 'box width: ', self.box_width
    self.box_height = height/self._BOXES_TALL

    self.tiles = []
    for i in range(World._BOXES_TALL):
      self.tiles.append([])
      for j in range(World._BOXES_WIDE):
        self.tiles[i].append(Tile())

  def update(self):
    pass

  def draw(self):
    y = 0
    for i in range(World._BOXES_TALL):
      y += self.box_height
      x = 0
      for j in range(World._BOXES_WIDE):
        x += self.box_width
        tile = self.tiles[i][j]
        draw_square(x, y, self.box_width, self.box_height, tile.hsv)

  def get_tile(self, x, y):
    """
      Gets the tile at location x,y

      Returns Tile instance
    """
    row = int(x/self.box_width)
    col = int(y/self.box_height)

    return self.tiles[col][row]
  
class Tile:
  def __init__(self):
    self.hsv = []
    self.hsv.append(random())  #hue
    self.hsv.append(random())  #value
    self.hsv.append(random())  #saturation