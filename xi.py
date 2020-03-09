import copy, os
import pygame
from pygame import Surface

debug=1

if debug: print "Starting Xi..."
#Config
size=600
wsize=(size,size)
selected=""

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
sel.fill((250,186,218,100))
sel.set_alpha(100)


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
      if piece:
        if debug: print "clicked "+piece+" at "+str(coords)
        selected=[coords[0]*cellsize,coords[1]*cellsize]
 

  #Screen and clock update
  pygame.display.flip()
  ms=clock.tick(30)

pygame.quit()

