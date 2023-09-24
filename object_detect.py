import tensorflow as tf

model = tf.keras.applications.MobileNetV2(weights='imagenet', include_top=True)
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
import numpy as np

def detect_objects(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    
    predictions = model.predict(x)
    decoded_predictions = decode_predictions(predictions, top=3)[0]
    
    return decoded_predictions
