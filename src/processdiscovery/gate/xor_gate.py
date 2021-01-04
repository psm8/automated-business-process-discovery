from processdiscovery.gate.gate import Gate
from processdiscovery.event.event import Event
from processdiscovery.exception.exception_decorator import only_throws
from processdiscovery.util.util import in_by_is

from functools import cached_property


class XorGate(Gate):
    def __init__(self, parent=None, elements=None):
        super().__init__("xor", parent, elements)

    @cached_property
    def get_model_min_length(self) -> int:
        return min(self.get_children_min_length())

    @cached_property
    def get_model_max_length(self) -> int:
        return max(self.get_children_max_length())

    @cached_property
    def get_complexity(self):
        return sum([x.get_complexity if isinstance(x, Gate) else 1 for x in self.elements])

    @cached_property
    def get_complexity_for_metric(self):
        return sum([x.get_complexity_for_metric if isinstance(x, Gate) else 1 for x in self.elements])

    @only_throws(ValueError)
    def add_element(self, element):
        self.check_valid_before_appending(element)
        self.elements.append(element)

    def compare(self, other):
        if not isinstance(other, type(self)):
            return False
        if len(self) != len(other):
            return False
        for x in self.elements:
            if not any([x.compare(y) for y in other.elements]):
                return False
        return True

    def set_children_boundaries(self):
        for i in range(len(self.elements)):
            self.elements[i].min_start = self.min_start
            self.elements[i].max_start = self.max_start
            self.elements[i].min_end = self.elements[i].min_start + self.elements[i].get_model_min_length
            self.elements[i].max_end = self.elements[i].max_start + self.elements[i].get_model_max_length
            if isinstance(self.elements[i], Gate):
                self.elements[i].set_children_boundaries()

    def get_all_n_length_routes(self, n: int, process) -> []:
        if n == 0:
            return []
        if self.get_model_max_length < n or n < self.get_model_min_length:
            return None

        local_list = []

        for elem in self.elements:
            if isinstance(elem, Event):
                if n == 1:
                    local_list.append([elem])
            else:
                # possibly should add lower limit
                try:
                    child_all_n_length_routes = elem.get_all_n_length_routes(n, process)
                except ValueError:
                    return None
                if child_all_n_length_routes is not None:
                    local_list.append(child_all_n_length_routes)

        result = []
        if local_list:
            for elem in local_list:
                if isinstance(elem, list):
                    [result.append(x) for x in elem if len(x) == n]
                else:
                    if len(elem) == n:
                        result.append(elem)

        if result:
            return result
        else:
            return None

    def get_next_possible_states(self, previous_events, caller_child, next_event, blocked_calls_to=[]):
        if in_by_is(caller_child, self.elements):
            if self.parent not in blocked_calls_to:
                yield from self.parent.get_next_possible_states(previous_events, self, None, blocked_calls_to)
        else:
            for x in self.elements:
                if isinstance(x, Gate):
                    yield from x.get_next_possible_states(tuple(), None, None, blocked_calls_to)
                else:
                    yield x
