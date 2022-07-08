from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from numpy import stack, loadtxt, array
from os import listdir
from os.path import join


def ls(path: str) -> list:
    return sorted(listdir(path))


train_path = "datasets/train"
test_path = "datasets/test"
train_images = join(train_path,
                    "images")
test_images = join(test_path,
                   "images")
y_train = loadtxt(join(train_path,
                       "labels.txt"))
y_test = loadtxt(join(test_path,
                      "labels.txt"))
x_train = []
x_test = []
gray_scale = 255
train_files = ls(train_images)
test_files = ls(test_images)
# for i,file in enumerate(train_files):
# filename = join(train_images,
# file)
# x = loadtxt(filename)
# x=x.astype('float32')
# x /=gray_scale
# x_train.append(x)
for i, file in enumerate(test_files):
    filename = join(test_images,
                    file)
    x = loadtxt(filename)
    x = x.astype('float32')
    x /= gray_scale
    x_test.append(x)
x_test = array(x_test)
print(x_test.shape)
# model = Sequential([
# # reshape 28 row * 28 column data to 28*28 rows
# Flatten(input_shape=(28, 28)),
# # dense layer 1
# Dense(256, activation='sigmoid'),
# # dense layer 2
# Dense(128, activation='sigmoid'),
# # output layer
# Dense(10, activation='sigmoid'),
# ])
# model.compile(optimizer='adam',
# loss='sparse_categorical_crossentropy',
# metrics=['accuracy'])
# model.fit(x_train,
# y_train,
# epochs=10,
# batch_size=2000,
# validation_split=0.2)
# results = model.evaluate(x_test,
# y_test,
# verbose=0)
# print('test loss, test acc:', results)
