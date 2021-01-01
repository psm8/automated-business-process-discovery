from utilities.algorithm.general import check_python_version

check_python_version()

from algorithm.parameters import set_params
from ponyge import mane

import sys


if __name__ == "__main__":
    set_params(sys.argv[1:])  # exclude the ponyge.py arg itself
    mane()
