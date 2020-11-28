from gate.gate import Gate
from util.list_util import is_struct_empty

class XorGate(Gate):
    def __init__(self, elements=None):
        super().__init__("xor", elements)

    def get_all_n_length_routes(self, n: int) -> []:
        if self.get_model_max_length() < n and n > 0:
            return None

        global_list = []

        for elem in self.elements:
            if isinstance(elem, str):
                if n == 1:
                    global_list.append(tuple(elem))
            else:
                child_all_n_length_routes = elem.get_all_n_length_routes(n)
                # indicated something wrong
                if is_struct_empty(child_all_n_length_routes):
                    return []
                if self.is_in_range(n, child_all_n_length_routes):
                    global_list.append(tuple(child_all_n_length_routes))

        return [tuple(global_list)]

    def get_model_min_length(self) -> int:
        return min(self.get_children_min_length())

    def get_model_max_length(self) -> int:
        return max(self.get_children_max_length())
