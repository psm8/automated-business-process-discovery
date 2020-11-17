from .process import Process
from .gate import Gate

class State:
    def __init__(self, process: Process, gate: Gate):
        self.process = process
        self.gate = gate
        #self.score
