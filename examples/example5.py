def is_palindrome(func):
    def wrapper(string, *args, **kwargs):
        # Проверка, что первый позиционный аргумент — строка
        if not isinstance(string, str):
            raise ValueError("Argument must be a palindrome")

        # Нормализуем для проверки: приводим к нижнему регистру и убираем пробелы (опционально)
        # Если нужна строгая проверка (с учётом регистра и пробелов), используй: normalized = string
        normalized = string.lower().replace(" ", "")

        if normalized != normalized[::-1]:
            raise ValueError("Argument must be a palindrome")

        return func(string, *args, **kwargs)

    # Сохраняем имя и документацию оригинальной функции
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__

    return wrapper

@is_palindrome
def reverse_string(string: str) -> str:
    """Возвращает перевёрнутую строку (аргумент гарантированно палиндром)."""
    return string[::-1]

print(reverse_string('racecar'))      # 'racecar'
print(reverse_string('Racecar'))      # 'racecaR' (функция работает с оригиналом, проверка — с нормализованной версией)
print(reverse_string('A man a plan a canal Panama'))  # 'amanaP lanac a nalp a nam A'

# reverse_string('hello')             # ValueError: Argument must be a palindrome