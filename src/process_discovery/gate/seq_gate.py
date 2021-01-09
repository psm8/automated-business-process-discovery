from process_discovery.event.base_group import BaseGroup
from process_discovery.gate.gate import Gate
from process_discovery.event.event import Event
from process_discovery.util.util import flatten_values
from process_discovery.event.event_group import EventGroup
from process_discovery.util.util import index_by_is

from functools import reduce, cached_property


class SeqGate(Gate):
    def __init__(self, parent=None, elements=None):
        super().__init__("seq", parent, elements)

    @cached_property
    def model_min_length(self) -> int:
        return sum(self.get_children_min_length())

    @cached_property
    def model_max_length(self) -> int:
        return sum(self.get_children_max_length())

    @cached_property
    def complexity(self) -> int:
        return reduce(lambda x, y: x*y, [x.complexity if isinstance(x, Gate) else 1 for x in self.elements])

    @cached_property
    def complexity_for_metric(self) -> int:
        return reduce(lambda x, y: x*y, [x.complexity_for_metric if isinstance(x, Gate) else 1 for x in self.elements])

    def compare(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        if len(self) != len(other):
            return False
        for i in range(len(self.elements)):
            if not self.elements[i].compare(other.elements[i]):
                return False
        return True

    def add_element(self, element) -> None:
        self.elements.append(element)

    def set_children_boundaries(self) -> None:
        min_lengths = self.get_children_min_length()
        max_lengths = self.get_children_max_length()

        self.elements[0].min_start = self.min_start
        self.elements[0].max_start = self.max_start
        self.elements[0].min_end = max(self.elements[0].min_start + self.elements[0].model_min_length,
                                       self.min_end - sum(max_lengths[1:]))
        self.elements[0].max_end = min(self.elements[0].max_start + self.elements[0].model_max_length,
                                       self.max_end - sum(min_lengths[1:]))
        if isinstance(self.elements[0], Gate):
            self.elements[0].set_children_boundaries()

        for i in range(1, len(self.elements)):
            self.elements[i].min_start = self.elements[i-1].min_end
            self.elements[i].max_start = self.elements[i-1].max_end
            self.elements[i].min_end = max(self.elements[i].min_start + self.elements[i].model_min_length,
                                           self.min_end - sum(max_lengths[i+1:]))
            self.elements[i].max_end = min(self.elements[i].max_start + self.elements[i].model_max_length,
                                           self.max_end - sum(min_lengths[i+1:]))
            if isinstance(self.elements[i], Gate):
                self.elements[i].set_children_boundaries()

    def get_all_n_length_routes(self, n: int, process) -> [BaseGroup]:
        if n == 0:
            return []
        if self.model_max_length < n or n < self.model_min_length:
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
                        return None
                    if child_all_n_length_routes is not None:
                        local_list.append(child_all_n_length_routes)

            if local_list:
                global_list.append(local_list)

        result = []
        if global_list:
            for elem in flatten_values(global_list):
                if self.check_length(n, elem):
                    result.append(EventGroup(elem))

        if result:
            return result
        else:
            return None

    def get_next_possible_states(self, previous_events, child_caller, next_event, blocked_calls_to=[]):
        if child_caller is None:
            x = self.elements[0]
            if isinstance(x, Gate):
                yield from x.get_next_possible_states(tuple(), None, None, blocked_calls_to)
            else:
                yield x
        else:
            if child_caller is self.elements[-1]:
                if self.parent is not None and self.parent not in blocked_calls_to:
                    yield from self.parent.get_next_possible_states(previous_events, self, None, blocked_calls_to)
                else:
                    return
            else:
                i = index_by_is(child_caller, self.elements)
                x = self.elements[i + 1]
                if isinstance(x, Gate):
                    yield from x.get_next_possible_states(tuple(), None, None, blocked_calls_to)
                else:
                    yield x
