from fitness.base_ff_classes.base_ff import base_ff
from gate.base_gate import BaseGate


def calculate_simplicity_metric(s):
    return


def calculate_fitness_metric(gate):
    list1 = ["abcd", "abd", "acd", "abdc"]
    result = 0
    for elem in list1:
        result += gate.traverse(elem)

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


class process(base_ff):
    maximise = True

    def __init__(self):
        # Initialise base fitness function class.
        super().__init__()

    def evaluate(self, ind, **kwargs):
        guess = ind.phenotype

        gate = BaseGate()
        gate.parse(guess)

        length_metric = calculate_length_metric(guess, 50)
        fitness_metric = calculate_fitness_metric(gate)
        return length_metric * fitness_metric
