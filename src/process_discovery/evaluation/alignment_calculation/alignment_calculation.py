import numpy as np
import math

from process_discovery.evaluation.alignment_calculation.cache import cached
from process_discovery.event.event import Event
from process_discovery.event.base_group import BaseGroup
from process_discovery.event.event_group import EventGroup
from process_discovery.util.util import subset_sum

from copy import copy
from itertools import permutations, combinations


class BestAlignment:

    def get_best_alignment(self, model, log, alignment_cache=None):
        result, model_result = calculate_alignment_manager(model, log, alignment_cache, calculate_alignment)
        return result[len(result)-1], model_result[len(model_result)-1]


class BestAlignmentCached:
    from_cache = False

    def get_best_alignment(self, model, log, alignment_cache):
        result, model_result = calculate_alignment_manager(model, log, alignment_cache, cached(calculate_alignment),
                                                           self)
        return result[len(result)-1], model_result[len(model_result)-1]


def calculate_alignment_manager(model, log, alignment_cache, calculate_alignment_method, alignment_class=None):
    if isinstance(model, EventGroup):
        result_x, model_results = calculate_alignment_method(resolve_event_group(model.events), log, alignment_cache,
                                                             calculate_alignment_method, alignment_class)
    else:
        if are_all_events(model.events):
            result_x, model_results = calculate_alignment_method([model.events], log, alignment_cache,
                                                                 calculate_alignment_method, alignment_class)
        else:
            event_permutations = permutations(model.events)

            result_x, model_results = get_maxes([calculate_alignment_method(resolve_event_group(list(events)), log,
                                                                            alignment_cache, calculate_alignment_method,
                                                                            alignment_class)
                                                 for events in event_permutations])

    return result_x, model_results


def get_maxes(results):
    processed_results = []
    result_models = []
    for result in results:
        if len(result[0]) - 1 != len(result[1]):
            raise Exception
        processed_results.append([result[0][i] for i in range(len(result[0]))])
        result_models.append([result[1][i] for i in range(len(result[1]))])
    np_array = np.array(processed_results)
    maxes = np.argmax(np_array, axis=0)
    return [processed_results[maxes[i]][i] for i in range(len(maxes))], \
           [result_models[maxes[i + 1]][i] for i in range(len(maxes) - 1)]


# def parallel_event_permutations(events):
#     event_permutations = []
#     grouped_events = set()
#     simple_events = set()
#     for event in events:
#         if isinstance(event, BaseGroup):
#             grouped_events.add(event)
#         else:
#             simple_events.add(event)
#
#     n = len(simple_events)
#     max_len = len(grouped_events) + 1
#
#     subsets = subset_sum([i for i in range(1, n+1)], n, max_len)
#
#     all_grouped_events = list(permutations(grouped_events))
#
#     grouped_simple_events = []
#     for subset in subsets:
#         local_grouped_simple_events = {combinations(simple_events, subset[0])}
#         left = [simple_events.difference(x) for x in local_grouped_simple_events]
#         for i in range(1, len(subset)):
#             local_local_grouped_simple_events = combinations(left, subset[i])
#             left = [left.difference(x) for x in local_grouped_simple_events]
#
#     return event_permutations


def diagonal(model, log, pt):
    if log == model.name:
        return pt['MATCH']
    else:
        return pt['MISMATCH']


def diagonal_parallel(model, log, pt):
    # not sure if most efficient to unpack event here
    for event in model:
        if log == event.name:
            model.remove(event)
            return pt['MATCH'], event
    return pt['MISMATCH'], None


# This function creates the alignment and pointers matrices
def calculate_alignment(model, log, alignment_cache, calculate_alignment_method, alignment_class):
    penalty = {'MATCH': 0, 'MISMATCH': -2, 'GAP': -1}  # A dictionary for all the penalty values.
    m = len(model) + 1  # The dimension of the matrix rows.
    n = len(log) + 1  # The dimension of the matrix columns.
    model_results_local = [None] * m
    al_mat = np.zeros((m, n), dtype=int)  # Initializes the alignment matrix with zeros.
    for j in range(n):
        al_mat[0][j] = penalty['GAP'] * j
    # Fill the matrix with the correct values.

    for i in range(1, m):
        if should_go_recurrent(model[i-1]):
            al_mat[i], model_results_local[i] = recurrent_alignment(al_mat[i - 1], model[i - 1],
                                                                    [x for x in substrings_of_string_reversed(log)],
                                                                    alignment_cache, calculate_alignment_method,
                                                                    alignment_class)
        elif len(model[i-1]) > 1:
            al_mat[i], model_results_local[i] = parallel_alignment(al_mat[i - 1], model[i - 1],
                                                                   [x for x in substrings_of_string_reversed(log)],
                                                                   penalty)
        else:
            al_mat[i][0] = al_mat[i-1][0] + penalty['GAP']
            basic_alignment(al_mat, model[i - 1], log, penalty, i, n)

    model_results = get_all_tracebacks(al_mat, penalty['GAP'], model, log, model_results_local)

    return al_mat[m-1], model_results


def basic_alignment(al_mat, model_event, log, penalty, i, n):
    for j in range(1, n):
        di = al_mat[i - 1][j - 1] + diagonal(model_event, log[j - 1], penalty)  # The value for match/mismatch.
        ho = al_mat[i][j - 1] + penalty['GAP']  # The value for gap - horizontal.(from the left cell)
        ve = al_mat[i - 1][j] + penalty['GAP']  # The value for gap - vertical.(from the upper cell)
        al_mat[i][j] = max(di, ho, ve)  # Fill the matrix with the maximal value.(based on the python default maximum)


def recurrent_alignment(al_mat_x, model_events, logs, alignment_cache, calculate_alignment_method, alignment_class):
    # could add some stop improvements
    result_x = get_best_error_using_gap_move(model_events, al_mat_x)
    model_results_local = []
    [model_results_local.append([]) for _ in range(len(result_x))]

    for i in range(len(logs)):
        local_result_x, model_result_local = calculate_alignment_manager(model_events, logs[i],
                                                                         alignment_cache, calculate_alignment_method,
                                                                         alignment_class)

        [model_results_local[i].append([]) for _ in range(len(model_result_local))]
        for j in range(len(local_result_x)):
            if al_mat_x[i] + local_result_x[j] > result_x[j + i]:
                result_x[j + i] = al_mat_x[i] + local_result_x[j]
            if len(model_result_local) - j - 1 >= 0:
                model_results_local[i][j] = model_result_local[len(model_result_local) - j - 1]
    return result_x, model_results_local


def parallel_alignment(al_mat_x, model_events, logs, pt):
    # could add some stop improvements
    result_x = get_best_error_using_gap_move(model_events, al_mat_x)
    model_results = []
    [model_results.append([]) for _ in range(len(result_x))]

    for i in range(len(logs)):
        [model_results[i].append([]) for _ in range(len(logs[i]))]
        local_model = copy(model_events)
        local_result_x = [0 for _ in range(len(logs[i]))]
        model_results_local = [None] * len(local_result_x)
        # initialize first elem
        local_result_x[0], event = diagonal_parallel(local_model, logs[i][0], pt)
        misses_counter = local_result_x[0]/pt["MISMATCH"]
        if event:
            model_results_local[0] = event

        for j in range(1, len(logs[i])):
            is_match, event = diagonal_parallel(local_model, logs[i][j], pt)
            misses_counter += is_match/pt["MISMATCH"]
            local_result_x[j] = max(local_result_x[j-1] + is_match, -int(misses_counter + len(local_model)))
            if event:
                model_results_local[j] = event

        for j in range(len(local_result_x)):
            penalty_for_skipped_model_events = get_penalty_for_model_skipped(model_events, j)
            # +1 because al_mat have extra column
            if al_mat_x[i] + local_result_x[j] - penalty_for_skipped_model_events >= result_x[j + i + 1]:
                result_x[j + i + 1] = al_mat_x[i] + local_result_x[j] - penalty_for_skipped_model_events
            model_results[i][j] = model_results_local[:(len(model_results_local) - j)]  # + [None] * (j+1)
    return result_x, model_results


def traceback(al_mat, penalty_gap, model, log_global, model_results_local) -> []:
    array = copy(al_mat)
    log = copy(log_global)
    model_result = []
    i = len(model)  # The dimension of the matrix rows.
    j = len(log)  # The dimension of the matrix columns.

    while i != 0:
        event_group_full_length = len(model[i - 1])
        if model_results_local[i] is not None:
            matched_flag = False
            if array[i][j] == array[i - 1][j] + event_group_full_length * penalty_gap:
                [model_result.append(None) for _ in range(event_group_full_length)]
                array[i][j] = 0
                i -= 1
            else:
                for k in range(j):
                    events = get_not_none(model_results_local[i][k][len(model_results_local[i][k]) - (j-k)], log)
                    if array[i][j] == array[i - 1][k] + \
                            (event_group_full_length + (j-k) - 2 * len(events)) * penalty_gap:
                        [model_result.append(x) for x in reversed(events)]
                        for x in events:
                            log.remove(x.name)
                        [model_result.append(None) for _ in range(event_group_full_length - len(events))]
                        array[i][j] = 0
                        i -= 1
                        j = k
                        matched_flag = True
                        break
                if not matched_flag:
                    if array[i][j] == array[i][j - 1] + penalty_gap:
                        array[i][j] = 0
                        j -= 1
        else:
            if array[i][j] == array[i - 1][j] + penalty_gap:
                model_result.append(None)
                array[i][j] = 0
                i -= 1
            elif array[i][j] == array[i][j - 1] + penalty_gap:
                array[i][j] = 0
                j -= 1
            elif array[i][j] == array[i - 1][j - 1]:
                model_result.append(model[i-1])
                log.remove(model[i-1].name)
                array[i][j] = 0
                i -= 1
                j -= 1

    return list(reversed(model_result))


def get_all_tracebacks(al_mat, penalty_gap, model, log, model_results_local):
    len_log = len(log)
    return [traceback(al_mat[:, :i + 2], penalty_gap, model, log[:i + 1],
                      model_results_local) for i in range(len_log)]


def get_not_none(model_result_local, log):
    return [x for x in model_result_local if x is not None and x.name in log]


def get_penalty_for_model_skipped(model_events, j):
    return max(0, len(model_events) - j - 1)


def get_best_error_using_gap_move(model_events, al_mat_x):
    return [(max([-len(model_events) - j + al_mat_x[i] for j in range(i+1)])) for i in range(len(al_mat_x))]


def should_go_recurrent(event):
    return not (isinstance(event, Event) or isinstance(event, list))


def are_all_events(events):
    return not any(isinstance(event, BaseGroup) for event in events)


def substrings_of_string_reversed(string):
    return (string[x:] for x in range(len(string)))


def resolve_event_group(event_group_local):
    model_list = []

    for event in event_group_local:
        if isinstance(event, Event):
            model_list.append(event)
        elif isinstance(event, EventGroup):
            if are_all_events(event.events):
                [model_list.append(x) for x in event.events]
            else:
                model_list.append(event)
        else:            # isinstance(EventGroupParallel):
            if are_all_events(event.events):
                model_list.append([event for event in event.events])
            else:
                model_list.append(event)

    return model_list


def get_worst_allowed_alignment(expression) -> int:
    return math.ceil(len(expression) / 2)
