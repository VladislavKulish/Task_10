import functools
import os
from typing import Callable, Optional, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def log(filename: Optional[str] = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Декоратор для логирования выполнения функций.

    :param filename: имя файла для записи логов. Если None — вывод в консоль.
    :return: обёрнутую функцию.
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok\n"
                _write_log(filename, message)
                return result
            except Exception as e:
                message = f"{func.__name__} error: {e}. Inputs: {args}, {kwargs}\n"
                _write_log(filename, message)
                raise

        return wrapper

    return decorator


def _write_log(filename: Optional[str], message: str) -> None:
    """Записывает лог-сообщение в файл или в консоль."""
    if filename is None:
        print(message, end="")
    else:
        os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
        with open(filename, "a", encoding="utf-8") as f:
            f.write(message)
