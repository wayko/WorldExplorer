import pygame
from setting import *
from tile import Tile
from player import Player
from debug import debug
from support import *
class Level:
	def __init__(self):
		#get the display surface
		self.display_surface = pygame.display.get_surface()

		self.visible_sprites = YSortCamerGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		self.create_map()


	def create_map(self):
		layouts = {
				 'boundry' : import_csv_layout('graphics/levels/0/level_o._FloorBlocks.csv')
		}
		for style,layout in layouts.items():
			for row_index, row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'boundry':
							Tile((x,y), [self.obstacle_sprites], 'invisible')
		# 		if col == 'x':
		# 			Tile((x,y),[self.visible_sprites,self.obstacle_sprites])
		# 		if col == 'p':
		self.player = Player((1500,720),[self.visible_sprites],self.obstacle_sprites)

	def run(self):
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		

class YSortCamerGroup(pygame.sprite.Group):
	def __init__(self):

		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

		#creating floor

		self.floor_surf = pygame.image.load('graphics/levels/level_data/floor.png').convert()
		self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

	def custom_draw(self, player):
		#Getting the offset
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf,floor_offset_pos)

		#for sprite in self.sprites():
		for sprite in sorted(self.sprites(), key= lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)
