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


def calculate_alignment_parallel(shorter: str, longer: str):
    penalty = 0
    for x in shorter:
        test = longer.find(x)
        if test == -1:
            penalty += 1
        else:
            # to check duplicates in future iterations
            longer = longer[:test] + longer[(test+1):]
    return penalty + len(longer)



#-------------------------------------------------------
#This function returns to values for cae of match or mismatch
def diagonal(n1,n2,pt):
    if n1 in n2:
        return pt['MATCH']
    else:
        return pt['MISMATCH']


#--------------------------------------------------------
#This function creates the aligment and pointers matrices
def nv(log, model, match=0, mismatch=-2, gap=-1):
    penalty = {'MATCH': match, 'MISMATCH': mismatch, 'GAP': gap} #A dictionary for all the penalty valuse.
    n = len(log) + 1 #The dimension of the matrix columns.
    m = len(model) + 1 #The dimension of the matrix rows.
    al_mat = np.zeros((m,n),dtype = int) #Initializes the alighment matrix with zeros.
    #Scans all the first rows element in the matrix and fill it with "gap penalty"
    for i in range(m):
        al_mat[i][0] = penalty['GAP'] * i
    #Scans all the first columns element in the matrix and fill it with "gap penalty"
    for j in range(n):
        al_mat[0][j] = penalty['GAP'] * j
    #Fill the matrix with the correct values.

    for i in range(1, m):
        for j in range(1, n):
            di = al_mat[i-1][j-1] + diagonal(log[j-1], model[i-1], penalty) #The value for match/mismatch -  diagonal.
            ho = al_mat[i][j-1] + penalty['GAP'] #The value for gap - horizontal.(from the left cell)
            ve = al_mat[i-1][j] + penalty['GAP'] #The value for gap - vertical.(from the upper cell)
            al_mat[i][j] = max(di, ho, ve) #Fill the matrix with the maximal value.(based on the python default maximum)
    print(np.matrix(al_mat))

# def event_group_to_strings(struct):
#     if struct:
#         # check if list of tuples
#         if isinstance(struct, BaseGroup):
#             values = []
#             for elem in struct:
#                 routes = event_group_to_strings(elem)
#                 for route in routes:
#                     values.append(route)
#             results = values
#         # else list of lists and events
#         else:
#             values = []
#             for elem in struct:
#                 # if isinstance(elem, list):
#                 #     values.append(routes_to_strings(elem))
#                 # else:
#                 values.append(elem)
#             results = flatten_values(values)
#
#         return results
#     else:
#         return []

# def touples_to_strings(struct):
#     if struct:
#         values = []
#         for elem in struct:
#             routes = routes_to_strings(elem)
#             for route in routes:
#                 values.append(route)
#         results = values
#         # else list of lists and events
#         return results
#     else:
#         return []
#
# def listss_to_strings(struct):
#     if struct:
#         values = []
#         for elem in struct:
#             if isinstance(elem, list):
#                 values.append(routes_to_strings(elem))
#             else:
#                 values.append(elem)
#         results = flatten_values(values)
#
#         return results
#     else:
#         return []


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
                new_result.append(results[i].add_event(values2d))
        results = new_result

    return results


def get_best_case() -> int:
    return 0


def get_worst_allowed_alignment(expression) -> int:
    return math.ceil(len(expression) / 2)

nv('abcd', 'abcthy')