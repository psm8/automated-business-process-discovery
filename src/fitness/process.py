from fitness.base_ff_classes.base_ff import base_ff
#from parser.parser import Parser


def calculate_simplicity_metric(s):
    return


class process(base_ff):
    maximise = True

    def __init__(self):
        # Initialise base fitness function class.
        super().__init__()

    def evaluate(self, ind, **kwargs):
        guess = ind.phenotype
        length = len(guess)
        #gate = Parser.parse(guess)
        # Loops as long as the shorter of two strings
        if length == 50:
            # Perfect match.
            fitness = 1
        else:
            # Imperfect match, find ASCII distance to match.
            distance = abs(50 - length)
            fitness = 1 / (1 +distance)
        return fitness
