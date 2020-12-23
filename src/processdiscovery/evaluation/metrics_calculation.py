from processdiscovery.gate.seq_gate import SeqGate
from processdiscovery.evaluation.alignment_calculation import calculate_best_alignment
from processdiscovery.util.util import is_struct_empty
from processdiscovery.evaluation.generalization_calculation import add_executions, reset_executions

import math
import csv

MINIMAL_ALIGNMENT_MODEL_WITH_LOG = 0.8
MINIMAL_ALIGNMENT_ROUTE_WITH_LOG = 0.6


def get_event_log_csv(filename) -> dict:
    with open('filename', newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=', ')
    events = {}
    for row in data:
        count = data.pop(0)
        events[set(data)] = count
    return events


def get_event_log() -> dict:
    return {("a", "b", "c", "d", "e", "f"): 1, ("a", "c", "b", "d", "e", "f"): 1}


def get_log_unique_events(keys):
    unique_events = set()
    [unique_events.add(x) for key in keys for x in key]
    return unique_events


def get_sum_of_processes_length(log: dict) -> int:
    return sum(len(key) * log[key] for key in log.keys())


def calculate_length_metric(guess, goal_length):
    length = len(guess)
    if length == goal_length:
        # Perfect match.
        fitness = 1
    else:
        # Imperfect match, find distance to match.
        distance = abs(goal_length - length)
        fitness = 1 / (1 + distance)

    return fitness


def calculate_simplicity_metric(s):
    return


def calculate_precision_metric(guess):
    # calculate precision based on R)metric calculation
    precision = 0

    return precision


def calculate_generalization_metric(model_events_list):
    return 1 - sum([math.pow(math.sqrt(model_event.no_visits), -1)
                    if model_event.no_visits != 0 else 0 for model_event in model_events_list]) / len(model_events_list)


def calculate_fitness_metric(best_local_error, event_log_length, log, n):
    return 1 + (best_local_error / (event_log_length + len(log) * n))


def compare_model_with_log_events(model_events_list, log_unique_events):
    model_event_names = set()
    [model_event_names.add(x.name) for x in model_events_list]
    return sum([x in model_event_names for x in log_unique_events])/len(log_unique_events)


def check_route_with_log_events(route):
    return MINIMAL_ALIGNMENT_ROUTE_WITH_LOG


def calculate_metrics(log, log_unique_events, sum_of_processes_length, process_average_length, gate, min_length,
                      max_length):
    n = round(process_average_length)
    i = 1
    best_result = 0
    model_events_list_with_parents = gate.get_events_with_parents()
    model_events_list = [x[1] for x in model_events_list_with_parents]
    model_parents_list = [x[0] for x in model_events_list_with_parents]
    model_to_log_events_ratio = compare_model_with_log_events(model_events_list, log_unique_events)
    if model_to_log_events_ratio < MINIMAL_ALIGNMENT_MODEL_WITH_LOG:
        return model_to_log_events_ratio/10
    # should be change later
    while not n < calculate_min_allowed_length(process_average_length) and \
            not n > calculate_max_allowed_length(process_average_length):
        if min_length <= n <= max_length:
            routes = gate.get_all_n_length_routes(n)
            if len(routes) > 10000:
                print(10000)
            reset_executions(model_events_list)
            if routes is not None and not is_struct_empty(routes):
                best_local_error = 0
                for elem in log.keys():
                    min_local = 1023
                    for event_group in routes:
                        value, events = calculate_best_alignment(event_group, list(elem))
                        if value < min_local:
                            min_local = value
                            events_global = events
                    add_executions(model_events_list, events_global)
                    best_local_error += min_local

                best_local_alignment = calculate_fitness_metric(best_local_error, sum_of_processes_length, log, n)
                best_local_generalization = calculate_generalization_metric(model_events_list)
                best_local_result = (best_local_alignment + best_local_generalization) / 2
                if best_local_result > best_result:
                    best_result = best_local_result
        if i % 2 == 1:
            n -= i
        else:
            n += i
        i += 1
    return best_result


def calculate_max_allowed_length(log_average_length):
    return math.ceil(1.5 * log_average_length)


def calculate_min_allowed_length(log_average_length):
    return math.floor(0.5 * log_average_length)


def evaluate_guess(guess):
    log = get_event_log()
    sum_of_processes_length = get_sum_of_processes_length(log)
    process_average_length = sum_of_processes_length / sum([x for x in log.values()])
    log_unique_events = get_log_unique_events(log.keys())
    gate = SeqGate()
    try:
        gate.parse(guess)
    except ValueError:
        return -100000
    min_length = gate.get_model_min_length()
    if min_length > calculate_max_allowed_length(process_average_length):
        return -100000
    max_length = gate.get_model_max_length()
    if max_length < calculate_min_allowed_length(process_average_length):
        return -100000
    # length_metric = calculate_length_metric(guess, 50)
    fitness_metric = calculate_metrics(log, log_unique_events, sum_of_processes_length, process_average_length, gate,
                                       min_length, max_length)

    return fitness_metric