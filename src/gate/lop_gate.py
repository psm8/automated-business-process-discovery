import copy

from gate.gate import Gate
from util.util import is_struct_empty
from fitness.alignment_calculation import routes_to_strings, flatten_values


class LopGate(Gate):
    def __init__(self, elements=None):
        super().__init__("lop", elements)

    def get_all_n_length_routes(self, n: int) -> []:
        min_lengths = self.get_children_min_length()
        global_list = []

        for elem in self.elements:
            if isinstance(elem, str):
                global_list.append(elem)
                min_lengths.pop(0)
            else:
                upper_limit = self.get_goal_length_upper_range(n, global_list, min_lengths)
                # TODO: consider adding in more places local list
                local_list = []
                for i in range(1, upper_limit + 1):
                    child_all_n_length_routes = elem.get_all_n_length_routes(i)
                    #indicated something wrong
                    if is_struct_empty(child_all_n_length_routes):
                        return []
                    if child_all_n_length_routes is not None:
                        [local_list.append(x) for x in routes_to_strings(child_all_n_length_routes)]
                if local_list:
                    global_list.append(local_list)
        if global_list:
            return self.to_n_length(n, flatten_values(global_list))
        else:
            return []


    def to_n_length(self, n, child_list):
        min_length = min([len(x) for x in child_list])
        max_length = n - min_length
        global_result = []
        for child in child_list:
            len_child = len(child)
            if len_child <= max_length:
                [global_result.append(x) for x in self.to_n_length_inner(n-len_child, max_length-len_child, child, child_list)]
            elif len_child == n:
                global_result.append(child)

        return global_result


    def to_n_length_inner(self, n, max_length, result, child_list):
        global_result = []
        for child in child_list:
            len_child = len(child)
            if len_child <= max_length:
                [global_result.append(copy.copy(result) + x) for x in self.to_n_length_inner(n-len_child, max_length-len_child, child, child_list)]
            elif len_child == n:
                global_result.append(copy.copy(result) + child)

        return global_result


    def get_model_min_length(self) -> int:
        return 0

    def get_model_max_length(self) -> int:
        return 127