from Scripts.Modules.params import get_params

params = get_params()
script = "Run_neural_model.py"
file = open("task", "w")
for model in params["neural models"]:
    for sky_model in params["clear sky models"]:
        for operation in params["comparison operations"]:
            for station in params["stations"]:
                file.write("python {} {} {} '{}' {}\n".format(script,
                                                              operation,
                                                              sky_model,
                                                              model,
                                                              station))
file.close()
