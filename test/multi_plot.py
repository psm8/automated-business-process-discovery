import os
import sys

from stats_parser import multi_save_average_plot_across_runs

if __name__ == "__main__":

    directory = os.path.join(os.getcwd(), "..", "results", sys.argv[1])
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                if not file.endswith("full_stats.csv"):
                    print(file)
                    multi_save_average_plot_across_runs(os.path.join(os.getcwd(), "..", "results", sys.argv[1], file),
                                                        os.path.join(os.getcwd(), "..", "results", sys.argv[2], file))