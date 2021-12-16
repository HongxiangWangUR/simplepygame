#!/usr/local/bin/python3

import pygame,sys
import pygame.locals
from gameconstant import *
import random
from abc import ABC, abstractmethod
from os import path
import json

def load_surface(image_path:str,scale_x:int=None,scale_y:int=None):
	if scale_x is not None and scale_y is not None:
		return pygame.transform.scale(pygame.image.load(image_path).convert_alpha(),(scale_x,scale_y))
	return pygame.image.load(image_path).convert_alpha()

class Sprite_Object(ABC,pygame.sprite.Sprite):
	'''
	abstract super class
	'''
	def __init__(self,surface,start_x:int,start_y:int):
		super().__init__()
		self.image=surface
		self.rect=self.image.get_rect()
		self.rect.topleft=(start_x,start_y)
	@abstractmethod
	def move(self):
		'''
		subclass must instantiate this
		'''
		pass
	def show(self,surface):
		surface.blit(self.image,self.rect)

class Floor(Sprite_Object):
	def __init__(self,image_surface):
		super().__init__(image_surface,0,710)
	def move(self):
		self.rect.move_ip(-SPEED,0)
		if self.rect.x < -500:
			self.rect.x=0

class Bird(Sprite_Object):
	def __init__(self,image_surface):
		super().__init__(image_surface,50,300)
		self.drop_speed=0
	def move(self):
		self.rect.move_ip(0,self.drop_speed)
		self.drop_speed+=DROP_ACCELERATION
	def fly(self):
		self.rect.move_ip(0,-50)
		self.drop_speed=0
	def show(self,surface):
		rotate_surface=pygame.transform.rotozoom(self.image,-self.drop_speed*0.8,1)
		surface.blit(rotate_surface,self.rect)
	def position_restore(self):
		self.rect.x=50
		self.rect.y=300
		self.drop_speed=0

class Pipe(Sprite_Object):
	def __init__(self,image_surface,type,height):
		super().__init__(image_surface,500,height)
		if type != 'upward':
			self.rect.bottomleft=(500,height-200)
		self.type=type
	def move(self):
		self.rect.move_ip(-SPEED,0)
	def show(self,surface):
		if self.type == 'upward':
			super().show(surface)
		else:
			surface.blit(pygame.transform.flip(self.image,False,True),self.rect)

class Coin(Sprite_Object):
	def __init__(self,image_surface,pipe_height):
		super().__init__(image_surface,0,0)
		self.rect.center=(535,pipe_height-100)
	def move(self):
		self.rect.move_ip(-SPEED,0)

class PipeGroup(pygame.sprite.Group):
	def draw(self,surface):
		pipe_sprites=self.sprites()
		for pipe in pipe_sprites:
			pipe.show(surface)

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
	global floor_surface
	global pipe_surface
	global bird_surface
	global coin_surface

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
	global welcome_surface
	global game_state_init
	global welcome_rect
	global rank_surface
	global rank_rect
	global rank_data
	global score_board_flag
	global score_board_surface
	global score_board_rect


	pygame.mixer.pre_init()
	pygame.init()
	SCREEN=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
	pygame.display.set_caption("flappy dog")
	clock=pygame.time.Clock()
	SCREEN.fill(COLOR_BLACK)
	background_surface=pygame.transform.scale2x(pygame.image.load('./pics/bg.png').convert())
	SCREEN.blit(background_surface,(0,0))
	ADD_PIPE=pygame.USEREVENT+1
	pygame.time.set_timer(ADD_PIPE,PIPE_GENERATE_INTERVAL)
	game_state_active=False
	game_state_init=True
	score_board_flag=False
	# pre load image surface
	floor_surface=load_surface("./pics/floor.png",1000,100)
	bird_surface=load_surface("./pics/dog.png",56,44)
	pipe_surface=load_surface('./pics/pipe.gif',70,500)
	coin_surface=load_surface("./pics/coin.png",30,30)
	welcome_surface=pygame.transform.scale(pygame.image.load("./pics/welcome.png").convert_alpha(),(367,97))

	floor=Floor(floor_surface)
	bird=Bird(bird_surface)
	obstacle_group=PipeGroup()
	obstacle_group.add(floor)
	fly_sound=pygame.mixer.Sound('./sound/wing.wav')
	hit_sound=pygame.mixer.Sound('./sound/hit.wav')
	score_sound=pygame.mixer.Sound('./sound/score.wav')

	game_over_surface=pygame.transform.scale(pygame.image.load("./pics/gameover.png").convert_alpha(),(309,85))
	game_over_rect=game_over_surface.get_rect(center=(250,300))
	current_score=0
	score_font=pygame.font.Font(None,40)
	score_surface=score_font.render("Score: {}".format(current_score),False,(255,255,255))
	score_rect=score_surface.get_rect(midtop=(250,20))

	restart_surface=pygame.transform.scale(pygame.image.load("./pics/restart.png").convert(),(100,60))
	restart_rect=restart_surface.get_rect(center=(150,450))
	welcome_rect=welcome_surface.get_rect(center=(250,300))

	coin_group=pygame.sprite.Group()
	rank_surface=pygame.transform.scale(pygame.image.load('./pics/rank.png').convert_alpha(),(100,60))
	rank_rect=rank_surface.get_rect(center=(350,450))

	score_board_surface=pygame.transform.scale(pygame.image.load('./pics/scoreboard.png').convert_alpha(),(370,180))
	score_board_rect=score_board_surface.get_rect(center=(250,300))

	if path.exists('rank.json'):
		try:
			with open('rank.json') as rank_file:
				scores=rank_file.read()
				rank_data=json.loads(scores)
		except Exception:
			print('parse rank.json error, rank data will be initialized in default')
			rank_data=[]
	else:
		rank_data=[]

if __name__ == "__main__":
	game_init()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.locals.QUIT:
				with open('rank.json','w') as rank_file:
					json.dump(rank_data,rank_file)
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if game_state_active and event.key == pygame.K_SPACE:
					bird.fly()
					fly_sound.play()
			elif event.type == ADD_PIPE:
				if game_state_active:
					height=random.randint(400,650)
					pipe_top=Pipe(pipe_surface,'upward',height)
					pipe_down=Pipe(pipe_surface,'downward',height)
					obstacle_group.add(pipe_top)
					obstacle_group.add(pipe_down)

					coin=Coin(coin_surface,height)
					coin_group.add(coin)
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_state_active:
				mouse_pos=pygame.mouse.get_pos()
				if restart_rect.collidepoint(mouse_pos):
					game_state_active=True
					game_state_init=False
					score_board_flag=False
					current_score=0
				elif rank_rect.collidepoint(mouse_pos):
					score_board_flag=True
					game_state_active=False
		# move all objects position
		floor.move()
		if game_state_active:
			obstacle_list=obstacle_group.sprites()
			coin_list=coin_group.sprites()
			for obstacle in obstacle_list:
				if obstacle is not floor:
					obstacle.move()
					if obstacle.rect.right<=0:
						obstacle.kill()
			bird.move()
			for coin in coin_list:
				coin.move()
				if coin.rect.right<=0:
					coin.kill()
		# draw objects
		SCREEN.blit(background_surface,(0,0))
		if game_state_active:
			obstacle_group.draw(SCREEN)
			coin_group.draw(SCREEN)
			bird.show(SCREEN)
		# collision detection
		if pygame.sprite.spritecollideany(bird,obstacle_group):
			pygame.sprite.Group.empty(obstacle_group)
			obstacle_group.add(floor)
			pygame.sprite.Group.empty(coin_group)
			game_state_active=False
			bird.position_restore()
			rank_data.append(current_score)
			rank_data.sort()
			if len(rank_data)>SCORE_BOARD_LIMIT:
				rank_data.pop(0)
			hit_sound.play()

		if pygame.sprite.spritecollideany(bird,coin_group):
			pygame.sprite.spritecollide(bird,coin_group,True)
			current_score+=1
			score_sound.play()
		if not game_state_active:
			if score_board_flag:
				SCREEN.blit(score_board_surface,score_board_rect)
				SCREEN.blit(restart_surface,restart_rect)
				#draw current score
				current_surface=score_font.render(" {} ".format(current_score),False,(255,255,255))
				current_rect=current_surface.get_rect(center=(360,280))
				SCREEN.blit(current_surface,current_rect)
				#draw best score
				best_score=current_score
				if rank_data is not None and len(rank_data)>0:
					best_score=max(rank_data)
					best_surface=score_font.render(' {} '.format(best_score),False,(255,255,255))
					best_rect=best_surface.get_rect(center=(360,340))
					SCREEN.blit(best_surface,best_rect)
			else:
				SCREEN.blit(restart_surface,restart_rect)
				SCREEN.blit(rank_surface,rank_rect)
				if game_state_init:
					SCREEN.blit(welcome_surface,welcome_rect)
				else:
					SCREEN.blit(game_over_surface,game_over_rect)
		else:
			score_surface=score_font.render("Score: {}".format(current_score),False,(255,255,255))
			SCREEN.blit(score_surface,score_rect)

		floor.show(SCREEN)
		pygame.display.update()
		clock.tick(50)
