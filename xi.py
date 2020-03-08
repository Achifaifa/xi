import copy
import pygame
from pygame import Surface

#Config
size=600
wsize=(size,size)

#Pygame stuff
pygame.init()
pygame.font.init()
screen=pygame.display.set_mode(wsize)
pygame.display.set_caption('Xi')
clock=pygame.time.Clock()

#Game data
"""
Pieces:
T -> san
. -> aon
: -> khoyor
/ -> ska
"""
lineup=[".",":","/","/",":","."]

def initialize_board():
  return copy.copy(lineup)+[["" for i in range(6)] for j in range(4)]+copy.copy(lineup)

board=initialize_board()
#Draw board
squaresize=wsize[1]/6
bg=pygame.Surface((wsize[1],wsize[1]))
bg.fill((192,192,192))
for i in (0,2,4):
  for j in range(6):
    pygame.draw.rect(bg,(128,128,128),((i+j%2)*squaresize,j*squaresize,squaresize,squaresize))


while 1:
  for event in pygame.event.get():
    if event.type==pygame.QUIT: break
    if event.type==pygame.KEYUP:
      if event.key==pygame.K_ESCAPE: break

  screen.blit(bg, (0,0))
  pygame.display.flip()
  ms=clock.tick(30)

pygame.quit

