from Modules.functions import (get_best_similarity_dates,
                               get_similarity_vectors,
                               get_cosine_similarity,
                               comparison_operation,
                               threshold_filter,
                               get_hourly_mean,
                               fill_data,
                               clean_data)
from Modules.data_model import (clean_data_model,
                                SIMA_model)
from Modules.clear_sky import clear_sky_model
from Modules.params import get_threshold
from pandas import DataFrame


class transform_data_model:
    def __init__(self,
                 params: dict) -> None:
        self.params = params
        self.SIMA_data = SIMA_model(params)
        self.clean_data = clean_data_model(params)

    def run(self,
            data: DataFrame) -> DataFrame:
        self._run_clear_sky(full_comparison=False)
        comparison = self._run_comparison(data,
                                          use_threshold=True)
        self.clear_data = self._run_clean_data(data,
                                               comparison)
        self._run_cosine_similarity(self.clear_data)
        self.full_data = self._run_full_data(self.clear_data)
        self._run_clear_sky(full_comparison=True)
        comparison = self._run_comparison(self.full_data,
                                          use_threshold=False)
        return comparison

    def _run_clear_sky(self,
                       full_comparison: bool):
        params = self.params.copy()
        clear_sky = clear_sky_model()
        if not full_comparison:
            params["clear sky mode"] = "GHI"
        clear_sky = clear_sky.run(params)
        self.clear_sky = get_hourly_mean(clear_sky)

    def _run_comparison(self,
                        data: DataFrame,
                        use_threshold: bool):
        operation = self.params["comparison operation"]
        comparison = comparison_operation(data,
                                          self.clear_sky,
                                          operation,
                                          use_threshold)
        if use_threshold:
            params = self.params.copy()
            params["clear sky model"] = "GHI"
            params["comparison operation"] = "ratio"
            params["threshold"] = get_threshold(params)
            comparison = threshold_filter(comparison,
                                          params)
        return comparison

    def _run_clean_data(self,
                        data: DataFrame,
                        comparison: DataFrame):
        clear_data = clean_data(data,
                                self.clear_sky,
                                comparison)
        return clear_data

    def _run_cosine_similarity(self,
                               data: DataFrame):
        cosine = get_cosine_similarity(data,
                                       self.clean_data,
                                       self.params)
        similarity_dates = get_best_similarity_dates(cosine,
                                                     self.params,
                                                     0)
        self.similarity_vectors = get_similarity_vectors(self.clean_data,
                                                         similarity_dates,
                                                         self.params)

    def _run_full_data(self,
                       data: DataFrame):
        full_data = fill_data(data,
                              self.similarity_vectors)
        return full_data
