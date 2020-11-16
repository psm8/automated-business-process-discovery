import math

from gate.gate import Gate


class BaseGate(Gate):
    def __init__(self):
        self.name = "base"
        self.elements = []

    def traverse(self, expression: str) -> int:
        worst_allowed_alignment = self.get_worst_allowed_alignment(expression)
        cumulative_error = 0
        matches = []
        self.traverse_process_children(expression)

        return 0

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
                    matches.append(elem.traverse(expression))
                    iterator += 1

        return matches

    def get_model_minimal_length(self) -> int:
        return sum(self.get_model_minimal_length_process_children())

    def get_worst_allowed_alignment(self, expression):
        return math.ceil(len(expression) / 2)

