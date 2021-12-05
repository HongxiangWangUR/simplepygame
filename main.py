#!/usr/local/bin/python3

import pygame,sys
import pygame.locals
from gameconstant import *
import random

pygame.init()

SCREEN=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("my game")
clock=pygame.time.Clock()
SCREEN.fill(COLOR_BLACK)

backgroundpic=pygame.image.load('./pics/bg.png').convert()
backgroundpic=pygame.transform.scale2x(backgroundpic)
floorpic=pygame.image.load('./pics/floor.png').convert()
floorpic=pygame.transform.scale(floorpic,(1000,100))
birdpic=pygame.image.load('./pics/bird1.png').convert_alpha()
birdpic=pygame.transform.scale(birdpic,(56,44))
pipe_surface=pygame.image.load("./pics/pipe.gif").convert()
pipe_surface=pygame.transform.scale(pipe_surface,(70,500))


SCREEN.blit(backgroundpic,(0,0))
floorrect=floorpic.get_rect()
birdrect=birdpic.get_rect()
birdrect.x=50
birdrect.y=300

drop_speed=0
drop_acceleration=0.3


floorrect.x=0
floorrect.y=710

pipe_list=[]

ADD_PIPE=pygame.USEREVENT+1
pygame.time.set_timer(ADD_PIPE,1000)

game_active=True


while True:
	for event in pygame.event.get():
		if event.type == pygame.locals.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				birdrect.y-=50
				drop_speed=0
		if event.type == ADD_PIPE:
			if game_active:
				pipe_rect=pipe_surface.get_rect()
				pipe_rect.x=500
				pipe_rect.y=random.randint(400,650)

				top_pipe_rect=pipe_surface.get_rect()
				top_pipe_rect.bottomleft=(500,pipe_rect.y-200)
				pipe_list.append((pipe_rect,top_pipe_rect))
			

	SCREEN.blit(backgroundpic,(0,0))
	floorrect.move_ip(-SPEED,0)

	if game_active:
		for pipes in pipe_list:
			for pipe in pipes:
				pipe.move_ip(-SPEED,0)

	if floorrect.x < -500:
		floorrect.x=0
	birdrect.move_ip(0,drop_speed)

	if game_active:
		for pipe in pipe_list:
			SCREEN.blit(pipe_surface,pipe[0])
			SCREEN.blit(pygame.transform.flip(pipe_surface,False,True),pipe[1])
	if game_active:
		SCREEN.blit(birdpic,birdrect)
	SCREEN.blit(floorpic,floorrect)

	pygame.display.update()

	for pipes in pipe_list:
		for pipe in pipes:
			if pipe.colliderect(birdrect):
				pipe_list.clear()
				game_active=False
	drop_speed+=drop_acceleration
	clock.tick(60)

