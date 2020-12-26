import copy

from itertools import chain, combinations
from processdiscovery.event.event import Event
from processdiscovery.event.event_group import EventGroup
from processdiscovery.event.event_group_parallel import EventGroupParallel
from processdiscovery.event.base_group import BaseGroup


def string_to_dictionary(string: str):
    dictionary = dict()
    i = 0
    for x in string:
        dictionary[i] = (x, -1)
        i += 1
    return dictionary


def is_struct_empty(in_list) -> bool:
    if in_list is None:
        return True
    if isinstance(in_list, set):
        return all(map(is_struct_empty, in_list))
    return False


def get_event_names(event_group: BaseGroup):
    for x in event_group.events:
        if isinstance(x, Event):
            yield x.name
        else:
            yield from get_event_names(x)


def to_n_length(n, child_list, process, max_depth):
    child_list = [x[0] if isinstance(x, list) and x else x for x in child_list]
    # child_list = filter_children_list([], child_list, process)
    min_length = min([len(x) for x in child_list])
    max_length = n - min_length
    child_list_copy = copy.copy(child_list)
    while child_list:
        child = child_list[0]
        len_child = len(child)
        if len_child <= max_length:
            yield from [(EventGroup(x)) for x in to_n_length_inner(n-len_child, max_length-len_child, [child],
                                                                   copy.copy(child_list_copy), process, 1, max_depth)]
        elif len_child == n:
            yield child
        child_list.remove(child_list[0])


def to_n_length_inner(n, max_length, result, child_list, process, current_depth, max_depth):
    # child_list = filter_children_list(result, child_list, process)
    child_list_copy = copy.copy(child_list)
    while child_list and current_depth < max_depth:
        child = child_list[0]
        len_child = len(child)
        if len_child <= max_length:
            yield from to_n_length_inner(n-len_child, max_length-len_child, result + [child],
                                         copy.copy(child_list_copy),  process, current_depth + 1, max_depth)
        elif len_child == n:
            yield result + [child]
        child_list.remove(child_list[0])


def filter_children_list(result, all_children, log_events):
    filtered = []
    result_dict = events_count(get_event_names(result))
    log_events_dict = events_count(log_events)
    penalty = 0
    for key in result_dict:
        if key in result_dict:
            result_dict
    log_events_dict = log_events_dict
    for child in all_children:
        child_dict = events_count(get_event_names(child))
        if check_route_with_log_process(child, [log_events.remove(x.name) for x in result]) > 0.7:
            filtered.append(child)

    return filtered


def check_route_with_log_process(route, log_process):
    route_event_names = list(get_event_names(route))

    hits_sum = 0
    for x in log_process:
        if x in route_event_names:
            hits_sum += 1
            route_event_names.remove(x)

    return hits_sum/len(log_process)


def events_count(events):
    result = dict()
    for event in events:
        if event in result:
            result[event] += 1
        else:
            result[event] = 1

    return result


def possible_positions():
    return 0


def to_n_length_opt(n, child_list):
    min_length = min([len(x) for x in child_list])
    max_length = n - min_length
    global_result = []
    while child_list:
        child = child_list[0]
        len_child = len(child)
        child_list.remove(child)
        if len_child <= max_length:
            [global_result.append(EventGroupParallel(x)) for x in to_n_length_inner_opt(n-len_child,
                                                                                        max_length-len_child, child,
                                                                                        copy.copy(child_list))]
        elif len_child == n:
            if isinstance(child, list):
                global_result.append(child[0])
            # possibly should be always list
            else:
                global_result.append(child)

    return global_result


def to_n_length_inner_opt(n, max_length, result, child_list):
    global_result = []
    while child_list:
        child = child_list[0]
        len_child = len(child)
        child_list.remove(child)
        if len_child <= max_length:
            if not isinstance(result, list):
                result = [result]
            xs = [x for x in to_n_length_inner_opt(n-len_child, max_length-len_child, child, copy.copy(child_list))]
            local_results = [copy.copy(result) for _ in xs]
            [local_results[i].append(x) for i in range(len(xs)) for x in xs[i]]
            [global_result.append(local_result) for local_result in local_results]
        elif len_child == n:
            if not isinstance(result, list):
                result = [result]
            local_result = copy.copy(result)
            if isinstance(child, list):
                local_result.append(child[0])

            else:
                local_result.append(child)
            global_result.append(local_result)

    return global_result


def flatten_values(values2d_list):
    results = []
    values2d = values2d_list.pop(0)
    for values in values2d:
        if isinstance(values, list):
            if any(x == [] for x in results):
                [results.append([x]) for x in values]
            else:
                if values == []:
                    results.append([])
                else:
                    [results.append([x]) if x else results.append([]) for x in values]
        else:
            results.append([values])

    for values2d in values2d_list:
        new_result = []
        for i in range(len(results)):
            empty_already_added = False
            for values in values2d:
                if isinstance(values, list):
                    if values:
                        for value in values:
                            local_result = copy.copy(results[i])
                            local_result.append(value)
                            new_result.append(local_result)
                    elif not empty_already_added:
                        local_result = copy.copy(results[i])
                        new_result.append(local_result)
                        empty_already_added = True
                else:
                    local_result = copy.copy(results[i])
                    local_result.append(values)
                    new_result.append(local_result)
        results = new_result

    return results


def event_list_length(global_list, min_or_max) -> int:
    if global_list:
        return sum(event_list_length_inner(local_list, min_or_max) for local_list in global_list)
    else:
        return 0


def event_list_length_inner(struct, min_or_max) -> int:
    results = []
    for inner_struct in struct:
        if isinstance(inner_struct, list):
            if inner_struct:
                results.append(min_or_max([len(x) for x in inner_struct]))
            else:
                results.append(0)
        else:
            results.append(len(struct))
    return min_or_max(results)


def subset_sum(numbers, target, max_len, current_len=0, partial=[], partial_sum=0):
    if current_len > max_len:
        return
    if partial_sum == target:
        yield partial
    if partial_sum >= target:
        return
    for i, n in enumerate(numbers):
        yield from subset_sum(numbers, target, max_len, current_len + 1, partial + [n], partial_sum + n)
