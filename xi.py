import copy, getopt, os, sys
from lib import move
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame import Surface

debug=1 if "-d" in sys.argv else 0
run=1
if debug: print "Starting Xi..."

#general config
size=600
wsize=(size,size)
selected=""
moves=[]
bestcolour=(250,186,218,8)
valid_coords=[]
turn=0
cellsize=size/6

#AI match config
fullai=0
aiblack=""
aiwhite=""
matches=1
pause=0

#Options and parameters

try:
  opts, args=getopt.getopt(sys.argv[1:],"w:b:n:p:d", ["help"])
  for i in opts:
    val=i[1]
    if "--help" in i:
      print """
      
      -d      debug
      -b      name of AI for black player (string)
      -w      name of AI for white player (string)
      ---For AI vs AI matches---
      -n      number of matches (default 1)
      -p      pause between moves (ms, default 0)
      """
      run=0
      
    if "-w" in i:
      if debug: print "selecting %s for white AI"%val
      try:
        exec("from ai import %s"%val)
        exec("aiwhite=%s.ai('w')"%val)
      except:
        run=0
        if debug: print "Error loading %s AI for white"%val
    if "-b" in i:
      if debug: print "selecting %s for black AI"%val
      try:
        exec("from ai import %s"%val)
        exec("aiblack=%s.ai('b')"%val)
      except:
        run=0
        if debug: print "Error loading %s AI for black"%val
    if "-n" in i:
      pass #configure number of rounds
    if "-p" in i:
      pass #configure turn pause
    
except getopt.GetoptError as err:
  print str(err)
  run=0
  
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
for i in os.listdir('img'):
  name=i.replace('.png','')
  imgsize=",(%i,%i))"%(cellsize,cellsize)
  exec(name+'=pygame.image.load("img/'+i+'")')
  exec(name+'=pygame.transform.scale('+name+imgsize)
  #exec(name+'_rect='+name+'.get_rect()') #haha get rekt
if debug: print "  [OK]"

#initialize board
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
if debug: print "  [OK]"

#misc functions
def movepiece(a,b):
  piece=board[a[1]][a[0]]
  board[a[1]][a[0]]=""
  board[b[1]][b[0]]=piece

def checkgame():
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
  if sum([1 for i in board[0] if i.startswith('b_sans')]): return 1
  if sum([1 for i in board[5] if i.startswith('w_sans')]): return -1

  #Continue normally
  return 0

#Main loop
if debug and run: print "Entering main loop\n---\nBlack moves"
if debug and not run: print "Skipping main loop"
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

    if ev.type==pygame.MOUSEBUTTONDOWN and checkgame()==0 and any([aiwhite, aiblack]):
      mousepos=pygame.mouse.get_pos()
      coords=[i/cellsize for i in mousepos]
      piece=board[coords[1]][coords[0]]
      piececolour=['b','w',''].index(piece.split('_')[0])
      allowed=1
      if (((aiwhite and piececolour==1) or (aiblack and piececolour==0)) and not selected) \
                        and not ((aiblack and not turn) or (aiwhite and turn)): allowed=0
      if allowed:
        if coords in valid_coords and selected:
          if debug: print 'moving '+piece+' to '+str(coords)
          movepiece(origin,coords)
          moves=[]
          selected=""
          origin=[]
          turn=not turn
          if debug: print ["Black", "White"][turn]+" moves"
        elif piece and piececolour==turn:
          if debug: print "clicked "+piece+" at "+str(coords)
          selected=[coords[0]*cellsize,coords[1]*cellsize]
          origin=coords
          valid_coords=move.possible_moves(board,coords)
          #Calculate line parameters
          pc=lambda x: x*cellsize+cellsize/2 #coordinates of the centre of the cell
          lsc=(pc(coords[0]),pc(coords[1])) #line start coordinates
          lec=[[pc(i[0]),pc(i[1])] for i in valid_coords] #line end coordinates
          moves=[lsc,lec]
        elif coords[1]==5 and not turn:
          board[coords[1]][coords[0]]="b_san"
          turn=not turn
          moves=[]
          selected=""
          origin=[]
        elif coords[1]==0 and turn:
          board[coords[1]][coords[0]]="w_san"
          turn=not turn
          moves=[]
          selected=""
          origin=[]
        else:
          selected=""
          moves=[]
          origin=[]
          
  if not turn and aiblack and checkgame()==0:
    if debug: print "moving black AI"
    movepiece(*aiblack.move(board))
    turn=not turn
  if turn and aiwhite and checkgame()==0:
    if debug: print "moving white AI"
    movepiece(*aiwhite.move(board))
    turn=not turn

  #Victory check
  cg=checkgame()
  if cg!=0:
    if cg==1 and debug: print "Black wins,",
    if cg==-1 and debug: print "White wins,",
    if debug: print "exiting"
    run=0

  #Screen and clock update
  pygame.display.flip()
  ms=clock.tick(30)

pygame.quit()

