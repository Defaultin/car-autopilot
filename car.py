import pygame
from pygame.math import Vector2
from math import sin, radians, degrees, copysign


__all__ = ('Car')


class Car:
	'''Kinematic model of a car with radars for calculating distances to objects'''
	def __init__(self, *, spawn_position=(3.1, 3.0)):
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

		self.car_sprite = pygame.image.load('sprites/car0.png')

	def check_params(self):
		'''Checks if params are out of maximum ranges'''
		self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))
		self.acceleration = max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))
		self.steering = max(-self.max_steering, min(self.steering, self.max_steering))

	def move(self, direction, dt):
		'''Updates motion parameters according to the kinematics laws and the input direction of the car'''
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

	def draw(self, screen):
		'''Renders a car model'''
		rotated = pygame.transform.rotate(self.car_sprite, self.angle)
		rect = rotated.get_rect()
		screen.blit(rotated, 32 * self.position - (rect.width / 2, rect.height / 2))