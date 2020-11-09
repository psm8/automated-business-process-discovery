from gate.gate import Gate


class BaseGate(Gate):
    def __init__(self):
        self.name = "base"
        self.elements = []
