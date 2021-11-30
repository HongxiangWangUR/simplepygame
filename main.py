#!/usr/local/bin/python3

import pygame,sys
import pygame.locals
from gameconstant import *

pygame.init()

SCREEN=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("my game")
clock=pygame.time.Clock()
SCREEN.fill(COLOR_BLACK)
backgroundpic=pygame.image.load('./pics/bg.png').convert()
backgroundpic=pygame.transform.scale2x(backgroundpic)
floorpic=pygame.image.load('./pics/floor.png').convert()
floorpic=pygame.transform.scale(floorpic,(800,100))

SCREEN.blit(backgroundpic,(0,0))
SCREEN.blit(floorpic,(0,700))
while True:
	for event in pygame.event.get():
		if event.type == pygame.locals.QUIT:
			pygame.quit()
			sys.exit()
	pygame.display.update()
	clock.tick(60)

