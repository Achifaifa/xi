def possible_moves(board, c):
  """
  returns possible moves for a given piece
  """

  piece=board[c[1]][c[0]]
  piececolour,piecetype=piece.split('_')

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
  valid_coords=[i for i in valid_coords if not board[i[1]][i[0]].startswith(piececolour)]

  return valid_coords