from __future__ import annotations

from itertools import islice
import collections
import importlib

from process_discovery.event.event import Event
from process_discovery.event.base_group import BaseGroup
from process_discovery.event.comparable_event import ComparableEvent
from process_discovery.exception.exception_decorator import only_throws
from process_discovery.util.util import event_list_length

from functools import cached_property
from typing import Generator
from copy import deepcopy


def consume(iterator, n):
    "Advance the iterator n-steps ahead. If n is none, consume entirely."
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        collections.deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)


class Gate(ComparableEvent):

    def __init__(self, name: str, parent: Gate, elements=None):
        self.name = name
        self.parent = parent
        if elements is None:
            self.elements = []
        else:
            self.elements = elements
        self.min_start = -1
        self.max_start = -1
        self.min_end = -1
        self.max_end = -1

    @cached_property
    def model_min_length(self) -> int:
        raise NotImplemented

    @cached_property
    def model_max_length(self) -> int:
        raise NotImplemented

    @cached_property
    def complexity(self) -> int:
        raise NotImplemented

    @cached_property
    def complexity_for_metric(self) -> int:
        raise NotImplemented

    def __len__(self):
        return sum(len(x) for x in self.elements)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.compare(other)

    def compare(self, other) -> bool:
        pass

    def add_element(self, element) -> None:
        pass

    def set_children_boundaries(self) -> None:
        pass

    def get_all_n_length_routes(self, n: int, process) -> [BaseGroup]:
        pass

    def get_next_possible_states(self, previous_events, child_caller, next_event,
                                 blocked_calls_to=[]) -> Generator[Event, None, None]:
        pass

    @only_throws(ValueError)
    def parse(self, expression: str) -> int:

        numbers = iter(range(len(expression)))
        for i in numbers:
            if expression[i] == "{":
                event = Event(expression[i + 1])
                self.add_element(event)
                consume(numbers, 2)
            elif expression[i] == ")":
                return i+1
            elif i+4 < len(expression):
                if expression[i:i+2] == 'lo' and expression[i:i+3] != 'lop':
                    gate_class = getattr(importlib.import_module("process_discovery.gate.lop_gate"),
                                         "LopGate")
                    gate = gate_class(self)
                    consume(numbers, 3)
                    processed_characters = gate.parse(expression[i + 4:])
                    if self.name == "seq" or self.name == "lop":
                        child_number = len(gate.elements)
                        if int(expression[i+2]) < child_number:
                            for x in gate.elements[(child_number - int(expression[i+2]) - 1):]:
                                to_add = deepcopy(x)
                                to_add.parent = self
                                self.add_element(to_add)

                else:
                    gate_class = getattr(importlib.import_module("process_discovery.gate." + expression[i:i+3] + "_gate"),
                                         expression[i:i+3].capitalize() + "Gate")
                    gate = gate_class(self)
                    consume(numbers, 3)
                    processed_characters = gate.parse(expression[i+4:])
                self.add_element(gate)
                consume(numbers, processed_characters)
            else:
                raise Exception

    def get_all_child_events(self) -> Generator[Event, None, None]:
        for elem in self.elements:
            if isinstance(elem, Event):
                yield elem
            else:
                yield from elem.get_all_child_events()

    def get_all_child_events_except(self, element) -> Generator[Event, None, None]:
        for elem in self.elements:
            if elem is not element:
                if isinstance(elem, Event):
                    yield elem
                else:
                    yield from elem.get_all_child_events()

    def get_all_child_gates(self, gate_type) -> Generator[Gate, None, None]:
        for elem in self.elements:
            if isinstance(elem, gate_type):
                yield elem
                yield from elem.get_all_child_gates(gate_type)
            elif isinstance(elem, Gate):
                yield from elem.get_all_child_gates(gate_type)

    def get_all_child_events_with_parents(self) -> {Event: Gate}:
        nodes = dict()

        for elem in self.elements:
            if isinstance(elem, Event):
                nodes[elem] = self
            else:
                nodes = dict(list(nodes.items()) + list(elem.get_all_child_events_with_parents().items()))

        return nodes

    def get_children_next_possible_states(self, child_caller, blocked_calls_to):
        result = set()
        for x in self.elements:
            if x is not child_caller:
                if isinstance(x, Gate):
                    [result.add(y) for y in x.get_next_possible_states(tuple(), None, None, blocked_calls_to + [self])]
                else:
                    result.add(x)
        return result

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

    def get_goal_length_lower_range(self, n, global_list, min_lengths, max_lengths):
        min_length_local = min_lengths.pop(0)
        max_lengths.pop(0)
        max_lengths_sum = sum(max_lengths)
        return max(min_length_local, n - (max_lengths_sum + event_list_length(global_list, max)))

    def get_goal_length_upper_range(self, n, global_list, min_lengths):
        min_lengths.pop(0)
        min_lengths_sum = sum(min_lengths)
        return n - (min_lengths_sum + event_list_length(global_list, min))

    def get_goal_length_range(self, n, global_list, min_lengths, max_lengths):
        min_length_local = min_lengths.pop(0)
        max_lengths.pop(0)
        min_lengths_sum = sum(min_lengths)
        max_lengths_sum = sum(max_lengths)
        return max(min_length_local, n - (max_lengths_sum + event_list_length(global_list, max))),\
            n - (min_lengths_sum + event_list_length(global_list, min))

    def check_length(self, n, global_list) -> bool:
        return sum([len(x) for x in global_list]) == n

    def get_children_min_length(self) -> []:
        lengths = []

        for elem in self.elements:
            if isinstance(elem, Event):
                lengths.append(1)
            else:
                lengths.append(elem.model_min_length)

        return lengths

    def get_children_max_length(self) -> []:
        lengths = []

        for elem in self.elements:
            if isinstance(elem, Event):
                lengths.append(1)
            else:
                lengths.append(elem.model_max_length)

        return lengths

