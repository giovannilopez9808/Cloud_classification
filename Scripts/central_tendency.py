"""
"""
from Modules.data_model import full_comparison_data
from Modules.params import get_params
import matplotlib.pyplot as plt

# Obtiene rutas y nombres de archivos
params = get_params()
# Parametros del programa
params.update({
    "graphics file": "distribution.png",
    # operacion de comparacion
    "comparison operation": "ratio",
    # modelo a comparar
    "clear sky model": "RS",
})
# Carga de documentos
comparison = full_comparison_data(params)
# Promedio diario
daily = comparison.get_daily_mean()
plt.subplots(figsize=(10, 4))
for station in daily.columns:
    # Grafica de cada estacion
    plt.scatter(daily.index,
                daily[station],
                label=station,
                marker=".")
plt.ylim(0, 1)
plt.legend(frameon=False,
           ncol=4)
plt.show()
