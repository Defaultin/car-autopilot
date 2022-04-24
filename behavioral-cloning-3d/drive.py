import base64
import numpy as np
import socketio
import eventlet.wsgi
import tensorflow as tf
from PIL import Image
from flask import Flask
from io import BytesIO
from keras.models import model_from_json
from data import preprocess


tf.python.control_flow_ops = tf
sio = socketio.Server()
app = Flask(__name__)
model = None
prev_image_array = None


@sio.on("telemetry")
def telemetry(sid, data):
    steering_angle = data["steering_angle"]
    throttle = data["throttle"]
    speed = data["speed"]
    imgString = data["image"]
    image = Image.open(BytesIO(base64.b64decode(imgString)))
    image_array = preprocess(np.asarray(image))
    transformed_image_array = image_array[None, :, :, :]
    steering_angle = float(model.predict(transformed_image_array, batch_size=1))
    throttle = .2 if float(speed) > 5 else 1.
    print(steering_angle, throttle)
    send_control(steering_angle, throttle)


@sio.on("connect")
def connect(sid, environ):
    print("connect ", sid)
    send_control(0, 0)


def send_control(steering_angle, throttle):
    sio.emit("steer", data={
        "steering_angle": str(steering_angle),
        "throttle": str(throttle)
    }, skip_sid=True)


def main():
    model_file = "model.json"
    weights_file = model_file.replace("json", "h5")

    with open(model_file, "r") as jfile:
        model = model_from_json(jfile.read())
        model.compile("adam", "mse")
        model.load_weights(weights_file)

    app = socketio.Middleware(sio, app)
    listner = eventlet.listen(("", 4567))
    eventlet.wsgi.server(listner, app)


if __name__ == "__main__":
    main()
