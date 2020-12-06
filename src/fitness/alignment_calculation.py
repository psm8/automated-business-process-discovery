import numpy as np
import math

from event.event import Event
from event.base_group import BaseGroup
from event.event_group import EventGroup
from event.event_group_parallel import EventGroupParallel

from itertools import permutations


#-------------------------------------------------------
#This function returns to values for cae of match or mismatch
def diagonal(log, model, pt):
    if isinstance(model, str):
        if log == model:
            return pt['MATCH']
        else:
            return pt['MISMATCH']
    else:
        if log in model:
            model.remove(log)
            return pt['MATCH']
        else:
            return pt['MISMATCH']


def nw_wrapper(log, model):
    result = nw_is_parallel_wrapper(log, model)
    return result[len(result)-1]


def nw_is_parallel_wrapper(log, model):
    if isinstance(model, EventGroup):
        result_x = nw(log, resolve_parallel_event_group(model.events))
    else:
        if are_all_events(model.events):
            model_parallel = []
            for i in range(len(model.events)):
                model_parallel.append([event.name for event in model.events])
            result_x = nw(log, model_parallel)
        else:
            event_permutations = permutations(model.events)

            result_x = get_maxes([nw(log, resolve_parallel_event_group(list(events))) for events in event_permutations])

    return result_x


#--------------------------------------------------------
#This function creates the alignment and pointers matrices
def nw(log, model):
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

    pos = 1
    if should_go_recurrent(model[0]):
        recurrent_nw(log, model[0], pos)

    # want to iterate in square pattern
    i = 1
    j = 1
    k = 1
    while True:
        for i in range(1, k + 1):
            basic_nw(al_mat, log, model[i - 1], penalty, i, j)
        if k == min(m, n) - 1:
            break
        i += 1
        for j in range(1, i):
            basic_nw(al_mat, log, model[i - 1], penalty, i, j)
        j += 1
        k += 1

    if n > min(m, n):
        for it in range(min(m, n), n):
            for i in range(1, min(m, n)):
                basic_nw(al_mat, log, model[i - 1], penalty, i, it)
    elif m > min(m, n):
        for it in range(min(m, n), m):
            for j in range(1, min(m, n)):
                basic_nw(al_mat, log, model[it - 1], penalty, it, j)

    np_array = np.array(al_mat)
    print(np_array)

    return al_mat[m-1]


def get_maxes(results):
    np_array = np.array(results)
    return np.max(np_array, axis=0)


def basic_nw(al_mat, log, model_event, penalty, i, j):
    di = al_mat[i - 1][j - 1] + diagonal(log[j - 1], model_event, penalty)  # The value for match/mismatch.
    ho = al_mat[i][j - 1] + penalty['GAP']  # The value for gap - horizontal.(from the left cell)
    ve = al_mat[i - 1][j] + penalty['GAP']  # The value for gap - vertical.(from the upper cell)
    al_mat[i][j] = max(di, ho, ve)  # Fill the matrix with the maximal value.(based on the python default maximum)


def fill_result_matrix(al_mat, local_result_matrix, pos):
    return al_mat


def recurrent_nw(log, model_events, pos):
    # could add some stop improvements
    result_x = [-999 for _ in (model_events + min(len(log) - pos, model_events))]
    for i in range(min(len(log) - pos, model_events)):
        local_result_x = nw_is_parallel_wrapper(trim_log(log, pos + i, len(model_events) + i), model_events)
        for j in range(len(local_result_x)):
            if local_result_x[j] - i > result_x[j + i]:
                result_x[j + i] = local_result_x[j] - i
    return result_x


def trim_log(log, pos, len_model):
    return log[pos:min(pos+len_model, len(log)-1)]


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
                for j in range(len(event.events)):
                    model_list.append([event.name for event in event.events])
            else:
                model_list.append(event)

    return model_list


# def event_group_to_strings(struct):
#     if struct:
#         # check if list of tuples
#         if isinstance(struct, BaseGroup):
#             values = []
#             for elem in struct:
#                 routes = event_group_to_strings(elem)
#                 for route in routes:
#                     values.append(route)
#             results = values
#         # else list of lists and events
#         else:
#             values = []
#             for elem in struct:
#                 # if isinstance(elem, list):
#                 #     values.append(routes_to_strings(elem))
#                 # else:
#                 values.append(elem)
#             results = flatten_values(values)
#
#         return results
#     else:
#         return []

# def touples_to_strings(struct):
#     if struct:
#         values = []
#         for elem in struct:
#             routes = routes_to_strings(elem)
#             for route in routes:
#                 values.append(route)
#         results = values
#         # else list of lists and events
#         return results
#     else:
#         return []
#
# def listss_to_strings(struct):
#     if struct:
#         values = []
#         for elem in struct:
#             if isinstance(elem, list):
#                 values.append(routes_to_strings(elem))
#             else:
#                 values.append(elem)
#         results = flatten_values(values)
#
#         return results
#     else:
#         return []

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
    if isinstance(values2d, list):
        for values in values2d:
            results.append(values)
    else:
        results.append(values2d)

    for values2d in values2d_list:
        new_result = []
        if isinstance(values2d, list):
            for values in values2d:
                for i in range(len(results)):
                    new_result.append(results[i] + values)
        else:
            for i in range(len(results)):
                new_result.append(results[i].add_event(values2d))
        results = new_result

    return results


def get_best_case() -> int:
    return 0


def get_worst_allowed_alignment(expression) -> int:
    return math.ceil(len(expression) / 2)


# event_group_events = []
# for x in 'pqacezxys':
#     event_group_events.append(Event(x))
# event_group = EventGroup(event_group_events)
#
# # self.assertEqual(nw_wrapper('zxabcdezx', event_group), -8)
# nw_wrapper('zxabcdezx', event_group)