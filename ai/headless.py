import random, sys
sys.path.insert(0,'..')
from lib import move

class ai():
  """
  AI that moves pieces at random
  """

  author="Yuri"
  comment=""

  def __init__(self,colour):
    self.colour=colour

  def move(self, board):
    selected=[]
    while 1:
      coords=[random.randrange(6),random.randrange(6)]
      if board[coords[1]][coords[0]].startswith(self.colour):
        avmoves=move.possible_moves(board,coords)
        if avmoves:
          return [coords, random.choice(avmoves)]
