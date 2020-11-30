import copy

from itertools import chain, combinations


def string_to_dictionary(string: str):
    dictionary = dict()
    i = 0
    for x in string:
        dictionary[i] = (x, -1)
        i += 1
    return dictionary


def is_struct_empty(in_list) -> bool:
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
    for child in child_list:
        len_child = len(child)
        if len_child <= max_length:
            # tuple()
            [global_result.append((x,)) for x in to_n_length_inner(n-len_child, max_length-len_child, child, child_list)]
        elif len_child == n:
            # tuple()
            global_result.append((child,))

    return global_result


def to_n_length_inner(n, max_length, result, child_list):
    global_result = []
    for child in child_list:
        len_child = len(child)
        if len_child <= max_length:
            [global_result.append(copy.copy(result) + x) for x in to_n_length_inner(n-len_child, max_length-len_child, child, child_list)]
        elif len_child == n:
            global_result.append(copy.copy(result) + child)

    return global_result
