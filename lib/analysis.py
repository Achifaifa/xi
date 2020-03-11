import copy

def checkgame(board):
  """
  1: black wins
  0: game ongoing
  -1: white wins
  """

  #Check if players have pieces left
  bboard=[[1 for j in i if j.startswith('b')] for i in board]
  bboard=sum([sum(i) for i in bboard])
  if bboard==0: return -1
  wboard=[[1 for j in i if j.startswith('w')] for i in board]
  wboard=sum([sum(i) for i in wboard])
  if wboard==0: return 1

  #Check if there are sans in the last row
  if sum([1 for i in board[0] if i.startswith('b_san')]): return 1
  if sum([1 for i in board[5] if i.startswith('w_san')]): return -1
  
  #Continue normally
  return 0

def possible_moves(board, c):
  """
  returns possible moves for a given piece
  """

  bd=copy.deepcopy(board)

  piece=bd[c[1]][c[0]]
  if piece:
    piececolour,piecetype=piece.split('_')
  else: 
    return []

  #Check adjacent squares for aons
  if piecetype=="aon":
    valid_coords=[[c[0]+1,c[1]],[c[0]-1,c[1]],[c[0],c[1]+1],[c[0],c[1]-1]]

  #Check squares 2 away for khoyors
  elif piecetype=="khoyor":
    valid_coords=[[c[0]+2,c[1]],[c[0]-2,c[1]],[c[0],c[1]+2],[c[0],c[1]-2]]

  #Check diagonal squares for skas
  elif piecetype=="ska":
    valid_coords=[[c[0]+1,c[1]+1],[c[0]-1,c[1]-1],[c[0]+1,c[1]-1],[c[0]-1,c[1]+1]]

  #Chcek square in front and jokes for sans
  elif piecetype=="san":
    if piececolour=='b':
      valid_coords=[[c[0],c[1]-1]]
    if piececolour=='w':
      valid_coords=[[c[0],c[1]+1]]

  #Remove invalid coords
  valid_coords=[i for i in valid_coords if all(j>=0 and j<6 for j in i)]
  valid_coords=[i for i in valid_coords if not bd[i[1]][i[0]].startswith(piececolour)]

  return copy.copy(valid_coords)

def getpiece(board, coords):
  """
  returns the content of the board in a position (Makes AIs cleaner)
  """

  return board[coords[1]][coords[0]]

def checklegal(board,move,colour):

  validmove=validsan=0
  if type(move[0]) is list:
    validmove=move[1] in possible_moves(board,move[0])
  elif type(move[0]) is int:
    row=0 if colour=="w" else 1
    validsan=getpiece(board,move)=="" and move[1]==row
  return validmove or validsan

def getpieces(board,colour):
  """
  returns all picees of a player
  """

  pieces=[]

  for ci,i in enumerate(board):
    for cj,j in enumerate(i):
      if j.startswith(colour): 
        pieces.append([cj,ci])

  return pieces

def homerow(board,colour):

  idx=5 if colour=="b" else 0
  return board[idx]