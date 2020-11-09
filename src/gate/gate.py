from itertools import islice
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
                if expression[i:i+3] == "and" or expression[i:i+3] == "ior" or expression[i:i+3] == "xor":
                    gate = Gate(expression)
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

    def traverse(self, expression: str) -> int:
        matches = 0
        elements = self.elements.copy()

        #python way to check empty
        if self.name == "trm":
            return matches
        elif self.name == "and":
            return matches
        elif self.name == "xor":
            return matches
        elif self.name == "ior":
            return matches
        else:
            while elements:
                if not expression:
                    break
                else:
                    elem = elements.pop(0)
                    if isinstance(elem, str):
                        if expression[0] == elem:
                            matches += 1
                            expression = expression[1:]
                    else:
                        return matches

        return matches


