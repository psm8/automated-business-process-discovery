from process_discovery.event.comparable_event import ComparableEvent

from functools import cached_property


class Event(ComparableEvent):

    def __init__(self, name: str):
        self.name = name
        self.no_visits = 0
        self.event_lop_twin = None
        self.min_start = -1
        self.max_start = -1
        self.min_end = -1
        self.max_end = -1

    @cached_property
    def model_min_length(self) -> int:
        return 1

    @cached_property
    def model_max_length(self) -> int:
        return 1

    def __len__(self):
        return 1

    def __hash__(self):
        hsh = ''
        for x in self.name:
            hsh += str(ord(x))
        return int(hsh)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return id(self) == id(other)

    def compare(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.name == other.name
