from tensorflow.keras.layers import Flatten, Dense
from sklearn.metrics import classification_report
from Modules.dataset_model import dataset_model
from tensorflow.keras.models import Sequential
from Modules.params import get_params
from numpy import argmax
from sys import argv

params = get_params()
params.update({
    "comparison operation": argv[1],
    "clear sky model": argv[2],
    # "hour initial": 8,
    # "hour final": 20,
})
dataset = dataset_model(params)
input_dim = params["hour final"]-params["hour initial"]+1
if params["hour initial"]==0 and params["hour final"]==24:
    input_dim=24
model = Sequential([
    Flatten(input_shape=(input_dim, 1)),
    # dense layer 1
    Dense(256, activation='sigmoid'),
    # dense layer 2
    Dense(128, activation='sigmoid'),
    # output layer
    Dense(3, activation="sigmoid"),
])
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.fit(dataset.train[0],
          dataset.train[1],
          epochs=50,
          batch_size=50,
          validation_data=dataset.validation)
results = model.predict(dataset.test[0])
results = argmax(results,
                 axis=1)
print(classification_report(dataset.test[1],
                            results))
