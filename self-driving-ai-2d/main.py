import pygame as pg
import sys
from highway import Highway
from car import Car


class Simulation:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Self-driving simulation')
        self.start = False
        self.window = 1320, 768
        self.width, self.height = self.window
        self.screen = pg.display.set_mode(self.window, pg.FULLSCREEN)
        self.clock = pg.time.Clock()
        self.highway = Highway((1320 // 2, 768 // 2), 300, complexity=5, width=50)
        self.car = Car(spawn_position=self.highway.start_position, spawn_angle=self.highway.start_angle)

    def run(self):
        while True:

            # events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit(0)
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:  # start simulation
                        self.start = True
                    elif event.key == pg.K_g:  # generate new highway
                        self.highway.generate()
                        self.car = Car(spawn_position=self.highway.start_position, spawn_angle=self.highway.start_angle)
                    elif event.key == pg.K_h:  # reset car position
                        self.car = Car(spawn_position=self.highway.start_position, spawn_angle=self.highway.start_angle)
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
            self.highway.draw(self.screen)
            self.car.move(car_movement, self.clock.get_time() * 0.01, self.screen, self.highway)
            self.car.draw(self.screen)

            pg.display.flip()
            self.clock.tick(0)

        pg.quit()


if __name__ == '__main__':
    Simulation().run()
