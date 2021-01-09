from process_discovery.gate.gate import Gate
from process_discovery.gate.opt_gate import OptGate
from process_discovery.gate.lop_gate import LopGate
from process_discovery.event.event import Event
from process_discovery.util.util import flatten_values, in_by_is, is_any_parent_optional
from process_discovery.event.event_group_parallel import EventGroupParallel
from process_discovery.exception.exception_decorator import only_throws

from functools import reduce, cached_property
from math import factorial


class AndGate(Gate):
    def __init__(self, parent=None, elements=None):
        super().__init__("and", parent, elements)

    @cached_property
    def model_min_length(self) -> int:
        return sum(self.get_children_min_length())

    @cached_property
    def model_max_length(self) -> int:
        return sum(self.get_children_max_length())

    @cached_property
    def complexity(self) -> int:
        return reduce(lambda x, y: x*y, [x.complexity if isinstance(x, Gate) else 1 for x in self.elements]) \
               * factorial(len(self.elements))

    @cached_property
    def complexity_for_metric(self) -> int:
        return reduce(lambda x, y: x*y, [x.complexity_for_metric if isinstance(x, Gate) else 1 for x in self.elements]) \
               * factorial(len(self.elements))

    def compare(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        if len(self) != len(other):
            return False
        for x in self.elements:
            if not any([x.compare(y) for y in other.elements]):
                return False
        return True

    @only_throws(ValueError)
    def add_element(self, element) -> None:
        self.check_valid_before_appending(element)
        self.elements.append(element)

    def set_children_boundaries(self) -> None:
        max_lengths = self.get_children_max_length()

        for i in range(len(self.elements)):
            self.elements[i].min_start = self.min_start
            self.elements[i].max_start = min(self.max_start + (sum(max_lengths) - self.elements[i].model_max_length),
                                             self.max_end - self.elements[i].model_min_length)
            self.elements[i].min_end = max(self.min_start + self.elements[i].model_min_length,
                                           self.min_end - (sum(max_lengths) - self.elements[i].model_max_length))
            self.elements[i].max_end = self.max_end
            if isinstance(self.elements[i], Gate):
                self.elements[i].set_children_boundaries()

    @only_throws(ValueError)
    def get_all_n_length_routes(self, n: int, process) -> []:
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
                    if n == 1:
                        # because always 1 elem list
                        result.append(elem[0])
                    else:
                        self.check_valid_for_get_n_length(elem)
                        result.append(EventGroupParallel(elem))
        if result:
            return result
        else:
            return None

    def get_next_possible_states(self, previous_events, child_caller, next_event, blocked_calls_to=[]):
        if next_event is not None and not in_by_is(next_event, self.get_all_child_events()):
            result = self.get_children_next_possible_states(child_caller, blocked_calls_to)
            not_enabled = result.difference(previous_events[-(len(list(self.get_all_child_events()))):])
            events_with_parents = self.get_all_child_events_with_parents()
            for x in not_enabled:
                if isinstance(events_with_parents[x], OptGate) or (isinstance(events_with_parents[x], LopGate) and sum(events_with_parents[x].get_children_min_length()) == 1):
                    yield from not_enabled
            if self.parent not in blocked_calls_to:
                yield from self.parent.get_next_possible_states(previous_events, self, None, blocked_calls_to)
        else:
            result = self.get_children_next_possible_states(child_caller, blocked_calls_to)
            if child_caller is None:
                len_child_caller = 0
            elif isinstance(child_caller, Event):
                len_child_caller = 1
            else:
                len_child_caller = len(list(child_caller.get_all_child_events()))
            not_enabled_yet = result.difference(previous_events[-(len(result) + len_child_caller):])
            if not_enabled_yet:
                if all([is_any_parent_optional(x, self, previous_events) for x in
                        result.difference(previous_events[-(len(list(self.get_all_child_events()))):])]):
                    yield from not_enabled_yet
                    if self.parent not in blocked_calls_to:
                        yield from self.parent.get_next_possible_states(previous_events, self, None, blocked_calls_to)
                else:
                    yield from not_enabled_yet
            else:
                if self.parent not in blocked_calls_to:
                    yield from self.parent.get_next_possible_states(previous_events, self, None, blocked_calls_to)
