from fitness.base_ff_classes.base_ff import base_ff
from processdiscovery.evaluation.metrics_calculation import evaluate_guess
from processdiscovery.log.log_util import LogInfo


class process_fitness(base_ff):
    maximise = True

    def __init__(self):
        # Initialise base fitness function class.
        super().__init__()
        self.alignment_cache = dict()
        self.routes_cache = dict()
        self.log_info = LogInfo('discovered-processes.csv')
        self.max_allowed_complexity = len(self.log_info.log) * 100

    def evaluate(self, ind, **kwargs):
        guess = ind.phenotype

        return evaluate_guess(guess, self.log_info, self.alignment_cache, self.max_allowed_complexity)
