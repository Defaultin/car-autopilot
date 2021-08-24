from autopilot import Simulation


def main():
    """"""
    sim = Simulation(epochs=1000, time_per_map=200)

    # Train autopilot on simulation environment
    best_genome = sim.train()
    sim.save(best_genome)

    # Test simulation environment with autopilot
    # best_genome = sim.load("checkpoints/best.pkl")
    # sim.test(best_genome)

    # Test simulation environment without autopilot
    # sim.test()


if __name__ == '__main__':
    main()
