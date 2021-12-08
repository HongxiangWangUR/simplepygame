import pygame
from pygame.locals import *
pygame.init()

class person(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()

group=pygame.sprite.Group()
group.add(person())