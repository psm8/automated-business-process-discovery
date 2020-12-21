from processdiscovery.event.event_group import EventGroup
from processdiscovery.event.event_group_parallel import EventGroupParallel


class Event:

    def __init__(self, name: str):
        self.name = name
        self.no_branches = 0
        self.no_visits = 0

    def __len__(self):
        return len(self.name)

    def add_event(self, event):
        event_group = EventGroup()
        if isinstance(event, EventGroup):
            return event_group.add_event_event_group(self, event)
        else:
            return event_group.add_events(self, event)

    def add_event_parallel(self, event):
        event_group_parallel = EventGroupParallel()
        return event_group_parallel.add_events(self, event)
