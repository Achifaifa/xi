import random, sys
# Uncomment the next lines to use additional functions
#sys.path.insert(0,'..')
#from lib import analysis, move

class ai():
  """
  Description of the general strategy the AI follows and implementation details
  """

  #Comment is optional, but may not be in the future
  name=""
  author=""
  comment=""

  #Doesn't have to return anything
  def __init__(self,colour):
    self.colour=colour

  #move() must return either a move [[a1,a2][b1,b2]] or coordinates to spawn a san in [a1,a2]
  #make sure the move is legal before returning with analysis.checklegal()
  def move(self, board):
    pass
