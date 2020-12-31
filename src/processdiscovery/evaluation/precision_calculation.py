def get_log_enabled(processes):
    unique_processes = dict()

    for process in processes:
        for i in range(len(process)):
            subprocess = process[:i]
            if subprocess not in unique_processes:
                unique_processes[subprocess] = set()
                unique_processes[subprocess].add(process[i])
            else:
                unique_processes[subprocess].add(process[i])

    return unique_processes


def count_model_enabled(previous_events_dict: dict, model_parents_list: dict):
    result = dict()
    for previous_events in previous_events_dict:
        if previous_events:
            event = previous_events[-1]
        else:
            event = None
        result[previous_events] = len(set(list(model_parents_list[event]
                                               .get_next_possible_states(previous_events, event,
                                                                         iter(previous_events_dict[previous_events])))))

    return result
