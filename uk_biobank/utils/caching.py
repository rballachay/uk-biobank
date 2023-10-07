import os
from functools import wraps
from pathlib import Path
import pickle


def cachewrapper(path: Path, use_cache: bool = True):
    """caching decorator to save intermediate dfs,
    makes repeated testing much faster
    """
    if isinstance(path, Path):
        path = str(path)

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if os.path.exists(path) and use_cache:
                with open(path, "rb") as obj:
                    data = pickle.load(obj)
            else:
                data = function(*args, **kwargs)
                with open(path, "wb") as obj:
                    pickle.dump(data, obj)
            return data

        return wrapper

    return decorator
