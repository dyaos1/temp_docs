import os

def abs_path(path: os.PathLike):
    return path if os.path.isabs(path) else os.path.abspath(path) 

def capitalize_first_letter(string: str):
    string = string.lower()
    
    return string[0].upper() + string[1:]

def none_check(value, default):
    if value is None:
        return default
    return value