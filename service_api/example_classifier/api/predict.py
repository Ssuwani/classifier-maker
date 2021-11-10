import json
import tensorflow as tf
import numpy as np

class_index = json.load(open("class_index.json"))

model = tf.keras.models.load_model("../saved_model")


def get_prediction(image_bytes):
    image = tf.io.decode_image(image_bytes)
    image = tf.image.resize(image, (160, 160))

    outputs = model.predict(image[np.newaxis, ...])
    predicted_idx = np.argmax(outputs[0], axis=-1)

    return class_index[str(predicted_idx)]
