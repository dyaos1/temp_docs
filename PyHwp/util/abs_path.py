import os

def abs_path(path: os.PathLike):
    return path if os.path.isabs(path) else os.path.abspath(path) 

