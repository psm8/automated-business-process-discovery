from __future__ import annotations

from itertools import islice, permutations
from copy import deepcopy
import collections
import importlib

from gate.process import Process


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

        numbers = iter(range(len(expression)))
        for i in numbers:
            if expression[i] == "{":
                self.add_element(expression[i + 1])
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

    # def check_repetitions(self, process):
    #     if self.name == "and" or self.name == "opt" or self.name == "xor":
    #         for elem in self.elements:
    #             if elem == process:
    #                 raise Exception

    def find_first_occurrence(self, global_process: Process) -> [Process]:

        all_processes = []
        elements = self.elements.copy()

        while global_process.flag < len(global_process.events) and \
                global_process.events.get(global_process.flag)[1] - global_process.flag <= \
                len(global_process.events) / 2:
            # python way to check empty
            if elements:
                if self.name == "and":
                    local_matches_and = 0
                    self.calc_and(all_processes, elements, global_process)
                    all_processes = self.remove_policy_and(all_processes)
                    model_minimal_length = self.get_model_minimal_length()
                    for i in range(global_process.flag, len(global_process.events)):
                        global_process.events[i] = (global_process.events.get(i)[0], len(elements) - local_matches_and - 1)
                elif self.name == "xor":
                    self.calc_xor(all_processes, elements, global_process)
                    all_processes = self.remove_policy_xor(all_processes)
                elif self.name == "seq":
                    self.calc_seq(all_processes, elements, global_process)
                    all_processes = self.remove_policy_seq(all_processes)
                elif self.name == "opt":
                    # python way to check empty
                    while elements:
                        elem = elements.pop(0)
                        process = Process(global_process.events, global_process.flag)
                        if isinstance(elem, str):
                            for i in range(process.flag, len(process.events)):
                                process.events[i] = (process.events.get(i)[0], process.events.get(i)[1] + 1)
                                if elem == process.events.get(process.flag)[0]:
                                    process.flag += 1
                                # the difference between and and xor
                                gate = Gate(self.name, elements)
                                gate.find_first_occurrence(process)
                            all_processes.append(process)
                        else:
                            all_processes.append(elem.find_first_occurrence(process, process.flag))
                    global_process.flag += 1
                elif self.name == "lop":
                    elem = elements.pop(0)
                    if isinstance(elem, str):
                        if elem == global_process.events.get(global_process.flag)[0]:
                            for i in range(global_process.flag, len(global_process.events)):
                                global_process.events[i] = (global_process.events.get(i)[0],
                                                            global_process.events.get(i)[1] + 1)
                                global_process.flag += 1
                    else:
                        global_process = elem.find_first_occurrence(global_process)
                else:
                    raise Exception

                if len(all_processes) > 1:
                    return self.split_if_multiple(all_processes, elements)

            else:
                for i in range(global_process.flag, len(global_process.events)):
                    global_process.events[i] = (global_process.events.get(i)[0], -1)
                return [global_process]

        for i in range(global_process.flag, len(global_process.events)):
            global_process.events[i] = (global_process.events.get(i)[0], -1)
        return [global_process]

    def calc_and(self, all_processes: [Process], elements: [Gate], global_process: Process):
        for elem in elements:
            if isinstance(elem, str):
                process = Process(global_process.events, global_process.flag)
                if elem == process.events.get(process.flag)[0]:
                    elements.remove(elem)
                    for i in range(process.flag, len(process.events)):
                        process.events[i] = (process.events.get(i)[0],
                                             process.events.get(i)[1] + 1)
                    process.flag += 1
                    # the difference between and and xor
                    self.calc_and(all_processes, elements, process)
                    all_processes.append(process)
            else:
                all_processes.append(elem.find_first_occurrence(process))
                elements.remove(elem)
                self.calc_and(all_processes, elements, process)

    def calc_xor(self, all_processes: [Process], elements: [Gate], global_process: Process):
        # python way to check empty
        while elements:
            elem = elements.pop(0)
            process = Process(global_process.events, global_process.flag)
            if isinstance(elem, str):
                for i in range(process.flag, len(process.events)):
                    process.events[i] = (process.events.get(i)[0], process.events.get(i)[1] + 1)
                    if elem == process.events.get(process.flag)[0]:
                        process.flag += 1
                all_processes.append(process)
            else:
                all_processes.append(elem.find_first_occurrence(process, global_process.flag))

    def calc_seq(self, all_processes: [Process], elements: [Gate], global_process: Process):
        while elements:
            process = deepcopy(global_process)
            self.calc_seq_inner(all_processes, elements, process)
            all_processes.append(process)
            elements = elements[1:]

    def calc_seq_inner(self, all_processes: [Process], elements: [Gate], process: Process):
        if process.flag < len(process.events):
            if isinstance(elements[0], str):
                if elements[0] == process.events.get(process.flag)[0]:
                    for i in range(process.flag, len(process.events)):
                        process.events[i] = (process.events.get(i)[0], process.events.get(i)[1] + 1)
                        # if process.flag == 0:

                    elements = elements[1:]
            else:
                elements[0].find_first_occurrence(process)
                if process.events.get(0)[1] != -1:
                    return process
            process.flag += 1
            self.calc_seq_inner(all_processes, elements, process)

    def remove_policy_and(self, all_processes: []):
        results = dict()
        for process in all_processes:
            for i in range(len(process.events)):
                if process.events.get(i) == -1:
                    if i > 0:
                        results[process.events] = ((process.events.get(i)[1] + 1) / i, i)
        if results:
            new_all_processes_with_flag = [k for k, v in results.items() if float(v) >= min(results, key=results.get)]
        else:
            new_all_processes_with_flag = []

        return new_all_processes_with_flag

    def remove_policy_xor(self, all_processes: [Process]) -> []:
        results = dict()
        for process in all_processes:
            for i in range(len(process.events)):
                if process.events.get(i) == -1:
                    if i > 0:
                        results[process.events] = ((process.events.get(i)[1] + 1)/i, i)
        if results:
            new_all_processes_with_flag = [k for k, v in results.items() if float(v) >= min(results, key=results.get)]
        else:
            new_all_processes_with_flag = []

        return new_all_processes_with_flag

    def remove_policy_seq(self, all_processes: [Process]) -> []:
        results = dict()
        for process in all_processes:
            for i in range(len(process.events)):
                if process.events.get(i) == -1:
                    if i > 0:
                        results[process.events] = ((process.events.get(i)[1] + 1)/i, i)
        if results:
            new_all_processes_with_flag = [k for k, v in results.items() if float(v) >= min(results, key=results.get)]
        else:
            new_all_processes_with_flag = []

        return new_all_processes_with_flag

    def calc_flags_seq(self) -> [Process]:
        return []

    def split_if_multiple(self, all_processes_with_flag, elements):
        new_all_processes = []
        for process in all_processes_with_flag:
            gate = Gate(self.name, elements)
            new_all_processes.append(gate.find_first_occurrence(process))
        return self.remove_policy_xor(new_all_processes)[0]

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

    def list_length_recursive(self, struct, min_or_max) -> int:
        if struct:
            # # check if set
            # if isinstance(struct, set) or isinstance(struct, frozenset):
            #     return min_or_max(self.list_length_recursive(x, min_or_max) for x in struct)
            # check if list of tuples
            if isinstance(struct[0], tuple):
                return min_or_max(self.list_length_recursive(x, min_or_max) for x in struct)
            # else list of lists and events
            else:
                local_result = []
                for elem in struct:
                    if isinstance(elem, list):
                        local_result.append(self.list_length_recursive(elem, min_or_max))
                    else:
                        local_result.append(len(elem))
                return sum(local_result)
        else:
            return 0

    # probably could be simplified because never nested lists
    def list_length_new(self, struct, min_or_max) -> int:
        if struct:
            result = 0
            if isinstance(struct[0], tuple):
                return min_or_max(self.list_length_new(x, min_or_max) for x in struct)
            for elem in struct:
                if isinstance(elem, list):
                    result += min_or_max(self.list_length_new(x, min_or_max) for x in elem)
                else:
                    result += len(elem)
            return result
        else:
            return 0

    # should i use it everywhere??????????????????
    #????????
    def is_in_range(self, n, global_list) -> bool:
        return self.list_length_new(global_list, min) <= n <= self.list_length_new(global_list, max)

    def get_children_min_length(self) -> []:
        lengths = []

        for elem in self.elements:
            if isinstance(elem, str):
                lengths.append(1)
            else:
                lengths.append(elem.get_model_min_length())

        return lengths

    def get_children_max_length(self) -> []:
        lengths = []

        for elem in self.elements:
            if isinstance(elem, str):
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
            if isinstance(elem, str):
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
