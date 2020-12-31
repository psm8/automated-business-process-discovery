from processdiscovery.gate.gate import Gate
from processdiscovery.event.event import Event
from processdiscovery.util.util import flatten_values
from processdiscovery.event.event_group_parallel import EventGroupParallel
from processdiscovery.exception.exception_decorator import only_throws

from functools import reduce
from math import factorial


class AndGate(Gate):
    def __init__(self, parent=None, elements=None):
        super().__init__("and", parent, elements)

    def compare(self, other):
        if not isinstance(other, type(self)):
            return False
        if len(self) != len(other):
            return False
        for x in self.elements:
            if not any([x.compare(y) for y in other.elements]):
                return False
        return True

    @only_throws(ValueError)
    def add_element(self, element):
        self.check_valid_before_appending(element)
        self.elements.append(element)

    @only_throws(ValueError)
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
                    if n == 1:
                        # because always 1 elem list
                        result.append(elem[0])
                    else:
                        self.check_valid_for_get_n_length(elem)
                        result.append(EventGroupParallel(elem))

        return result

    def get_model_min_length(self) -> int:
        return sum(self.get_children_min_length())

    def get_model_max_length(self) -> int:
        return sum(self.get_children_max_length())

    def get_next_possible_states(self, previous_events, elem, next_event):
        if next_event is not None and next_event not in self.get_events():
            yield from self.parent.get_next_possible_states(previous_events, self, None)
        else:
            result = {x.get_next_possible_states(set(), self, None) if isinstance(x, Gate) else x for x in self.elements}
            not_enabled_yet = result.difference(previous_events)
            if not_enabled_yet:
                yield from not_enabled_yet
            else:
                yield from self.parent.get_next_possible_states(previous_events, self, None)

    def get_complexity(self):
        return reduce(lambda x, y: x*y, [x.get_complexity() if isinstance(x, Gate) else 1 for x in self.elements]) \
               * factorial(len(self.elements))

    def get_complexity_for_metric(self):
        return reduce(lambda x, y: x*y, [x.get_complexity_for_metric() if isinstance(x, Gate) else 1 for x in self.elements]) \
               * factorial(len(self.elements))
