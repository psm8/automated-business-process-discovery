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
    print(matrix)
    return 2 * matrix[size_x - 1, size_y - 1] + size_y - size_x


def get_best_case():
    return 0


def get_worst_allowed_alignment(self, expression):
    return math.ceil(len(expression) / 2)


print(calculate_alignment("aaaatxtxt", "abbbtxt", 0))

