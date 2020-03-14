import random, sys
sys.path.insert(0,'..')
from lib import analysis, move

class ai():
  """
  AI that moves pieces and spawns sans at random.
  Whenever there is a chance to take a piece, it does so.
  """

  name="zombie"
  author="Yuri"
  comment=""

  def __init__(self,colour):
    self.colour=colour
    self.opcolour="w" if colour=="b" else "b"

  def move(self, board):

    pieces=[]
    #Check if a piece can be taken first
    for ci,i in enumerate(board):
      for cj,j in enumerate(i):
        if j.startswith(self.colour): pieces.append([cj,ci])
    for i in pieces:
      for j in analysis.possible_moves(board,i):
        if analysis.getpiece(board, j).startswith(self.opcolour):
          return [i,j]

    #Move or spawn at random
    while 1:
      coords=[random.randrange(6),random.randrange(6)]
      if analysis.getpiece(board,coords).startswith(self.colour):
        avmoves=analysis.possible_moves(board,coords)
        if avmoves:
          for i in avmoves:
            piece=analysis.getpiece(board,i)
            if piece and not piece.startswith(self.colour):
              return [coords, i]
          return [coords, random.choice(avmoves)]
      if ((self.colour=="b" and coords[1]==5) or (self.colour=="w" and coords[1]==0)) \
        and analysis.getpiece(board,coords)=="" \
        and all([not i for i in analysis.homerow(board,self.colour)]):
        return coords


