import math

from itertools import islice, permutations
import collections


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

    def __init__(self, expression: str):
        self.name = expression[0:3]
        self.elements = []

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
                if expression[i:i+3] == "and" or expression[i:i+3] == "opt" or expression[i:i+3] == "xor" or \
                        expression[i:i+3] == "lop" or expression[i:i+3] == "seq":
                    gate = Gate(expression[i:])
                    consume(numbers, 3)
                    processed_characters = gate.parse(expression[i+4:])
                    self.add_element(gate)
                    consume(numbers, processed_characters)
                elif expression[i:i+3] == "trm":
                    self.add_element(Gate("trm"))
                    consume(numbers, 4)
                else:
                    raise Exception
            else:
                raise Exception

    # def check_repetitions(self, process):
    #     if self.name == "and" or self.name == "opt" or self.name == "xor":
    #         for elem in self.elements:
    #             if elem == process:
    #                 raise Exception

    def traverse(self, expression: str, goal_length: int) -> int:
        cumulative_error = 0
        matches = []
        if self.name == "and":
            return 0
        elif self.name == "xor":
            return 0
        elif self.name == "seq":
            return sum(self.traverse_process_children(expression))
        # python way to check empty
        elif self.name == "opt":
            return 0
        elif self.name == "trm":
            return 0
        elif self.name == "lop":
            return 0
        else:
            raise Exception

    # def traverse_2(self, expression: str, goal_length: int) -> int:
    #     cumulative_error = 0
    #     matches = []
    #     if self.name == "and":
    #         if not elem in matches
    #             cumulative_error +=1
    #         else:
    #             next elem
    #     elif self.name == "xor":
    #         if not elem in matches
    #             cumulative_error += 1
    #     elif self.name == "seq":
    #         if elem != matches[0]:
    #             cumulative_error += 1
    #     # python way to check empty
    #     elif self.name == "opt":
    #         if elem in matches:
    #             next elem
    #     elif self.name == "trm":
    #         return 0
    #     elif self.name == "lop":
    #         if elem == matches[0]:
    #             next elem
    #     else:
    #         raise Exception

    def find_first_occurrence(self, global_processes: dict, flag: int) -> []:
        all_processes = []
        elements = self.elements.copy()

        while flag < len(global_processes) or global_processes.get(flag)[1] - flag <= len(global_processes) / 2:
            # python way to check empty
            if elements:
                if self.name == "and":
                    elem = elements.pop(0)
                    # python way to check empty
                    while elements:
                        processes = global_processes.copy()
                        if isinstance(elem, str):
                            for i in range(flag, len(processes)):
                                processes[i] = (processes.get(i)[0], processes.get(i)[1] + 1)
                                if elem == processes.get(flag)[0]:
                                    flag += 1
                                # the difference between and and xor
                                self.find_first_occurrence(processes, flag)
                            all_processes.append(processes)
                        else:
                            all_processes.append(elem.find_first_occurrence(processes, flag))
                elif self.name == "xor":
                    elem = elements.pop(0)
                    # python way to check empty
                    while elements:
                        processes = global_processes.copy()
                        if isinstance(elem, str):
                            for i in range(flag, len(processes)):
                                processes[i] = (processes.get(i)[0], processes.get(i)[1] + 1)
                                if elem == processes.get(flag)[0]:
                                    flag += 1
                            all_processes.append(processes)
                        else:
                            all_processes.append(elem.find_first_occurrence(processes, flag))
                elif self.name == "seq":
                    elem = elements.pop(0)
                    if isinstance(elem, str):
                        if elem == global_processes.get(flag)[0]:
                            for i in range(flag, len(global_processes)):
                                global_processes[i] = (global_processes.get(i)[0],
                                                       global_processes.get(i)[1] + 1)
                    else:
                        global_processes = elem.find_first_occurrence(global_processes, flag)
                    flag += 1
                elif self.name == "opt":
                    elem = elements.pop(0)
                    # python way to check empty
                    while elements:
                        processes = global_processes.copy()
                        if isinstance(elem, str):
                            for i in range(flag, len(processes)):
                                processes[i] = (processes.get(i)[0], processes.get(i)[1] + 1)
                                if elem == processes.get(flag)[0]:
                                    flag += 1
                                # the difference between and and xor
                                self.find_first_occurrence(processes, flag)
                            all_processes.append(processes)
                        else:
                            all_processes.append(elem.find_first_occurrence(processes, flag))
                    flag += 1
                elif self.name == "trm":
                    return global_processes
                elif self.name == "lop":
                    elem = elements.pop(0)
                    if isinstance(elem, str):
                        if elem == global_processes.get(flag)[0]:
                            for i in range(flag, len(global_processes)):
                                global_processes[i] = (global_processes.get(i)[0],
                                                       global_processes.get(i)[1] + 1)
                                flag += 1
                    else:
                        global_processes = elem.find_first_occurrence(global_processes, flag)
                else:
                    raise Exception

            else:
                for i in range(flag, len(global_processes)):
                    global_processes[i] = (global_processes.get(i)[0], -1)
                return global_processes

        for i in range(flag, len(global_processes)):
            global_processes[i] = (global_processes.get(i)[0], -1)
        return global_processes

    def remove_policy_and(self, all_processes: []):
        new_global_processes = []

        return new_global_processes

    def remove_policy_xor(self, all_processes: []) -> []:
        results = dict()
        for processes in all_processes:
            for i in range(len(processes)):
                if processes == -1:
                    if i > 0:
                        results[processes] = (processes.get(i)[1] + 1)/i
                    else:
                        results[processes] = 999

        new_all_processes = [k for k, v in results.items() if float(v) >= min(results, key=results.get)]

        return new_all_processes

    def continue_processing_xor(self, all_processes):
        new_global_processes = []

        return new_global_processes

    def traverse_and_gate(self, expression: str, goal_length: int) -> []:
        if self.traverse_inner() == goal_length:
            return list(permutations([1, 2, 3]))

    def traverse_inner(self) -> []:
        processes = []
        iterator = 0
        elements = self.elements.copy()

        while elements:
            elem = elements.pop(0)
            if isinstance(elem, str):
                processes.append(elem)
            else:
                processes.append(elem.traverse())
                iterator += 1

        return processes

    def get_model_minimal_length(self) -> int:
        if self.name == "and":
            length = sum(self.get_model_minimal_length_process_children())
        elif self.name == "xor":
            length = min(self.get_model_minimal_length_process_children())
        elif self.name == "seq":
            length = sum(self.get_model_minimal_length_process_children())
        elif self.name == "opt":
            length = 0
        elif self.name == "trm":
            length = 0
        elif self.name == "lop":
            length = 0
        else:
            raise Exception
        return length

    def get_model_minimal_length_process_children(self) -> []:
        lengths = []
        elements = self.elements.copy()

        while elements:
            elem = elements.pop(0)
            if isinstance(elem, str):
                lengths.append(1)
            else:
                lengths.append(elem.get_model_minimal_length())

        return lengths

    def traverse_process_children(self, expression: str) -> []:
        matches = []
        iterator = 0
        elements = self.elements.copy()

        while elements:
            if not expression:
                break
            else:
                elem = elements.pop(0)
                if isinstance(elem, str):
                    if expression[0] == elem:
                        if len(matches) <= iterator:
                            matches.append(1)
                            iterator += 1
                        else:
                            matches[iterator] += 1
                        expression = expression[1:]

                else:
                    matches.append(elem.traverse(expression, len(expression)))
                    iterator += 1

        return matches

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