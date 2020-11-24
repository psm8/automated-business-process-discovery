from fitness.base_ff_classes.base_ff import base_ff
from gate.seq_gate import SeqGate
from fitness.alignment_calculation import routes_to_strings

import math


def string_to_dictionary(string: str):
    dictionary = dict()
    i = 0
    for x in string:
        dictionary[i] = (x, -1)
        i += 1
    return dictionary


def get_model_average_length():
    return 3.5


def calculate_simplicity_metric(s):
    return


def calculate_fitness_metric(gate):
    list1 = ["abcd", "abd", "acd", "abdc"]
    result = 0
    for elem in list1:
        result += 1

    return result/14


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


def calculate_max_allowed_length():
    return math.ceil(1.5 * get_model_average_length())

def calculate_min_allowed_length():
    return math.floor(0.5 * get_model_average_length())

class process_fitness(base_ff):
    maximise = True

    def __init__(self):
        # Initialise base fitness function class.
        super().__init__()

    def evaluate(self, ind, **kwargs):
        guess = ind.phenotype

        gate = SeqGate()
        gate.parse(guess)
        min_length = gate.get_model_min_length()
        if min_length > calculate_max_allowed_length():
            return -100000
        max_length = gate.get_model_max_length()
        if max_length < calculate_min_allowed_length():
            return -100000
        processes = gate.get_processes_list()
        routes = gate.get_all_n_length_routes(min_length)
        # first_occurrences = gate.find_first_occurrence(Process(string_to_dictionary("abcd"), 0))
        test = routes_to_strings(routes)
        length_metric = calculate_length_metric(guess, 50)
        fitness_metric = calculate_fitness_metric(gate)
        return length_metric * fitness_metric
