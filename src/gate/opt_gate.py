from itertools import permutations

from gate.gate import Gate


class OptGate(Gate):
    def __init__(self, elements=None):
        super().__init__("opt", elements)

    def get_all_n_length_routes(self, n: int) -> []:
        min_lengths = self.get_children_minimal_length()
        global_list = []

        for elem in self.elements:
            if isinstance(elem, str):
                global_list.append(elem)
            else:
                lower_limit, upper_limit = self.get_goal_length_range(n, global_list, min_lengths)
                local_list = []
                for i in range(lower_limit, upper_limit + 1):
                    local_list.append(elem.get_all_n_length_routes(i))
                global_list.append(list(permutations(local_list)))

        return global_list

    def get_goal_length_range(self, n, global_list, min_lengths):
        min_length_local = min_lengths.pop()
        min_lengths_sum = sum(min_lengths)
        return max(min_length_local, n - (min_lengths_sum + max(len(x) for x in global_list) if global_list else 0)),  \
            n - (min_lengths_sum - min(len(x) for x in global_list) if global_list else 0)

    def get_model_minimal_length(self) -> int:
        return 0
