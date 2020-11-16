class Process:

    def __init__(self, expression: str, elements=[]):
        self.name = expression[0:3]
        self.elements = elements