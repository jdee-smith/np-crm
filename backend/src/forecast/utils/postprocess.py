from typing import List

from forecast.api.models.forecast import IndividualForecast


def postprocess(forecasts) -> List[IndividualForecast]:
    ind_forecasts = []
    for i, series in enumerate(forecasts):
        for j, sample in enumerate(series):
            for k, step in enumerate(sample):
                ind_forecast = IndividualForecast(
                    series=i + 1, sample=j + 1, step=k + 1, value=step.item()
                )
                ind_forecasts.append(ind_forecast)
    return ind_forecasts
