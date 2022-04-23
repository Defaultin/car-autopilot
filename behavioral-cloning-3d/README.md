# Self-Driving AI

Autopilot deep learning model trained based on behavioral cloning metodology using Udacity's self driving car 3D [simulator](https://github.com/udacity/self-driving-car-sim)

---

## Project structure

| File           | Description                                                                                                                    |
| :------------: | ------------------------------------------------------------------------------------------------------------------------------ |
| `data.py`      | Methods related to data augmentation, preprocessing and batching                                                               |
| `model.py`     | Implements model architecture and runs the training pipeline                                                                   |
| `model.json`   | JSON file containing model architecture                                                                                        |
| `model.h5`     | H5 file containing model weights                                                                                               |
| `drive.py`     | Callbacks for communication with the driving app providing model predictions based on real-time data simulator app is sending  |

---

## Autopilot Model 

![](https://github.com/Defaultin/car-autopilot/blob/master/behavioral-cloning-3d/demo/model.png "Model")

```python
from keras import models
from keras.layers import core, convolutional, pooling

model = models.Sequential()
model.add(convolutional.Convolution2D(16, 3, 3, input_shape=(32, 128, 3), activation='relu'))
model.add(pooling.MaxPooling2D(pool_size=(2, 2)))
model.add(convolutional.Convolution2D(32, 3, 3, activation='relu'))
model.add(pooling.MaxPooling2D(pool_size=(2, 2)))
model.add(convolutional.Convolution2D(64, 3, 3, activation='relu'))
model.add(pooling.MaxPooling2D(pool_size=(2, 2)))
model.add(core.Flatten())
model.add(core.Dense(500, activation='relu'))
model.add(core.Dense(100, activation='relu'))
model.add(core.Dense(20, activation='relu'))
model.add(core.Dense(1))
``` 

---

## Autopilot Demo

<p align="center">
  <img src="demo/demo.mp4" alt="Autopilot Demo"/>
</p>
