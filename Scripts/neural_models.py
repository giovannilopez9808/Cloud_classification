from Modules.neural_models import neural_model
from Modules.params import get_params
from sys import argv

params = get_params()
params.update({
    "comparison operation": argv[1],
    "clear sky model": argv[2],
    "neural model": argv[3],
    # "hour initial": 8,
    # "hour final": 20,
})

model = neural_model()
model.build(params)
