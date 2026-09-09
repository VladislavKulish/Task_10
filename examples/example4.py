def positive_integers(func):
    def wrapper(*args, **kwargs):
        # Проверяем позиционные аргументы
        for arg in args:
            # Исключаем bool (т.к. bool — подкласс int в Python)
            if isinstance(arg, bool) or not isinstance(arg, int) or arg <= 0:
                raise ValueError("All arguments must be positive integers")

        # Проверяем именованные аргументы
        for value in kwargs.values():
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError("All arguments must be positive integers")

        return func(*args, **kwargs)

    return wrapper

@positive_integers
def multiply(*args):
    result = 1
    for arg in args:
        result *= arg
    return result

multiply(2, 3, 4) # Вывод: 24
multiply(2, 0, 4) # Выбрасывает исключение ValueError с сообщением "All arguments must be positive integers"