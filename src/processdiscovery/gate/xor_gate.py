from processdiscovery.gate.gate import Gate
from processdiscovery.event.event import Event
from processdiscovery.exception.exception_decorator import only_throws


class XorGate(Gate):
    def __init__(self, parent=None, elements=None):
        super().__init__("xor", parent, elements)

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

    def get_all_n_length_routes(self, n: int, process) -> []:
        if n == 0:
            return []
        if self.get_model_max_length() < n and n > 0:
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
                    return []
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
        else:
            return local_list

        return result

    def get_model_min_length(self) -> int:
        return min(self.get_children_min_length())

    def get_model_max_length(self) -> int:
        return max(self.get_children_max_length())

    def get_next_possible_states(self, previous_events, caller_child, next_event):
        if caller_child in self.elements:
            yield from self.parent.get_next_possible_states(previous_events, self, None)
        else:
            yield from (x.get_next_possible_states(set(), self, None) if isinstance(x, Gate) else x for x in self.elements)

    def get_complexity(self):
        return sum([x.get_complexity() if isinstance(x, Gate) else 1 for x in self.elements])
