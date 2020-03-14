import copy, random, sys
sys.path.insert(0,'..')
from lib import analysis, move

class ai():
  """
  Uses a decision tree to choose the best choice looking n moves ahead 
  """

  name="ent"
  author="Yuri"
  comment=""
  depth=1

  def __init__(self,colour):

    self.colour=colour

  def move(self, board):

    dtree=tree(board, self.colour)
    for i in range(self.depth): dtree.populate()
    dec= dtree.decide()
    return dec

class tree():

  def __init__(self,bd,colour):

    self.colour=colour

    #Create nodes with the available moves
    self.moves=[]
    for piece in analysis.getpieces(bd,self.colour):
      for pmove in analysis.possible_moves(bd,piece):
        self.moves.append(node([piece,pmove],move.movepiece(copy.deepcopy(bd),piece,pmove),self.colour))

    #Create nodes for san spawning if homerow is empty
    if all([not i for i in analysis.homerow(bd,self.colour)]):
      for idi,i in enumerate(analysis.homerow(bd,self.colour)):
        sancoords=[idi,5 if self.colour=="b" else 0]
        if not i: self.moves.append(node(sancoords,move.spawnsan(copy.deepcopy(bd),sancoords,self.colour),self.colour))

  def populate(self):

    for n in self.moves:
      n.populate()

  def decide(self):
    """
    Chooses the best available move in the tree.
    """

    scores=[]
    rev=["w","b"].index(self.colour)
    for i in self.moves:
      scores.append([i.process(), i.move])
    scores=sorted(scores, key=lambda x: x[0], reverse=rev)
    #scores=sorted([[i.process(),i.move] for i in self.moves],key=lambda x: x[0], reverse=["w","b"].index(self.colour))
    
    #If there are various moves with the same score, choose a random one
    bs=scores[0][0]
    bestmoves=filter(lambda x: x[0]==bs, scores)
    choice=random.choice(bestmoves)
    return choice[1]

class node():

  def __init__(self,mov,board,colour):

    self.colour=colour
    self.move=mov
    self.board=copy.copy(board)
    self.childs=[]
    self.score=float(0)

  def populate(self):
    """
    populates the node with all the moves <colour> can make on the board
    """

    if not self.childs and analysis.checkgame(self.board)==0:
      #Changes the colour when populating this node to simulate alternating players
      nc="b" if self.colour=="w" else "w"
      for i in analysis.getpieces(self.board,nc):
        for j in analysis.possible_moves(self.board,i):
          self.childs.append(node([i,j],move.movepiece(self.board,i,j),nc))
    else:
      for i in self.childs:
        i.populate()

  def process(self):
    """
    Calculates node score
    """


    if not self.childs:

      #Regular pieces are worth 3, sans are worth 1
      wpieces=analysis.getpieces(self.board,"w")
      wpieces=[analysis.getpiece(self.board,i) for i in wpieces]
      wscore=sum([1 if "san" in i else 3 for i in wpieces])
      bpieces=analysis.getpieces(self.board,"b")
      bpieces=[analysis.getpiece(self.board,i) for i in bpieces]
      bscore=sum([1 if "san" in i else 3 for i in bpieces])
      diff=bscore-wscore
      self.score+=diff*5

      #Also prioritize maximizing number of moves
      bmoves=wmoves=0
      for i in analysis.getpieces(self.board,"b"):
        for j in analysis.possible_moves(self.board,i):
          bmoves+=1
      for i in analysis.getpieces(self.board,"w"):
        for j in analysis.possible_moves(self.board,i):
          wmoves+=1
      movediff=bmoves-wmoves
      self.score+=movediff*2

      #Check if the current node is winning or losing
      outcome=analysis.checkgame(self.board)
      if outcome:
        self.score+=1000*outcome

    else:
      for i in self.childs:
        self.score+=i.process()
      self.score/=len(self.childs)

    return self.score
