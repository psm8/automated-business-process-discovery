from gate.gate import Gate
from util.util import is_struct_empty
from event.event import Event
from fitness.alignment_calculation import flatten_values
from event.event_group import EventGroup


class SeqGate(Gate):
    def __init__(self, elements=None):
        super().__init__("seq", elements)

    def add_element(self, element):
        self.elements.append(element)

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
                lower_limit, upper_limit = self.get_goal_length_range(n, global_list, min_lengths, max_lengths)
                for i in range(lower_limit, upper_limit + 1):
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

        result = []
        if global_list:
            for elem in flatten_values(global_list):
                if self.is_in_range(n, elem):
                    result.append(EventGroup(elem))

        return result

    def get_model_min_length(self) -> int:
        return sum(self.get_children_min_length())

    def get_model_max_length(self) -> int:
        return sum(self.get_children_max_length())

