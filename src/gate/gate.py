from __future__ import annotations

from itertools import islice
import collections
import importlib

from event.event import Event
from event.event_group import EventGroup
from event.event_group_parallel import EventGroupParallel


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

    def add_element(self, element):
        self.elements.append(element)

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

    # def check_repetitions(self, process):
    #     if self.name == "and" or self.name == "opt" or self.name == "xor":
    #         for elem in self.elements:
    #             if elem == process:
    #                 raise Exception

    def get_goal_length_lower_range(self, n, global_list, min_lengths, max_lengths):
        min_length_local = min_lengths.pop(0)
        max_length_local = max_lengths.pop(0)
        max_lengths_sum = sum(max_lengths)
        return max(1, min_length_local, n - (max_lengths_sum + self.list_length_new(global_list, max)))

    # could add max lengths
    def get_goal_length_upper_range(self, n, global_list, min_lengths):
        min_length_local = min_lengths.pop(0)
        min_lengths_sum = sum(min_lengths)
        return n - (min_lengths_sum + self.list_length_new(global_list, min))

    # could add max lengths
    def get_goal_length_range(self, n, global_list, min_lengths, max_lengths):
        min_length_local = min_lengths.pop(0)
        max_length_local = max_lengths.pop(0)
        min_lengths_sum = sum(min_lengths)
        max_lengths_sum = sum(max_lengths)
        return max(1, min_length_local, n - (max_lengths_sum + self.list_length_new(global_list, max))),\
            n - (min_lengths_sum + self.list_length_new(global_list, min))

    # probably could be simplified because never nested lists
    def list_length_new(self, struct, min_or_max) -> int:
        if struct:
            if isinstance(struct, list):
                return sum(self.list_length_new(x, min_or_max) for x in struct)
            else:
                return len(struct)
        else:
            return 0

    # should i use it everywhere??????????????????
    #????????
    def is_in_range(self, n, global_list) -> bool:
        return self.list_length_new(global_list, min) <= n <= self.list_length_new(global_list, max)

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

    def get_processes_list(self) -> []:
        processes = []
        iterator = 0
        elements = self.elements.copy()

        while elements:
            elem = elements.pop(0)
            if isinstance(elem, Event):
                processes.append(elem)
            else:
                processes.append(elem.get_processes_list())
                iterator += 1

        return processes

# class TimeoutException(Exception):
#     def __init__(self, msg=None):
#         #: The message from the remark tag or element
#         self.msg = msg
#
#     def __str__(self):
#         if self.msg is None:
#             return "No error message provided"
#         if not isinstance(self.msg, str):
#             return str(self.msg)
#         return self.msg
