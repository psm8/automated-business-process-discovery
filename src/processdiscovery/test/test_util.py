from processdiscovery.event.event import Event


def string_to_events(string: str):
    event_group_events = []
    for x in string:
        event_group_events.append(Event(x))
    return event_group_events


def events_to_char_list(model_result: []):
    result = []
    for event in model_result:
        if event:
            result.append(event.name)
    return result
