from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Flatten
from tensorflow.keras.datasets import mnist
from tensorflow.keras.layers import Dense

gray_scale = 255
train, test = mnist.load_data()
x_train, y_train = train
x_test, y_test = test
# Cast the records into float values
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= gray_scale
x_test /= gray_scale
model = Sequential([
    # reshape 28 row * 28 column data to 28*28 rows
    Flatten(input_shape=(28, 28)),
    # dense layer 1
    Dense(256, activation='sigmoid'),
    # dense layer 2
    Dense(128, activation='sigmoid'),
    # output layer
    Dense(10, activation='sigmoid'),
])
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.fit(x_train,
          y_train,
          epochs=10,
          batch_size=2000,
          validation_split=0.2)
results = model.evaluate(x_test,
                         y_test,
                         verbose=0)
print('test loss, test acc:', results)
