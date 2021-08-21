# Self-parking AI

Autopilot model trained using NeuroEvolution of Augmenting Topologies ([NEAT](https://github.com/Defaultin/car-autopilot/blob/master/papers/neat.pdf)) on on randomly generated parking lot in a 2D simulation.

---

## Autopilot Demo

### Train process
https://user-images.githubusercontent.com/50778301/130317126-05031708-a00b-4a59-b427-0fdbe1dc7393.mp4

### Test process
https://user-images.githubusercontent.com/50778301/130317082-910b5248-8bde-4d65-a882-f3db897f6f6c.mp4

---

## Parking Lot



---

## Car

* Сar model is described in terms of acceleration, velocity, steering, and position according to kinematic laws.
* Сar model has 4 sensors which determine collisions with obstacles while driving.
* Сar model has 8 radars which determine position of obstacles and distance to them.

![](https://github.com/Defaultin/car-autopilot/blob/master/self-parking-ai-2d/demo/car-model.png "Car model")

---

## Simulation

* Population of models is initialized and evolves according to the specified [configurations](https://github.com/Defaultin/car-autopilot/blob/master/self-parking-ai-2d/autopilot/self-parking.conf).
* Normalized distances to obstacles from each radar and current distance to target parking spot are fed to the neural network inputs.
* Outputs of the neural network are the direction and rotation parameters of the car.
* Each model of a generation is rewarded for the closest distance to the target parking spot and penalized for colliding with obstacles, crossing road markings and idle time.

![](https://github.com/Defaultin/car-autopilot/blob/master/self-parking-ai-2d/demo/neat-model.png "NEAT model")

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
$ pip3 install -r self-driving-ai-2d/requirements.txt
```

* neat-python
* numpy
* pygame
* scipy
