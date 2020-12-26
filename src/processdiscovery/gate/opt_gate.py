from processdiscovery.gate.gate import Gate
from processdiscovery.util.util import to_n_length_opt
from processdiscovery.util.util import flatten_values
from processdiscovery.event.event import Event
from processdiscovery.exception.exception_decorator import only_throws
from processdiscovery.event.base_group import BaseGroup


class OptGate(Gate):
    OPT_GATE_MAX_NUMBER_OF_CHILDREN = 5

    def __init__(self, elements=None):
        super().__init__("opt", elements)

    @only_throws(ValueError)
    def add_element(self, element):
        self.check_valid_before_appending(element)
        if len(self.elements) >= self.OPT_GATE_MAX_NUMBER_OF_CHILDREN:
            raise ValueError
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
                lower_limit = self.get_goal_length_lower_range(n, global_list, min_lengths, max_lengths)
                for i in range(lower_limit, n + 1):
                    try:
                        child_all_n_length_routes = elem.get_all_n_length_routes(i)
                    except ValueError:
                        return []
                    if child_all_n_length_routes is not None:
                        local_list.append(child_all_n_length_routes)

            if local_list:
                global_list.append(local_list)

        if global_list:
            flattened_list = flatten_values(global_list)
            results = []
            for elem in flattened_list:
                [results.append(x) for x in to_n_length_opt(n, elem)]
            for result in list(set(results)):
                if isinstance(result, BaseGroup):
                    self.check_valid_for_get_n_length(result.events)
            return results
        else:
            return []

    def get_model_min_length(self) -> int:
        return 0

    def get_model_max_length(self) -> int:
        return sum(self.get_children_max_length())

