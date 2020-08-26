import pygame
from pygame.math import Vector2
from math import sqrt, sin, cos, radians, degrees, copysign
RATIO = 32


__all__ = ('Car')


class Car:
	'''Kinematic model of a car with radars for calculating distances to objects'''
	def __init__(self, *, spawn_position=(3.1, 3.0)):
		self.car_sprite = pygame.image.load('sprites/car0.png')
		self.angle = -90.0
		self.chassis_length = 2.0

		self.position = Vector2(*spawn_position)
		self.velocity = Vector2(0.0, 0.0)
		self.acceleration = 0.0
		self.steering = 0.0

		self.brake_deceleration = 10.0
		self.free_deceleration = 2.0

		self.max_velocity = 10.0
		self.max_acceleration = 5.0
		self.max_steering = 40.0

		self.is_alive = True
		self.start_distance = 0
		self.distance_score = 0
		self.movement_score = 0
		self.time_score = pygame.time.Clock().get_time()
		
		self.show_collision_points = False
		self.show_radars = False

	def compute_collision_points(self):
		'''Calculates collision points along the sides of the car'''
		rect = self.car_sprite.get_rect()
		w, h = rect.width / 2 - 5, rect.height / 2 - 10
		x, y = RATIO * self.position.x, RATIO * self.position.y
		old = [(x + w, y + h), (x + w, y - h), (x - w, y + h), (x - w, y - h)]
		sin_alpha = sin(radians(-self.angle))
		cos_alpha = cos(radians(-self.angle))

		self.collision_points = []
		for old_x, old_y in old:
			old_x, old_y = old_x - x, old_y - y
			new_x = x + old_x * cos_alpha - old_y * sin_alpha
			new_y = y + old_x * sin_alpha + old_y * cos_alpha
			self.collision_points.append((int(new_x), int(new_y)))

	def check_collision(self, parking):
		'''Checks for collisions and reduces score for collisions with grass and markings'''
		self.is_alive = True
		for point in self.collision_points:
			try:
				color = parking.background.get_at(point)
				if color == parking.grass_color:
					self.is_alive = False
					self.movement_score -= 100
					break
				elif color == parking.markup_color:
					self.movement_score -= 1
					break
			except IndexError:
				self.is_alive = False
				self.movement_score -= 100

	def compute_radars(self, screen, parking):
		'''Calculates radars and distances from car to parking facilities'''
		self.radars, self.radars_data = [], []
		center = int(RATIO * self.position.x), int(RATIO * self.position.y)
		car_angles = [radians(360 - self.angle - 45 * angle) for angle in range(9)]
		for angle in car_angles:
			length = 0
			while length <= 300:
				length += 1
				x = int(center[0] + length * cos(angle))
				y = int(center[1] + length * sin(angle))
				try:
					if not self.check_colors(screen.get_at((x, y)), parking): 
						break
				except IndexError:
					break

			self.radars.append((x, y))
			self.radars_data.append(length)

	def color_distance(self, *colors):
		'''Calculates distance between rgb colors'''
		return sqrt(sum(map(lambda a, b: (a - b) ** 2, *colors)))

	def check_colors(self, color, surface, *, limit=60):
		'''Checks that the surface color matches the colors allowed for driving'''
		return any([
					self.color_distance(color, surface.road_color) < limit,
					self.color_distance(color, surface.pointers_color) < limit,
					self.color_distance(color, surface.road_pointers_color) < limit
				])

	def compute_score(self, parking):
		'''Calculates reward as driving time, distance to target and current speed'''
		target = parking.get_target_position()
		target_distance = sqrt((RATIO * self.position.x - target[0]) ** 2 + (RATIO * self.position.y - target[1]) ** 2)

		self.movement_score += abs(self.velocity.x) * 0.1
		self.time_score -= 0.1

		if 5.6 <= self.position.x <= 6.3 and 15.6 <= self.position.y <= 20.6:
			self.start_distance = target_distance
		if self.start_distance:
			self.distance_score = -100 * target_distance / self.start_distance + 100

	def check_params(self):
		'''Checks if params are out of maximum ranges'''
		self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))
		self.acceleration = max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))
		self.steering = max(-self.max_steering, min(self.steering, self.max_steering))

	def move(self, direction, dt, screen, parking):
		'''Updates motion parameters according to the kinematics laws and the input direction of the car'''
		if self.is_alive:
			if direction[0] == 1: # forward
				if self.velocity.x < 0:
					self.acceleration = self.brake_deceleration
				else:
					self.acceleration += dt
			elif direction[0] == 0: # neutral
				if abs(self.velocity.x) > dt * self.free_deceleration:
					self.acceleration = -copysign(self.free_deceleration, self.velocity.x)
				else:
					if dt != 0:
						self.acceleration = -self.velocity.x / dt
			elif direction[0] == -1: #backward
				if self.velocity.x > 0:
					self.acceleration = -self.brake_deceleration
				else:
					self.acceleration -= dt
			
			if direction[1] == 1: # right
				self.steering -= self.max_steering * dt
			elif direction[1] == 0: # neutral
				self.steering = 0
			elif direction[1] == -1: #left
				self.steering += self.max_steering * dt

			self.velocity += (self.acceleration * dt, 0)
			self.check_params()

			if self.steering:
				turning_radius = self.chassis_length / sin(radians(self.steering))
				angular_velocity = self.velocity.x / turning_radius
			else:
				angular_velocity = 0

			self.position += self.velocity.rotate(-self.angle) * dt
			self.angle += degrees(angular_velocity) * dt

			self.compute_collision_points()
			self.check_collision(parking)
			self.compute_radars(screen, parking)
			self.compute_score(parking)

	def draw(self, screen):
		'''Renders a car model with radars and collision points'''
		if self.show_radars:
			center = RATIO * self.position.x, RATIO * self.position.y
			for coords in self.radars:
				pygame.draw.line(screen, (255, 140, 0), center, coords, 1)
				pygame.draw.circle(screen, (255, 140, 0), coords, 5)

		if self.show_collision_points:
			for coords in self.collision_points:
				if self.is_alive:
					pygame.draw.circle(screen, (15, 192, 252), coords, 5)
				else:
					pygame.draw.circle(screen, (255, 0, 0), coords, 5)

		rotated = pygame.transform.rotate(self.car_sprite, self.angle)
		rect = rotated.get_rect()
		screen.blit(rotated, RATIO * self.position - (rect.width / 2, rect.height / 2))