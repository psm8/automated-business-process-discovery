from gate.gate import Gate
from util.util import is_struct_empty, to_n_length
from fitness.alignment_calculation import routes_to_strings, flatten_values
from event.event import Event


class OptGate(Gate):
    def __init__(self, elements=None):
        super().__init__("opt", elements)

    def get_all_n_length_routes(self, n: int) -> []:
        if self.get_model_max_length() < n:
            return None

        min_lengths = self.get_children_min_length()
        max_lengths = self.get_children_max_length()
        global_list = []

        for elem in self.elements:
            if isinstance(elem, Event):
                global_list.append(elem)
                min_lengths.pop(0)
                max_lengths.pop(0)
            else:
                lower_limit = self.get_goal_length_lower_range(n, global_list, min_lengths, max_lengths)
                local_list = []
                for i in range(lower_limit, n + 1):
                    child_all_n_length_routes = elem.get_all_n_length_routes(i)
                    # indicated something wrong
                    if is_struct_empty(child_all_n_length_routes):
                        return []
                    if child_all_n_length_routes is not None:
                        [local_list.append(x) for x in routes_to_strings(child_all_n_length_routes)]
                if local_list:
                    global_list.append(local_list)
                if global_list:
                    return to_n_length(n, flatten_values(global_list))
                else:
                    return []

    def get_model_min_length(self) -> int:
        return 0

    def get_model_max_length(self) -> int:
        return sum(self.get_children_max_length())

