def count_log_enabled_old(processes):
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


def count_log_enabled(processes):
    unique_processes = dict()

    for process in processes:
        for i in range(len(process)):
            if not process[:i] in unique_processes:
                unique_processes[process[:i]] = set(process[i])
            else:
                unique_processes[process[:i]].add(process[i])

    result = dict()
    for key in unique_processes.keys():
        result[key] = len(unique_processes[key])

    return result


def count_model_enabled():
    return 0