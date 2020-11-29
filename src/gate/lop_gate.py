from gate.gate import Gate
from util.util import is_struct_empty

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
                lower_limit, upper_limit = self.get_goal_length_range(n, global_list, min_lengths)
                for i in range(lower_limit, upper_limit + 1):
                    child_all_n_length_routes = elem.get_all_n_length_routes(i)
                    #indicated something wrong
                    if is_struct_empty(child_all_n_length_routes):
                        return []
                    if self.get_factor_of_n(n, child_all_n_length_routes):
                        local_list = []
                        global_list.append(child_all_n_length_routes)

        if self.is_in_range(n, global_list):
            return global_list
        else:
            return []

    def get_factor_of_n(self, n, child_list):
        list_min_length = self.list_length_new(self, child_list, min)
        if n%list_min_length == 0:
            return n/list_min_length
        else:
            return 0

    def get_model_min_length(self) -> int:
        return 0

    def get_model_max_length(self) -> int:
        return 127