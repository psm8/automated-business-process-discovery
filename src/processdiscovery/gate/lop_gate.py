from processdiscovery.gate.gate import Gate
from processdiscovery.util.util import to_n_length
from processdiscovery.util.util import flatten_values
from processdiscovery.event.event import Event


class LopGate(Gate):
    LOP_GATE_MAX_NUMBER_OF_CHILDREN_COMBINATIONS = 32
    LOP_GATE_MAX_DEPTH = 3

    def __init__(self, elements=None):
        super().__init__("lop", elements)

    def add_element(self, element):
        self.elements.append(element)

    def get_all_n_length_routes(self, n: int) -> []:
        if n == 0:
            return []
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
            flattened_list = flatten_values(global_list)
            if len(flattened_list) < self.LOP_GATE_MAX_NUMBER_OF_CHILDREN_COMBINATIONS:
                results = [x for x in to_n_length(n, flattened_list, self.LOP_GATE_MAX_DEPTH)]
                return results
            else:
                return []
        else:
            return []

    def get_model_min_length(self) -> int:
        return 0

    def get_model_max_length(self) -> int:
        return self.LOP_GATE_MAX_DEPTH * sum(self.get_children_max_length())
