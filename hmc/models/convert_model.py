import tensorflow as tf

hmc = tf.keras.models.load_model("hmc.tflite")
converter = tf.lite.TFLiteConverter.from_keras_model(hmc)
hmc_lite = converter.convert()
open("converted_model.tflite", "wb").write(hmc_lite)
