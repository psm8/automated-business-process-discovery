def calculate_simplicity_metric(model_events_list, log_unique_events):
    lop_allowed_duplicates = sum(x.event_lop_twin is not None for x in model_events_list)
    model_unique_events = set()
    [model_unique_events.add(x.name) for x in model_events_list]
    return 1 - (((len(model_events_list) - len(model_unique_events) - lop_allowed_duplicates) +
                 (len(log_unique_events) - len(model_unique_events))) /
                (len(model_events_list) - lop_allowed_duplicates + len(log_unique_events)))
