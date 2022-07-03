from Modules.params import get_params, get_classification_params
from Modules.classification_classic_models import SVM_model
from sklearn.metrics import classification_report
from Modules.dataset_model import dataset_model
from sklearn.metrics import confusion_matrix
from Modules.functions import get_labels

params = get_params()
params.update({
    "comparison operation": "diff",
    "classification model": "SVM",
    "clear sky model": "RS",
})
_, labels = get_labels(params)
class_params = get_classification_params(params)
dataset = dataset_model(params)
model = SVM_model()
model.run(dataset.train,
          class_params)
results = model.predict(dataset.test)
print(classification_report(dataset.test[1],
                            results))
