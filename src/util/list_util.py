def is_struct_empty(in_list) -> bool:
    if isinstance(in_list, list) or isinstance(in_list, tuple):
        return all(map(is_struct_empty, in_list))
    return False
