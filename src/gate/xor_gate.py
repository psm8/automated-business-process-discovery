from gate.gate import Gate


class XorGate(Gate):
    def __init__(self, elements=None):
        super().__init__("xor", elements)

    def get_all_n_length_routes(self, n: int) -> []:
        if self.get_model_max_length() < n:
            return []

        min_lengths = self.get_children_min_length()
        global_list = []

        for elem in self.elements:
            if isinstance(elem, str):
                global_list.append(elem)
            else:
                lower_limit, upper_limit = self.get_goal_length_range(n, global_list, min_lengths)
                for i in range(lower_limit, upper_limit + 1):
                    child_all_n_length_routes = elem.get_all_n_length_routes(i)
                    if child_all_n_length_routes is not None:
                        global_list.append(child_all_n_length_routes)

        return global_list

    def get_model_min_length(self) -> int:
        return min(self.get_children_min_length())

    def get_model_max_length(self) -> int:
        return max(self.get_children_max_length())
