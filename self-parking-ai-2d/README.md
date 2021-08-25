# Self-parking AI

Autopilot model trained using NeuroEvolution of Augmenting Topologies ([NEAT](https://github.com/Defaultin/car-autopilot/blob/master/papers/neat.pdf)) on randomly generated parking lot in a 2D simulation.

---

## Autopilot Demo

### Train process

https://user-images.githubusercontent.com/50778301/130321844-fb652aeb-89e4-4e70-9c27-3852d542830a.mp4

### Test process

https://user-images.githubusercontent.com/50778301/130618597-903dbfd0-5d80-4e6f-a0e3-40eee2f0fe2d.mp4

---

## Parking Lot

Cars are randomly placed on the parking lot and a target spot for subsequent parking is selected.

![](https://github.com/Defaultin/car-autopilot/blob/master/self-parking-ai-2d/autopilot/sprites/small-parking.png "Small parking")
![](https://github.com/Defaultin/car-autopilot/blob/master/self-parking-ai-2d/autopilot/sprites/large-parking.png "Large parking")

---

## Car

* Сar model is described in terms of acceleration, velocity, steering, and position according to kinematical laws.
* Сar model has 4 sensors which determine collisions with obstacles while driving.
* Сar model has 8 radars which determine position of obstacles and distance to them.

![](https://github.com/Defaultin/car-autopilot/blob/master/self-parking-ai-2d/demo/car-model.png "Car model")

---

## Simulation

* Population of models is initialized and evolves according to the specified [configurations](https://github.com/Defaultin/car-autopilot/blob/master/self-parking-ai-2d/autopilot/self-parking.conf).
* Normalized distances to obstacles from each radar, navigation movements and current distance to target parking spot are fed to the neural network inputs.
* Outputs of the neural network are the direction and rotation parameters of the car.
* Each model of a generation is rewarded for the closest distance to the target parking spot and penalized for colliding with obstacles, crossing road markings and idle time.

![](https://github.com/Defaultin/car-autopilot/blob/master/self-parking-ai-2d/demo/neat-model-new.png "NEAT model")

---

## Usage

### Train autopilot on simulation environment
```python
from autopilot import Simulation

sim = Simulation(epochs=1000, time_per_map=500)
best_genome = sim.train()
sim.save(best_genome)
```

### Test simulation environment with autopilot
```python
from autopilot import Simulation

sim = Simulation()
best_genome = sim.load("checkpoints/best.pkl")
sim.test(best_genome)
```

### Test simulation environment without autopilot
```python
from autopilot import Simulation

sim = Simulation()
sim.test()
```

---

## Dependencies

```bash
$ pip3 install -r self-parking-ai-2d/requirements.txt
```

* neat-python
* numpy
* pygame
