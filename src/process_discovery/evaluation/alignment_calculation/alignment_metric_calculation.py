from math import pow


def calculate_alignment_metric(best_local_error: dict, log_info, n):

    average_alignment_error = sum(best_local_error[process] / (len(process) + n) *
                                  log_info.log[process] for process in best_local_error) / \
                              log_info.sum_of_processes_length

    return average_alignment_error, pow(1 + average_alignment_error, 4)
