import matplotlib
from os import path

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rc('font', family='Times New Roman')


def save_plots_from_data(fitness, alignment, complexity, generalization, precision, simplicity, name):
    """
    Saves a plot of a given set of data.

    :param data: the data to be plotted
    :param name: the name of the data to be plotted.
    :return: Nothing.
    """

    from algorithm.parameters import params

    # Initialise up figure instance.
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)

    # Plot data.
    ax1.plot(fitness, label='fitness')
    ax1.plot(alignment, label='alignment')
    ax1.plot(complexity, label='complexity')
    ax1.plot(generalization, label='generalization')
    ax1.plot(precision, label='precision')
    ax1.plot(simplicity, label='simplicity')

    # Set labels.
    ax1.set_ylabel(name, fontsize=14)
    ax1.set_xlabel('Generation', fontsize=14)

    # Plot title.
    plt.title(name)

    # Save plot and close.
    plt.savefig(path.join(params['FILE_PATH'], (name + '.pdf')))
    plt.close()
