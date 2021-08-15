import pygame as pg
from random import randint, shuffle

__all__ = 'Parking'


class Parking:
	"""Parking lot with parking places and parked cars"""
	def __init__(self, *, spawn_cars=None):
		if spawn_cars is None:
			self.cars_num = randint(0, 63)
		elif 0 <= spawn_cars <= 63:
			self.cars_num = spawn_cars
		else:
			raise ValueError('There are only 63+1 parking places in the parking lot!')

		self.background = pg.image.load('sprites/parking.png')
		self.grass_color = 63, 155, 11, 255
		self.markup_color = 255, 255, 255, 255
		self.road_color = 80, 80, 80, 255
		self.pointers_color = 242, 188, 10, 255
		self.road_pointers_color = 161, 134, 45, 255
		self.spaces = {}
		self.cars_sprites = []
		self.parked_idxs = []
		self.target_idx = None
		self._init_parking()

	def _init_parking(self):
		"""Initializes parking elements"""

		# init parking spaces
		bottom_coords = [(243 + x, 658, 54, 98) for x in range(0, 901, 60)]
		right_coords = [(1197, 602 - y, 98, 54) for y in range(0, 481, 60)]
		top_coords = [(1143 - x, 24, 54, 98) for x in range(0, 841, 60)]
		left_coords = [(204, 122 + y, 98, 54) for y in range(0, 301, 60)]
		downcenter_coords = [(483 + x, 404, 54, 98) for x in range(0, 481, 60)]
		upcenter_coords = [(483 + x, 278, 54, 98) for x in range(0, 481, 60)]
		spaces_coords = bottom_coords + right_coords + top_coords + left_coords + downcenter_coords + upcenter_coords
		self.spaces = {k: v for k, v in zip(range(1, 65), spaces_coords)}

		# init cars sprites
		for i in range(64):
			sprite = pg.image.load('sprites/car' + str(i+1) + '.png')
			self.cars_sprites.append(sprite)

		# init parked cars and target space
		self.randomize()

	def randomize(self):
		"""Shuffles occupied parking spaces and target space"""
		random_spaces = list(self.spaces.keys())
		shuffle(random_spaces)
		self.target_idx = random_spaces[-1]
		self.parked_idxs = random_spaces[:self.cars_num]

	@staticmethod
	def get_center(place, car):
		"""Returns the center of a parking space relative to the car sprite"""
		return place[0] + place[2] / 2 - car.get_size()[0] / 2, place[1] + place[3] / 2 - car.get_size()[1] / 2

	def get_target_position(self):
		"""Returns the center of a target space"""
		x, y, w, h = self.spaces[self.target_idx]
		return x + w / 2, y + h / 2

	def draw(self, screen):
		"""Renders parked cars and target space"""
		pg.draw.rect(screen, self.pointers_color, self.spaces[self.target_idx], 5)
		for i in self.parked_idxs:
			car = self.cars_sprites[i-1]
			pos = self.spaces[i]
			screen.blit(car, self.get_center(pos, car))
