from processdiscovery.gate.gate import Gate


def count_log_enabled(processes):
    unique_processes = dict()

    for process in processes:
        for i in range(len(process)):
            if not process[:i] in unique_processes:
                unique_processes[process[:i]] = set()
                unique_processes[process[:i]].add(process[i])
            else:
                unique_processes[process[:i]].add(process[i])

    result = dict()
    for key in unique_processes.keys():
        result[key] = len(unique_processes[key])

    return result


def count_model_enabled(previous_events_list: set, model_parents_list: dict):
    result = dict()
    for previous_events in previous_events_list:
        event = previous_events
        result[previous_events] = model_parents_list[event].get_next_possible_states(previous_events, event)

    return result
