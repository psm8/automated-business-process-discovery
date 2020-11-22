from fitness.base_ff_classes.base_ff import base_ff
from gate.seq_gate import SeqGate

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
    return math.floor(2 * get_model_average_length()) - 1


class process_fitness(base_ff):
    maximise = True

    def __init__(self):
        # Initialise base fitness function class.
        super().__init__()

    def evaluate(self, ind, **kwargs):
        guess = ind.phenotype

        gate = SeqGate()
        gate.parse(guess)
        min_length = gate.get_model_minimal_length()
        if min_length > calculate_max_allowed_length():
            return -100000
        processes = gate.get_processes_list()
        routes = gate.get_all_n_length_routes(8)
        # first_occurrences = gate.find_first_occurrence(Process(string_to_dictionary("abcd"), 0))

        length_metric = calculate_length_metric(guess, 50)
        fitness_metric = calculate_fitness_metric(gate)
        return length_metric * fitness_metric
