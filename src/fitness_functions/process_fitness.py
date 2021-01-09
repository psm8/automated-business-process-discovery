from fitness.base_ff_classes import base_ff
from processdiscovery.evaluation.metrics_calculation import evaluate_guess
from processdiscovery.log.log_util import LogInfo
from processdiscovery.exception.timout_exception import timeout, TimeoutException
from algorithm import params

import cachetools
import pickle
import os
import logging


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class process_fitness(base_ff, metaclass=Singleton):
    maximise = True

    def __init__(self):
        super().__init__()
        self.alignment_cache = self.load_caches()
        self.guess = ''
        self.vars = LogInfo(params["DATASET"]).log_unique_events
        self.log_info = LogInfo(params["DATASET"])
        self.max_allowed_complexity = len(self.log_info.log) * params["MAX_ALLOWED_COMPLEXITY_FACTOR"]

    def __call__(self, ind, **kwargs):
        """


        :param ind: An individual to be evaluated.
        :return: The fitness of the evaluated individual.
        """

        try:
            # Evaluate the fitness using the evaluate() function. This function
            # can be over-written by classes which inherit from this base
            # class.
            fitness = self.evaluate(ind, **kwargs)

        except (FloatingPointError, ZeroDivisionError, OverflowError,
                MemoryError):
            # FP err can happen through eg overflow (lots of pow/exp calls)
            # ZeroDiv can happen when using unprotected operators
            fitness = base_ff.default_fitness

            # These individuals are valid (i.e. not invalids), but they have
            # produced a runtime error.
            ind.runtime_error = True

        except Exception as err:
            # Other errors should not usually happen (unless we have
            # an unprotected operator) so user would prefer to see them.
            logging.error(self.guess)
            logging.error(err)
            self.save_cache("alignment-cache" + str(id(self)) + ".pickle")
            raise

        return fitness

    def evaluate(self, ind, **kwargs):
        self.guess = ind.phenotype

        try:
            fitness = timeout(params["TIMEOUT"])(evaluate_guess)(self.guess, self.log_info, self.alignment_cache,
                                                                 self.max_allowed_complexity)
        except TimeoutException:
            logging.error("TimeoutException: " + self.guess)
            return 0
        return fitness

    def save_cache(self, path: str):
        with open("../cache/" + path, 'wb') as f:
            pickle.dump(self.alignment_cache, f)

    def load_caches(self):
        full_cache = cachetools.LRUCache(params["ALIGNMENT_CACHE_SIZE"])
        for filename in os.listdir("../cache"):
            with open("../cache/" + filename, 'rb') as f:
                partial_cache = pickle.load(f)
                for x in partial_cache:
                    full_cache[x] = partial_cache[x]
        return full_cache
