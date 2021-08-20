from simulation import Simulation


def main():
    """
        ****** Running generation 99 ******

    Population's average fitness: 147.95706 stdev: 615.36547
    Best fitness: 2974.53187 - size: (5, 7) - species 39 - id 1106
    Average adjusted fitness: 0.064
    Mean genetic distance 2.556, standard deviation 0.808
    Population of 32 members in 8 species:
       ID   age  size  fitness  adj fit  stag
      ====  ===  ====  =======  =======  ====
        33   26     2     38.5    0.021     2
        38   12     3    -13.5    0.019     7
        39   12     9   2974.5    0.112     7
        40    6     3     31.5    0.028     4
        41    6     3    -13.5    0.019     1
        42    4     3    -13.5    0.013     1
        43    3     8   1987.5    0.235     0
        44    0     1       --       --     0
    Total extinctions: 0
    Generation time: 59.423 sec (52.256 average)
    """
    sim = Simulation(epochs=100, map_spread=(150, 350), map_complexity=5, time_per_map=3000)

    # Train autopilot on simulation environment
    best_genome = sim.train("self-driving.conf")
    sim.save(best_genome)

    # Test simulation environment with autopilot
    # best_genome = sim.load("checkpoints/best.pkl")
    # sim.test(best_genome, "self-driving.conf")

    # Test simulation environment without autopilot
    # sim.test()


if __name__ == '__main__':
    main()
