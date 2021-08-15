import sys
import pygame as pg
from car import Car
from parking import Parking


class Simulation:
    def __init__(self, *, parked_cars=None):
        pg.init()
        pg.display.set_caption('Self-parking simulation')
        self.window = 1320, 768
        self.width, self.height = self.window
        self.start = False
        self.screen = pg.display.set_mode(self.window, pg.FULLSCREEN)
        self.clock = pg.time.Clock()
        self.parking = Parking(spawn_cars=parked_cars)
        self.car = Car(spawn_position=(60, 70), spawn_angle=-90)

    def draw_info(self):
        label_color = 75, 0, 130
        font = pg.font.SysFont('Roboto', 40)

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
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit(0)
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:  # start simulation
                        self.start = True
                    elif event.key == pg.K_g:  # shuffle parked cars
                        self.parking.randomize()
                        self.car = Car(spawn_position=(60, 70), spawn_angle=-90)
                    elif event.key == pg.K_h:  # reset car position
                        self.car = Car(spawn_position=(60, 70), spawn_angle=-90)
                    elif event.key == pg.K_j:  # show collision points
                        self.car.show_collision_points = False if self.car.show_collision_points else True
                    elif event.key == pg.K_k:  # show collision radars
                        self.car.show_radars = False if self.car.show_radars else True
                    elif event.key == pg.K_ESCAPE:  # exit simulation
                        sys.exit(0)

            if not self.start:
                continue

            # car control inputs
            pressed = pg.key.get_pressed()
            car_movement = {"direction": "neutral", "rotation": "neutral"}

            if pressed[pg.K_w]:
                car_movement["direction"] = "forward"
            elif pressed[pg.K_s]:
                car_movement["direction"] = "backward"
            else:
                car_movement["direction"] = "neutral"

            if pressed[pg.K_d]:
                car_movement["rotation"] = "right"
            elif pressed[pg.K_a]:
                car_movement["rotation"] = "left"
            else:
                car_movement["rotation"] = "neutral"

            # rendering
            self.screen.blit(self.parking.background, (0, 0))
            self.parking.draw(self.screen)
            self.draw_info()
            self.car.move(car_movement, self.clock.get_time() * 0.01, self.screen, self.parking)
            self.car.draw(self.screen)

            pg.display.flip()
            self.clock.tick(0)

        pg.quit()


if __name__ == '__main__':
    Simulation().run()
