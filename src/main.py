from utilities.algorithm.general import check_python_version

check_python_version()

from algorithm.parameters import set_params
from ponyge import mane
import logging
import sys


if __name__ == "__main__":
    logging.basicConfig(filename='process-discovery-log.txt',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.ERROR)

    set_params(sys.argv[1:])  # exclude the ponyge.py arg itself
    mane()
