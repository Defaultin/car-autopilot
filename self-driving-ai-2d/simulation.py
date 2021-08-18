import sys
import neat
import pickle
import pygame as pg
from highway import Highway
from car import Car

__all__ = "Simulation"


class Simulation:
    """Self-driving car training on simulation with the random-generated highway map"""
    def __init__(self, epochs=10000, map_spread=(150, 350), map_complexity=5, time_per_map=5000):
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
                f"Time: {self.time}/{self.time_per_map}",
                f"Cars: {self.cars_left}/{len(self.cars)}",
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
                    elif event.key == pg.K_ESCAPE:  # exit simulation
                        sys.exit(0)

            # render highway map
            self.highway.draw(self.screen)

            self.cars_left = 0
            for net, car, gen in zip(self.nets, self.cars, genomes):
                # get movement params from network
                output = net.activate(car.radars_data)

                # movement params mapping
                direction, rotation = divmod(output.index(max(output)), 3)
                movement_params = {"direction": "forward", "rotation": rotation - 1}

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

    def train(self, config_file):
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

    def test(self):
        """Tests simulation environment"""
        car = Car(self.highway.start_position, self.highway.start_angle, scale=0.5)

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
            self.highway.draw(self.screen)
            car.move(movement_params, self.clock.get_time() * 0.01, self.screen, self.highway)
            car.draw(self.screen)
            self._draw_info(car)
            pg.display.flip()
            self.clock.tick(0)

    @staticmethod
    def save(genome):
        """Dumps genome configuration to file"""
        with open("checkpoints/best.pickle", "wb") as f:
            pickle.dump(genome, f)

    @staticmethod
    def load(file):
        """Loads genome configuration for file"""
        with open(file, "rb") as f:
            return pickle.load(f)
