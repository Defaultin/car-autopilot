from simulation import Simulation


def main():
    sim = Simulation(epochs=1000, time_per_map=500)
    best = sim.train("self-parking.conf")
    sim.save(best)


if __name__ == '__main__':
    main()
