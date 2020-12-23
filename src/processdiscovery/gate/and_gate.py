from processdiscovery.gate.gate import Gate
from processdiscovery.event.event import Event
from processdiscovery.util.util import flatten_values
from processdiscovery.event.event_group_parallel import EventGroupParallel
from processdiscovery.exception.exception_decorator import only_throws


class AndGate(Gate):
    def __init__(self, elements=None):
        super().__init__("and", elements)

    @only_throws(ValueError)
    def add_element(self, element):
        self.check_valid_before_appending(element)
        self.elements.append(element)

    @only_throws(ValueError)
    def get_all_n_length_routes(self, n: int) -> []:
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
                        child_all_n_length_routes = elem.get_all_n_length_routes(i)
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

