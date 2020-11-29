from itertools import product

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
                _, upper_limit = self.get_goal_length_range(n, global_list, min_lengths)
                for i in range(1, upper_limit + 1):
                    child_all_n_length_routes = elem.get_all_n_length_routes(i)
                    #indicated something wrong
                    if is_struct_empty(child_all_n_length_routes):
                        return []
                    if child_all_n_length_routes is not None:
                        global_list.append(routes_to_strings(child_all_n_length_routes))

            return [p for p in product(flatten_values(global_list), repeat=n)]
        else:
            return []

    def get_factor_of_n(self, n, child_list):
        list_min_length = self.list_length_new(child_list, min)
        if n % list_min_length == 0:
            return n/list_min_length
        else:
            return 0

    def to_n_length(self, n, child_list):
        global_result = []
        for child in child_list:
            factor_of_n = self.get_factor_of_n(n, child)
            # factor_of_n > 0
            # need to be all compinations
            if factor_of_n:
                global_result.append([child for _ in range(int(factor_of_n))])

        return global_result


    def get_model_min_length(self) -> int:
        return 0

    def get_model_max_length(self) -> int:
        return 127