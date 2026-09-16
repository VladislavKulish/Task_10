# Пример 1

# Обьявление
def add(a, b):
    """Просто складывает два числа и возвращает результат."""
    result = a + b
    return result


# Вызов
sum = add(10, 5)
print(sum)


# Пример 2

def greeting_maker(greeting):
    """Внешняя функция, которая создает приветствия."""

    def inner(name):
        """Внутренняя функция, которая использует переменную из внешней."""
        return f"{greeting}, {name}!"

    return inner  # Возвращаем саму внутреннюю функцию, а не ее результат!


# Создаем разные "фабрики" приветствий
say_hello = greeting_maker("Привет")
say_hi = greeting_maker("Hi")

# Используем их
print(say_hello("Анна"))  # Выведет: Привет, Анна!
print(say_hi("Alex"))  # Выведет: Hi, Alex!


# Функция сложения
def add(x, y):
    return x + y


# Функция умножения
def multiply(x, y):
    return x * y


# Функция вычитания
def subtract(x, y):
    return x - y


# Логирование для функции add
def log_add(x, y):
    print(f"Аргументы: ({x}, {y})")
    result = add(x, y)
    print(f"Результат: {result}")
    return result


# Логирование для функции multiply
def log_multiply(x, y):
    print(f"Аргументы: ({x}, {y})")
    result = multiply(x, y)
    print(f"Результат: {result}")
    return result


# Логирование для функции subtract
def log_subtract(x, y):
    print(f"Аргументы: ({x}, {y})")
    result = subtract(x, y)
    print(f"Результат: {result}")
    return result


# Вызов функций с логированием
log_add(3, 5)
log_multiply(2, 4)
log_subtract(10, 6)
