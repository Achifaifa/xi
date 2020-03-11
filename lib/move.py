import copy

def move(board,mov,c):
  tm=type(mov[0])
  if tm is int: 
    return spawnsan(board,mov,c)
  if tm is list:
    return movepiece(board,*mov)

def movepiece(board,a,b):
  "Moves whatever is in A to B"
  tb=copy.copy(board)
  tb[a[1]][a[0]], tb[b[1]][b[0]]="", tb[a[1]][a[0]]
  return tb

def spawnsan(board,a,c):
  "Spawns a san of colour c in A"
  tb=copy.copy(board)
  tb[a[1]][a[0]]=c+"_san"
  return tb