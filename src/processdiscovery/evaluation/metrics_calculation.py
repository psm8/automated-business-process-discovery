from processdiscovery.gate.seq_gate import SeqGate
from processdiscovery.evaluation.alignment_calculation import calculate_best_alignment
from processdiscovery.util.util import is_struct_empty, get_event_names
from processdiscovery.evaluation.generalization_calculation import add_executions, reset_executions
from processdiscovery.evaluation.precision_calculation import count_log_enabled
from processdiscovery.log.log_util import get_sum_of_processes_length

import math

MINIMAL_ALIGNMENT_MODEL_WITH_LOG = 0.95
MINIMAL_ALIGNMENT_ROUTE_WITH_LOG = 0.7
BIG_PENALTY = -10000


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


def calculate_simplicity_metric(model_events_list, log_unique_events):
    model_unique_events = set()
    [model_unique_events.add(x.name) for x in model_events_list]
    return 1 - (((len(model_events_list) - len(model_unique_events)) + (len(log_unique_events) -
                                                                        len(model_unique_events))) /
                (len(model_events_list) + len(log_unique_events)))


def calculate_precision_metric(log, model_parents_list):
    if log:
        # log = get_event_log_csv('discovered-processes.csv')
        sum_of_processes_length = get_sum_of_processes_length(log)
        log_count = count_log_enabled(log.keys())
        # model_count = [1, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
        precision = 1 - sum([log[process] * (model_parents_list[x] - log_count[process[:x]])/(model_parents_list[x])
                            for process in log.keys() for x in range(len(process))]) / sum_of_processes_length

        return precision
    else:
        return 0


def calculate_generalization_metric(model_events_list):
    if any([model_event.no_visits == 0 for model_event in model_events_list]):
        return 0
    else:
        return 1 - sum([math.pow(math.sqrt(model_event.no_visits), -1)
                        if model_event.no_visits != 0 else 1 for model_event in model_events_list]) / \
               len(model_events_list)


def calculate_fitness_metric(best_local_error, sum_of_processes_length, log, n):
    return 1 + (best_local_error / (sum_of_processes_length + len(log) * n))


def compare_model_with_log_events(model_events_list, log_unique_events):
    model_event_names = set()
    [model_event_names.add(x.name) for x in model_events_list]
    return sum([x in model_event_names for x in log_unique_events])/len(log_unique_events)


def check_route_with_log_events(route, log_unique_events):
    route_event_names = set()
    [route_event_names.add(x) for x in get_event_names(route)]

    return sum([x in route_event_names for x in log_unique_events])/len(log_unique_events)


def calculate_metrics(log_info, gate, min_length,
                      max_length, alignment_cache):
    n = round(log_info.process_average_length)
    i = 1
    best_result = 0
    model_events_list_with_parents = gate.get_events_with_parents()
    model_events_list = list(model_events_list_with_parents.keys())
    model_to_log_events_ratio = compare_model_with_log_events(model_events_list, log_info.log_unique_events)
    if model_to_log_events_ratio < MINIMAL_ALIGNMENT_MODEL_WITH_LOG:
        return model_to_log_events_ratio/10
    # should be change later
    while not n < calculate_min_allowed_length(log_info.process_average_length) and \
            not n > calculate_max_allowed_length(log_info.process_average_length):
        if min_length <= n <= max_length:
            routes = set(gate.get_all_n_length_routes(n))
            if len(routes) > 10000:
                print(len(routes))
                n += (-i if i % 2 == 1 else i)
                i += 1
                continue
            reset_executions(model_events_list)
            if routes is not None and not is_struct_empty(routes):
                perfectly_aligned_logs = dict()
                events_global = []
                best_local_error = 0
                for elem in log_info.log.keys():
                    min_local = -1023
                    for event_group in routes:
                        route_to_log_events_ratio = check_route_with_log_events(event_group, log_info.log_unique_events)
                        if route_to_log_events_ratio < MINIMAL_ALIGNMENT_ROUTE_WITH_LOG:
                            continue
                        value, events = calculate_best_alignment(event_group, list(elem), alignment_cache)
                        if value == 0:
                            perfectly_aligned_logs[tuple(events)] = log_info.log[elem]
                            break
                        if value > min_local:
                            min_local = value
                            events_global = events
                    add_executions(model_events_list, events_global)
                    best_local_error += min_local

                best_local_alignment = calculate_fitness_metric(best_local_error, log_info.sum_of_processes_length, log_info.log, n)
                best_local_generalization = calculate_generalization_metric(model_events_list)
                best_local_precision = calculate_precision_metric(perfectly_aligned_logs, model_events_list_with_parents)
                best_local_simplicity = calculate_simplicity_metric(model_events_list, log_info.log_unique_events)
                best_local_result = (best_local_alignment + best_local_generalization + best_local_precision +
                                     best_local_simplicity) / 4
                if best_local_result > best_result:
                    if best_local_result > 1:
                        print(best_local_result)
                    best_result = best_local_result
        n += (-i if i % 2 == 1 else i)
        i += 1
    return best_result


def calculate_max_allowed_length(log_average_length):
    return math.ceil(1.5 * log_average_length)


def calculate_min_allowed_length(log_average_length):
    return math.floor(0.5 * log_average_length)


def evaluate_guess(guess, log_info, alignment_cache):
    gate = SeqGate()
    try:
        gate.parse(guess)
    except ValueError:
        return BIG_PENALTY
    min_length = gate.get_model_min_length()
    log_info.log
    if min_length > calculate_max_allowed_length(log_info.process_average_length):
        return BIG_PENALTY
    max_length = gate.get_model_max_length()
    if max_length < calculate_min_allowed_length(log_info.process_average_length):
        return BIG_PENALTY
    # length_metric = calculate_length_metric(guess, 50)
    fitness_metric = calculate_metrics(log_info, gate, min_length, max_length, alignment_cache)

    return fitness_metric
