from processdiscovery.event.event import Event


def add_executions(model_events_list: [Event], events: [Event], n: int):
    for model_event in model_events_list:
        if model_event in events:
            model_event.no_visits += n
        # else:


def reset_executions(model_events_list: [Event]):
    for model_event in model_events_list:
        model_event.no_visits = 0


# def fix_event_from_cache(model_event, events):
#     # problem how to differentiate 2 events same names
#     result = []
#     for x in cache_results[-1]:
#         if x is None:
#             result.append(None)
#         else:
#             for event in flat_events:
#                 if x.name == event.name:
#                     result.append(event)
#                     flat_events.remove(event)
#                     break
#
#     mapped = cache_results[:-1]
#     mapped.append(result)
#     return cache[0], mapped
