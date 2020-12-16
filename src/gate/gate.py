from __future__ import annotations

from itertools import islice
import collections
import importlib

from event.event import Event
from exception.exception_decorator import only_throws
from util.util import event_list_length


def consume(iterator, n):
    "Advance the iterator n-steps ahead. If n is none, consume entirely."
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        collections.deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)


class Gate:

    def __init__(self, name: str, elements=None):
        self.name = name[0:3]
        if elements is None:
            self.elements = []
        else:
            self.elements = elements

    @only_throws(ValueError)
    def check_valid_for_get_n_length(self, elements_with_groups):
        elements = []
        for elem in elements_with_groups:
            if isinstance(elem, Event):
                elements.append(elem)
        for i in range(len(elements)):
            for j in range(i + 1, len(elements)):
                if elements[i].name == elements[j].name:
                    raise ValueError

    @only_throws(ValueError)
    def check_valid_before_appending(self, element):
        for elem in self.elements:
            if isinstance(elem, Event):
                if element.name == elem.name:
                    raise ValueError

    @only_throws(ValueError)
    def parse(self, expression: str) -> int:

        locally_added_events = []
        numbers = iter(range(len(expression)))
        for i in numbers:
            if expression[i] == "{":
                event = Event(expression[i + 1])
                locally_added_events.append(event)
                self.add_element(event)
                consume(numbers, 2)
            elif expression[i] == ")":
                return i+1
            elif i+4 < len(expression):
                gate_class = getattr(importlib.import_module("gate." + expression[i:i+3] + "_gate"),
                                     expression[i:i+3].capitalize() + "Gate")
                gate = gate_class()
                consume(numbers, 3)
                processed_characters = gate.parse(expression[i+4:])
                self.add_element(gate)
                consume(numbers, processed_characters)
            else:
                raise Exception
        for event in locally_added_events:
            event.no_branches += 1

    def get_goal_length_lower_range(self, n, global_list, min_lengths, max_lengths):
        min_length_local = min_lengths.pop(0)
        max_length_local = max_lengths.pop(0)
        max_lengths_sum = sum(max_lengths)
        return max(1, min_length_local, n - (max_lengths_sum + event_list_length(global_list, max)))

    # could add max lengths
    def get_goal_length_upper_range(self, n, global_list, min_lengths):
        min_length_local = min_lengths.pop(0)
        min_lengths_sum = sum(min_lengths)
        return n - (min_lengths_sum + event_list_length(global_list, min))

    # could add max lengths
    def get_goal_length_range(self, n, global_list, min_lengths, max_lengths):
        min_length_local = min_lengths.pop(0)
        max_length_local = max_lengths.pop(0)
        min_lengths_sum = sum(min_lengths)
        max_lengths_sum = sum(max_lengths)
        return max(1, min_length_local, n - (max_lengths_sum + event_list_length(global_list, max))),\
            n - (min_lengths_sum + event_list_length(global_list, min))

    # should i use it everywhere??????????????????
    #????????
    def is_in_range(self, n, global_list) -> bool:
        return event_list_length(global_list, min) <= n <= event_list_length(global_list, max)

    def get_children_min_length(self) -> []:
        lengths = []

        for elem in self.elements:
            if isinstance(elem, Event):
                lengths.append(1)
            else:
                lengths.append(elem.get_model_min_length())

        return lengths

    def get_children_max_length(self) -> []:
        lengths = []

        for elem in self.elements:
            if isinstance(elem, Event):
                lengths.append(1)
            else:
                lengths.append(elem.get_model_max_length())

        return lengths

    def get_events_with_parents(self) -> [tuple]:
        nodes = []

        for elem in self.elements:
            if isinstance(elem, Event):
                nodes.append((self, elem))
            else:
                [nodes.append(x) for x in elem.get_events_with_parents()]

        return nodes
