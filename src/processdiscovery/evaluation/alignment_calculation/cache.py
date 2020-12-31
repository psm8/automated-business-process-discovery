from functools import wraps


def cached(f):
    @wraps(f)
    def wrapped(model, log, alignment_cache):
        cache_id = get_cache_id(model, log)
        if cache_id in alignment_cache:
            return alignment_cache[cache_id]
        result_x, model_results = f(model, log, alignment_cache)
        alignment_cache[cache_id] = result_x, model_results

        return result_x, model_results
    return wrapped


def get_cache_id(model, log):
    model = tuple(tuple(hash(y) for y in x) if isinstance(x, list) else hash(x) for x in model)
    return model, tuple(log)


# def get_cache(model_results):
#     return [[y.name if y is not None else None for y in x] for x in model_results]
#
#
# def map_cache_to_events(cache, events):
#     events_local = []
#     [events_local + x if isinstance(x, list) else events_local.append(x) for x in events]
#     flat_events = list(get_events(events_local))
#
#     cache_results = cache[1]
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
