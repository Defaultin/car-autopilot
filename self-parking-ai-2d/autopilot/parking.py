import pygame as pg
from random import randint, shuffle

__all__ = "SmallParking", "LargeParking"


class SmallParking:
	"""Small parking lot with parking places and parked cars"""
	CAPACITY = 54

	def __init__(self, spawn_cars=None):
		if spawn_cars is None:
			self.cars_num = randint(0, self.CAPACITY - 1)
		elif 0 <= spawn_cars < self.CAPACITY:
			self.cars_num = spawn_cars
		else:
			raise ValueError(f"There are only {self.CAPACITY-1}+1 parking places in the parking lot!")

		self.background = pg.image.load("autopilot/sprites/small-parking.png")
		self.grass_color = 63, 155, 11, 255
		self.markup_color = 255, 255, 255, 255
		self.road_color = 80, 80, 80, 255
		self.pointers_color = 242, 188, 10, 255
		self.road_pointers_color = 161, 134, 45, 255

		self.spaces = {}
		self.cars_sprites = []
		self.parked_idxs = []
		self.target_idx = None
		self.target_position = None
		self.start_angle = 0
		self.start_position = 660, 384

		self._init_parking()

	def _init_parking(self):
		"""Initializes parking elements"""

		# init parking spaces
		bottom_coords = [(123 + x, 659, 54, 98) for x in range(0, 1021, 60)]
		top_coords = [(1143 - x, 23, 54, 98) for x in range(0, 1021, 60)]
		right_coords = [(1199, 603 - y, 98, 54) for y in range(0, 481, 60)]
		left_coords = [(24, 123 + y, 98, 54) for y in range(0, 481, 60)]
		spaces_coords = bottom_coords + right_coords + top_coords + left_coords
		self.spaces = {idx: coord for idx, coord in zip(range(self.CAPACITY), spaces_coords)}

		# init cars sprites
		for i in range(self.CAPACITY):
			if 0 <= i <= 17:
				angle = 90
			elif 18 <= i <= 26:
				angle = 180
			elif 27 <= i <= 44:
				angle = 270
			else:
				angle = 0

			sprite = pg.image.load("autopilot/sprites/car" + str(i + 1) + ".png")
			self.cars_sprites.append(pg.transform.rotate(sprite, angle))

		# init parked cars and target space
		self.randomize()

	def randomize(self):
		"""Shuffles occupied parking spaces and target space"""
		random_spaces = list(self.spaces.keys())
		shuffle(random_spaces)
		self.target_idx = random_spaces[-1]
		self.parked_idxs = random_spaces[:self.cars_num]
		x, y, w, h = self.spaces[self.target_idx]
		self.target_position = x + w / 2, y + h / 2
		self.start_angle = randint(0, 360)
		self.start_position = randint(396, 924), randint(230, 538)

	@staticmethod
	def get_center(place, car):
		"""Returns the center of a parking space relative to the car sprite"""
		return place[0] + place[2] / 2 - car.get_size()[0] / 2, place[1] + place[3] / 2 - car.get_size()[1] / 2

	def draw(self, screen):
		"""Renders parked cars and target space"""
		screen.blit(self.background, (0, 0))
		pg.draw.rect(screen, self.pointers_color, self.spaces[self.target_idx], 5)
		for i in self.parked_idxs:
			pos = self.spaces[i]
			car = self.cars_sprites[i]
			screen.blit(car, self.get_center(pos, car))


class LargeParking:
	"""Large parking lot with parking places and parked cars"""
	CAPACITY = 64

	def __init__(self, spawn_cars=None):
		if spawn_cars is None:
			self.cars_num = randint(0, self.CAPACITY - 1)
		elif 0 <= spawn_cars < self.CAPACITY:
			self.cars_num = spawn_cars
		else:
			raise ValueError(f"There are only {self.CAPACITY - 1}+1 parking places in the parking lot!")

		self.background = pg.image.load("autopilot/sprites/large-parking.png")
		self.grass_color = 63, 155, 11, 255
		self.markup_color = 255, 255, 255, 255
		self.road_color = 80, 80, 80, 255
		self.pointers_color = 242, 188, 10, 255
		self.road_pointers_color = 161, 134, 45, 255

		self.spaces = {}
		self.cars_sprites = []
		self.parked_idxs = []
		self.target_idx = None
		self.target_position = None
		self.start_angle = 0
		self.start_position = 100, 580
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
		self.spaces = {idx: coord for idx, coord in zip(range(self.CAPACITY), spaces_coords)}

		# init cars sprites
		for i in range(self.CAPACITY):
			if 0 <= i <= 15 or 46 <= i <= 54:
				angle = 90
			elif 16 <= i <= 24:
				angle = 180
			elif 25 <= i <= 39 or 55 <= i <= 63:
				angle = 270
			else:
				angle = 0

			sprite = pg.image.load("autopilot/sprites/car" + str(i + 1) + ".png")
			self.cars_sprites.append(pg.transform.rotate(sprite, angle))

		# init parked cars and target space
		self.randomize()

	def randomize(self):
		"""Shuffles occupied parking spaces and target space"""
		random_spaces = list(self.spaces.keys())
		shuffle(random_spaces)
		self.target_idx = random_spaces[-1]
		self.parked_idxs = random_spaces[:self.cars_num]
		x, y, w, h = self.spaces[self.target_idx]
		self.target_position = x + w / 2, y + h / 2

	@staticmethod
	def get_center(place, car):
		"""Returns the center of a parking space relative to the car sprite"""
		return place[0] + place[2] / 2 - car.get_size()[0] / 2, place[1] + place[3] / 2 - car.get_size()[1] / 2

	def draw(self, screen):
		"""Renders parked cars and target space"""
		screen.blit(self.background, (0, 0))
		pg.draw.rect(screen, self.grass_color, (20, 20, 160, 481), 0)
		pg.draw.rect(screen, self.markup_color, (20, 20, 160, 481), 5)
		pg.draw.rect(screen, self.pointers_color, self.spaces[self.target_idx], 5)
		for i in self.parked_idxs:
			pos = self.spaces[i]
			car = self.cars_sprites[i]
			screen.blit(car, self.get_center(pos, car))
