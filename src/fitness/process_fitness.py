from fitness.base_ff_classes.base_ff import base_ff
from gate.seq_gate import SeqGate
from fitness.alignment_calculation import flatten_values, nw_wrapper
from util.util import is_struct_empty, string_to_dictionary
from fitness.generalization_calculation import add_executions, reset_executions

import math


def get_event_log():
    return ["abcdef", "acbdef"]


def get_event_log_length(log: list):
    return sum(len(x) for x in log)


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


def calculate_metrics(log, log_length, log_average_length, gate, min_length, max_length):
    n = round(log_average_length)
    i = 1
    best_result = 0
    # should be change later
    while not n < calculate_min_allowed_length(log_average_length) and \
            not n > calculate_max_allowed_length(log_average_length):
        if min_length <= n <= max_length:
            routes = gate.get_all_n_length_routes(n)
            model_events_list_with_parents = gate.get_events_with_parents()
            model_events_list = [x[1] for x in model_events_list_with_parents]
            model_parents_list = [x[0] for x in model_events_list_with_parents]
            reset_executions(model_events_list)
            #fix_routes to strings inside gate
            if routes is not None and not is_struct_empty(routes):
                best_local_error = 0
                for elem in log:
                    min_local = 1023
                    for event_group in routes:
                        value, events = nw_wrapper(event_group, elem)
                        if value < min_local:
                            min_local = value
                            events_global = events
                    add_executions(model_events_list, events_global)
                    best_local_error += min_local

                best_local_alignment = calculate_fitness_metric(best_local_error, log_length, log, n)
                best_local_generalization = calculate_generalization_metric(model_events_list)
                best_local_result = (best_local_alignment + best_local_generalization)/2
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
    log_length = get_event_log_length(log)
    log_average_length = log_length / len(log)
    gate = SeqGate()
    try:
        gate.parse(guess)
    except ValueError:
        return -100000
    min_length = gate.get_model_min_length()
    if min_length > calculate_max_allowed_length(log_average_length):
        return -100000
    max_length = gate.get_model_max_length()
    if max_length < calculate_min_allowed_length(log_average_length):
        return -100000
    # processes = gate.get_processes_list()
    # first_occurrences = gate.find_first_occurrence(Process(string_to_dictionary("abcd"), 0))
    # length_metric = calculate_length_metric(guess, 50)
    fitness_metric = calculate_metrics(log, log_length, log_average_length, gate,
                                       min_length, max_length)

    return fitness_metric


class process_fitness(base_ff):
    maximise = True

    def __init__(self):
        # Initialise base fitness function class.
        super().__init__()

    def evaluate(self, ind, **kwargs):
        guess = ind.phenotype

        return evaluate_guess(guess)
