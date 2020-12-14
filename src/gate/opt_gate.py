from gate.gate import Gate
from util.util import is_struct_empty, to_n_length_opt
from fitness.alignment_calculation import flatten_values
from event.event import Event
from exception.exception_decorator import only_throws
from event.base_group import BaseGroup

class OptGate(Gate):
    def __init__(self, elements=None):
        super().__init__("opt", elements)

    @only_throws(ValueError)
    def add_element(self, element):
        self.check_valid_before_appending(element)
        self.elements.append(element)

    @only_throws(ValueError)
    def get_all_n_length_routes(self, n: int) -> []:
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
                    # indicated something wrong
                    if is_struct_empty(child_all_n_length_routes):
                        return []
                    if child_all_n_length_routes is not None:
                        local_list.append(child_all_n_length_routes)

            if local_list:
                global_list.append(local_list)

        if global_list:
            results = to_n_length_opt(n, flatten_values(global_list))
            for result in results:
                if isinstance(result, BaseGroup):
                    self.check_valid_for_get_n_length(result.events)
            return results
        else:
            return []

    def get_model_min_length(self) -> int:
        return 0

    def get_model_max_length(self) -> int:
        return sum(self.get_children_max_length())

