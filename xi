#!/usr/bin/env python

import copy, getopt, os, sys
from lib import analysis, move

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
      -d      debug (prints events to stdout)
      -r      record (Records list of moves to file) [TO-DO]
      -f      replays game recorded on file [TO-DO]

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
      except Exception as e:
        run=0
        print e
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

if aiblack and aiwhite:
  if aiblack.name==aiwhite.name: 
    aiwhite.name+=" (%s)"%aiwhite.author
    aiblack.name+=" (%s)"%aiblack.author
    if aiblack.name==aiwhite.name: 
      aiwhite.name+=" B"
  
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
  img_thinking=pygame.image.load("img/thinking.png")
  img_thinking=pygame.transform.scale(img_thinking, (cellsize,cellsize))
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

def show(board):

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

#Main loop
if debug and run: print "Entering main loop\n---"
while run:

  if showboard:
    show(board)

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
      if ev.type==pygame.MOUSEBUTTONDOWN and analysis.checkgame(board)==0:

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
            move.movepiece(board,origin,coords)
            next=1
            resetmove()

          #A piece of the proper colour is clicked
          elif piece and piececolour==turn:
            if debug: print "clicked "+piece+" at "+str(coords)
            selected=[coords[0]*cellsize,coords[1]*cellsize]
            origin=coords
            valid_coords=analysis.possible_moves(board,coords)
            #Calculate line parameters
            lsc=pc(coords) #line start coordinates
            lec=[pc(i) for i in valid_coords] #line end coordinates
            moves=[lsc,lec]
            next=0
          
          #Black san spawning
          elif coords[1]==5 and not turn:
            move.spawnsan(board,coords,"b")
            next=1
            resetmove()
          #White san spawning
          elif coords[1]==0 and turn:
            move.spawnsan(board,coords,"w")
            next=1
            resetmove()

          else:
            resetmove()
            next=0

        #show board again after input
        show(board)
        if (aiblack or aiwhite) and next: screen.blit(img_thinking,(2.5*cellsize,2.5*cellsize))
  
  #AI movement
  if not turn and aiblack and analysis.checkgame(board)==0:
    bmove=aiblack.move(copy.copy(board))
    board=move.move(board,bmove,"b")
    movesleft-=1
    next=1

  if turn and aiwhite and analysis.checkgame(board)==0:
    wmove=aiwhite.move(copy.copy(board))
    board=move.move(board,wmove,"w")
    movesleft-=1
    next=1
  
  if next: 
    turn=not turn
    next=0

  #Victory check
  cg=analysis.checkgame(board)
  if cg!=0 and aiblack and aiwhite:
    matchesdiff=(matches-matchesleft)%2
    if cg==1:
      if debug: print "(%i/%i): %s wins"%(matches-matchesleft+1, matches, aiblack.name)
      score.append(aiblack.name)
    if cg==-1:
      if debug: print "(%i/%i): %s wins"%(matches-matchesleft+1, matches, aiwhite.name)
      score.append(aiwhite.name)
    if movesleft<0:
      score.append("t")
      if debug: print "(%i/%i): Timeout after %i moves"%(matches-matchesleft+1, matches, maxmoves)
    matchesleft-=1
    
    if aiblack and aiwhite:
      #Swap AIs and restart game
      if matchesleft>0:
        aiwhite,aiblack=aiblack,aiwhite
        initialize_board()
        movesleft=maxmoves
        turn=0

      else: 
        aia=aiblack.name
        aib=aiwhite.name

        scorea=score.count(aia)
        scoreb=score.count(aib)
        print "%s %i | Ties %i | %s %i"%(aia,scorea,score.count("t"),aib,scoreb)
        run=0

  #Screen and clock update
  if showboard:
    pygame.display.flip()
    ms=clock.tick(30)
  
  #sleep if the match is AI vs AI
  if aiblack and aiwhite and showboard: pygame.time.wait(pause)

pygame.quit()

