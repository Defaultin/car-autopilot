import sys
import neat
import pickle
import numpy as np
import pygame as pg
from autopilot.highway import Highway
from autopilot.car import Car

__all__ = "Simulation"


class Simulation:
    """Self-driving car training on simulation with the random-generated highway map"""
    def __init__(self, epochs=10000, map_spread=(150, 350), map_complexity=5, time_per_map=10000):
        pg.init()
        pg.display.set_caption("Self-driving simulation")
        self.window = 1320, 768
        self.width, self.height = self.window
        self.screen = pg.display.set_mode(self.window, pg.FULLSCREEN)
        self.clock = pg.time.Clock()

        self.highway = Highway((self.width // 2, self.height // 2), map_spread, map_complexity, width=30)
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
                f"Cars: {self.cars_left}/{len(self.cars)}",
                f"Time: {self.time}/{self.time_per_map}",
                f"Best score: {round(self.best_score)}",
                f"Epoch: {self.generation}/{self.generations}"
            ]

        label_color = 75, 0, 130
        font = pg.font.SysFont("Comic Sans MS", 20)
        for i, text in enumerate(texts[::-1]):
            label = font.render(text, True, label_color)
            label_rect = label.get_rect()
            label_rect.center = (120, self.height - 40 - 20 * i)
            self.screen.blit(label, label_rect)

    def _init_new_generation(self, genomes, config):
        """Initializes new generation of networks and cars according to genomes"""
        self.nets, self.cars = [], []
        self.best_score = 0
        self.generation += 1

        for _, gen in genomes:
            gen.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(gen, config)
            car = Car(spawn_position=self.highway.start_position, spawn_angle=self.highway.start_angle, scale=0.5)
            self.nets.append(net)
            self.cars.append(car)

    def _run_generation(self, genomes, config):
        """Controls the logic of car training on each generation simulation"""
        self._init_new_generation(genomes, config)

        while True:
            # events binding
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit(0)
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_g:         # generate new highway
                        self.highway.generate()
                        self.map += 1
                        self.time = 0
                        return
                    elif event.key == pg.K_j:       # show collision points
                        for car in self.cars:
                            car.show_collision_points = False if car.show_collision_points else True
                    elif event.key == pg.K_k:       # show collision radars
                        for car in self.cars:
                            car.show_radars = False if car.show_radars else True
                    elif event.key == pg.K_l:       # show score
                        for car in self.cars:
                            car.show_score = False if car.show_score else True
                    elif event.key == pg.K_ESCAPE:  # exit simulation
                        sys.exit(0)

            # render highway map
            self.highway.draw(self.screen)

            self.cars_left = 0
            for net, car, gen in zip(self.nets, self.cars, genomes):
                # get movement params from network
                output = net.activate(np.append(car.radars_data, car.velocity.x / car.max_velocity))

                # movement params mapping
                direction, rotation = [0 if -0.33 < out < 0.33 else np.sign(out) for out in output]
                movement_params = {"direction": direction, "rotation": rotation}

                # move a car
                t = self.clock.get_time() * 0.01
                car.move(movement_params, t, self.screen, self.highway)

                # update car fitness
                self.best_score = max(self.best_score, car.score)
                gen[1].fitness = car.score
                self.cars_left += 1 if car.is_alive else 0

            # render cars
            self._draw_info()
            for car in self.cars:
                car.draw(self.screen)

            # check if cars or time left to continue
            if not self.cars_left:
                break
            elif self.time > self.time_per_map:
                self.highway.generate()
                self.map += 1
                self.time = 0
                break
            else:
                self.time += 1
                pg.display.flip()
                self.clock.tick(0)

    def train(self, config_file="autopilot/self-driving.conf"):
        """Initializes NEAT from config and starts training process on simulation"""
        config = neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_file
        )

        population = neat.Population(config)
        population.add_reporter(neat.StdOutReporter(True))
        population.add_reporter(neat.StatisticsReporter())
        population.add_reporter(neat.Checkpointer(10, filename_prefix="checkpoints/self-driving-checkpoint-"))

        return population.run(self._run_generation, self.generations)

    def test(self, genome=None, config_file="autopilot/self-driving.conf"):
        """Tests simulation environment"""
        car = Car(self.highway.start_position, self.highway.start_angle, scale=0.5)
        if genome:
            config = neat.config.Config(
                neat.DefaultGenome,
                neat.DefaultReproduction,
                neat.DefaultSpeciesSet,
                neat.DefaultStagnation,
                config_file
            )
            autopilot = neat.nn.FeedForwardNetwork.create(genome, config)
        else:
            autopilot = None

        while True:
            # events binding
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit(0)
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_g:         # generate new highway
                        self.highway.generate()
                        car = Car(self.highway.start_position, self.highway.start_angle, scale=0.5)
                    elif event.key == pg.K_h:       # reset car position
                        car = Car(self.highway.start_position, self.highway.start_angle, scale=0.5)
                    elif event.key == pg.K_j:       # show collision points
                        car.show_collision_points = False if car.show_collision_points else True
                    elif event.key == pg.K_k:       # show collision radars
                        car.show_radars = False if car.show_radars else True
                    elif event.key == pg.K_l:       # show score
                        car.show_score = False if car.show_score else True
                    elif event.key == pg.K_ESCAPE:  # exit simulation
                        sys.exit(0)

            # keyboard inputs
            if autopilot:
                output = autopilot.activate(np.append(car.radars_data, car.velocity.x / car.max_velocity))
                direction, rotation = [0 if -0.33 < out < 0.33 else np.sign(out) for out in output]
            else:
                pressed = pg.key.get_pressed()
                if pressed[pg.K_UP] or pressed[pg.K_w]:
                    direction = "forward"
                elif pressed[pg.K_DOWN] or pressed[pg.K_s]:
                    direction = "backward"
                else:
                    direction = "neutral"

                if pressed[pg.K_RIGHT] or pressed[pg.K_d]:
                    rotation = "right"
                elif pressed[pg.K_LEFT] or pressed[pg.K_a]:
                    rotation = "left"
                else:
                    rotation = "neutral"

            # car movement logic
            self.highway.draw(self.screen)
            movement_params = {"direction": direction, "rotation": rotation}
            car.move(movement_params, self.clock.get_time() * 0.01, self.screen, self.highway)
            car.draw(self.screen)
            self._draw_info(car)
            pg.display.flip()
            self.clock.tick(0)

    @staticmethod
    def save(genome):
        """Dumps genome configuration to file"""
        with open("checkpoints/best.pkl", "wb") as f:
            pickle.dump(genome, f)

    @staticmethod
    def load(file):
        """Loads genome configuration for file"""
        with open(file, "rb") as f:
            return pickle.load(f)
