from gate.gate import Gate
from util.util import is_struct_empty, to_n_length
from util.util import flatten_values
from event.event import Event


class LopGate(Gate):
    def __init__(self, elements=None):
        super().__init__("lop", elements)

    def add_element(self, element):
        self.elements.append(element)

    def get_all_n_length_routes(self, n: int) -> []:
        min_lengths = self.get_children_min_length()
        global_list = []

        for elem in self.elements:
            local_list = []
            if isinstance(elem, Event):
                local_list.append(elem)
                min_lengths.pop(0)
            else:
                upper_limit = self.get_goal_length_upper_range(n, global_list, min_lengths)
                for i in range(1, upper_limit + 1):
                    try:
                        child_all_n_length_routes = elem.get_all_n_length_routes(i)
                    except ValueError:
                        return []
                    if child_all_n_length_routes is not None:
                        local_list.append(child_all_n_length_routes)

            if local_list:
                global_list.append(local_list)

        if global_list:
            return to_n_length(n, flatten_values(global_list))
        else:
            return []

    def get_model_min_length(self) -> int:
        return 0

    def get_model_max_length(self) -> int:
        return 127