import sys
import neat
import pickle
import pygame as pg
from car import Car
from parking import Parking


class Simulation:
    """Self-driving car training on simulation with the random-generated parking map"""
    def __init__(self, epochs=10000, parked_cars=None, time_per_map=5000):
        pg.init()
        pg.display.set_caption('Self-parking simulation')
        self.window = 1320, 768
        self.width, self.height = self.window
        self.screen = pg.display.set_mode(self.window, pg.FULLSCREEN)
        self.clock = pg.time.Clock()

        self.parking = Parking(spawn_cars=parked_cars)
        self.best_score = -float("inf")
        self.time_per_map = time_per_map
        self.generations = epochs
        self.generation = 0
        self.map = 0
        self.time = 0
        self.cars_left = 0

    def _draw_info(self, car=None):
        """Renders training information as a text fields"""
        if car:
            texts = [
                f"Speed: {round(car.velocity.x, 2)}",
                f"Boost: {round(car.acceleration, 2)}",
                f"Rudder: {round(car.steering, 2)}",
                f"Score: {round(car.score, 2)}"
            ]
        else:
            texts = [
                f"Map: {self.map}",
                f"Time: {self.time}",
                f"Cars: {self.cars_left}/{len(self.cars)}",
                f"Best score: {round(self.best_score)}",
                f"Epoch: {self.generation}/{self.generations}"
            ]

        label_color = 75, 0, 130
        font = pg.font.SysFont("Comic Sans MS", 40)
        for i, text in enumerate(texts[::-1]):
            label = font.render(text, True, label_color)
            label_rect = label.get_rect()
            label_rect.center = (160, self.height - 50 - 40 * i)
            self.screen.blit(label, label_rect)

    def _init_new_generation(self, genomes, config):
        """Initializes new generation of networks and cars according to genomes"""
        self.nets, self.cars = [], []
        self.generation += 1

        for _, gen in genomes:
            gen.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(gen, config)
            car = Car(spawn_position=(100, 70), spawn_angle=-90)
            self.nets.append(net)
            self.cars.append(car)

    def _run_generation(self, genomes, config):
        """Controls the logic of car training on each generation simulation"""
        pass

    def train(self):
        pass

    def test(self):
        car = Car(spawn_position=(100, 70), spawn_angle=-90)

        while True:
            # events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit(0)
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_g:         # shuffle parked cars
                        self.parking.randomize()
                        car = Car(spawn_position=(100, 70), spawn_angle=-90)
                    elif event.key == pg.K_h:       # reset car position
                        car = Car(spawn_position=(100, 70), spawn_angle=-90)
                    elif event.key == pg.K_j:       # show collision points
                        car.show_collision_points = False if car.show_collision_points else True
                    elif event.key == pg.K_k:       # show collision radars
                        car.show_radars = False if car.show_radars else True
                    elif event.key == pg.K_ESCAPE:  # exit simulation
                        sys.exit(0)

            # keyboard inputs
            pressed = pg.key.get_pressed()
            movement_params = dict()

            if pressed[pg.K_UP] or pressed[pg.K_w]:
                movement_params["direction"] = "forward"
            elif pressed[pg.K_DOWN] or pressed[pg.K_s]:
                movement_params["direction"] = "backward"
            else:
                movement_params["direction"] = "neutral"

            if pressed[pg.K_RIGHT] or pressed[pg.K_d]:
                movement_params["rotation"] = "right"
            elif pressed[pg.K_LEFT] or pressed[pg.K_a]:
                movement_params["rotation"] = "left"
            else:
                movement_params["rotation"] = "neutral"

            # car movement logic
            self.screen.blit(self.parking.background, (0, 0))
            self.parking.draw(self.screen)
            car.move(movement_params, self.clock.get_time() * 0.01, self.screen, self.parking)
            car.draw(self.screen)
            self._draw_info(car)
            pg.display.flip()
            self.clock.tick(0)

    @staticmethod
    def save(genome):
        with open("checkpoints/best.pickle", "wb") as f:
            pickle.dump(genome, f)

    @staticmethod
    def load(file):
        with open(file, "rb") as f:
            return pickle.load(f)
