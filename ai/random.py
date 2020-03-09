class ai():
  """
  AI that moves pieces at random
  """

  author="Yuri"
  comment=""

  def __init__(self,colour):
    self.colour=colour

  def move(board):
    selected=[]
    while not selected:
      coords=(random.randint(6),random.randint(6))
      if board[coords[1]][coords[0]].startswith(self.colour):
        #get all possible moves
        #pick one of them at random
        selected=[] #chosen coords
    return[coords, selected]
