import copy

from itertools import chain, combinations
from event.event_group import EventGroup
from event.event_group_parallel import EventGroupParallel


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
    if isinstance(in_list, list) or isinstance(in_list, tuple):
        return all(map(is_struct_empty, in_list))
    return False


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def to_n_length(n, child_list):
    min_length = min([len(x) for x in child_list])
    max_length = n - min_length
    global_result = []
    while child_list:
        len_child = len(child_list[0])
        if len_child <= max_length:
            [global_result.append(EventGroup(x)) for x in to_n_length_inner(n-len_child, max_length-len_child,
                                                                            child_list[0], copy.copy(child_list))]
        elif len_child == n:
            if isinstance(child_list[0], list):
                global_result.append(child_list[0][0])
                # possibly should be always list
            else:
                global_result.append(child_list[0])
        child_list.remove(child_list[0])

    return global_result


def to_n_length_inner(n, max_length, result, child_list):
    global_result = []
    while child_list:
        len_child = len(child_list[0])
        if len_child <= max_length:
            if not isinstance(result, list):
                result = [result]
            xs = [x for x in to_n_length_inner(n-len_child, max_length-len_child, child_list[0], copy.copy(child_list))]
            local_results = [copy.copy(result) for _ in xs]
            [local_results[i].append(x) for i in range(len(xs)) for x in xs[i]]
            [global_result.append(local_result) for local_result in local_results]
        elif len_child == n:
            if not isinstance(result, list):
                result = [result]
            local_result = copy.copy(result)
            if isinstance(child_list[0], list):
                local_result.append(child_list[0][0])
                # possibly should be always list
            else:
                local_result.append(child_list[0])
            global_result.append(local_result)
        child_list.remove(child_list[0])

    return global_result


def to_n_length_opt(n, child_list):
    min_length = min([len(x) for x in child_list])
    max_length = n - min_length
    global_result = []
    while child_list:
        child = child_list[0]
        len_child = len(child)
        child_list.remove(child)
        if len_child <= max_length:
            [global_result.append(EventGroupParallel(x)) for x in to_n_length_inner_opt(n-len_child, max_length-len_child, child, copy.copy(child_list))]
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
            [results.append([x]) for x in values]
        else:
            results.append([values])

    for values2d in values2d_list:
        new_result = []
        for i in range(len(results)):
            for values in values2d:
                if isinstance(values, list):
                    for value in values:
                        local_result = copy.copy(results[i])
                        local_result.append(value)
                        new_result.append(local_result)
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
    for inner_struct in struct:
        if isinstance(inner_struct, list):
            return min_or_max([len(x) for x in inner_struct])
        else:
            return len(struct)
