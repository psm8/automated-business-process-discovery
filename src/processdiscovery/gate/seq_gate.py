from processdiscovery.gate.gate import Gate
from processdiscovery.event.event import Event
from processdiscovery.util.util import flatten_values
from processdiscovery.event.event_group import EventGroup


class SeqGate(Gate):
    def __init__(self, parent=None, elements=None):
        super().__init__("seq", parent, elements)

    def add_element(self, element):
        self.elements.append(element)

    def get_all_n_length_routes(self, n: int, process) -> []:
        if n == 0:
            return []
        if self.get_model_max_length() < n:
            return None

        min_lengths = self.get_children_min_length()
        max_lengths = self.get_children_max_length()
        global_list = []

        for elem in self.elements:
            local_list = []
            if isinstance(elem, Event):
                local_list.append(elem)
                min_lengths.pop(0)
                max_lengths.pop(0)
            else:
                lower_limit, upper_limit = self.get_goal_length_range(n, global_list, min_lengths, max_lengths)
                for i in range(lower_limit, upper_limit + 1):
                    try:
                        child_all_n_length_routes = elem.get_all_n_length_routes(i, process)
                    except ValueError:
                        return []
                    if child_all_n_length_routes is not None:
                        local_list.append(child_all_n_length_routes)

            if local_list:
                global_list.append(local_list)

        result = []
        if global_list:
            for elem in flatten_values(global_list):
                if self.check_length(n, elem):
                    result.append(EventGroup(elem))

        return result

    def get_model_min_length(self) -> int:
        return sum(self.get_children_min_length())

    def get_model_max_length(self) -> int:
        return sum(self.get_children_max_length())

    def get_next_possible_states(self, previous_events, child_caller, next_event):
        if child_caller is None:
            x = self.elements[0]
            if isinstance(x, Gate):
                yield from x.get_next_possible_states(set(), None, None)
            else:
                yield x
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
