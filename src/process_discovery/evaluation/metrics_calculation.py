from algorithm.parameters import params
from process_discovery.evaluation.alignment_calculation.alignment_metric_calculation import calculate_alignment_metric
from process_discovery.evaluation.complexity_calculation.complexity_metric_calculation import \
    calculate_complexity_metric
from process_discovery.evaluation.precision_calculation.precision_metric_calculation import calculate_precision_metric
from process_discovery.evaluation.simplicity_calculation.simplicity_metric_calculation import \
    calculate_simplicity_metric
from process_discovery.gate.seq_gate import SeqGate
from process_discovery.gate.lop_gate import LopGate
from process_discovery.evaluation.alignment_calculation.alignment_calculation import \
    get_best_alignment, get_best_alignment_cached
from process_discovery.util.util import is_struct_empty, check_route_with_log_process
from process_discovery.evaluation.generalization_calculation.generalization_metric_calculation import add_executions, \
    calculate_generalization_metric

import math
import logging


def evaluate_guess(guess, log_info, alignment_cache, max_allowed_complexity):
    gate = SeqGate()
    try:
        gate.parse(guess)
    except ValueError:
        return 0

    min_length = gate.model_min_length
    if min_length > calculate_max_allowed_length(log_info.process_average_length):
        return 0

    max_length = gate.model_max_length
    if max_length < calculate_min_allowed_length(log_info.process_average_length):
        return 0

    if max_allowed_complexity < gate.complexity:
        return 0

    fitness_metric = calculate_metrics(log_info, gate, min_length, max_length, alignment_cache)

    if params['MINIMIZE_SOLUTION_LENGTH']:
        fitness_metric -= minimize_solution_length_factor(guess)

    return fitness_metric


def calculate_metrics(log_info, model, min_length, max_length, alignment_cache):
    metrics = dict()

    model_events_list_with_parents = model.get_all_child_events_with_parents()
    model_events_list = list(model_events_list_with_parents.keys())

    for x in model.get_all_child_gates(LopGate):
        x.set_twin_events_and_complexity()
    metrics['SIMPLICITY'] = calculate_simplicity_metric(model_events_list, log_info.log_unique_events)
    if metrics['SIMPLICITY'] < 2/3:
        return 0

    model_to_log_events_ratio = compare_model_with_log_events(model_events_list, log_info.log_unique_events)
    if model_to_log_events_ratio < 1 - 3 * params['RESULT_TOLERANCE_PERCENT']/100:
        return model_to_log_events_ratio/10

    perfectly_aligned_logs = dict()
    cumulated_error = 0

    for process in log_info.log.keys():
        best_local_error, best_aligned_process, best_event_group = \
            calculate_metrics_for_single_process(process, model, min_length, max_length, alignment_cache)
        if any(event is not None and event not in model_events_list for event in best_aligned_process):
            best_local_error, best_aligned_process = get_best_alignment(best_event_group, list(process), dict())
        best_local_error = calculate_alignment_metric(best_local_error, len(process), model.model_min_length)
        if best_local_error == 0:
            perfectly_aligned_logs[tuple(best_aligned_process)] = log_info.log[process]
        add_executions(model_events_list, best_aligned_process, log_info.log[process])
        cumulated_error += best_local_error * log_info.log[process]

    cumulated_average_error = cumulated_error/log_info.sum_of_processes_length
    metrics['ALIGNMENT'] = 1 + cumulated_average_error
    metrics['PRECISION'] = calculate_precision_metric(perfectly_aligned_logs, model, model_events_list_with_parents)
    metrics['GENERALIZATION'] = calculate_generalization_metric(model_events_list)
    metrics['COMPLEXITY'] = calculate_complexity_metric(cumulated_average_error, model)

    if any(metrics[x] > 1.0000001 for x in metrics):
        logging.error([x.no_visits for x in model_events_list])
        logging.error(perfectly_aligned_logs)
        logging.error(len(alignment_cache))
        logging.error(model_events_list_with_parents)
        logging.error(metrics)
        raise Exception(metrics)

    best_result = (metrics['ALIGNMENT'] * params['WEIGHT_ALIGNMENT'] +
                   metrics['PRECISION'] * params['WEIGHT_PRECISION'] +
                   metrics['GENERALIZATION'] * params['WEIGHT_GENERALIZATION'] +
                   metrics['SIMPLICITY'] * params['WEIGHT_SIMPLICITY'] +
                   metrics['COMPLEXITY'] * params['WEIGHT_COMPLEXITY']) /\
                  (params['WEIGHT_ALIGNMENT'] + params['WEIGHT_PRECISION'] + params['WEIGHT_GENERALIZATION'] +
                   params['WEIGHT_SIMPLICITY'] + params['WEIGHT_COMPLEXITY'])

    return best_result


def calculate_metrics_for_single_process(process, model, min_length, max_length, alignment_cache):
    len_process = len(process)
    n = len_process
    i = 1
    min_error_local = -(len_process + model.model_min_length)
    best_aligned_process = []
    best_event_group = []
    find = False
    best_error_local = -(len_process + model.model_min_length)
    lower_limit_reached = False
    higher_limit_reached = False

    while not (lower_limit_reached and higher_limit_reached):
        if n >= min(calculate_max_allowed_length(len_process), len_process - min_error_local):
            higher_limit_reached = True
            n += (-i if i % 2 == 1 else i)
            i += 1
            continue
        if n <= max(calculate_min_allowed_length(len_process), len_process + min_error_local):
            lower_limit_reached = True
            n += (-i if i % 2 == 1 else i)
            i += 1
            continue
        if min_length <= n <= max_length:
            set_model_children_boundaries(model, n)
            routes = model.get_all_n_length_routes(n, process)

            if routes is not None and not is_struct_empty(routes):
                routes = set(routes)
                route_and_process_events_ratios = []
                for event_group in routes:
                    ratio = check_route_with_log_process(event_group, process)
                    if ratio >= 1 - 10 * params['RESULT_TOLERANCE_PERCENT']/100:
                        route_and_process_events_ratios.append((event_group, ratio))
                sorted_routes_and_ratios = sorted(route_and_process_events_ratios, key=lambda x: -x[1])
                for event_group_and_ratios in sorted_routes_and_ratios:
                    if event_group_and_ratios[1] <= 1 + min_error_local/len_process:
                        break
                    value, best_aligned_process_local = get_best_alignment_cached(event_group_and_ratios[0],
                                                                                  list(process), alignment_cache)
                    if value > min_error_local:
                        min_error_local = value
                        best_aligned_process = best_aligned_process_local
                        best_event_group = event_group_and_ratios[0]
                    if value == 0:
                        find = True
                        break

                if min_error_local > best_error_local:
                    best_error_local = min_error_local
                if find:
                    break

        n += (-i if i % 2 == 1 else i)
        i += 1

    return best_error_local, best_aligned_process, best_event_group


def minimize_solution_length_factor(guess):
    return len(guess) * 10e-16


def set_model_children_boundaries(model, n):
    model.min_start = 0
    model.max_start = 0
    model.min_end = n
    model.max_end = n
    model.set_children_boundaries()


def compare_model_with_log_events(model_events_list, log_unique_events):
    model_event_names = set()
    [model_event_names.add(x.name) for x in model_events_list]
    return sum([x in model_event_names for x in log_unique_events])/len(log_unique_events)


def calculate_max_allowed_length(log_length):
    return math.ceil((1 + 1 * params['RESULT_TOLERANCE_PERCENT']/100) * log_length)


def calculate_min_allowed_length(log_length):
    return math.floor((1 - 11 * params['RESULT_TOLERANCE_PERCENT']/100) * log_length)

