from processdiscovery.event.event import Event


def add_executions(model_events_list: [Event], events: [Event], n: int):
    for model_event in model_events_list:
        if model_event in events:
            model_event.no_visits += n
