from utilities import check_python_version

check_python_version()

from wrappers.params_wrapper import set_params
from stats import get_stats
from algorithm import params
import logging
import sys


def mane():
    """ Run program """

    # Run evolution
    individuals = params['SEARCH_LOOP']()

    # Print final review
    get_stats(individuals, end=True)

if __name__ == "__main__":
    logging.basicConfig(filename='process-discovery-log.txt',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.ERROR)

    set_params(sys.argv[1:])  # exclude the ponyge.py arg itself
    mane()
