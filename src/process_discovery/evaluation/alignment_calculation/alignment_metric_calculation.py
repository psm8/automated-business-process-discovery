def calculate_alignment_metric(best_local_error, len_elem, n):
    return best_local_error / (len_elem + n)
