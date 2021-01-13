from process_discovery.event.event import Event
from process_discovery.event.base_group import BaseGroup
from algorithm.parameters import params


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


def get_event_names(event_group: BaseGroup):
    result = []
    for x in event_group.events:
        if isinstance(x, Event):
            result.append(x.name)
        else:
            result.append(get_event_names(x))

    return result


def get_event_names2(event_group: BaseGroup):
    result = []
    for x in event_group.events:
        if isinstance(x, Event):
            result.append(x.name)
        else:
            [result.append(y) for y in get_event_names2(x)]

    return result

def set_params():
    params['RESULT_TOLERANCE_PERCENT'] = 5
    params['WEIGHT_ALIGNMENT'] = 12
    params['WEIGHT_COMPLEXITY'] = 4
    params['WEIGHT_GENERALIZATION'] = 4
    params['WEIGHT_PRECISION'] = 1
    params['WEIGHT_SIMPLICITY'] = 4
    params['MINIMIZE_SOLUTION_LENGTH'] = True