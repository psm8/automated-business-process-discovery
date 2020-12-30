from processdiscovery.gate.gate import Gate
from processdiscovery.util.util import to_n_length
from processdiscovery.util.util import flatten_values
from processdiscovery.event.event import Event


class LopGate(Gate):
    LOP_GATE_MAX_NUMBER_OF_CHILDREN_COMBINATIONS = 32
    LOP_GATE_MAX_DEPTH = 3

    def __init__(self, parent=None, elements=None):
        super().__init__("lop", parent, elements)

    def add_element(self, element):
        self.elements.append(element)

    def get_all_n_length_routes(self, n: int, process) -> []:
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
                        child_all_n_length_routes = elem.get_all_n_length_routes(i, process)
                    except ValueError:
                        return []
                    if child_all_n_length_routes is not None:
                        local_list.append(child_all_n_length_routes)

            if local_list:
                global_list.append(local_list)

        if global_list:
            # fix flatten values and to_n_length
            flattened_list = flatten_values(global_list)
            if len(flattened_list) < self.LOP_GATE_MAX_NUMBER_OF_CHILDREN_COMBINATIONS:
                results = [x for x in to_n_length(n, flattened_list, process, self.LOP_GATE_MAX_DEPTH)]
                return results
            else:
                return []
        else:
            return []

    def get_model_min_length(self) -> int:
        return 0

    def get_model_max_length(self) -> int:
        return self.LOP_GATE_MAX_DEPTH * sum(self.get_children_max_length())

    def get_next_possible_states(self, previous_events, child_caller, next_event) -> set:
        if child_caller is None:
            x = self.elements[0]
            if isinstance(x, Gate):
                yield from x.get_next_possible_states(set(), None, None)
            else:
                yield x
            yield from self.parent.get_next_possible_states(previous_events, self, None)
        else:
            if child_caller == self.elements[-1]:
                yield from self.parent.get_next_possible_states(previous_events, self, None)
            else:
                i = self.elements.index(child_caller)
                x = self.elements[i + 1]
                if isinstance(x, Gate):
                    yield from x.get_next_possible_states(set(), None, None)
                else:
                    yield x
