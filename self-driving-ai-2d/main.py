import pygame as pg
import sys
import neat
from highway import Highway
from car import Car


class Simulation:
    """Self-driving car training on simulation with the random-generated highway map"""
    def __init__(self, epochs, time_per_map):
        pg.init()
        pg.display.set_caption('Self-driving simulation')
        self.window = 1320, 768
        self.width, self.height = self.window
        self.screen = pg.display.set_mode(self.window, pg.FULLSCREEN)
        self.clock = pg.time.Clock()

        self.highway = Highway((1320 // 2, 768 // 2), (250, 350), complexity=5, width=30)
        self.best_score = -float("inf")
        self.generations = epochs
        self.generation = 0
        self.map = 0
        self.time = 0
        self.time_per_map = time_per_map

    def draw_info(self, cars_left):
        """Renders training information as a text fields"""
        label_color = 75, 0, 130
        font = pg.font.SysFont('Comic Sans MS', 40)

        texts = [
            f'Map: {self.map}',
            f'Time: {self.time}',
            f'Cars: {cars_left}/{len(self.cars)}',
            f'Best score: {round(self.best_score)}',
            f'Epoch: {self.generation}/{self.generations}'
        ]

        for i, text in enumerate(texts[::-1]):
            label = font.render(text, True, label_color)
            label_rect = label.get_rect()
            label_rect.center = (160, self.height - 50 - 40 * i)
            self.screen.blit(label, label_rect)

    def init_new_generation(self, genomes, config):
        """Initializes new generation of networks and cars according to genomes"""
        self.nets, self.cars = [], []
        self.generation += 1

        for _, gen in genomes:
            gen.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(gen, config)
            car = Car(spawn_position=self.highway.start_position, spawn_angle=self.highway.start_angle, scale=0.5)
            self.nets.append(net)
            self.cars.append(car)

    def run_generation(self, genomes, config):
        """Controls the logic of car training on each generation simulation"""
        self.init_new_generation(genomes, config)

        while True:
            # events binding
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit(0)
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_g:  # generate new highway
                        self.highway.generate()
                        self.map += 1
                        self.time = 0
                        break
                    elif event.key == pg.K_j:  # show collision points
                        for car in self.cars:
                            car.show_collision_points = False if car.show_collision_points else True
                    elif event.key == pg.K_k:  # show collision radars
                        for car in self.cars:
                            car.show_radars = False if car.show_radars else True
                    elif event.key == pg.K_ESCAPE:  # exit simulation
                        sys.exit(0)

            # render map
            self.highway.draw(self.screen)

            cars_left = 0
            for net, car, gen in zip(self.nets, self.cars, genomes):
                # get movement params from network
                output = net.activate(car.radars_data)
                choice = output.index(max(output))

                # movement params mapping
                movement_params = dict()
                movement_params["direction"] = "forward"
                if choice == 0:
                    movement_params["rotation"] = "right"
                elif choice == 1:
                    movement_params["rotation"] = "neutral"
                elif choice == 2:
                    movement_params["rotation"] = "left"

                # move a car
                car.move(movement_params, self.clock.get_time() * 0.01, self.screen, self.highway)

                # update car fitness
                gen[1].fitness = car.score
                self.best_score = max(self.best_score, car.score)
                cars_left += 1 if car.is_alive else 0

            # render cars
            self.draw_info(cars_left)
            for car in self.cars:
                car.draw(self.screen)

            # check if cars or time left
            if not cars_left:
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

    def run(self):
        """Initializes NEAT from config and starts training process on simulation"""
        config_path = "self-driving.conf"
        config = neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_path
        )

        population = neat.Population(config)
        population.add_reporter(neat.StdOutReporter(True))
        population.add_reporter(neat.StatisticsReporter())
        population.add_reporter(neat.Checkpointer(10))
        population.run(self.run_generation, self.generations)


if __name__ == '__main__':
    Simulation(100, 1000).run()
