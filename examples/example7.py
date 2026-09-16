import time
from functools import reduce

# --- @memoize ---
def memoize(func):
    cache = {}

    def wrapper(*args, **kwargs):
        # Для хеширования превращаем kwargs в отсортированный кортеж пар (ключ, значение)
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper


# --- @slowit(n) ---
def slowit(n=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            time.sleep(n)
            return func(*args, **kwargs)
        return wrapper
    return decorator


# --- @timeit ---
def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"Function {func.__name__} took {end - start:.6f} seconds")
        return result
    return wrapper


# --- Примеры использования ---

@timeit
@slowit(2)
def product_no_cache(n):
    return reduce(lambda x, y: x * y, range(1, n + 1)) if n > 0 else None

print("Без кеширования:")
product_no_cache(10)
product_no_cache(10)  # Каждый раз будет задержка 2 секунды + вычисление


@timeit
@memoize
@slowit(2)
def product_with_cache(n):
    return reduce(lambda x, y: x * y, range(1, n + 1)) if n > 0 else None

print("\nС кешированием:")
product_with_cache(10)  # Задержка 2 секунды + вычисление
product_with_cache(10)  # Почти мгновенно (результат из кеша, без sleep)