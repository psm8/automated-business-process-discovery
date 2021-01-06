from processdiscovery.gate.seq_gate import SeqGate
from processdiscovery.gate.lop_gate import LopGate
from processdiscovery.evaluation.alignment_calculation.alignment_calculation import \
    get_best_alignment, get_best_alignment_cached
from processdiscovery.util.util import is_struct_empty, check_route_with_log_process
from processdiscovery.evaluation.generalization_calculation import add_executions
from processdiscovery.evaluation.precision_calculation import get_log_enabled, count_model_enabled
from processdiscovery.log.log_util import get_sum_of_processes_length
from processdiscovery.event.event import Event

import math
import logging

MINIMAL_ALIGNMENT_MODEL_WITH_LOG = 0.95
MINIMAL_ALIGNMENT_ROUTE_WITH_LOG = 0.7
BIG_PENALTY = 0


def calculate_complexity_metric(cumulated_average_error, model):
    if cumulated_average_error == 0:
        return 1
    complexity = model.complexity_for_metric
    return math.pow(math.sqrt(1 - cumulated_average_error * math.sqrt(complexity)), -1)


def calculate_simplicity_metric(model_events_list, log_unique_events):
    lop_allowed_duplicates = sum(x.event_lop_twin is not None for x in model_events_list)
    model_unique_events = set()
    [model_unique_events.add(x.name) for x in model_events_list]
    return 1 - (((len(model_events_list) - len(model_unique_events) - lop_allowed_duplicates) +
                 (len(log_unique_events) - len(model_unique_events))) /
                (len(model_events_list) - lop_allowed_duplicates + len(log_unique_events)))


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


def calculate_generalization_metric(model_events_list: [Event]):
    return 1 - sum([math.pow(math.sqrt(model_event.no_visits if model_event.event_lop_twin is None else model_event.no_visits + model_event.event_lop_twin.no_visits), -1)
                    if model_event.no_visits != 0 else 1 for model_event in model_events_list]) / \
           len(model_events_list)


def calculate_fitness_metric(best_local_error, len_elem, n):
    return best_local_error / (len_elem + n)


def compare_model_with_log_events(model_events_list, log_unique_events):
    model_event_names = set()
    [model_event_names.add(x.name) for x in model_events_list]
    return sum([x in model_event_names for x in log_unique_events])/len(log_unique_events)


def calculate_metrics_for_single_process(elem, model, min_length, max_length, alignment_cache):
    len_elem = len(elem)
    n = len_elem
    i = 1
    min_local = -2 * n
    events_global = []
    best_event_group = []
    find = False

    while not n <= max(calculate_min_allowed_length(len_elem), len_elem + min_local) and \
            not n >= min(calculate_max_allowed_length(len(elem)), len_elem - min_local):
        best_local_alignment = -1
        if min_length <= n <= max_length:
            model.min_start = 0
            model.max_start = 0
            model.min_end = n
            model.max_end = n
            model.set_children_boundaries()
            routes = model.get_all_n_length_routes(n, elem)

            if routes is not None and not is_struct_empty(routes):
                routes = set(routes)
                route_and_process_events_ratios = []
                for event_group in routes:
                    ratio = check_route_with_log_process(event_group, elem)
                    if ratio >= MINIMAL_ALIGNMENT_ROUTE_WITH_LOG:
                        route_and_process_events_ratios.append((event_group, ratio))
                sorted_routes_and_ratios = sorted(route_and_process_events_ratios, key=lambda x: -x[1])
                for event_group_and_ratios in sorted_routes_and_ratios:
                    if event_group_and_ratios[1] <= 1 + min_local/len_elem:
                        break
                    value, events = get_best_alignment_cached(event_group_and_ratios[0], list(elem), alignment_cache)
                    if value > min_local:
                        min_local = value
                        events_global = events
                        best_event_group = event_group_and_ratios[0]
                    if value == 0:
                        find = True
                        break

                local_alignment = calculate_fitness_metric(min_local, len(elem), n)
                if local_alignment > best_local_alignment:
                    best_local_alignment = local_alignment
                if find:
                    break

        n += (-i if i % 2 == 1 else i)
        i += 1

    return best_local_alignment, events_global, best_event_group


def calculate_metrics(log_info, gate, min_length, max_length, alignment_cache):

    metrics = dict()

    model_events_list_with_parents = gate.get_all_child_events_with_parents()
    model_events_list = list(model_events_list_with_parents.keys())
    model_to_log_events_ratio = compare_model_with_log_events(model_events_list, log_info.log_unique_events)
    if model_to_log_events_ratio < MINIMAL_ALIGNMENT_MODEL_WITH_LOG:
        return model_to_log_events_ratio/10

    perfectly_aligned_logs = dict()
    cumulated_error = 0

    for elem in log_info.log.keys():
        best_local_error, events_global, best_event_group = \
            calculate_metrics_for_single_process(elem, gate, min_length, max_length, alignment_cache)

        if any(event is not None and event not in model_events_list for event in events_global):
            value, events_global = get_best_alignment(best_event_group, list(elem), dict())
            if value != 0:
                best_local_error = calculate_fitness_metric(value, len(elem), best_event_group)
        if best_local_error == 0:
            perfectly_aligned_logs[tuple(events_global)] = log_info.log[elem]
        add_executions(model_events_list, events_global, log_info.log[elem])
        cumulated_error += best_local_error * log_info.log[elem]

    cumulated_average_error = cumulated_error/log_info.sum_of_processes_length
    metrics['alignment'] = (1 + cumulated_average_error, 7)
    for x in gate.get_all_child_gates(LopGate):
        x.set_event_lop_twin_and_count_complexity_if_seq_parent()
    metrics['precision'] = (calculate_precision_metric(perfectly_aligned_logs, gate, model_events_list_with_parents), 2)
    metrics['generalization'] = (calculate_generalization_metric(model_events_list), 2)
    metrics['simplicity'] = (calculate_simplicity_metric(model_events_list, log_info.log_unique_events), 1)
    metrics['complexity'] = (calculate_complexity_metric(cumulated_average_error, gate), 2)

    if any(metrics[x][0] > 1.0000001 for x in metrics):
        logging.error([x.no_visits for x in model_events_list])
        logging.error(perfectly_aligned_logs)
        logging.error(len(alignment_cache))
        logging.error(model_events_list_with_parents)
        logging.error(metrics)
        raise Exception(metrics)

    best_result = (metrics['alignment'][0] * metrics['alignment'][1] +
                   metrics['precision'][0] * metrics['precision'][1] +
                   metrics['generalization'][0] * metrics['generalization'][1] +
                   metrics['simplicity'][0] * metrics['simplicity'][1] +
                   metrics['complexity'][0] * metrics['complexity'][1]) \
                  / sum(x[1] for x in metrics.values())

    return best_result


def calculate_max_allowed_length(log_length):
    return math.ceil(1.1 * log_length)


def calculate_min_allowed_length(log_length):
    return math.floor(0.9 * log_length)


def evaluate_guess(guess, log_info, alignment_cache, max_allowed_complexity):
    gate = SeqGate()
    try:
        gate.parse(guess)
    except ValueError:
        return BIG_PENALTY

    min_length = gate.model_min_length
    if min_length > calculate_max_allowed_length(log_info.process_average_length):
        return BIG_PENALTY

    max_length = gate.model_max_length
    if max_length < calculate_min_allowed_length(log_info.process_average_length):
        return BIG_PENALTY

    if max_allowed_complexity < gate.complexity:
        return BIG_PENALTY

    fitness_metric = calculate_metrics(log_info, gate, min_length, max_length, alignment_cache)

    return fitness_metric
