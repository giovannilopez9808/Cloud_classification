from Modules.dataset_model import dataset_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from Modules.params import get_params
from sys import argv

params = get_params()
params.update({
    "comparison operation": argv[1],
    "clear sky model": argv[2],
})
dataset = dataset_model(params)
model = Sequential([
    # reshape 28 row * 28 column data to 28*28 rows
    Flatten(input_shape=(24)),
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
model.fit(dataset.train[0],
          dataset.train[1],
          epochs=10,
          batch_size=2000,
          validation_split=0.2)
results = model.evaluate(dataset.test[0],
                         dataset.train[1],
                         verbose=0)
print('test loss, test acc:', results)
