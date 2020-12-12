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
    if log == model:
        return pt['MATCH']
    else:
        return pt['MISMATCH']


def diagonal_parallel(model, log, pt):
    if log in model:
        model.remove(log)
        return pt['MATCH']
    else:
        return pt['MISMATCH']


def nw_wrapper(model, log):
    result = nw_is_parallel_wrapper(model, log)
    return result[len(result)-1]


def nw_is_parallel_wrapper(model, log):
    if isinstance(model, EventGroup):
        result_x = nw(resolve_parallel_event_group(model.events), log)
    else:
        if are_all_events(model.events):
            result_x = nw([[event.name for event in model.events]], log)
        else:
            event_permutations = permutations(model.events)

            result_x = get_maxes([nw(resolve_parallel_event_group(list(events)), log) for events in event_permutations])

    return result_x


#--------------------------------------------------------
#This function creates the alignment and pointers matrices
def nw(model, log):
    penalty = {'MATCH': 0, 'MISMATCH': -2, 'GAP': -1} #A dictionary for all the penalty values.
    n = len(log) + 1 #The dimension of the matrix columns.
    m = len(model) + 1 #The dimension of the matrix rows.
    al_mat = np.zeros((m, n), dtype=int) #Initializes the alignment matrix with zeros.
    #Scans all the first rows element in the matrix and fill it with "gap penalty"
    for i in range(m):
        al_mat[i][0] = penalty['GAP'] * i
    #Scans all the first columns element in the matrix and fill it with "gap penalty"
    for j in range(n):
        al_mat[0][j] = penalty['GAP'] * j
    #Fill the matrix with the correct values.

    for i in range(1, m):
        if should_go_recurrent(model[i-1]):
            al_mat[i] = recurrent_nw(al_mat[i-1], model[i-1], [x for x in substrings_of_string_reversed(log)], i)
        elif len(model[i-1]) > 1:
            al_mat[i] = parallel_nw(al_mat[i-1], model[i-1], [x for x in substrings_of_string_reversed(log)], penalty, i)
        else:
            basic_nw(al_mat, model[i - 1], log, penalty, i, n)

    np_array = np.array(al_mat)
    print(model)
    print(np_array)

    return al_mat[m-1]


def get_maxes(results):
    np_array = np.array(results)
    return np.max(np_array, axis=0)


def basic_nw(al_mat, model_event, log, penalty, i, n):
    for j in range(1, n):
        di = al_mat[i - 1][j - 1] + diagonal(model_event, log[j - 1], penalty)  # The value for match/mismatch.
        ho = al_mat[i][j - 1] + penalty['GAP']  # The value for gap - horizontal.(from the left cell)
        ve = al_mat[i - 1][j] + penalty['GAP']  # The value for gap - vertical.(from the upper cell)
        al_mat[i][j] = max(di, ho, ve)  # Fill the matrix with the maximal value.(based on the python default maximum)


def recurrent_nw(al_mat_x, model_events, logs, pos):
    # could add some stop improvements
    result_x = get_best_error_using_gap_move(model_events, al_mat_x)

    for i in range(len(logs)):
        local_result_x = nw_is_parallel_wrapper(model_events, logs[i])

        for j in range(len(local_result_x)):
            if al_mat_x[i] + local_result_x[j] > result_x[j + i]:
                result_x[j + i] = al_mat_x[i] + local_result_x[j]
    return result_x


def parallel_nw(al_mat_x, model_events, logs, pt, pos):
    # could add some stop improvements
    result_x = get_best_error_using_gap_move(model_events, al_mat_x)

    for i in range(len(logs)):
        local_model = copy(model_events)
        local_result_x = [0 for _ in range(len(logs[i]))]
        # initialize first elem
        local_result_x[0] = diagonal_parallel(local_model, logs[i][0], pt)
        misses_counter = local_result_x[0]/pt["MISMATCH"]

        for j in range(1, len(logs[i])):
            is_match = diagonal_parallel(local_model, logs[i][j], pt)
            misses_counter += is_match/pt["MISMATCH"]
            local_result_x[j] = max(local_result_x[j-1] + is_match, -int(misses_counter + len(local_model)))

        for j in range(len(local_result_x)):
            penalty_for_skipped_model_events = get_penalty_for_model_skipped(model_events, j)
            number_of_matches = (j + 1) - int(local_result_x[j]/pt["MISMATCH"])
            # +1 because al_mat have extra column
            if al_mat_x[i] + local_result_x[j] - penalty_for_skipped_model_events > result_x[j + i + 1]:
                result_x[j + i + 1] = al_mat_x[i] + local_result_x[j] - penalty_for_skipped_model_events
    return result_x


def get_penalty_for_model_skipped(model_events, j):
    return max(0, len(model_events) - j - 1)


def get_best_error_using_gap_move(model_events, al_mat_x):
    return [(max([-len(model_events) - j + al_mat_x[i] for j in range(i+1)])) for i in range(len(al_mat_x))]


def should_go_recurrent(event):
    if isinstance(event, str) or isinstance(event, list):
        return False
    else:
        return True


def are_all_events(events):
    for event in events:
        if isinstance(event, BaseGroup):
            return False
    return True


def substrings_of_string(string):
    return [string[:x] for x in range(len(string))]


def substrings_of_string_reversed(string):
    return [string[x:] for x in range(len(string))]


def resolve_parallel_event_group(event_group):
    model_list = []

    for event in event_group:
        if isinstance(event, Event):
            model_list.append(event.name)
        elif isinstance(event, EventGroup):
            if are_all_events(event.events):
                [model_list.append(x.name) for x in event.events]
            else:
                model_list.append(event)
        else:            # isinstance(EventGroupParallel):
            if are_all_events(event.events):
                model_list.append([event.name for event in event.events])
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


# event_group = EventGroupParallel([Event('t'),
#                                   EventGroupParallel([EventGroupParallel(string_to_events('tp')), Event('q')]),
#                                   EventGroup([EventGroupParallel(string_to_events('ac')),
#                                               EventGroup(string_to_events('ez'))]),
#                                   EventGroupParallel(string_to_events('xys'))])
#
# # self.assertEqual(nw_wrapper('zxabcdezx', event_group), -8)
# nw_wrapper(event_group, 'zxabcdezxq')
