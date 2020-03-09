import copy, os
import pygame
from pygame import Surface

debug=1

if debug: print "Starting Xi..."
#Config
size=600
wsize=(size,size)
selected=""
moves=[]
bestcolour=(250,186,218,8)
valid_coords=[]

#Pygame stuff
if debug: print "Initializing pygame...",
pygame.init()
pygame.font.init()
screen=pygame.display.set_mode(wsize)
pygame.display.set_caption('Xi')
clock=pygame.time.Clock()
if debug: print "  [OK]"

#Load resources
if debug: print "Loading resources...",
cellsize=size/6
for i in os.listdir('img'):
  name=i.replace('.png','')
  imgsize=",(%i,%i))"%(cellsize,cellsize)
  exec(name+'=pygame.image.load("img/'+i+'")')
  exec(name+'=pygame.transform.scale('+name+imgsize)
  #exec(name+'_rect='+name+'.get_rect()') #haha get rekt
if debug: print "  [OK]"

#Game data
#Pieces:
#T -> san
#. -> aon
#: -> khoyor
#/ -> ska

if debug: print "Initializing board...",
lineup=["aon","khoyor","ska","ska","khoyor","aon"]

def initialize_board():
  return [["w_"+z for z in lineup]]+[['' for i in range(6)] for j in range(4)]+[["b_"+z for z in lineup]]

board=initialize_board()

#Draw board background
bg=pygame.Surface((wsize[1],wsize[1]))
bg.fill((192,192,192))
for i in (0,2,4):
  for j in range(6):
    pygame.draw.rect(bg,(128,128,128),((i+j%2)*cellsize,j*cellsize,cellsize,cellsize))
#Selection square
sel=pygame.Surface((cellsize,cellsize), pygame.SRCALPHA)
sel.fill(bestcolour)

#functions
def possible_moves(c):
  """
  Draws arrows with the possible moves for a clicked piece
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
    pass

  #Remove invalid coords
  valid_coords=[i for i in valid_coords if all(j>=0 and j<6 for j in i)]
  valid_coords=[i for i in valid_coords if not board[i[1]][i[0]].startswith(piececolour)]
  
  #Draw line
  pc=lambda x: x*cellsize+cellsize/2 #coordinates of the centre of the cell
  lsc=(pc(c[0]),pc(c[1])) #line start coordinates
  lec=[[pc(i[0]),pc(i[1])] for i in valid_coords] #line end coordinates
  return [valid_coords,[lsc,lec]]

def movepiece(a,b):
  piece=board[a[1]][a[0]]
  board[a[1]][a[0]]=""
  board[b[1]][b[0]]=piece

#Main loop
if debug: print "  [OK]\nEntering main loop\n---"
run=1
while run:
  #Draw board
  screen.blit(bg,(0,0))
  for idi,i in enumerate(board):
    for idj,j in enumerate(i):
      position=(cellsize*idj,cellsize*idi)
      if selected: screen.blit(sel,selected)
      if moves:
        for z in moves[1]:
          pygame.draw.line(screen,bestcolour,moves[0],z,10)
          pygame.draw.circle(screen,bestcolour,z,20)
      if j: screen.blit(eval(j),position)

  #Event detection
  for ev in pygame.event.get():
    if ev.type==pygame.QUIT: run=0
    if ev.type==pygame.KEYDOWN:
      keys=pygame.key.get_pressed()
      if keys[pygame.K_ESCAPE]: 
        if debug: print "Escape pressed, quitting"
        run=0

    if ev.type==pygame.MOUSEBUTTONDOWN:
      mousepos=pygame.mouse.get_pos()
      coords=[i/cellsize for i in mousepos]
      piece=board[coords[1]][coords[0]]
      if coords in valid_coords and selected:
        if debug: print 'moving '+piece+' to '+str(coords)
        movepiece(origin,coords)
        moves=[]
        selected=""
        origin=[]
      elif piece:
        if debug: print "clicked "+piece+" at "+str(coords)
        selected=[coords[0]*cellsize,coords[1]*cellsize]
        origin=coords
        valid_coords,moves=possible_moves(coords)
      else:
        selected=""
        moves=[]
        origin=[]

  #Screen and clock update
  pygame.display.flip()
  ms=clock.tick(30)

pygame.quit()

