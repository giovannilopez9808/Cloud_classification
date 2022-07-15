from pandas import DataFrame, concat
from .functions import get_labels
from os.path import join


class Report_reader:
    def __init__(self,
                 params: dict) -> None:
        self.params = params

    def run(self,
            model_type: str) -> DataFrame:
        if model_type == "Neural model":
            report = self._read_file(model_type)
            report = self._read_neural_model(report)
            return report
        if model_type == "Classical model":
            report = self._read_file(model_type)
            report = self._read_classical_model(report)
            return report

    def _get_filename(self,
                      model_type: str) -> str:
        if model_type == "Neural model":
            comparison = self.params["comparison operation"]
            sky_model = self.params["clear sky model"]
            folder = self.params["Neural model path"]
            filename = "{}_{}_report.csv".format(comparison,
                                                 sky_model)
        if model_type == "Classical model":
            folder = self.params["Classical model path"]
            filename = "report.csv"
        model = self.params["model name"].replace(" ",
                                                  "_")
        folder = join(self.params["path results"],
                      folder,
                      model,
                      self.params["station"])
        filename = join(folder,
                        filename)
        return filename

    def _read_file(self,
                   model_type: str) -> str:
        filename = self._get_filename(model_type)
        file = open(filename,
                    "r")
        report = file.read()
        file.close()
        return report

    def _read_neural_model(self,
                           report: str,
                           use_header: bool = False) -> DataFrame:
        report = report.splitlines()
        self._get_header_report(report)
        if use_header:
            header = self.header
        else:
            header = self.params["model name"]
        report = report[3:]
        report = self._to_table(report,
                                header)
        return report

    def _read_classical_model(self,
                              report: str) -> DataFrame:
        report = report.splitlines()
        report = ["\n".join(report[i*12:12*i+12])
                  for i in range(4)]
        results = DataFrame()
        for subreport in report:
            subreport = self._read_neural_model(subreport,
                                                True)
            results = concat([results,
                              subreport],
                             axis=1)
        operation = self.params["comparison operation"]
        sky_model = self.params["clear sky model"]
        header = f"{operation} {sky_model}"
        results = DataFrame(results[header])
        return results

    def _get_header_report(self,
                           report: list) -> None:
        row = report[1]
        row = row.split()
        self.header = [row[4],
                       row[2]]
        self.header = " ".join(self.header)

    def _to_table(self,
                  report: list,
                  header: str) -> DataFrame:
        result = list()
        result += [self._get_value(report,
                                   2,
                                   3)]
        result += [self._get_value(report,
                                   3,
                                   4)]
        result += [self._get_value(report,
                                   4,
                                   4)]
        result += [self._get_value(report,
                                   6,
                                   1)]
        _, labels = get_labels(self.params)
        labels += ["accuracy"]
        result = DataFrame(result,
                           index=labels,
                           columns=[header])
        return result

    def _get_value(self,
                   report: list,
                   nrow: int,
                   ncolumn: int) -> float:
        row = report[nrow]
        row = row.split()
        value = row[ncolumn]
        return value
