from Scripts.Modules.params import get_params

params = get_params()
script = "get_resume_estimators.py"
file = open("task", "w")
for operation in params["comparison operations"]:
    for sky_model in params["clear sky models"]:
        for model in params["neural models"]:
            file.write("python {} {} {} '{}'\n".format(script,
                                                       operation,
                                                       sky_model,
                                                       model))
        for model in params["classical models"]:
            file.write("python {} {} {} '{}'\n".format(script,
                                                       operation,
                                                       sky_model,
                                                       model))

file.close()
