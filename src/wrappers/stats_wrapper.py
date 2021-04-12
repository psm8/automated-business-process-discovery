from copy import copy
from sys import stdout
from time import time
import numpy as np

from algorithm.parameters import params
from stats.stats import get_moo_stats
from utilities.algorithm.state import create_state
from utilities.stats import trackers
from utilities.stats.file_io import save_stats_headers, save_stats_to_file
from wrappers import trackers_ext
from wrappers.file_io_wrapper import save_best_ind_to_file
from wrappers.save_plots_ext import save_plots_from_data

"""Algorithm statistics"""
stats = {
        "gen": 0,
        "total_inds": 0,
        "regens": 0,
        "invalids": 0,
        "runtime_error": 0,
        "unique_inds": len(trackers.cache),
        "unused_search": 0,
        "ave_genome_length": 0,
        "max_genome_length": 0,
        "min_genome_length": 0,
        "ave_used_codons": 0,
        "max_used_codons": 0,
        "min_used_codons": 0,
        "ave_tree_depth": 0,
        "max_tree_depth": 0,
        "min_tree_depth": 0,
        "ave_tree_nodes": 0,
        "max_tree_nodes": 0,
        "min_tree_nodes": 0,
        "ave_fitness": 0,
        "best_phenotype": "",
        "best_fitness": 0,
        "alignment": 0,
        "complexity": 0,
        "generalization": 0,
        "precision": 0,
        "simplicity": 0,
        "time_taken": 0,
        "total_time": 0,
        "time_adjust": 0
}

def get_stats(individuals, end=False):
    """
    Generate the statistics for an evolutionary run. Save statistics to
    utilities.trackers.stats_list. Print statistics. Save fitness plot
    information.

    :param individuals: A population of individuals for which to generate
    statistics.
    :param end: Boolean flag for indicating the end of an evolutionary run.
    :return: Nothing.
    """

    if hasattr(params['FITNESS_FUNCTION'], 'multi_objective'):
        # Multiple objective optimisation is being used.

        # Remove fitness stats from the stats dictionary.
        stats.pop('best_fitness', None)
        stats.pop('ave_fitness', None)

        # Update stats.
        get_moo_stats(individuals, end)

    else:
        # Single objective optimisation is being used.
        get_soo_stats(individuals, end)

    if params['SAVE_STATE'] and not params['DEBUG'] and \
                            stats['gen'] % params['SAVE_STATE_STEP'] == 0:
        # Save the state of the current evolutionary run.
        create_state(individuals)


def get_soo_stats(individuals, end):
    """
    Generate the statistics for an evolutionary run with a single objective.
    Save statistics to utilities.trackers.stats_list. Print statistics. Save
    fitness plot information.

    :param individuals: A population of individuals for which to generate
    statistics.
    :param end: Boolean flag for indicating the end of an evolutionary run.
    :return: Nothing.
    """

    # Get best individual.
    best = max(individuals)

    if not trackers.best_ever or best > trackers.best_ever:
        # Save best individual in trackers.best_ever.
        trackers.best_ever = best

    if end or params['VERBOSE'] or not params['DEBUG']:
        # Update all stats.
        update_stats(individuals, end)

    # Save fitness plot information
    if params['SAVE_PLOTS'] and not params['DEBUG']:
        if not end:
            trackers.best_fitness_list.append(trackers.best_ever.fitness)
            trackers_ext.best_alignment_list.append(trackers.best_ever.metrics['ALIGNMENT'])
            trackers_ext.best_complexity_list.append(trackers.best_ever.metrics['COMPLEXITY'])
            trackers_ext.best_generalization_list.append(trackers.best_ever.metrics['GENERALIZATION'])
            trackers_ext.best_precision_list.append(trackers.best_ever.metrics['PRECISION'])
            trackers_ext.best_simplicity_list.append(trackers.best_ever.metrics['SIMPLICITY'])

        if params['VERBOSE'] or end:
            save_plots_from_data(trackers.best_fitness_list, trackers_ext.best_alignment_list,
                                 trackers_ext.best_complexity_list, trackers_ext.best_generalization_list,
                                 trackers_ext.best_precision_list, trackers_ext.best_simplicity_list, "best_fitness")

    # Print statistics
    if params['VERBOSE'] and not end:
        print_generation_stats()

    elif not params['SILENT']:
        # Print simple display output.
        perc = stats['gen'] / (params['GENERATIONS']+1) * 100
        stdout.write("Evolution: %d%% complete\r" % perc)
        stdout.flush()

    # Generate test fitness on regression problems
    if hasattr(params['FITNESS_FUNCTION'], "training_test") and end:

        # Save training fitness.
        trackers.best_ever.training_fitness = copy(trackers.best_ever.fitness)

        # Evaluate test fitness.
        trackers.best_ever.test_fitness = params['FITNESS_FUNCTION'](
            trackers.best_ever, dist='test')

        # Set main fitness as training fitness.
        trackers.best_ever.fitness = trackers.best_ever.training_fitness

    # Save stats to list.
    if params['VERBOSE'] or (not params['DEBUG'] and not end):
        trackers.stats_list.append(copy(stats))

    # Save stats to file.
    if not params['DEBUG']:

        if stats['gen'] == 0:
            save_stats_headers(stats)

        save_stats_to_file(stats, end)

        if params['SAVE_ALL']:
            save_best_ind_to_file(stats, trackers.best_ever, end, stats['gen'])

        elif params['VERBOSE'] or end:
            save_best_ind_to_file(stats, trackers.best_ever, end)

    if end and not params['SILENT']:
        print_final_stats()


def update_stats(individuals, end):
    """
    Update all stats in the stats dictionary.

    :param individuals: A population of individuals.
    :param end: Boolean flag for indicating the end of an evolutionary run.
    :return: Nothing.
    """

    if not end:
        # Time Stats
        trackers.time_list.append(time() - stats['time_adjust'])
        stats['time_taken'] = trackers.time_list[-1] - \
                              trackers.time_list[-2]
        stats['total_time'] = trackers.time_list[-1] - \
                              trackers.time_list[0]

    # Population Stats
    stats['total_inds'] = params['POPULATION_SIZE'] * (stats['gen'] + 1)
    stats['runtime_error'] = len(trackers.runtime_error_cache)
    if params['CACHE']:
        stats['unique_inds'] = len(trackers.cache)
        stats['unused_search'] = 100 - stats['unique_inds'] / \
                                       stats['total_inds'] * 100

    # Genome Stats
    genome_lengths = [len(i.genome) for i in individuals]
    stats['max_genome_length'] = np.nanmax(genome_lengths)
    stats['ave_genome_length'] = np.nanmean(genome_lengths)
    stats['min_genome_length'] = np.nanmin(genome_lengths)

    # Used Codon Stats
    codons = [i.used_codons for i in individuals]
    stats['max_used_codons'] = np.nanmax(codons)
    stats['ave_used_codons'] = np.nanmean(codons)
    stats['min_used_codons'] = np.nanmin(codons)

    # Tree Depth Stats
    depths = [i.depth for i in individuals]
    stats['max_tree_depth'] = np.nanmax(depths)
    stats['ave_tree_depth'] = np.nanmean(depths)
    stats['min_tree_depth'] = np.nanmin(depths)

    # Tree Node Stats
    nodes = [i.nodes for i in individuals]
    stats['max_tree_nodes'] = np.nanmax(nodes)
    stats['ave_tree_nodes'] = np.nanmean(nodes)
    stats['min_tree_nodes'] = np.nanmin(nodes)

    if not hasattr(params['FITNESS_FUNCTION'], 'multi_objective'):
        # Fitness Stats
        fitnesses = [i.fitness for i in individuals]
        stats['ave_fitness'] = np.nanmean(fitnesses, axis=0)
        stats['best_fitness'] = trackers.best_ever.fitness
        stats['best_phenotype'] = trackers.best_ever.phenotype
        stats['alignment'] = trackers.best_ever.metrics['ALIGNMENT']
        stats['complexity'] = trackers.best_ever.metrics['COMPLEXITY']
        stats['generalization'] = trackers.best_ever.metrics['GENERALIZATION']
        stats['precision'] = trackers.best_ever.metrics['PRECISION']
        stats['simplicity'] = trackers.best_ever.metrics['SIMPLICITY']


def print_generation_stats():
    """
    Print the statistics for the generation and individuals.

    :return: Nothing.
    """

    print("______\n")
    for stat in sorted(stats.keys()):
        print(" ", stat, ": \t", stats[stat])
    print("\n")


def print_final_stats():
    """
    Prints a final review of the overall evolutionary process.

    :return: Nothing.
    """

    if hasattr(params['FITNESS_FUNCTION'], "training_test"):
        print("\n\nBest:\n  Training fitness:\t",
              trackers.best_ever.training_fitness)
        print("  Test fitness:\t\t", trackers.best_ever.test_fitness)
    else:
        print("\n\nBest:\n  Fitness:\t", trackers.best_ever.fitness)
        print("\nMetrics:    Alignment:\t", trackers.best_ever.metrics['ALIGNMENT'])
        print(" Complexity:\t", trackers.best_ever.metrics['COMPLEXITY'])
        print(" Generalization:\t", trackers.best_ever.metrics['GENERALIZATION'])
        print(" Precision:\t", trackers.best_ever.metrics['PRECISION'])
        print(" Simplicity:\t", trackers.best_ever.metrics['SIMPLICITY'])

    print("  Phenotype:", trackers.best_ever.phenotype)
    print("  Genome:", trackers.best_ever.genome)
    print_generation_stats()
