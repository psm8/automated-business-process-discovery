class Gate:

    def __init__(self, name: str):
        self.name = name
        self.gates = []
        self.processes = []

    def add_gate(self, gate: Gate):
        self.gates.extend(gate)

    def parse(self, expression: str):

        expression_local = ""
        for i in len(expression):
            if expression(i) == "(":
                break
            elif expression(i) == ")":
                gate = Gate(expression[i:i+3])

                expression = expression[i+3:]
                i += 3
                gate.parse(expression)
            elif expression(i) == ",":
                break
            else:
                self.processes.extend(expression(i))

    def add_process(self, process: str):
        self.processes.extend(process)

