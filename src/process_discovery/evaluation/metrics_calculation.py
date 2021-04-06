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
    BestAlignment, BestAlignmentCached
from process_discovery.util.util import is_struct_empty, check_route_with_log_process
from process_discovery.evaluation.generalization_calculation.generalization_metric_calculation import add_executions, \
    calculate_generalization_metric
from process_discovery.event.event import Event

import math
import logging
from cachetools import LRUCache


def evaluate_guess(guess, log_info, alignment_cache, max_allowed_complexity):
    gate = SeqGate()
    metrics = {'SIMPLICITY': 0, 'PRECISION': 0, 'GENERALIZATION': 0, 'COMPLEXITY': 0, 'ALIGNMENT': 0}
    try:
        gate.parse(guess)
    except ValueError:
        return 0, metrics

    min_length = gate.model_min_length
    if min_length > calculate_max_allowed_length(log_info.process_average_length):
        return 0, metrics

    max_length = gate.model_max_length
    if max_length < calculate_min_allowed_length(log_info.process_average_length):
        return 0, metrics

    if max_allowed_complexity < gate.complexity:
        return 0, metrics

    result = calculate_metrics(log_info, gate, min_length, max_length, alignment_cache, Event('end'))

    if isinstance(result, tuple):
        fitness_metric, metrics = result
    else:
        fitness_metric = result

    if params['MINIMIZE_SOLUTION_LENGTH']:
        fitness_metric -= minimize_solution_length_factor(guess)

    return fitness_metric, metrics


def calculate_metrics(log_info, model, min_length, max_length, alignment_cache, end_event):
    metrics = dict()
    model_events_list_with_parents = model.get_all_child_events_with_parents()
    model_events_list = list(model_events_list_with_parents.keys())

    for x in model.get_all_child_gates(LopGate):
        x.set_twin_events_and_complexity()
    metrics['SIMPLICITY'] = calculate_simplicity_metric(model_events_list, log_info.log_unique_events)
    if metrics['SIMPLICITY'] < params['MIN_SIMPLICITY_THRESHOLD']:
        return 0

    model_to_log_events_ratio = compare_model_with_log_events(model_events_list, log_info.log_unique_events)
    if model_to_log_events_ratio < 1 - 3 * params['RESULT_TOLERANCE_PERCENT']/100:
        return model_to_log_events_ratio/10

    best_alignment_errors_local_dict = dict()
    perfectly_aligned_logs = dict()

    for process in log_info.log.keys():
        min_alignment_error_local, best_aligned_process, best_event_group, is_best_from_cache = \
            calculate_metrics_for_single_process(process, model, min_length, max_length, alignment_cache)
        if is_best_from_cache:
            best_alignment = BestAlignment()
            min_alignment_error_local, best_aligned_process = \
                best_alignment.get_best_alignment(best_event_group, list(process), dict())

        best_alignment_errors_local_dict[process] = min_alignment_error_local
        if min_alignment_error_local == 0:
            perfectly_aligned_logs[tuple(best_aligned_process + [end_event])] = log_info.log[process]
        add_executions(model_events_list, best_aligned_process, log_info.log[process])

    average_alignment_error, metrics['ALIGNMENT'] = calculate_alignment_metric(best_alignment_errors_local_dict,
                                                                               log_info, model.model_min_length)
    metrics['GENERALIZATION'] = calculate_generalization_metric(model_events_list)
    metrics['COMPLEXITY'] = calculate_complexity_metric(average_alignment_error, model)
    metrics['PRECISION'] = calculate_precision_metric(perfectly_aligned_logs, model, model_events_list_with_parents,
                                                      end_event)

    if any(metrics[x] > 1.0000001 for x in metrics):
        logger = logging.getLogger()
        logger.error([x.no_visits for x in model_events_list])
        logger.error(perfectly_aligned_logs)
        logger.error(len(alignment_cache))
        logger.error(model_events_list_with_parents)
        logger.error(metrics)
        raise Exception(metrics)

    best_result = (metrics['ALIGNMENT'] * params['WEIGHT_ALIGNMENT'] +
                   metrics['PRECISION'] * params['WEIGHT_PRECISION'] +
                   metrics['GENERALIZATION'] * params['WEIGHT_GENERALIZATION'] +
                   metrics['SIMPLICITY'] * params['WEIGHT_SIMPLICITY'] +
                   metrics['COMPLEXITY'] * params['WEIGHT_COMPLEXITY']) /\
                  (params['WEIGHT_ALIGNMENT'] + params['WEIGHT_PRECISION'] + params['WEIGHT_GENERALIZATION'] +
                   params['WEIGHT_SIMPLICITY'] + params['WEIGHT_COMPLEXITY'])

    return best_result, metrics


def calculate_metrics_for_single_process(process, model, min_length, max_length, alignment_cache):
    len_process = len(process)
    n = len_process
    i = 1
    min_alignment_error_local = -(len_process + model.model_min_length)
    best_aligned_events = []
    best_event_group = []
    lower_limit_reached = False
    higher_limit_reached = False
    is_best_from_cache = False

    while not (lower_limit_reached and higher_limit_reached):
        if n >= min(calculate_max_allowed_length(len_process), len_process - min_alignment_error_local):
            higher_limit_reached = True
            n += (-i if i % 2 == 1 else i)
            i += 1
            continue
        if n <= max(calculate_min_allowed_length(len_process), len_process + min_alignment_error_local):
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
                    if event_group_and_ratios[1] <= 1 + min_alignment_error_local/len_process:
                        break
                    try:
                        best_alignment_cached = BestAlignmentCached()
                        alignment_error, aligned_events = \
                            best_alignment_cached.get_best_alignment(event_group_and_ratios[0],
                                                                     list(process), alignment_cache)
                        is_from_cache = best_alignment_cached.from_cache
                    except KeyError:
                        logger = logging.getLogger()
                        logger.error("KeyError was raised. Check if you have enough RAM. Recreating cache.")
                        logging.error("KeyError was raised. Check if you have enough RAM. Recreating cache.")
                        params["FITNESS_FUNCTION"].alignment_cache = LRUCache(params["ALIGNMENT_CACHE_SIZE"])
                        best_alignment = BestAlignment()
                        alignment_error, aligned_events = \
                            best_alignment.get_best_alignment(event_group_and_ratios[0], list(process))
                        is_from_cache = False
                    except RuntimeError as e:
                        if e.args[0] == 'OrderedDict mutated during iteration':
                            logger = logging.getLogger()
                            logger.error("OrderedDict mutated during iteration error was raised. Recreating cache.")
                            logging.error("OrderedDict mutated during iteration error was raised. Recreating cache.")
                            params["FITNESS_FUNCTION"].alignment_cache = LRUCache(params["ALIGNMENT_CACHE_SIZE"])
                            best_alignment = BestAlignment()
                            alignment_error, aligned_events = \
                                best_alignment.get_best_alignment(event_group_and_ratios[0], list(process))
                            is_from_cache = False
                    if alignment_error > min_alignment_error_local:
                        min_alignment_error_local = alignment_error
                        best_aligned_events = aligned_events
                        best_event_group = event_group_and_ratios[0]
                        is_best_from_cache = is_from_cache
                    if alignment_error == 0:
                        return min_alignment_error_local, best_aligned_events, best_event_group, is_best_from_cache

        n += (-i if i % 2 == 1 else i)
        i += 1

    return min_alignment_error_local, best_aligned_events, best_event_group, is_best_from_cache


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

