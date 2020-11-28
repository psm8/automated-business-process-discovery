import numpy as np
import math


def calculate_alignment(shorter: str, longer: str, max: int):
    size_x = len(shorter) + 1
    size_y = len(longer) + 1
    matrix = np.zeros((size_x, size_y))
    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if shorter[x - 1] == longer[y - 1]:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1],
                    matrix[x, y - 1] + 1
                )
            else:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1] + 1,
                    matrix[x, y - 1] + 1
                )
    return 2 * matrix[size_x - 1, size_y - 1] - abs(size_y - size_x)


def routes_to_strings(struct):
    if struct:
        # # check if set
        # if isinstance(struct, set) or isinstance(struct, frozenset):
        #     values = []
        #     for elem in struct:
        #         routes = routes_to_strings(elem)
        #         for route in routes:
        #             values.append(route)
        #     results = values
        # check if list of tuple
        if isinstance(struct[0], tuple):
            values = []
            for elem in struct:
                routes = routes_to_strings(elem)
                for route in routes:
                    values.append(route)
            results = values
        # else list of lists and events
        else:
            values = []
            for elem in struct:
                if isinstance(elem, list):
                    values.append(routes_to_strings(elem))
                else:
                    values.append(elem)
            results = flatten_values(values)

        return results
    else:
        return []


def flatten_values(values2d_list):
    results = []
    values2d = values2d_list.pop(0)
    if isinstance(values2d, list):
        for values in values2d:
            results.append(values)
    else:
        results.append(values2d)

    for values2d in values2d_list:
        new_result = []
        if isinstance(values2d, list):
            for values in values2d:
                for i in range(len(results)):
                    new_result.append(results[i] + values)
        else:
            for i in range(len(results)):
                new_result.append(results[i] + values2d)
        results = new_result

    return results


def get_best_case() -> int:
    return 0


def get_worst_allowed_alignment(expression) -> int:
    return math.ceil(len(expression) / 2)

# result = routes_to_strings_inner([[('a', 'b'), ('b', 'a')], [('b', 'c'), ('c', 'b')]])
