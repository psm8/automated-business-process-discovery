def is_struct_empty(in_list) -> bool:
    if isinstance(in_list, list) or isinstance(in_list, tuple):
        return all(map(is_struct_empty, in_list))
    return False

def string_to_dictionary(string: str):
    dictionary = dict()
    i = 0
    for x in string:
        dictionary[i] = (x, -1)
        i += 1
    return dictionary

