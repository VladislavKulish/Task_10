def get_mask_card_number(card_number: str) -> str:
    """Функциz маскировки номера банковской карты"""
    # Удаляем все пробелы из входного номера
    clean_number = card_number.replace(" ", "")

    # Проверяем, достаточно ли цифр в номере
    if len(clean_number) < 4:
        return clean_number  # Возвращаем исходную строку, если цифр мало

    # Формируем маску: первые 6 цифр, затем 2 звезды, затем последние 4 цифры
    masked_number = clean_number[:6] + "******" + clean_number[-4:]

    # Разбиваем результат на блоки по 4 символа с пробелами
    return " ".join(masked_number[i: i + 4] for i in range(0, len(masked_number),))


def get_mask_account(account_number: int) -> str:
    """Функцию маскировки номера банковского счета"""
    # Преобразуем аргумент в строку, чтобы работать с ней как с последовательностью символов
    account_str = str(account_number)
    # Возвращаем строку с двумя звёздочками, за которыми следуют последние 4 цифры
    return "**" + account_str[-4:]
