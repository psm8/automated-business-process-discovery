from processdiscovery.gate.gate import Gate
from processdiscovery.gate.seq_gate import SeqGate
from processdiscovery.util.util import to_n_length
from processdiscovery.util.util import flatten_values
from processdiscovery.event.event import Event

from functools import reduce
from math import pow


class LopGate(Gate):
    LOP_GATE_MAX_NUMBER_OF_CHILDREN_COMBINATIONS = 32
    LOP_GATE_MAX_DEPTH = 3

    def __init__(self, parent=None, elements=None):
        super().__init__("lop", parent, elements)

    def add_element(self, element):
        self.elements.append(element)

    def compare(self, other):
        if not isinstance(other, type(self)):
            return False
        if len(self) != len(other):
            return False
        for i in range(len(self.elements)):
            if not self.elements[i].compare(other.elements[i]):
                return False
        return True

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
                for i in range(max(1, elem.get_model_min_length()), upper_limit + 1):
                    try:
                        child_all_n_length_routes = elem.get_all_n_length_routes(i, process)
                    except ValueError:
                        return []
                    if child_all_n_length_routes is not None:
                        local_list.append(child_all_n_length_routes)

            if local_list:
                global_list.append(local_list)

        if global_list:
            flattened_list = flatten_values(global_list)
            if len(flattened_list) < self.LOP_GATE_MAX_NUMBER_OF_CHILDREN_COMBINATIONS:
                results = [x for x in to_n_length(n, flattened_list, process, self.LOP_GATE_MAX_DEPTH, 0)]
                return results
            else:
                return []
        else:
            return []

    def get_model_min_length(self) -> int:
        return 0

    def get_model_max_length(self) -> int:
        return self.LOP_GATE_MAX_DEPTH * sum(self.get_children_max_length())

    def get_next_possible_states(self, previous_events, child_caller, next_event, blocked_parent_call=False) -> set:
        if child_caller is None:
            x = self.elements[0]
            if isinstance(x, Gate):
                yield from x.get_next_possible_states(set(), None, None)
            else:
                yield x
            if not blocked_parent_call:
                yield from self.parent.get_next_possible_states(previous_events, self, None)
        else:
            if child_caller == self.elements[-1]:
                if not blocked_parent_call:
                    yield from self.parent.get_next_possible_states(previous_events, self, None)
                x = self.elements[0]
                if isinstance(x, Gate):
                    yield from x.get_next_possible_states(set(), None, None, True)
                else:
                    yield x

            else:
                i = self.elements.index(child_caller)
                x = self.elements[i + 1]
                if isinstance(x, Gate):
                    yield from x.get_next_possible_states(set(), None, None)
                else:
                    yield x

    def get_complexity(self):
        n = self.LOP_GATE_MAX_DEPTH
        return sum(pow(reduce(lambda x, y: x*y,
                              [x.get_complexity() if isinstance(x, Gate) else 1 for x in self.elements]),
                       i) for i in range(n + 1))

    def get_complexity_for_metric(self):
        n = 2
        divide_by_complexity = self.count_complexity_if_seq_parent()
        return sum(pow(reduce(lambda x, y: x * y,
                              [x.get_complexity_for_metric() if isinstance(x, Gate) else 1 for x in self.elements]),
                       i)/divide_by_complexity for i in range(1, n + 1))

    def count_repeating_if_seq_parent(self):
        if isinstance(self.parent, SeqGate):
            count = 0
            i = self.parent.elements.index(self)
            i -= 1
            j = 1
            while i >= 0 and j <= len(self.elements):
                if isinstance(self.elements[-j], Event) and isinstance(self.parent.elements[i], Event) and \
                        self.elements[-j].name == self.parent.elements[i].name:
                    count += 1
                elif isinstance(self.elements[-j], Gate) and isinstance(self.parent.elements[i], Gate) and \
                        self.elements[-j] == self.parent.elements[i]:
                    count += len(self.elements[-j])
                else:
                    break
                i -= 1
                j += 1

            return count
        else:
            return 0

    def count_complexity_if_seq_parent(self):
        if isinstance(self.parent, SeqGate):
            count = 1
            i = self.parent.elements.index(self)
            i -= 1
            j = 1
            while i >= 0 and j <= len(self.elements):
                if isinstance(self.elements[-j], Event) and isinstance(self.parent.elements[i], Event) and \
                        self.elements[-j].name == self.parent.elements[i].name:
                    count *= 1
                elif isinstance(self.elements[-j], Gate) and isinstance(self.parent.elements[i], Gate) and \
                        self.elements[-j] == self.parent.elements[i]:
                    count *= self.elements[-j].get_complexity_for_metric()
                else:
                    break
                i -= 1
                j += 1

            return count
        else:
            return 1

