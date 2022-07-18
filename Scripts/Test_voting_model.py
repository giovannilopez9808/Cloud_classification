from Modules.neural_models import Voting_model
from Modules.params import get_params
from sys import argv

params = get_params()
params.update({
    "comparison operation": argv[1],
    "clear sky model": argv[2],
    "station": argv[3],
    "voting models": [
        "CNN",
        "perceptron",
        "Bi LSTM",
    ]
})
model = Voting_model()
model.run(params)
