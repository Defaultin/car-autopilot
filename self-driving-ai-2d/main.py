from autopilot import Simulation


def main():
    sim = Simulation(epochs=100, map_spread=(150, 350), map_complexity=5, time_per_map=3000)

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
