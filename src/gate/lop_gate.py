from gate.gate import Gate


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
                local_list = []
                for i in range(lower_limit, upper_limit + 1):
                    child_all_n_length_routes = elem.get_all_n_length_routes(i)
                    if child_all_n_length_routes is not None:
                        local_list.append(child_all_n_length_routes)
                global_list.append(local_list)

        return global_list

    def get_model_min_length(self) -> int:
        return 0

    def get_model_max_length(self) -> int:
        return 127