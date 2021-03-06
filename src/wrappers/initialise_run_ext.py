from datetime import datetime
from os import getpid
from random import seed
from time import time

from algorithm.parameters import params
from utilities.stats import trackers
from utilities.stats.file_io import generate_folders_and_files


def initialise_run_params(create_files):
    """
    Initialises all lists and trackers. Generates save folders and initial
    parameter files if debugging is not active.

    :return: Nothing
    """

    start = datetime.now()
    trackers.time_list.append(time())

    # Set random seed
    if params['RANDOM_SEED'] is None:
        params['RANDOM_SEED'] = int(start.microsecond)
    seed(params['RANDOM_SEED'])

    # Generate a time stamp for use with folder and file names.
    hms = "%02d%02d%02d" % (start.hour, start.minute, start.second)
    params['TIME_STAMP'] = "_".join([str(params['DATASET']),
                                     str(start.year)[2:],
                                     str(start.month),
                                     str(start.day),
                                     hms,
                                     str(getpid()),
                                     str(params['RANDOM_SEED'])])
    if not params['SILENT']:
        print("\nStart:\t", start, "\n")

    # Generate save folders and files
    if params['DEBUG']:
        print("Seed:\t", params['RANDOM_SEED'], "\n")
    elif create_files:
        generate_folders_and_files()