# Self-driving AI

Autopilot model trained using NeuroEvolution of Augmenting Topologies ([NEAT](https://github.com/Defaultin/car-autopilot/blob/master/papers/neat.pdf)) on on randomly generated highways in a 2D simulation.

---

## Demo

### Train process
![Train process](https://user-images.githubusercontent.com/50778301/130316936-ae71e6c5-3ba8-41b8-9f7f-c4bc9909e923.mp4)

### Test process
![Train process](https://github.com/Defaultin/car-autopilot/blob/master/self-driving-ai-2d/demo/test-demo.mp4)

---

## Highway

---

## Car

---

## Simulation

---

## Usage

### Train autopilot on simulation environment
```python
from autopilot import Simulation

sim = Simulation(epochs=100, map_spread=(150, 350), map_complexity=5, time_per_map=3000)
best_genome = sim.train()
sim.save(best_genome)
```

### Test simulation environment with autopilot
```python
sim = Simulation(map_spread=(150, 350), map_complexity=5)
best_genome = sim.load("checkpoints/best.pkl")
sim.test(best_genome)
```

### Test simulation environment without autopilot
```python
sim = Simulation(map_spread=(150, 350), map_complexity=5)
sim.test()
```

---

## Dependencies

* neat-python
* numpy
* pygame
* scipy

```bash
$ pip3 install -r self-driving-ai-2d/requirements.txt
```
