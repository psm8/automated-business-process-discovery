def count_log_enabled(processes):
    max_length = max([len(x) for x in processes])
    unique_processes = dict()

    for i in range(max_length):
        unique_processes[i] = set()

    for process in processes:
        for i in range(len(process)):
            unique_processes[i].add(process[i])

    result = dict()
    for i in unique_processes.keys():
        result[i] = len(unique_processes[i])

    return result

def count_model_enabled():
    return 0