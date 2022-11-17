import pygame
from setting import *

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,groups,obsticle_sprites):
		super().__init__(groups)
		try:
			self.image = pygame.image.load('graphics/player.png').convert_alpha()
			self.rect = self.image.get_rect(topleft = pos)
			self.hitbox = self.rect.inflate(0,-26)
			self.direction = pygame.math.Vector2()
			self.speed = 5

			self.obsticle_sprites = obsticle_sprites
		except pygame.error as e:
			print(f"Unable to load sprtesheet image")
			raise SystemExit(e)

			

	def input(self):
		key = pygame.key.get_pressed()

		if key[pygame.K_UP]:
			self.direction.y = -1
		elif key[pygame.K_DOWN]:
			self.direction.y = 1
		else:
			self.direction.y = 0
		if key[pygame.K_RIGHT]:
			self.direction.x = 1
		elif key[pygame.K_LEFT]:
			self.direction.x = -1
		else:
			self.direction.x = 0
	
	def move(self,speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.hitbox.x += self.direction.x * speed
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * speed
		self.collision('verticle')
		self.rect.center = self.hitbox.center
		
		

	def collision(self,direction):
		if direction == 'horizontal':
			for sprite in self.obsticle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0:
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0:
						self.hitbox.left = sprite.hitbox.right

		if direction == 'verticle':
			for sprite in self.obsticle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y < 0:
						self.hitbox.top = sprite.hitbox.bottom
					if self.direction.y > 0:
						self.hitbox.bottom = sprite.hitbox.top

	def update(self):
		self.input()
		self.move(self.speed)
