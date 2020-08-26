import sys
import pygame
from car import Car
from parking import Parking


class Simulation():
	def __init__(self, *, parked_cars=None):
		pygame.init()
		pygame.display.set_caption('Self-parking simulation')
		self.window = 1320, 768
		self.width, self.height = self.window
		self.start = False
		self.screen = pygame.display.set_mode(self.window, pygame.FULLSCREEN)
		self.clock = pygame.time.Clock()
		self.parking = Parking(spawn_cars=parked_cars)
		self.car = Car()

	def draw_info(self):
		label_color = 75, 0, 130
		font = pygame.font.SysFont('Roboto', 40)

		text = f'T/M/D: {round(self.car.time_score)}/{round(self.car.movement_score)}/{round(self.car.distance_score)}'
		label = font.render(text, True, label_color)
		label_rect = label.get_rect()
		label_rect.center = (120, self.height - 80)
		self.screen.blit(label, label_rect)

		text = f'Score: {round(self.car.time_score + self.car.movement_score + self.car.distance_score)}'
		label = font.render(text, True, label_color)
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
					if event.key == pygame.K_SPACE: # start simulation
						self.start = True
					elif event.key == pygame.K_g: # shuffle parked cars
						self.parking.randomize()
					elif event.key == pygame.K_h: # reset car position
						self.car = Car()
					elif event.key == pygame.K_j: # show collision points
						self.car.show_collision_points = False if self.car.show_collision_points else True
					elif event.key == pygame.K_k: # show collision radars 
						self.car.show_radars = False if self.car.show_radars else True
					elif event.key == pygame.K_ESCAPE: # exit simulation
						sys.exit(0)

			if not self.start:
				continue

			# car control inputs
			pressed = pygame.key.get_pressed()
			car_direction = [0, 0]

			if pressed[pygame.K_w]:
				car_direction[0] = 1
			elif pressed[pygame.K_s]:
				car_direction[0] = -1

			if pressed[pygame.K_d]:
				car_direction[1] = 1
			elif pressed[pygame.K_a]:
				car_direction[1] = -1

			# drawing and car logic
			self.screen.blit(self.parking.background, (0, 0))
			self.parking.draw(self.screen)
			self.draw_info()
			self.car.move(car_direction, self.clock.get_time() * 0.001, self.screen, self.parking)
			self.car.draw(self.screen)

			pygame.display.flip()
			self.clock.tick(0)

		pygame.quit()



if __name__ == '__main__':
	Simulation().run()