#!/usr/bin/env python

import ast, copy, datetime, getopt, os, sys
from lib import analysis, move, network

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
bestcolour=(250,186,218,128)
cellsize=size/6
history=[]
archive_directory="./games"

#option latching
reverse=0
net=0
record=0
replay=0

#AI match config
aiblack=""
aiwhite=""
matches=1
pause=0
maxmoves=1000
movesleft=maxmoves

#Options and parameters
try:
  opts,args=getopt.getopt(sys.argv[1:],"w:b:n:p:dlrf:tc:s", ["help"])
  for i in opts:
    val=i[1]
    if "--help" in i:
      print \
      """
      ---General options---

      -d      debug (prints events to stdout)
      -r      record (Records list of moves to file)
      -f      replays game recorded on file

      ---Network play---

      -c      connect to a server (ip). Play as white
      -s      start a server. Play as black

      ---AI options---

      -b      name of AI for black player (string)
      -w      name of AI for white player (string)

      ---AI vs AI matches---

      -n      number of matches (default 1)
              If n>1, board is not shown
      -p      pause between moves (ms, default 1)
      -l      max allowed moves in a match (default 1000)
      -t      places black on top instead of bottom ([TO-DO] Doesn't work with player inputs)
      """
      sys.exit(0)
      
    #General options
    if "-t" in i:
      reverse=1
    if "-r" in i:
      record=1
    if "-f" in i:
      replay=1
      replay_file=val

    #AI options
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

    #AI vs AI matches
    if "-n" in i:
      matches=int(val)
    if "-p" in i:
      pause=int(val)
    if "-l" in i:
      maxmoves=int(val)

    #Network play
    if "-s" in i:
      net=1
    if "-c" in i:
      net=val
  
except Exception as e:
  print e
  sys.exit(1)
  
showboard=1 if matches==1 else 0
matchesleft=matches
score=[]

#Differentiation for AI vs AI
if aiblack and aiwhite:
  if aiblack.name==aiwhite.name: 
    aiwhite.name+=" (%s)"%aiwhite.author
    aiblack.name+=" (%s)"%aiblack.author
    if aiblack.name==aiwhite.name: 
      aiwhite.name+=" 2"

#Network setup
if net==1:
  if debug: print "Waiting for client connection..."
  c=network.connection()
  c.receive()
elif net:
  if debug: print "Connecting to server at %s..."%net
  c=network.connection(net)
if debug: print "Connection established"
  
#Pygame stuff
if debug: print "Initializing pygame...",
pygame.init()
clock=pygame.time.Clock()
if showboard:
  pygame.font.init()
  screen=pygame.display.set_mode(wsize)
  pygame.display.set_caption('Xi '+" ".join(sys.argv[1:]))
if debug: print "  [OK]"

#Load resources
if showboard:
  if debug: print "Loading resources...",
  for i in os.listdir('img'):
    name=i.replace('.png','')
    imgsize=",(%i,%i))"%(cellsize,cellsize)
    exec(name+'=pygame.image.load("img/'+i+'").convert_alpha()')
    exec(name+'=pygame.transform.scale('+name+imgsize)


  #Board background and auxiliary graphics
  bg=pygame.Surface((wsize[1],wsize[1]))
  bg.fill((192,192,192))
  for i in (0,2,4):
    for j in range(6):
      pygame.draw.rect(bg,(128,128,128),((i+j%2)*cellsize,j*cellsize,cellsize,cellsize))
  #Selection square
  sel=pygame.Surface((cellsize,cellsize), pygame.SRCALPHA)
  sel.fill(bestcolour)
  #Move highlight square
  mov=pygame.Surface((cellsize,cellsize), pygame.SRCALPHA)
  mov.fill((128,0,128,128))
  if debug: print "  [OK]"

#initialize board
if debug: print "Initializing board...",
lineup=["aon","khoyor","ska","ska","khoyor","aon"]

def initialize_board():
  global board
  board=[["w_"+z for z in lineup]]+[['' for i in range(6)] for j in range(4)]+[["b_"+z for z in lineup]]

initialize_board()
if debug: print "  [OK]"

#misc functions
def turn():

  return len(history)%2

def resetmove():
  "Resets move state variables"

  global moves
  global selected
  global origin
  moves=[]
  selected=""
  origin=[]

def show(board):

  #Draw background
  screen.blit(bg,(0,0))

  #Highlight previous move
  if history:
    for q in history[-1]:
      screen.blit(mov,[i*cellsize for i in q])

  #Piece and possible moves
  if selected: screen.blit(sel,selected)
  if moves:
    for z in moves:
      screen.blit(sel,z)

  #Draw pieces
  for idi,i in enumerate(board):
    for idj,j in enumerate(i):
      position=(cellsize*idj,cellsize*idi)
      if j: screen.blit(eval(j),position)

  if reverse==1: screen.blit(pygame.transform.rotate(screen, 180), (0, 0))

  #Feedback images
  if analysis.checkgame(board)==1:
    screen.blit(img_blackwins,(cellsize*2,cellsize*2))
  elif analysis.checkgame(board)==-1:
    screen.blit(img_whitewins,(cellsize*2,cellsize*2))
  if ((aiblack and not turn()) or (aiwhite and turn())) and analysis.checkgame(board)==0 \
               and not (aiblack and aiwhite): 
    screen.blit(img_thinking,(2.5*cellsize,2.5*cellsize))

  pygame.display.flip()

#Replay loop
if replay:
  if debug: print "Replaying game %s"%replay_file
  with open("%s/%s"%(archive_directory,replay_file), "r") as f:
    for i in f.readlines():
      i=ast.literal_eval(i)
      cc=["b","w"][turn()]
      show(board)
      board=move.move(board,i,cc)
      history.append(i)
      ms=clock.tick(30)
      pygame.time.wait(pause)
  exit(0)

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
      player_enabled=not ((aiblack and net==1) or (aiwhite and type(net)==str))\
                and not (aiblack and aiwhite) \
                and not ((net==1 and turn()) or (type(net)==str and not turn()))

      if ev.type==pygame.MOUSEBUTTONDOWN and analysis.checkgame(board)==0 and player_enabled:

        mousepos=pygame.mouse.get_pos()
        coords=[i/cellsize for i in mousepos]
        piece=board[coords[1]][coords[0]]
        piececolour=['b','w',''].index(piece.split('_')[0])
        reset=1
          
        #Piece was already selected and valid destination is clicked
        if selected and coords in valid_coords:
          if debug: print 'moving to '+str(coords)
          move.movepiece(board,origin,coords)
          history.append([origin,coords])
          if debug: print "Sending move to network"
          if net: c.send(history[-1])
          
        #A piece of the proper colour is clicked
        elif piece and piececolour==turn():
          if debug: print "clicked "+piece+" at "+str(coords)
          selected=[coords[0]*cellsize,coords[1]*cellsize]
          origin=coords
          valid_coords=analysis.possible_moves(board,coords)
          moves=[[i*cellsize for i in j] for j in valid_coords]
          reset=0
        
        #Black san spawning
        elif coords[1]==5 and not turn() and all([not i for i in analysis.homerow(board,"b")]):
          move.spawnsan(board,coords,"b")
          history.append([coords])
        #White san spawning
        elif coords[1]==0 and turn() and all([not i for i in analysis.homerow(board,"w")]):
          move.spawnsan(board,coords,"w")
          history.append([coords])

        if reset:
          resetmove()

      show(board)

  if analysis.checkgame(board)==0:

    if not turn():
      if type(net)==str:
        screen.blit(img_waiting,(2.5*cellsize,2.5*cellsize))
        pygame.display.flip()
        if debug: print "Waiting for black move over network"
        bmove=c.receive()
        if debug: print "Received move:", bmove
        board=move.move(board,bmove,"b")
        history.append(bmove)
      if aiblack:
        if debug: print "Black AI calculating move"
        bmove=aiblack.move(copy.copy(board))
        board=move.move(board,bmove,"b")
        movesleft-=1
        history.append(bmove)
        if net: c.send(history[-1])

    if turn():
      if net==1:
        screen.blit(img_waiting,(2.5*cellsize,2.5*cellsize))
        pygame.display.flip()
        if debug: print "Waiting for white move over network"
        wmove=c.receive()
        if debug: print "Received move:",wmove
        board=move.move(board,wmove,"w")
        history.append(wmove)
      if aiwhite:
        if debug: print "White AI calculating move"
        wmove=aiwhite.move(copy.copy(board))
        board=move.move(board,wmove,"w")
        movesleft-=1
        history.append(wmove)
        if net: c.send(history[-1])

  #Victory check
  cg=analysis.checkgame(board)

  #Record gamet o file
  if cg and record:
    date=datetime.datetime.now().isoformat().split(".")[0]
    bp=aiblack.name if aiblack else "network" if type(net)==str else "human"
    wp=aiwhite.name if aiwhite else "network" if net==1 else "human"
    with open('%s/xi_%s_%s_%s'%(archive_directory,date,bp,wp),'w+') as f:
      for i in history:
        f.write(str(i)+"\n")
    record=0

  #AI match cycling
  if cg and aiblack and aiwhite:
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
    show(board)
    ms=clock.tick(30)
  
  #sleep if the match is AI vs AI
  if aiblack and aiwhite and showboard: pygame.time.wait(pause)

if net: c.closeconn()
pygame.quit()
