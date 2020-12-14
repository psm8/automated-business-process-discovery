from gate.gate import Gate
from util.util import is_struct_empty
from event.event import Event
from exception.exception_decorator import only_throws


class XorGate(Gate):
    def __init__(self, elements=None):
        super().__init__("xor", elements)

    @only_throws(ValueError)
    def add_element(self, element):
        self.check_valid_before_appending(element)
        self.elements.append(element)

    def get_all_n_length_routes(self, n: int) -> []:
        if self.get_model_max_length() < n and n > 0:
            return None

        global_list = []

        for elem in self.elements:
            if isinstance(elem, Event):
                if n == 1:
                    global_list.append([elem])
            else:
                # possibly should add lower limit
                child_all_n_length_routes = elem.get_all_n_length_routes(n)
                # indicated something wrong
                if is_struct_empty(child_all_n_length_routes):
                    return []
                if self.is_in_range(n, child_all_n_length_routes):
                    global_list.append(child_all_n_length_routes)

        if global_list:
            # because always 1 elem list
            return [x[0] for x in global_list]
        else:
            return global_list

    def get_model_min_length(self) -> int:
        return min(self.get_children_min_length())

    def get_model_max_length(self) -> int:
        return max(self.get_children_max_length())
