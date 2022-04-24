import os
import numpy as np
import skimage.transform as sktransform
import random
import matplotlib.image as mpimg


cameras = ["left", "center", "right"]
cameras_steering_correction = [.25, 0., -.25]


def preprocess(image, top_offset=.375, bottom_offset=.125):
    length = image.shape[0]
    top = int(top_offset * length)
    bottom = int(bottom_offset * length)
    image = sktransform.resize(image[top:-bottom, :], (32, 128, 3))
    return image


def generate_samples(data, root_path, augment=True, batch_size=128):
    while True:
        indices = np.random.permutation(data.count()[0])
        for batch in range(0, len(indices), batch_size):
            batch_indices = indices[batch:(batch + batch_size)]
            x = np.empty([0, 32, 128, 3], dtype=np.float32)
            y = np.empty([0], dtype=np.float32)

            for i in batch_indices:
                camera = np.random.randint(len(cameras)) if augment else 1
                image = mpimg.imread(os.path.join(root_path, data[cameras[camera]].values[i].strip()))
                angle = data.steering.values[i] + cameras_steering_correction[camera]

                if augment:
                    h, w = image.shape[0], image.shape[1]
                    x1, x2 = np.random.choice(w, 2, replace=False)
                    k = h / (x2 - x1)
                    b = -k * x1
                    for i in range(h):
                        c = (i - b) // k
                        image[i, :c, :] = (image[i, :c, :] * .5).astype(np.int32)

                v_delta = .05 if augment else 0
                image = preprocess(
                    image,
                    top_offset=random.uniform(.375 - v_delta, .375 + v_delta),
                    bottom_offset=random.uniform(.125 - v_delta, .125 + v_delta)
                )

                x = np.append(x, [image], axis=0)
                y = np.append(y, [angle])

            flip_indices = random.sample(range(x.shape[0]), x.shape[0] // 2)
            x[flip_indices] = x[flip_indices, :, ::-1, :]
            y[flip_indices] = -y[flip_indices]
            yield x, y
