#!/usr/local/bin/python3

import pygame,sys
import pygame.locals
from gameconstant import *

pygame.init()

SCREEN=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("my game")
clock=pygame.time.Clock()
SCREEN.fill(COLOR_BLACK)
backgroundpic=pygame.image.load('./pics/background.png').convert()

SCREEN.blit(backgroundpic,(0,0))
while True:
	for event in pygame.event.get():
		if event.type == pygame.locals.QUIT:
			pygame.quit()
			sys.exit()
	pygame.display.update()
	clock.tick(60)

