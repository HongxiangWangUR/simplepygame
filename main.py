#!/usr/local/bin/python3

import pygame,sys
import pygame.locals
from gameconstant import *
import random
from abc import ABC, abstractmethod

background_surface=None
clock=None
SCREEN=None
ADD_PIPE=pygame.USEREVENT+1
game_state_active=True

class Sprite_Object(ABC,pygame.sprite.Sprite):
	'''
	abstract super class
	'''
	def __init__(self,image_path:str,start_x:int,start_y:int,scale_x:int=None,scale_y:int=None):
		super().__init__()
		if scale_x!=None and scale_y!=None:
			self.surface=pygame.transform.scale(pygame.image.load(image_path).convert_alpha(),(scale_x,scale_y))
		else:
			self.surface=pygame.image.load(image_path).convert_alpha()
		self.rect=self.surface.get_rect()
		self.rect.x=start_x
		self.rect.y=start_y
	@abstractmethod
	def move(self):
		'''
		subclass must instantiate this
		'''
		pass
	def show(self,surface):
		surface.blit(self.surface,self.rect)

class Floor(Sprite_Object):
	def __init__(self,image_path):
		super().__init__(image_path,0,710,1000,100)
	def move(self):
		self.rect.move_ip(-SPEED,0)

class Bird(Sprite_Object):
	def __init__(self,image_path):
		super().__init__(image_path,50,300,56,44)
		self.drop_speed=0
	def move(self):
		self.rect.move_ip(0,self.drop_speed)
		self.drop_speed+=DROP_ACCELERATION
	def fly(self):
		self.rect.move_ip(0,-50)
		self.drop_speed=0

class Pipe(Sprite_Object):
	def __init__(self,image_path,type,height):
		super().__init__(image_path,500,height,70,500)
		if type != 'upward':
			self.rect.bottomleft=(500,height-200)
		self.type=type
	def move(self):
		self.rect.move_ip(-SPEED,0)
	def show(self,surface):
		if self.type == 'upward':
			super().show(surface)
		else:
			surface.blit(pygame.transform.flip(self.surface,False,True),self.rect)

if __name__ == "__main__":
	pygame.init()
	SCREEN=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
	pygame.display.set_caption("flappy bird")
	clock=pygame.time.Clock()
	SCREEN.fill(COLOR_BLACK)
	background_surface=pygame.transform.scale2x(pygame.image.load('./pics/bg.png').convert())
	SCREEN.blit(background_surface,(0,0))
	pygame.time.set_timer(ADD_PIPE,PIPE_GENERATE_INTERVAL)

	floor=Floor("./pics/floor.png")
	bird=Bird("./pics/bird1.png")
	pipe_list=[]

	obstacle_group=pygame.sprite.Group()
	# obstacle_group.add(floor)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.locals.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					bird.fly()
			if event.type == ADD_PIPE:
				height=random.randint(400,650)
				pipe_top=Pipe('./pics/pipe.gif','upward',height)
				pipe_down=Pipe('./pics/pipe.gif','downward',height)
				pipe_list.extend([pipe_top,pipe_down])
				obstacle_group.add(pipe_top)
				obstacle_group.add(pipe_down)
		floor.move()
		if floor.rect.x < -500:
			floor.rect.x=0
		for pipe in pipe_list:
			pipe.move()
		bird.move()
		# draw screen
		SCREEN.blit(background_surface,(0,0))
		for pipe in pipe_list:
			pipe.show(SCREEN)
		bird.show(SCREEN)
		floor.show(SCREEN)
		pygame.display.update()
		# collision detection
		if pygame.sprite.spritecollideany(bird,obstacle_group):
			print('collision')

		clock.tick(60)
