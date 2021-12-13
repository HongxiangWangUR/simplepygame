#!/usr/local/bin/python3

import pygame,sys
import pygame.locals
from gameconstant import *
import random
from abc import ABC, abstractmethod


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
		if floor.rect.x < -500:
			floor.rect.x=0

class Bird(Sprite_Object):
	def __init__(self,image_path,surface):
		if surface is None:
			super().__init__(image_path,50,300,56,44)
		else:
			self.surface=surface
			self.rect=self.surface.get_rect()
			self.rect.x=50
			self.rect.y=300
		self.drop_speed=0
	def move(self):
		self.rect.move_ip(0,self.drop_speed)
		self.drop_speed+=DROP_ACCELERATION
	def fly(self):
		self.rect.move_ip(0,-50)
		self.drop_speed=0
	def show(self,surface):
		rotate_surface=pygame.transform.rotozoom(self.surface,-self.drop_speed*0.8,1)
		surface.blit(rotate_surface,self.rect)
	def position_restore(self):
		self.rect.x=50
		self.rect.y=300
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

class Coin(Sprite_Object):
	def __init__(self,image_path,pipe_height):
		super().__init__(image_path,0,0,30,30)
		self.rect.center=(535,height-100)
	def move(self):
		self.rect.move_ip(-SPEED,0)

def game_init():
	global SCREEN
	global background_surface
	global clock
	global ADD_PIPE
	global floor
	global game_over_surface
	global game_over_rect
	global fly_sound
	global hit_sound
	global score_sound

	# below are variables that will change with game state
	global bird
	global pipe_list
	global game_state_active
	global obstacle_group
	global restart_surface
	global restart_rect
	global coin_list
	global coin_group
	global current_score
	global score_surface
	global score_rect
	global score_font
	global coin_surface

	pygame.mixer.pre_init()
	pygame.init()
	SCREEN=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
	pygame.display.set_caption("flappy bird")
	clock=pygame.time.Clock()
	SCREEN.fill(COLOR_BLACK)
	background_surface=pygame.transform.scale2x(pygame.image.load('./pics/bg.png').convert())
	SCREEN.blit(background_surface,(0,0))
	ADD_PIPE=pygame.USEREVENT+1
	pygame.time.set_timer(ADD_PIPE,PIPE_GENERATE_INTERVAL)
	game_state_active=True
	floor=Floor("./pics/floor.png")
	bird=Bird("./pics/bird.png",None)
	pipe_list=[]
	obstacle_group=pygame.sprite.Group()
	obstacle_group.add(floor)
	fly_sound=pygame.mixer.Sound('./sound/wing.wav')
	hit_sound=pygame.mixer.Sound('./sound/hit.wav')
	score_sound=pygame.mixer.Sound('./sound/score.wav')

	font=pygame.font.Font(None,50)
	game_over_surface=font.render("Game Over",False, (255,255,255))
	game_over_rect=game_over_surface.get_rect()
	game_over_rect.x=150
	game_over_rect.y=300
	current_score=0
	score_font=pygame.font.Font(None,40)
	score_surface=score_font.render("Score: {}".format(current_score),False,(255,255,255))
	score_rect=score_surface.get_rect(midtop=(250,20))

	restart_surface=pygame.transform.scale(pygame.image.load("./pics/restart.png").convert(),(100,50))
	restart_rect=restart_surface.get_rect(center=(250,400))

	coin_surface=pygame.transform.scale(pygame.image.load("./pics/coin.png").convert(),(30,30))
	coin_list=[]
	coin_group=pygame.sprite.Group()

def filter_out_of_screen_obj(objlist:list):
	return list(filter(lambda x:x.rect.right>0,objlist))

if __name__ == "__main__":
	game_init()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.locals.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if game_state_active and event.key == pygame.K_SPACE:
					bird.fly()
					fly_sound.play()
			elif event.type == ADD_PIPE:
				if game_state_active:
					height=random.randint(400,650)
					pipe_top=Pipe('./pics/pipe.gif','upward',height)
					pipe_down=Pipe('./pics/pipe.gif','downward',height)
					pipe_list.extend([pipe_top,pipe_down])
					obstacle_group.add(pipe_top)
					obstacle_group.add(pipe_down)

					coin=Coin('./pics/coin.png',height)
					coin_list.append(coin)
					coin_group.add(coin)
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				mouse_pos=pygame.mouse.get_pos()
				if restart_rect.collidepoint(mouse_pos):
					game_state_active=True
					bird.position_restore()
		floor.move()
		if game_state_active:
			for pipe in pipe_list:
				pipe.move()
			bird.move()
			for coin in coin_list:
				coin.move()
		# draw screen
		SCREEN.blit(background_surface,(0,0))
		for pipe in pipe_list:
			if pipe.rect.right<=0:
				pipe.kill()
			else:
				pipe.show(SCREEN)
		for coin in coin_list:
			if coin.rect.right<=0:
				coin.kill()
			else:
				coin.show(SCREEN)
		pipe_list=filter_out_of_screen_obj(pipe_list)
		coin_list=filter_out_of_screen_obj(coin_list)
		if game_state_active:
			bird.show(SCREEN)
		# collision detection
		if pygame.sprite.spritecollideany(bird,obstacle_group):
			pygame.sprite.Group.empty(obstacle_group)
			obstacle_group.add(floor)
			pipe_list.clear()
			pygame.sprite.Group.empty(coin_group)
			coin_list.clear()
			game_state_active=False
			bird.position_restore()
			hit_sound.play()

		if pygame.sprite.spritecollideany(bird,coin_group):
			collide_coin_list=pygame.sprite.spritecollide(bird,coin_group,True)
			current_score+=1
			coin_list=list(filter(lambda x:x not in collide_coin_list,coin_list))
			score_sound.play()
		if not game_state_active:
			SCREEN.blit(restart_surface,restart_rect)
			SCREEN.blit(game_over_surface,game_over_rect)
			current_score=0
		else:
			score_surface=score_font.render("Score: {}".format(current_score),False,(255,255,255))
			SCREEN.blit(score_surface,score_rect)

		floor.show(SCREEN)
		pygame.display.update()
		clock.tick(60)
