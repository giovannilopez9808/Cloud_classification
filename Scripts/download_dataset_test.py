from numpy import savetxt
from os.path import join
import tensorflow as tf

train, test = tf.keras.datasets.mnist.load_data()
for i, image in train[0]:
    filename = f"{i}.txt"
    filename = join("datasets/train/images",
                    filename)
    savetxt(filename, image)
filename = join("datasets/train",
                "labels.txt")
savetxt(filename, train[1])
for i, image in test[0]:
    filename = f"{i}.txt"
    filename = join("datasets/test/images",
                    filename)
    savetxt(filename, image)
filename = join("datasets/test",
                "labels.txt")
savetxt(filename, test[1])
