import os
import sys

import matplotlib
from os import path, getcwd, listdir, makedirs
import pandas as pd

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rc('font', family='Times New Roman')


def parse_stats_from_run(experiment_name, y1, y2, gen_no=1000):
    # Get file name
    file_name = path.join(experiment_name, "stats.tsv")

    # Load in data
    data = pd.read_csv(file_name, sep="\t")

    alignment = list(data['alignment'][:gen_no])
    complexity = list(data['complexity'][:gen_no])
    generalization = list(data['generalization'][:gen_no])
    precision = list(data['precision'][:gen_no])
    simplicity = list(data['simplicity'][:gen_no])
    fitness = list(data['best_fitness'][:gen_no])

    save_plots_from_data(fitness, alignment, complexity, generalization, precision, simplicity, experiment_name, "result_graph", y1, y2)


def save_plots_from_data(fitness, alignment, complexity, generalization, precision, simplicity, experiment_name, name, y1, y2):

    # Initialise up figure instance.
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)

    # Plot data.
    ax1.plot(fitness, label='średnia ważona')
    ax1.plot(alignment, label='odwzorowanie')
    ax1.plot(complexity, label='złożoność')
    ax1.plot(generalization, label='generalizacja')
    ax1.plot(precision, label='precyzja')
    ax1.plot(simplicity, label='prostota')

    ax1.set_ylim(None, None)

    # Set plot.
    plt.legend(loc="lower right")

    # Set labels.
    ax1.set_ylabel('Czas w sekundach', fontsize=14)
    ax1.set_xlabel('Generacja', fontsize=14)

    # Plot title.
    plt.title('Średnia wartość średniej ważonej')

    # Save plot and close.
    plt.savefig(path.join(experiment_name, (name + '9.pdf')))
    plt.close()

if __name__ == "__main__":
    parse_stats_from_run(os.path.join(os.getcwd(), "..", "results", sys.argv[1]),  sys.argv[2],  sys.argv[3], int(sys.argv[4]))
