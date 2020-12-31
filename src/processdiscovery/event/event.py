from processdiscovery.event.comparable_event import ComparableEvent


class Event(ComparableEvent):

    def __init__(self, name: str):
        self.name = name
        self.no_branches = 0
        self.no_visits = 0

    def __len__(self):
        return 1

    def __hash__(self):
        return hash(id(self.name))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return id(self) == id(other)

    def compare(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.name == other.name
