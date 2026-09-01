def mask_card_number(card_number: str) -> str:
    """Маскирует номер карты: первые 4 цифры, 2 цифры, ****, последние 4 цифры."""
    if len(card_number) < 16:
        return card_number
    first_part = card_number[:4]
    middle_part = card_number[4:6]
    last_part = card_number[-4:]
    return f"{first_part} {middle_part}** **** {last_part}"


def mask_account_number(account_number: str) -> str:
    """Маскирует номер счёта: ** + последние 4 цифры."""
    if len(account_number) < 4:
        return account_number
    last_four = account_number[-4:]
    return f"**{last_four}"


def mask_account_card(info: str) -> str:
    """
    Обрабатывает строку с типом и номером (карты или счёта) без использования re.
    Добавляет защиту от некорректного ввода:
      - пустой ввод
      - отсутствие цифр
      - слишком много «частей» (более 2 смысловых подстрок: префикс + номер)
    """
    # Проверка на пустой ввод или только пробелы
    if not info or not info.strip():
        raise ValueError("Ввод пуст или содержит только пробелы.")

    info = info.strip()

    # Находим начало числовой части, двигаясь с конца
    i = len(info) - 1
    while i >= 0 and info[i].isdigit():
        i -= 1

    number_start = i + 1

    # Если цифр нет вообще
    if number_start >= len(info):
        raise ValueError("В строке не найден номер (отсутствуют цифры).")

    prefix = info[:number_start].strip()
    number = info[number_start:]

    # Проверяем, что номер состоит только из цифр
    if not number.isdigit():
        raise ValueError("Номер должен состоять только из цифр.")

    # Защита от «слишком многих подстрок»: считаем количество слов в префиксе.
    # Ожидаем ровно 1 смысловую часть (например, «Счет» или «Visa Platinum» — считаем как 1 логический тип).
    # Но если в префиксе больше 3 слов — считаем это подозрительным и отклоняем.
    prefix_words = prefix.split()
    if len(prefix_words) == 0:
        raise ValueError("Не указан тип (карта/счёт).")
    if len(prefix_words) > 3:
        # Например, «Visa Platinum Extra Bonus» — уже подозрительно; можно ослабить порог при необходимости.
        raise ValueError(
            "Слишком много слов в описании типа. Ожидается краткий тип (например, 'Visa Platinum' или 'Счет').")

    if prefix.lower().startswith("счет"):
        masked_number = mask_account_number(number)
        return f"{prefix} {masked_number}"
    else:
        masked_number = mask_card_number(number)
        return f"{prefix} {masked_number}"


def get_date(date_str: str) -> str:
    """
    Преобразует строку даты из формата 'YYYY-MM-DDTHH:MM:SS.ffffff' в 'ДД.ММ.ГГГГ'.
    Добавляет валидацию на корректный формат и наличие частей.
    """
    if not date_str or not date_str.strip():
        raise ValueError("Ввод пуст или содержит только пробелы.")

    date_str = date_str.strip()

    # Ищем разделитель 'T'
    t_index = date_str.find('T')
    if t_index == -1:
        raise ValueError("Формат даты неверен: отсутствует символ 'T' между датой и временем.")

    date_part = date_str[:t_index]
    # После T должно быть хотя бы что-то (время), но для формата даты это не критично
    # time_part = date_str[t_index+1:]  # можно использовать для дальнейшей валидации

    parts = date_part.split('-')
    if len(parts) != 3:
        raise ValueError("Дата должна быть в формате YYYY-MM-DD (ровно 3 части через дефис).")

    year, month, day = parts

    # Простая проверка, что все части — числа и нужной длины
    if not (year.isdigit() and month.isdigit() and day.isdigit()):
        raise ValueError("Год, месяц и день должны состоять только из цифр.")
    if not (len(year) == 4 and len(month) == 2 and len(day) == 2):
        raise ValueError("Год должен быть 4 символа, месяц и день — по 2 символа.")

    return f"{day}.{month}.{year}"


def process_data(input_value: str, mode: str) -> str:
    """
    Единый интерфейс для выбора нужной операции с валидацией режима.

    Параметры:
      - input_value: входная строка (номер карты/счёта либо дата)
      - mode: тип операции:
          * "mask" — маскировка номера карты/счёта
          * "date" — форматирование даты

    Возвращает обработанную строку.
    """
    if mode == "mask":
        return mask_account_card(input_value)
    elif mode == "date":
        return get_date(input_value)
    else:
        raise ValueError("Неверный режим. Допустимые значения: 'mask', 'date'.")


'''
# --- Примеры проверки ---
test_masks = [
    "Maestro 1596837868705199",
    "Счет 64686473678894779589",
    "MasterCard 7158300734726758",
    "Счет 35383033474447895560",
    "Visa Classic 6831982476737658",
    "Visa Platinum 8990922113665229",
    "Visa Gold 5999414228426353",
    "Счет 73654108430135874305",
]

test_dates = [
    "2024-03-11T02:26:18.671407",
    "2023-12-05T14:30:00.123456",
    "2000-01-01T00:00:00.000000",
]

# Примеры некорректных вводов для демонстрации защиты
bad_inputs = [
    "",  # пустой ввод
    "   ",  # только пробелы
    "Visa",  # нет номера
    "Счет",  # нет номера счёта
    "Visa 123",  # номер слишком короткий
    "Visa Platinum Extra 1234567812345678",  # слишком много слов в префиксе
    "2024-03T02:26:18",  # неверная дата (нет дня)
    "2024/03/11T02:26:18",  # неверный формат даты (не дефисы)
]

print("--- Маскировка карт и счетов ---")
for t in test_masks:
    try:
        print(f"{t} → {process_data(t, 'mask')}")
    except ValueError as e:
        print(f"{t} → Ошибка: {e}")

print("\n--- Форматирование дат ---")
for t in test_dates:
    try:
        print(f"{t} → {process_data(t, 'date')}")
    except ValueError as e:
        print(f"{t} → Ошибка: {e}")

print("\n--- Некорректные вводы (проверка защиты) ---")
for t in bad_inputs:
    for mode in ["mask", "date"]:
        try:
            print(f"[{mode}] {repr(t)} → {process_data(t, mode)}")
        except ValueError as e:
            print(f"[{mode}] {repr(t)} → Ошибка: {e}")
'''
