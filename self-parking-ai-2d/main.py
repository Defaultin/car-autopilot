from simulation import Simulation


def main():
    sim = Simulation(epochs=1000, time_per_map=5000)
    sim.test()


if __name__ == '__main__':
    main()
