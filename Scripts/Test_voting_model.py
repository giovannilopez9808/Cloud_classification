from Modules.neural_models import Voting_model
from Modules.params import (get_params,
                            get_voting_models)
from sys import argv

params = get_params()
params.update({
    "comparison operation": argv[1],
    "clear sky model": argv[2],
    "station": argv[3],
})
params["voting models"] = get_voting_models(params)
model = Voting_model()
model.run(params)
