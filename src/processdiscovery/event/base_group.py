from processdiscovery.event.comparable_event import ComparableEvent


class BaseGroup(ComparableEvent):

    def __init__(self, events=None):
        if events is None:
            events = []
        self.events = events

    def __len__(self):
        return sum(len(x) for x in self.events)

    def add_event(self, event):
        self.events.append(event)
        return self

    def add_events(self, event1, event2):
        self.events.append(event1)
        self.events.append(event2)
        return self

    def add_event_event_group(self, event, event_group):
        self.events.append(event)
        for event_local in event_group:
            self.events.append(event_local)
        return self

    def compare(self, other):
        pass

    def get_event_names_hash(self):
        pass
