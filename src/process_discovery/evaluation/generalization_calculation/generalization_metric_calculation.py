from process_discovery.event.event import Event

import math


def calculate_generalization_metric(model_events_list: [Event]):
    return 1 - sum([math.pow(math.sqrt(model_event.no_visits if model_event.event_lop_twin is None
                                       else model_event.no_visits + model_event.event_lop_twin.no_visits), -1)
                    if model_event.no_visits != 0 else 1 for model_event in model_events_list]) / \
           len(model_events_list)


def add_executions(model_events_list: [Event], events: [Event], n: int):
    for model_event in model_events_list:
        if model_event in events:
            model_event.no_visits += n
