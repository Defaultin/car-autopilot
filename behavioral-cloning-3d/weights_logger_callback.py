import os
import shutil
from keras.callbacks import Callback


class WeightsLogger(Callback):
    def __init__(self, root_path):
        super(WeightsLogger, self).__init__()
        self.weights_root_path = os.path.join(root_path, "weights/")
        shutil.rmtree(self.weights_root_path, ignore_errors=True)
        os.makedirs(self.weights_root_path, exist_ok=True)

    def on_epoch_end(self, epoch, logs={}):
        weights_file = f"model_epoch_{epoch + 1}.h5"
        self.model.save_weights(os.path.join(self.weights_root_path, weights_file))
