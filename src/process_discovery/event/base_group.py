from process_discovery.event.comparable_event import ComparableEvent


class BaseGroup(ComparableEvent):

    def __init__(self, events=None):
        if events is None:
            events = []
        self.events = events

    def __len__(self):
        return sum(len(x) for x in self.events)

    def compare(self, other):
        pass

    def to_bytes(self):
        pass
