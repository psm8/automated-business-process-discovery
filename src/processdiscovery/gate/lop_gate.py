from processdiscovery.gate.gate import Gate
from processdiscovery.gate.seq_gate import SeqGate
from processdiscovery.util.util import to_n_length, flatten_values, index_by_is
from processdiscovery.event.event import Event
from processdiscovery.event.base_group import BaseGroup

from functools import reduce, cached_property
from math import pow


class LopGate(Gate):
    LOP_GATE_MAX_NUMBER_OF_CHILDREN_COMBINATIONS = 32
    LOP_GATE_MAX_DEPTH = 3

    def __init__(self, parent=None, elements=None):
        super().__init__("lop", parent, elements)
        self.twin_complexity = 1

    @cached_property
    def model_min_length(self) -> int:
        return 0

    @cached_property
    def model_max_length(self) -> int:
        return self.LOP_GATE_MAX_DEPTH * sum(self.get_children_max_length())

    @cached_property
    def complexity(self) -> int:
        n = self.LOP_GATE_MAX_DEPTH
        return sum(pow(reduce(lambda x, y: x*y,
                              [x.complexity if isinstance(x, Gate) else 1 for x in self.elements]),
                       i) for i in range(n + 1))

    @cached_property
    def complexity_for_metric(self) -> int:
        n = 2
        divide_by_complexity = self.twin_complexity
        return sum(pow(reduce(lambda x, y: x * y,
                              [x.complexity_for_metric if isinstance(x, Gate) else 1 for x in self.elements]),
                       i)/divide_by_complexity for i in range(1, n + 1))

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

    def set_children_boundaries(self):
        min_lengths = self.get_children_min_length()
        max_lengths = self.get_children_max_length()

        self.elements[0].min_start = self.min_start
        self.elements[0].max_start = self.max_start
        self.elements[0].min_end = max(self.elements[0].min_start + self.elements[0].model_min_length,
                                       self.min_end - self.LOP_GATE_MAX_DEPTH * sum(max_lengths[1:]))
        self.elements[0].max_end = min(self.elements[0].max_start +
                                       self.LOP_GATE_MAX_DEPTH * self.elements[0].model_max_length,
                                       self.max_end - sum(min_lengths[1:]))
        if isinstance(self.elements[0], Gate):
            self.elements[0].set_children_boundaries()

        for i in range(1, len(self.elements)):
            self.elements[i].min_start = self.elements[i-1].min_end
            self.elements[i].max_start = self.elements[i-1].max_end
            self.elements[i].min_end = max(self.elements[i].min_start + self.elements[i].model_min_length,
                                           self.min_end - self.LOP_GATE_MAX_DEPTH * sum(max_lengths[i+1:]))
            self.elements[i].max_end = min(self.elements[i].max_start +
                                           self.LOP_GATE_MAX_DEPTH * self.elements[i].model_max_length,
                                           self.max_end - sum(min_lengths[i+1:]))
            if isinstance(self.elements[i], Gate):
                self.elements[i].set_children_boundaries()

    def get_all_n_length_routes(self, n: int, process) -> [BaseGroup]:
        if n == 0:
            return []
        if self.model_max_length < n or n < sum(self.get_children_min_length()):
            return None
        min_lengths = self.get_children_min_length()
        global_list = []

        for elem in self.elements:
            local_list = []
            if isinstance(elem, Event):
                local_list.append(elem)
                min_lengths.pop(0)
            else:
                upper_limit = self.get_goal_length_upper_range(n, global_list, min_lengths)
                for i in range(max(1, elem.model_min_length), upper_limit + 1):
                    try:
                        child_all_n_length_routes = elem.get_all_n_length_routes(i, process)
                    except ValueError:
                        return None
                    if child_all_n_length_routes is not None:
                        local_list.append(child_all_n_length_routes)

            if local_list:
                global_list.append(local_list)

        if global_list:
            flattened_list = flatten_values(global_list)
            if len(flattened_list) < self.LOP_GATE_MAX_NUMBER_OF_CHILDREN_COMBINATIONS:
                results = [x for x in to_n_length(n, flattened_list, process, self.LOP_GATE_MAX_DEPTH, 0)]
                if results:
                    return results
                else:
                    return None
            else:
                return None
        else:
            return None

    def get_next_possible_states(self, previous_events, child_caller, next_event, blocked_calls_to=[]) -> {Event}:
        if child_caller is None:
            x = self.elements[0]
            if isinstance(x, Gate):
                yield from x.get_next_possible_states(tuple(), None, None, blocked_calls_to)
            else:
                yield x
            if self.parent not in blocked_calls_to:
                yield from self.parent.get_next_possible_states(previous_events, self, None, blocked_calls_to)
        else:
            if child_caller is self.elements[-1]:
                if self.parent not in blocked_calls_to:
                    yield from self.parent.get_next_possible_states(previous_events, self, None, blocked_calls_to)
                x = self.elements[0]
                if isinstance(x, Gate):
                    yield from x.get_next_possible_states(tuple(), None, None, blocked_calls_to + [self])
                else:
                    yield x

            else:
                i = index_by_is(child_caller, self.elements)
                x = self.elements[i + 1]
                if isinstance(x, Gate):
                    yield from x.get_next_possible_states(tuple(), None, None, blocked_calls_to)
                else:
                    yield x

    def set_twin_events_and_complexity(self):
        if isinstance(self.parent, SeqGate) or isinstance(self.parent, LopGate):
            i = self.parent.elements.index(self)
            i -= 1
            j = 1
            while i >= 0 and j <= len(self.elements):
                if isinstance(self.elements[-j], Event) and isinstance(self.parent.elements[i], Event) and \
                        self.elements[-j].name == self.parent.elements[i].name:
                    self.elements[-j].event_lop_twin = self.parent.elements[i]
                elif isinstance(self.elements[-j], Gate) and isinstance(self.parent.elements[i], Gate) and \
                        self.elements[-j] == self.parent.elements[i]:
                    self.twin_complexity *= self.elements[-j].complexity_for_metric
                    for x in self.elements[-j].get_all_child_events():
                        for y in self.parent.elements[i].get_all_child_events():
                            x.event_lop_twin = y
                            break
                else:
                    break
                i -= 1
                j += 1
