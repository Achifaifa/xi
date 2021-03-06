import random, sys
sys.path.insert(0,'..')
from lib import analysis, move

class ai():
  """
  Improved zombie. If no pieces can be taken, it moves and spawns sans first.
  """

  name="smart_zombie"
  author="Yuri"
  comment=""

  def __init__(self,colour):
    self.colour=colour
    self.opcolour="w" if colour=="b" else "b"

  def move(self, board):

    #Define home row
    homerown=5 if self.colour=="b" else 0
    homerow=board[homerown]

    #Get all pieces and sans
    pieces=[]
    sans=[]
    for ci,i in enumerate(board):
      for cj,j in enumerate(i):
        if j.startswith(self.colour): 
          pieces.append([cj,ci])
        if j==(self.colour+"_san"):
          sans.append([cj,ci])

    #Check if a piece can be taken first
    for i in pieces:
      for j in analysis.possible_moves(board,i):
        if analysis.getpiece(board, j).startswith(self.opcolour):
          return [i,j]

    #Check if a san can be moved 
    #Move the most advanced first 
    rev=1 if self.colour=="b" else 0
    sans.sort(key=lambda x: x[1], reverse=rev)
    if sans:
      if analysis.possible_moves(board,sans[0]):
        return(sans[0],analysis.possible_moves(board,sans[0])[0])

    #Spawn san if able before moving at random
    if all([not i for i in analysis.homerow(board,self.colour)]):
      for idi,i in enumerate(homerow):
        if not i:
          return([idi,homerown])

    #Move or spawn
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



