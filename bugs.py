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

  def __init__(self, mom=None, dad=None):
    """
      Creates a bug from two parents.

      mom - bugs.Bug
      dad - bugs.Bug
    """
    if mom is not None and dad is not None:
      self.brain = brain
      self.x = (mom.x + dad.x)/2
      self.y = (mom.y + dad.y)/2
    else:
      # Default constructor
      self.brain = Brain()
      self.x = 1
      self.y = 1

  def draw(self):
    """
      Draws the Bug.
    """



class Antennae:
  """
    Main sensory organs of a Bug.

    Attributes:
      theta1 - Angle from x+ of first antenna
      theta2 - Angle from x+ of second antenna
      l1 - Length of antenna 1 
      l2 - Length of antenna 2
  """


class Brain:
  """
    Dictates the bug's senses and actions
  """
  def __init__(self, brain1, brain2):
    print 'Warning: brain not yet implemented.'
