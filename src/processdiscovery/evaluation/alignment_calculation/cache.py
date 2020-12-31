from functools import wraps


def cached(f):
    @wraps(f)
    def wrapped(model, log, alignment_cache, calculate_alignment_method):
        cache_id = get_cache_id(model, log)
        if cache_id in alignment_cache:
            return alignment_cache[cache_id]
        result_x, model_results = f(model, log, alignment_cache, calculate_alignment_method)
        alignment_cache[cache_id] = result_x, model_results

        return result_x, model_results
    return wrapped


def get_cache_id(model, log):
    model = tuple(tuple(hash(y) for y in x) if isinstance(x, list) else hash(x) for x in model)
    return model, tuple(log)
