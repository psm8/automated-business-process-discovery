from processdiscovery.event.event import Event


def add_executions(model_events_list: [Event], events: [Event], n: int):
    for event in events:
        for model_event in model_events_list:
            if event == model_event:
                model_event.no_visits += n


def reset_executions(model_events_list: [Event]):
    for model_event in model_events_list:
        model_event.no_visits = 0
