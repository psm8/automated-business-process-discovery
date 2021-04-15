import sys

from stats_parser import multi_save_average_plot_across_runs

if __name__ == "__main__":

    multi_save_average_plot_across_runs(sys.argv[1], sys.argv[2])