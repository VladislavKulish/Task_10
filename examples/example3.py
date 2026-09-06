# Пример 1. Подсчет времени выполнения функции
import time


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)  # вызываем исходную функцию
        end = time.time()
        print(f"Функция {func.__name__} выполнилась за {end - start:.2f} сек")
        return result

    return wrapper


@timer
def long_calculation():
    time.sleep(2)  # искусственная задержка


long_calculation()  # Вывод: "Функция long_calculation выполнилась за 2.00 сек"


# Пример 2. Кэширование
def cache(func):
    saved_results = {}  # хранилище результатов

    def wrapper(*args):
        if args in saved_results:
            print("Беру результат из кэша!")
            return saved_results[args]
        result = func(*args)
        saved_results[args] = result
        return result

    return wrapper


@cache
def factorial(n):
    return 1 if n == 0 else n * factorial(n - 1)


print(factorial(5))  # Считает впервые
print(factorial(5))  # Вывод: "Беру результат из кэша!" и возвращает 120


# Пример 3. Права доступа
def check_permission(required_role):
    def decorator(func):
        def wrapper(user_role, *args, **kwargs):
            if user_role != required_role:
                raise PermissionError("Доступ запрещен!")
            return func(*args, **kwargs)

        return wrapper

    return decorator


@check_permission(required_role="admin")
def delete_database():
    print("База данных удалена!")


delete_database(user_role="admin")  # Работает
delete_database(user_role="user")  # Ошибка: PermissionError