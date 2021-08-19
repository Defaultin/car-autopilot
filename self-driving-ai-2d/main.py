from simulation import Simulation


def main():
    """
     ****** Running generation 99 ******

    Population's average fitness: 179.75563 stdev: 652.22002
    Best fitness: 3922.85129 - size: (2, 7) - species 22 - id 836
    Average adjusted fitness: 0.052
    Mean genetic distance 3.534, standard deviation 1.785
    Population of 35 members in 9 species:
       ID   age  size  fitness  adj fit  stag
      ====  ===  ====  =======  =======  ====
        11   83     3     -3.9    0.008    11
        22   52    10   3922.9    0.332     2
        31   17     4    151.9    0.040     2
        32   14     3    -10.4    0.005     6
        33   14     3    -10.4    0.007    11
        34   14     3     42.6    0.013     6
        35    9     3    131.9    0.037     1
        36    8     3     79.3    0.015     3
        37    4     3     81.4    0.016     1
    Total extinctions: 0
    Generation time: 17.703 sec (21.931 average)
    Saving checkpoint to checkpoints/self-driving-checkpoint-99
    """
    sim = Simulation(epochs=100, map_spread=(150, 350), map_complexity=5, time_per_map=3000)
    best = sim.train("self-driving.conf")
    sim.save(best)


if __name__ == '__main__':
    main()
