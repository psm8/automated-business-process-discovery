from fitness.base_ff_classes.base_ff import base_ff
from gate.seq_gate import SeqGate
from fitness.alignment_calculation import calculate_alignment, flatten_values, nv
from util.util import is_struct_empty, string_to_dictionary
from event.event_group import EventGroup
from event.event_group_parallel import EventGroupParallel

import math

def get_log():
    return ["abcdefghijklmn", "acbdefghijklmn"]


def get_log_length(log: list):
    return sum(len(x) for x in log)


def calculate_simplicity_metric(s):
    return


def calculate_precision_metric(guess):
    sum_branches = sum([mappings[char].event for char in guess])
    precision = 0
    
    return precision


def calculate_fitness_metric(log, log_length, log_average_length, gate, min_length, max_length):
    n = round(log_average_length)
    i = 1
    best_alignment = 0
    # should be change later
    while not n < calculate_min_allowed_length(log_average_length) and \
            not n > calculate_max_allowed_length(log_average_length):
        if min_length <= n <= max_length:
            routes = gate.get_all_n_length_routes(n)
            #fix_routes to strings inside gate
            if routes is not None and not is_struct_empty(routes):
                strings_list = flatten_values(routes)
                best_local_error = 0
                for elem in log:
                    min_local = 1023
                    for string in strings_list:
                        value = nv(elem, resolve_parallel(string), n)
                        if value < min_local:
                            min_local = value
                            string_global = string
                    best_local_error += min_local
                best_local_alignment = 1 - (best_local_error / (log_length + len(log) * len(strings_list[0])))
                if best_local_alignment > best_alignment:
                    best_alignment = best_local_alignment
        if i % 2 == 1:
            n -= i
        else:
            n += i
        i += 1
    return best_alignment


def resolve_parallel(route):
    model_list = []
    for event_group in range(len(route)):
        if isinstance(route[i], EventGroup):
            [model_list.append(event) for event in route[i].events]
        else:                                       # isinstance(EventGroupParallel):
            for j in range(len(route[i].events)):
                model_list.append(route[i].events)
    return model_list


# def resolve_parallel(route):
#     model_list = []
#     first_event_in_parallel_group = -1
#     parallel_group = []
#     for i in range(len(route)):
#         if isinstance(EventGroup):
#             model_list.append(route[i].event.)
#             first_event_in_parallel_group = -1
#             parallel_group = []
#         else:
#             parallel_group += route[i]
#             model_list.append(parallel_group)
#             if first_event_in_parallel_group != -1:
#                 len_model_list = len(model_list)
#                 for j in range(first_event_in_parallel_group, len_model_list - 1):
#                     model_list[j] = parallel_group
#             else:
#                 first_event_in_parallel_group = i


def decode(string: str) -> []:
    local_result = ""
    # test against lambda
    for char in string:
        local_result += mappings[char].event
    return local_result


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


def calculate_max_allowed_length(log_average_length):
    return math.ceil(1.5 * log_average_length)


def calculate_min_allowed_length(log_average_length):
    return math.floor(0.5 * log_average_length)


def evaluate_guess(guess):
    log = get_log()
    log_length = get_log_length(log)
    log_average_length = log_length / len(log)
    gate = SeqGate()
    gate.parse(guess)
    min_length = gate.get_model_min_length()
    if min_length > calculate_max_allowed_length(log_average_length):
        return -100000
    max_length = gate.get_model_max_length()
    if max_length < calculate_min_allowed_length(log_average_length):
        return -100000
    # processes = gate.get_processes_list()
    # first_occurrences = gate.find_first_occurrence(Process(string_to_dictionary("abcd"), 0))
    # length_metric = calculate_length_metric(guess, 50)
    fitness_metric = calculate_fitness_metric(log, log_length, log_average_length, gate,
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
