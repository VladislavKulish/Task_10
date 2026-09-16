def logging(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"Function {func.__name__} called with args: {args} and kwargs: {kwargs}. Result: {result}")
        return result

    # Сохраняем имя и документацию оригинальной функции
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__

    return wrapper

@logging
def multiply(x, y):
    return x * y

multiply(2, 3)
# Вывод: Function multiply called with args: (2, 3) and kwargs: {}. Result: 6

@logging
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Alice")
# Вывод: Function greet called with args: ('Alice',) and kwargs: {}. Result: Hello, Alice!

greet("Bob", greeting="Hi")
# Вывод: Function greet called with args: ('Bob',) and kwargs: {'greeting': 'Hi'}. Result: Hi, Bob!