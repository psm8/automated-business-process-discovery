""" This program cues up and executes multiple runs of PYGE. Results of runs
    are parsed and placed in a spreadsheet for easy visual analysis.

    Copyright (c) 2014 Michael Fenton
    Hereby licensed under the GNU GPL v3."""
from multiprocessing import Pool
from sys import path

from algorithm.parameters import params
from scripts.experiment_manager import check_params
from wrappers.params_wrapper import set_params

path.append("../src")

from utilities.algorithm.general import check_python_version

check_python_version()

from subprocess import call
import sys


from scripts.stats_parser import parse_stats_from_runs


def execute_run(seed):
    """
    Initialise all aspects of a run.

    :return: Nothing.
    """

    exec_str = "python main.py " \
               "--random_seed " + str(seed) + " " + " ".join(sys.argv[1:])

    call(exec_str, shell=True)

def execute_runs():
    """
    Execute multiple runs in series using multiple cores.

    :return: Nothing.
    """

    # Initialise empty list of results.
    results = []

    # Initialise pool of workers.
    pool = Pool(processes=params['CORES'])

    for run in range(params['RUNS']):
        # Execute a single evolutionary run.
        results.append(pool.apply_async(execute_run, (run,)))

    for result in results:
        result.get()

    # Close pool once runs are finished.
    pool.close()


def main():
    """
    The main function for running the experiment manager. Calls all functions.

    :return: Nothing.
    """

    # Setup run parameters.
    set_params(sys.argv[1:], create_files=False)

    # Check the correct parameters are set for this set of runs.
    check_params()

    # Execute multiple runs.
    execute_runs()

    # # Save spreadsheets and all plots for all runs in the 'EXPERIMENT_NAME'
    # # folder.
    # parse_stats_from_runs(params['EXPERIMENT_NAME'])


if __name__ == "__main__":
    main()
