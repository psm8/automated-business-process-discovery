from process_discovery.log.log_util import get_sum_of_processes_length

import logging
import math


def calculate_precision_metric(log, model, model_parents_list):
    if log:
        sum_of_processes_length = get_sum_of_processes_length(log)
        log_enabled = get_log_enabled(log.keys())
        log_count = {key: len(log_enabled[key]) for key in log_enabled.keys()}
        model_parents_list[None] = model
        model_count = count_model_enabled(log_enabled, model_parents_list)
        if any(log_count[x] > model_count[x] for x in log_count):
            logger = logging.getLogger()
            logger.error(log_count)
            logger.error(model_count)
            for x in log_count:
                if log_count[x] > model_count[x]:
                    model_count[x] = log_count[x]
        precision = 1 - sum([log[process] * (model_count[process[:x]] - log_count[process[:x]]) /
                             model_count[process[:x]]
                            for process in log.keys() for x in range(len(process))]) / sum_of_processes_length
        return math.pow(precision, 1/3)
    else:
        return 0


def get_log_enabled(processes):
    unique_processes = dict()

    for process in processes:
        for i in range(len(process)):
            subprocess = process[:i]
            if subprocess not in unique_processes:
                unique_processes[subprocess] = set()
                unique_processes[subprocess].add(process[i])
            else:
                unique_processes[subprocess].add(process[i])

    return unique_processes


def count_model_enabled(previous_events_dict: dict, model_parents_list: dict):
    result = dict()
    for previous_events in previous_events_dict:
        if previous_events:
            event = previous_events[-1]
        else:
            event = None
        result[previous_events] = len(set(list(model_parents_list[event]
                                               .get_next_possible_states(previous_events, event,
                                                                         next(iter(previous_events_dict[previous_events]))))))

    return result
