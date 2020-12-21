from fitness.base_ff_classes.base_ff import base_ff
from processdiscovery.evaluation.metrics_calculation import evaluate_guess


class process_fitness(base_ff):
    maximise = True

    def __init__(self):
        # Initialise base fitness function class.
        super().__init__()

    def evaluate(self, ind, **kwargs):
        guess = ind.phenotype

        return evaluate_guess(guess)
