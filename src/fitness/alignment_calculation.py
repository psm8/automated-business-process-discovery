import numpy as np
import math

from event.event import Event
from event.base_group import BaseGroup
from event.event_group import EventGroup
from event.event_group_parallel import EventGroupParallel
from test.test_util import string_to_events

from copy import copy
from itertools import permutations


#-------------------------------------------------------
#This function returns to values for cae of match or mismatch
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


def nw_wrapper(model, log):
    result, model_result = nw_is_parallel_wrapper(model, log)
    return result[len(result)-1], model_result[len(model_result)-1]


def nw_is_parallel_wrapper(model, log):
    if isinstance(model, EventGroup):
        result_x, model_results = nw(resolve_parallel_event_group(model.events), log)
    else:
        if are_all_events(model.events):
            result_x, model_results = nw([[event for event in model.events]], log)
        else:
            # change way permutations are calculated
            event_permutations = permutations(model.events)

            result_x, model_results = get_maxes([nw(resolve_parallel_event_group(list(events)), log) for events in event_permutations])

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


def parallel_event_permutations(events):
    event_permutations = []
    grouped_events = []
    simple_events = []
    for event in events:
        if isinstance(event, BaseGroup):
            grouped_events.append(event)
        else:
            simple_events.append(event)

    slot_lengths = permutations([i for i in range( + 1)])


#--------------------------------------------------------
#This function creates the alignment and pointers matrices
def nw(model, log):
    penalty = {'MATCH': 0, 'MISMATCH': -2, 'GAP': -1} #A dictionary for all the penalty values.
    m = len(model) + 1 #The dimension of the matrix rows.
    model_results_local = [None] * m
    n = len(log) + 1 #The dimension of the matrix columns.
    al_mat = np.zeros((m, n), dtype=int) #Initializes the alignment matrix with zeros.
    #Scans all the first rows element in the matrix and fill it with "gap penalty"
    for i in range(m):
        al_mat[i][0] = penalty['GAP'] * i
    #Scans all the first columns element in the matrix and fill it with "gap penalty"
    # possibly could be removed
    for j in range(n):
        al_mat[0][j] = penalty['GAP'] * j
    #Fill the matrix with the correct values.

    for i in range(1, m):
        if should_go_recurrent(model[i-1]):
            al_mat[i], model_results_local[i] = recurrent_nw(al_mat[i-1], model[i-1],
                                                             [x for x in substrings_of_string_reversed(log)], i)
        elif len(model[i-1]) > 1:
            al_mat[i], model_results_local[i] = parallel_nw(al_mat[i-1], model[i-1],
                                                            [x for x in substrings_of_string_reversed(log)], penalty, i)
        else:
            al_mat[i][0] = al_mat[i-1][0] + penalty['GAP']
            basic_nw(al_mat, model[i - 1], log, penalty, i, n)

    model_results = get_all_tracebacks(al_mat, penalty['GAP'], model, log, model_results_local)

    # print(model)
    # print(al_mat)

    return al_mat[m-1], model_results


def basic_nw(al_mat, model_event, log, penalty, i, n):
    for j in range(1, n):
        di = al_mat[i - 1][j - 1] + diagonal(model_event, log[j - 1], penalty)  # The value for match/mismatch.
        ho = al_mat[i][j - 1] + penalty['GAP']  # The value for gap - horizontal.(from the left cell)
        ve = al_mat[i - 1][j] + penalty['GAP']  # The value for gap - vertical.(from the upper cell)
        al_mat[i][j] = max(di, ho, ve)  # Fill the matrix with the maximal value.(based on the python default maximum)


def recurrent_nw(al_mat_x, model_events, logs, pos):
    # could add some stop improvements
    result_x = get_best_error_using_gap_move(model_events, al_mat_x)
    model_results_local = []
    [model_results_local.append([]) for _ in range(len(result_x))]

    for i in range(len(logs)):
        local_result_x, model_result_local = nw_is_parallel_wrapper(model_events, logs[i])

        [model_results_local[i].append([]) for _ in range(len(model_result_local))]
        for j in range(len(local_result_x)):
            if al_mat_x[i] + local_result_x[j] > result_x[j + i]:
                result_x[j + i] = al_mat_x[i] + local_result_x[j]
            if len(model_result_local) - j - 1 >= 0:
                model_results_local[i][j] = model_result_local[len(model_result_local) - j - 1]
    return result_x, model_results_local


def parallel_nw(al_mat_x, model_events, logs, pt, pos):
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
            number_of_matches = (j + 1) - int(local_result_x[j]/pt["MISMATCH"])
            # +1 because al_mat have extra column
            if al_mat_x[i] + local_result_x[j] - penalty_for_skipped_model_events >= result_x[j + i + 1]:
                result_x[j + i + 1] = al_mat_x[i] + local_result_x[j] - penalty_for_skipped_model_events
            model_results[i][j] = model_results_local[:(len(model_results_local) - j)] # + [None] * (j+1)
    return result_x, model_results


def traceback_col_seq(al_mat, penalty_gap, model, log_global, model_results_local):
    array = copy(al_mat)
    log = copy(log_global)
    model_result = []
    i = len(model)  #The dimension of the matrix rows.
    j = len(log)  #The dimension of the matrix columns.

    while i != 0:
        event_group_full_length = len(model[i - 1])
        if model_results_local[i] is not None:
            if array[i][j] == array[i - 1][j] + event_group_full_length * penalty_gap:
                [model_result.append(None) for _ in range(event_group_full_length)]
                array[i][j] = 0
                i -= 1

            else:
                for k in range(j):
                    processes = get_not_none(model_results_local[i][k], log)
                    if array[i][j] == array[i - 1][k] + (event_group_full_length + (j-k) - 2 * len(processes)) * penalty_gap:
                        [model_result.append(x) for x in processes]
                        for x in processes:
                            log = log.replace(x.name, "", 1)
                        [model_result.append(None) for _ in range(event_group_full_length - len(processes))]
                        array[i][j] = 0
                        i -= 1
                        j = k
                        break

        else:
            if array[i][j] == array[i - 1][j] + penalty_gap:
                model_result.append(None)
                array[i][j] = 0
                i -= 1
            elif array[i][j] == array[i - 1][j - 1]:
                model_result.append(model[i-1])
                log = log.replace(model[i-1].name, "", 1)
                array[i][j] = 0
                i -= 1
                j -= 1
            elif array[i][j] == array[i][j - 1] + penalty_gap:
                array[i][j] = 0
                j -= 1

    # print(model_result)
    # print(log_result)
    # print(array)

    return model_result


def get_all_tracebacks(al_mat, penalty_gap, model, log, model_results_local):
    len_log = len(log)
    return [traceback_col_seq(al_mat[:, :i+2], penalty_gap, model, log[:i+1],
                              prepare_model_result(model_results_local, i, len_log)) for i in range(len_log)]


def prepare_model_result(model_results_local, i, len_log):
    result = []
    for model_result_local in model_results_local:
        if model_result_local is not None:
            model_result_local = model_result_local[:i+1]
            result.append([x[len_log - (i + 1)] for x in model_result_local])
        else:
            result.append(model_result_local)

    return result


def get_not_none(model_result_local, log):
    return [x for x in model_result_local if x is not None and x.name in log]


def get_penalty_for_model_skipped(model_events, j):
    return max(0, len(model_events) - j - 1)


def get_best_error_using_gap_move(model_events, al_mat_x):
    return [(max([-len(model_events) - j + al_mat_x[i] for j in range(i+1)])) for i in range(len(al_mat_x))]


def should_go_recurrent(event):
    if isinstance(event, Event) or isinstance(event, list):
        return False
    else:
        return True


def are_all_events(events):
    for event in events:
        if isinstance(event, BaseGroup):
            return False
    return True


def substrings_of_string_reversed(string):
    return [string[x:] for x in range(len(string))]


def resolve_parallel_event_group(event_group_local):
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


# def resolve_parallel(event_group):
#     model_list = []
#     if isinstance(event_group, EventGroup):
#         for i in range(len(event_group.events)):
#             if isinstance(event_group.events[i], Event):
#                 model_list.append(event_group.events[i])
#             elif are_all_events(event_group.events[i]):
#                 model_list.append(event_group.events[i])
#             elif isinstance(event_group.events[i], EventGroup):
#                 [model_list.append(event) for event in event_group.events[i].events]
#             else:                                       # isinstance(EventGroupParallel):
#                 for j in range(len(event_group.events[i].events.events)):
#                     model_list.append(event_group.events[i].events.events)
#     else:           # isinstance(EventGroupParallel):
#         if are_all_events(event_group):
#             for i in range(len(event_group.events)):
#                 model_list.append(event_group.events[i])
#         else:
#             for i in range(len(event_group.events)):
#                 event_permutations = permutations(event_group.events[i])
#                 [model_list.append(list(x)) for x in event_permutations]
#
#     return model_list

def flatten_values(values2d_list):
    results = []
    values2d = values2d_list.pop(0)
    for values in values2d:
        if isinstance(values, list):
            results.append(values)
        else:
            results.append([values])

    for values2d in values2d_list:
        new_result = []
        for values in values2d:
            if isinstance(values, list):
                for i in range(len(results)):
                    local_result = copy(results[i])
                    [local_result.append(value) for value in values]
                    new_result.append(local_result)
            else:
                # it probably doesnt work
                for i in range(len(results)):
                    local_result = copy(results[i])
                    local_result.append(values)
                    new_result.append(local_result)
        results = new_result

    return results


def get_best_case() -> int:
    return 0


def get_worst_allowed_alignment(expression) -> int:
    return math.ceil(len(expression) / 2)


# event_group = EventGroupParallel(string_to_events('pqacezxys'))
#
# result, model_result = nw_wrapper(event_group, 'zxklmnozx')