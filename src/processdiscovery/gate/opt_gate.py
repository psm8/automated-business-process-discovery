from processdiscovery.gate.gate import Gate
from processdiscovery.util.util import to_n_length_opt, flatten_values
from processdiscovery.event.event import Event
from processdiscovery.exception.exception_decorator import only_throws
from processdiscovery.event.base_group import BaseGroup

from functools import reduce, cached_property
from math import factorial, comb


class OptGate(Gate):
    OPT_GATE_MAX_NUMBER_OF_CHILDREN = 5

    def __init__(self, parent=None, elements=None):
        super().__init__("opt", parent, elements)

    @cached_property
    def model_min_length(self) -> int:
        return 0

    @cached_property
    def model_max_length(self) -> int:
        return sum(self.get_children_max_length())

    @cached_property
    def complexity(self):
        n = len(self.elements)
        return reduce(lambda x, y: x*y, [x.complexity if isinstance(x, Gate) else 1 for x in self.elements]) \
               * sum(factorial(i) * comb(n, i) for i in range(n + 1))

    @cached_property
    def complexity_for_metric(self):
        n = len(self.elements)
        return reduce(lambda x, y: x * y, [x.complexity_for_metric if isinstance(x, Gate) else 1 for x in self.elements]) \
               * sum(factorial(i) * comb(n, i) for i in range(n + 1))

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
    def add_element(self, element):
        self.check_valid_before_appending(element)
        if len(self.elements) >= self.OPT_GATE_MAX_NUMBER_OF_CHILDREN:
            raise ValueError
        self.elements.append(element)

    @only_throws(ValueError)
    def get_all_n_length_routes(self, n: int, process) -> []:
        if n == 0:
            return []
        if self.model_max_length < n or n < min(self.get_children_min_length()):
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
                lower_limit = self.get_goal_length_lower_range(n, global_list, min_lengths, max_lengths)
                for i in range(lower_limit, n + 1):
                    try:
                        child_all_n_length_routes = elem.get_all_n_length_routes(i, process)
                    except ValueError:
                        return None
                    if child_all_n_length_routes is not None:
                        local_list.append(child_all_n_length_routes)

            if local_list:
                global_list.append(local_list)

        results = []
        if global_list:
            flattened_list = flatten_values(global_list)
            for elem in flattened_list:
                [results.append(x) for x in to_n_length_opt(n, elem)]
            for result in list(set(results)):
                if isinstance(result, BaseGroup):
                    self.check_valid_for_get_n_length(result.events)

        if results:
            return results
        else:
            return None

    def get_next_possible_states(self, previous_events, child_caller, next_event, blocked_calls_to=[]):
        result = set()
        for x in self.elements:
            if isinstance(x, Gate):
                if x is not child_caller:
                    [result.add(y) for y in x.get_next_possible_states(tuple(), None, None, blocked_calls_to + [self])]
            else:
                result.add(x)
        not_enabled_yet = result.difference(previous_events[-len(result):])
        if not_enabled_yet:
            yield from not_enabled_yet
        if self.parent not in blocked_calls_to:
            yield from self.parent.get_next_possible_states(previous_events, self, None, blocked_calls_to)
