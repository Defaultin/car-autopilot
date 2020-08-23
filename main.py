import sys
import pygame
from car import Car
from parking import Parking


class Simulation():
	def __init__(self, *, parked_cars=None):
		pygame.init()
		pygame.display.set_caption('Simulation')
		self.window = 1320, 768
		self.width, self.height = self.window
		self.start = False
		self.screen = pygame.display.set_mode(self.window, pygame.FULLSCREEN)
		self.background = pygame.image.load('sprites/parking.png')
		self.clock = pygame.time.Clock()
		self.parking = Parking(spawn_cars=parked_cars)
		self.car = Car()

	def draw_info(self):
		font = pygame.font.SysFont('Roboto', 40)
		label_color = 128, 0, 0

		label = font.render(f'Cars: {self.parking.cars_num}/63', True, label_color)
		label_rect = label.get_rect()
		label_rect.center = (120, self.height - 80)
		self.screen.blit(label, label_rect)

		label = font.render(f'Target: {self.parking.target_idx}', True, label_color)
		label_rect = label.get_rect()
		label_rect.center = (120, self.height - 50)
		self.screen.blit(label, label_rect)

	def run(self):
		while True:

			# events
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						self.start = True
					elif event.key == pygame.K_g:
						self.parking.randomize()
					elif event.key == pygame.K_ESCAPE:
						sys.exit(0)

			if not self.start:
				continue

			# inputs
			pressed = pygame.key.get_pressed()
			car_direction = [0, 0]

			if pressed[pygame.K_UP]:
				car_direction[0] = 1
			elif pressed[pygame.K_DOWN]:
				car_direction[0] = -1

			if pressed[pygame.K_RIGHT]:
				car_direction[1] = 1
			elif pressed[pygame.K_LEFT]:
				car_direction[1] = -1

			# logic
			self.car.move(car_direction, self.clock.get_time() * 0.001)

			# drawing
			self.screen.blit(self.background, (0, 0))
			self.parking.draw(self.screen)
			self.draw_info()
			self.car.draw(self.screen)

			pygame.display.flip()
			self.clock.tick(0)

		pygame.quit()


if __name__ == '__main__':
	Simulation().run()