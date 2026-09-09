def my_decorator(func):  # my_decorator 1
    def wrapper(*args, **kwargs):
        print(f"Аргументы: {args}")
        result = func(*args, **kwargs)
        print(f"Результат: {result}")
        return result

    return wrapper


# Применяем декоратор к функциям
@my_decorator
def add(x, y):  # add 2
    return x + y


@my_decorator
def multiply(x, y):  # multiply 2
    return x * y


@my_decorator
def subtract(x, y):  # subtract 2
    return x - y


# Вызов функций
add(3, 5)
multiply(2, 4)
subtract(10, 6)