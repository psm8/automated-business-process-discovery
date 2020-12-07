from event.event import Event


def string_to_events(string: str):
    event_group_events = []
    for x in string:
        event_group_events.append(Event(x))
    return event_group_events