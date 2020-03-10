#!/usr/bin/env python

import copy, getopt, os, sys
from lib import move

os.environ['PYGAME_HIDE_SUPPORT_PROMPT']="hide"
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
origin=[]
valid_coords=[]
bestcolour=(250,186,218,8)
turn=0
next=0
cellsize=size/6

#AI match config
aiblack=""
aiwhite=""
matches=1
pause=0
maxmoves=1000
movesleft=maxmoves

#Options and parameters
try:
  opts,args=getopt.getopt(sys.argv[1:],"w:b:n:p:dl:", ["help"])
  for i in opts:
    val=i[1]
    if "--help" in i:
      print \
      """
      -d      debug (prints to stdout)

      -b      name of AI for black player (string)
      -w      name of AI for white player (string)

      ---For AI vs AI matches---

      -n      number of matches (default 1)
              If n>1, board is not shown
      -p      pause between moves (ms, default 0)
      -l      max allowed moves in a match (default 1000)
      """
      sys.exit(0)
      
    #TO-DO this can be cleaned further
    ai=0
    if "-w" in i:
      aic="w"
      aicol="white"
      ai=1
    if "-b" in i:
      aic="b"
      aicol="black"
      ai=1
    if ai:
      if debug: print "selecting %s for %s AI"%(val,aicol)
      try:
        exec("from ai import %s"%val)
        exec("ai%s=%s.ai('%s')"%(aicol,val,aic))
      except:
        run=0
        if debug: print "Error loading %s AI for %s"%(val,aicol)

    if "-n" in i:
      matches=int(val)
    if "-p" in i:
      pause=int(val)
    if "-l" in i:
      maxmoves=int(val)
  
except getopt.GetoptError as err:
  print str(err)
  sys.exit(1)
  
showboard=1 if matches==1 else 0
matchesleft=matches
score=[]
  
#Pygame stuff
if debug: print "Initializing pygame...",
pygame.init()
clock=pygame.time.Clock()
if showboard:
  pygame.font.init()
  screen=pygame.display.set_mode(wsize)
  pygame.display.set_caption('Xi')
if debug: print "  [OK]"

#Load resources
if showboard:
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
  global board
  board=[["w_"+z for z in lineup]]+[['' for i in range(6)] for j in range(4)]+[["b_"+z for z in lineup]]
initialize_board()

#Draw board background
if showboard:
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
  "Moves whatever is in A to B"
  board[a[1]][a[0]], board[b[1]][b[0]]="", board[a[1]][a[0]]
  resetmove()

def spawnsan(a,c):
  "Spawns a san of colour c in A"
  board[a[1]][a[0]]=c+"_san"
  resetmove()

def resetmove():
  "Resets move state variables"

  global moves
  global selected
  global origin
  moves=[]
  selected=""
  origin=[]

def pc(coords):
  "Calculates px coords of the middle of a square"

  return [i*cellsize+cellsize/2 for i in coords]

def checkgame():
  """
  1: black wins
  0: game ongoing
  -1: white wins
  t: timeout
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
  
  if movesleft<=0: return "t"

  #Continue normally
  return 0

#Main loop
if debug and run: print "Entering main loop\n---"
while run:
  if showboard:
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
      #Key handling
      if ev.type==pygame.KEYDOWN:
        keys=pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]: 
          if debug: print "Escape pressed, quitting"
          run=0

      #Mouse click handling
      if ev.type==pygame.MOUSEBUTTONDOWN and checkgame()==0:

        mousepos=pygame.mouse.get_pos()
        coords=[i/cellsize for i in mousepos]
        piece=board[coords[1]][coords[0]]
        piececolour=['b','w',''].index(piece.split('_')[0])

        #TO-DO this if is horrible
        # Decides if the player can click in something when AIs are involved
        if 1: #Temporarily disabled, no issues if AI is fast
        #if not (((aiwhite and piececolour==1) or (aiblack and piececolour==0)) and not selected):
           #or ((aiblack and not turn) or (aiwhite and turn)):
          
          #Piece was already selected and valid destination is clicked
          if selected and coords in valid_coords:
            if debug: print 'moving '+piece+' to '+str(coords)
            movepiece(origin,coords)
            next=1

          #A piece of the proper colour is clicked
          elif piece and piececolour==turn:
            if debug: print "clicked "+piece+" at "+str(coords)
            selected=[coords[0]*cellsize,coords[1]*cellsize]
            origin=coords
            valid_coords=move.possible_moves(board,coords)
            #Calculate line parameters
            lsc=pc(coords) #line start coordinates
            lec=[pc(i) for i in valid_coords] #line end coordinates
            moves=[lsc,lec]
            next=0
          
          #Black san spawning
          elif coords[1]==5 and not turn:
            spawnsan(coords,"b")
            next=1
          #White san spawning
          elif coords[1]==0 and turn:
            spawnsan(coords,"w")
            next=1

          else:
            resetmove()
            next=0
  
  #AI movement
  if not turn and aiblack and checkgame()==0:
    movepiece(*aiblack.move(board))
    movesleft-=1
    next=1

  elif turn and aiwhite and checkgame()==0:
    movepiece(*aiwhite.move(board))
    movesleft-=1
    next=1
  
  if next: 
    turn=not turn
    next=0

  #Victory check
  cg=checkgame()
  if cg!=0:
    matchesdiff=(matches-matchesleft)%2
    if cg==1:
      if debug: print "(%i/%i): Black wins"%(matches-matchesleft+1, matches)
      score.append(1-matchesdiff*-2)
    if cg==-1:
      if debug: print "(%i/%i): White wins"%(matches-matchesleft+1, matches)
      score.append(-1+matchesdiff*2)
    if cg=="t":
      score.append(0)
      if debug: print "(%i/%i): Timeout after %i moves"%(matches-matchesleft+1, matches, maxmoves)
    matchesleft-=1
  
    #Swap AIs and restart game
    if matchesleft>0:
      aiwhite,aiblack=aiblack,aiwhite
      initialize_board()
      movesleft=maxmoves
      turn=0

    else: 
      print "Black %i | Ties %i | White %i"%(score.count(1),score.count(0),score.count(-1))
      run=0

  #Screen and clock update
  if showboard:
    pygame.display.flip()
    ms=clock.tick(30)
  
  #sleep if the match is AI vs AI
  if aiblack and aiwhite and showboard: pygame.time.wait(pause)

pygame.quit()

