from algorithm.parameters import params
from representation.individual import Individual


class IndividualWithMetrics(Individual):

    def __init__(self, individual: Individual):
        self.genome = individual.genome
        self.tree = individual.tree
        self.name = individual.name
        self.depth = individual.depth
        self.nodes = individual.nodes
        self.phenotype = individual.phenotype
        self.runtime_error = individual.runtime_error
        self.used_codons = individual.used_codons
        self.invalid = individual.invalid
        self.fitness = individual.fitness
        self.metrics = params['FITNESS_FUNCTION'].metrics

    def evaluate(self):
        """
        Evaluates phenotype in using the fitness function set in the params
        dictionary. For regression/classification problems, allows for
        evaluation on either training or test distributions. Sets fitness
        value.

        :return: Nothing unless multi-core evaluation is being used. In that
        case, returns self.
        """

        # Evaluate fitness using specified fitness function.
        self.fitness = params['FITNESS_FUNCTION'](self)
        self.metrics = params['FITNESS_FUNCTION'].metrics

        if params['MULTICORE']:
            return self
