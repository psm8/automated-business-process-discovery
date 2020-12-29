from processdiscovery.gate.seq_gate import SeqGate
from processdiscovery.evaluation.alignment_calculation import calculate_best_alignment
from processdiscovery.util.util import is_struct_empty, check_route_with_log_process
from processdiscovery.evaluation.generalization_calculation import add_executions, reset_executions
from processdiscovery.evaluation.precision_calculation import get_log_enabled, count_model_enabled
from processdiscovery.log.log_util import get_sum_of_processes_length

import math

MINIMAL_ALIGNMENT_MODEL_WITH_LOG = 0.95
MINIMAL_ALIGNMENT_ROUTE_WITH_LOG = 0.7
BIG_PENALTY = -10000


def calculate_simplicity_metric(model_events_list, log_unique_events):
    model_unique_events = set()
    [model_unique_events.add(x.name) for x in model_events_list]
    return 1 - (((len(model_events_list) - len(model_unique_events)) + (len(log_unique_events) -
                                                                        len(model_unique_events))) /
                (len(model_events_list) + len(log_unique_events)))


def calculate_precision_metric(log, model, model_parents_list):
    if log:
        sum_of_processes_length = get_sum_of_processes_length(log)
        log_enabled = get_log_enabled(log.keys())
        log_count = {key: len(log_enabled[key]) for key in log_enabled.keys()}
        model_parents_list[None] = model
        model_count = count_model_enabled(log_enabled, model_parents_list)
        precision = 1 - sum([log[process] * (model_count[process[:x]] - log_count[process[:x]]) /
                             model_count[process[:x]]
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


def calculate_fitness_metric(best_local_error, len_elem, n):
    return best_local_error / (len_elem + n)


def compare_model_with_log_events(model_events_list, log_unique_events):
    model_event_names = set()
    [model_event_names.add(x.name) for x in model_events_list]
    return sum([x in model_event_names for x in log_unique_events])/len(log_unique_events)


def calculate_metrics(guess, log_info, gate, min_length,
                      max_length, alignment_cache):

    # routes_cache = dict()
    model_events_list_with_parents = gate.get_events_with_parents()
    model_events_list = list(model_events_list_with_parents.keys())
    model_to_log_events_ratio = compare_model_with_log_events(model_events_list, log_info.log_unique_events)
    if model_to_log_events_ratio < MINIMAL_ALIGNMENT_MODEL_WITH_LOG:
        return model_to_log_events_ratio/10

    perfectly_aligned_logs = dict()
    best_local_error = 0
    # reset_executions(model_events_list)
    for elem in log_info.log.keys():
        n = len(elem)
        i = 1
        min_local = -2 * n
        events_global = []
        find = False
        # should be change later
        while not n < calculate_min_allowed_length(len(elem)) and \
                not n > calculate_max_allowed_length(len(elem)):
            best_local_alignment = -1
            if min_length <= n <= max_length:
                # cache_id = guess + str(n)
                # if cache_id in routes_cache:
                #     routes = routes_cache[cache_id]
                # else:
                routes = set(gate.get_all_n_length_routes(n, elem))
                    # routes_cache[cache_id] = routes
                if len(routes) > 35000:
                    print(len(routes))
                    n += (-i if i % 2 == 1 else i)
                    i += 1
                    continue
                if routes is not None and not is_struct_empty(routes):
                    for event_group in routes:
                        route_to_process_events_ratio = check_route_with_log_process(event_group, elem)
                        if route_to_process_events_ratio < MINIMAL_ALIGNMENT_ROUTE_WITH_LOG:
                            continue
                        value, events = calculate_best_alignment(event_group, list(elem), alignment_cache)
                        if value > min_local:
                            min_local = value
                            events_global = events
                        if value == 0:
                            perfectly_aligned_logs[tuple(events)] = log_info.log[elem]
                            find = True
                            break

                    local_alignment = calculate_fitness_metric(min_local, len(elem), n)
                    if local_alignment > best_local_alignment:
                        best_local_alignment = local_alignment
                    if find:
                        break

            n += (-i if i % 2 == 1 else i)
            i += 1

        add_executions(model_events_list, events_global, log_info.log[elem])
        best_local_error += best_local_alignment * log_info.log[elem]

    alignment = 1 + best_local_error/log_info.sum_of_processes_length
    precision = calculate_precision_metric(perfectly_aligned_logs, gate, model_events_list_with_parents)
    generalization = calculate_generalization_metric(model_events_list)
    simplicity = calculate_simplicity_metric(model_events_list, log_info.log_unique_events)
    best_result = (alignment + generalization + precision + simplicity) / 4
    return best_result


def calculate_max_allowed_length(log_length):
    return math.ceil(1.1 * log_length)


def calculate_min_allowed_length(log_length):
    return math.floor(0.9 * log_length)


def evaluate_guess(guess, log_info, alignment_cache):
    gate = SeqGate()
    try:
        gate.parse(guess)
    except ValueError:
        return BIG_PENALTY
    min_length = gate.get_model_min_length()
    if min_length > calculate_max_allowed_length(log_info.process_average_length):
        return BIG_PENALTY
    max_length = gate.get_model_max_length()
    if max_length < calculate_min_allowed_length(log_info.process_average_length):
        return BIG_PENALTY
    fitness_metric = calculate_metrics(guess, log_info, gate, min_length, max_length, alignment_cache)

    return fitness_metric
