import math


def calculate_complexity_metric(cumulated_average_error, model):
    if cumulated_average_error == 0:
        return 1
    complexity = model.complexity_for_metric
    return math.pow(math.sqrt(1 - cumulated_average_error * math.sqrt(complexity)), -1)
