from typing import Any, TypeVar, Type
from functools import wraps

T = TypeVar('T')

def singleton(cls: Type[T]) -> Type[T]:
    """
    Decorator to make a class a singleton.

    Usage:
        @singleton
        class MyClass:
            pass
    """
    instances = {}

    @wraps(cls)
    def get_instance(*args: Any, **kwargs: Any) -> T:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance