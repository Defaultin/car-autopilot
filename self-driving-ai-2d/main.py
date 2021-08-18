from simulation import Simulation


def main():
    sim = Simulation(epochs=1000, map_spread=(150, 350), map_complexity=5, time_per_map=5000)
    best = sim.train("self-driving.conf")
    sim.save(best)


if __name__ == '__main__':
    main()
