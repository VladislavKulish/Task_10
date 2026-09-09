from widget import mask_account_card


def filter_by_currency(transactions, currency):
    """
    Возвращает итератор по транзакциям с указанной валютой (без учёта регистра).

    :param transactions: список словарей с транзакциями
    :param currency: строка с названием валюты, например 'USD' (регистр не важен)
    :return: итератор (generator)
    """
    currency_lower = currency.lower()

    for transaction in transactions:
        curr = transaction.get("operationAmount", {}).get("currency", {}).get("name")
        if curr and curr.lower() == currency_lower:
            yield transaction


"""
- Итератор, а не список. Функция использует yield, поэтому возвращает генератор — это экономит память на больших списках, что хорошо сочетается с твоими предыдущими задачами (фильтрация, сортировка).
- Безопасный доступ. Используется цепочка .get(...), чтобы не падать, если какого‑то ключа нет.
- Структура данных. Код ориентирован на ту структуру транзакций, которую ты уже использовал (с operationAmount → currency → name). Если у тебя валюта хранится иначе (например, просто "currency": "USD"), скажи — подстрою функцию под нужный формат.
"""


def transaction_descriptions(transactions):
    """
    Генератор, который по очереди возвращает описание каждой транзакции.

    Формат описания:
      "[Дата] [Описание] | [Отправитель] -> [Получатель] | [Сумма] [Валюта]"

    Если какого-то поля нет — оно просто не включается.

    :param transactions: список словарей с транзакциями
    :return: генератор строк-описаний
    """
    for t in transactions:
        parts = []

        # Дата
        date_raw = t.get("date", "")
        if date_raw:
            # Тут можно вставить твой get_date, если он уже есть
            # date_formatted = get_date(date_raw)
            date_formatted = date_raw[:10]  # простой вариант: YYYY-MM-DD
            parts.append(date_formatted)

        # Описание
        description = t.get("description", "")
        if description:
            parts.append(description)

        # Отправитель и получатель (с маскировкой, как в прошлых задачах)
        from_field = t.get("from", "")
        to_field = t.get("to", "")

        from_masked = mask_account_card(from_field) if from_field else ""
        to_masked = mask_account_card(to_field) if to_field else ""

        if from_masked and to_masked:
            parts.append(f"{from_masked} -> {to_masked}")
        elif from_masked:
            parts.append(from_masked)
        elif to_masked:
            parts.append(to_masked)

        # Сумма и валюта
        amount_str = ""
        currency_name = ""

        op = t.get("operationAmount")
        if isinstance(op, dict):
            amount_val = op.get("amount")
            if amount_val is not None:
                amount_str = str(amount_val)

            curr = op.get("currency")
            if isinstance(curr, dict):
                currency_name = curr.get("name", "")

        if amount_str:
            if currency_name:
                parts.append(f"{amount_str} {currency_name}")
            else:
                parts.append(amount_str)

        yield " | ".join(parts) if parts else "(транзакция без данных)"


"""
- Генератор (yield) — экономит память и хорошо сочетается с твоими предыдущими задачами (фильтрация, сортировка).
- Безопасный доступ через .get() — не упадёт, если какого-то ключа нет.
- Маскировка — использует ту же mask_account_card, что и в process_data.
- Гибкость формата: если хочешь другой разделитель или порядок полей — легко поменять строку с " | ".join(parts).
"""


def card_number_generator(start: int, end: int):
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

    Raises:
        ValueError: если start или end вне диапазона [1, 9_999_999_999_999_999],
                    или если start > end.
    """
    max_value = 9_999_999_999_999_999

    if not (1 <= start <= max_value):
        raise ValueError("start must be between 1 and 9_999_999_999_999_999")
    if not (1 <= end <= max_value):
        raise ValueError("end must be between 1 and 9_999_999_999_999_999")
    if start > end:
        raise ValueError("start must not be greater than end")

    for number in range(start, end + 1):
        num_str = f"{number:016d}"
        yield f"{num_str[:4]} {num_str[4:8]} {num_str[8:12]} {num_str[12:]}"


"""
    Эти номера не являются валидными платёжными картами: у них нет корректной контрольной цифры по алгоритму Луна, и они не привязаны к реальным банкам. Генератор подходит только для:
    тестов (как в твоих предыдущих задачах с фильтрацией транзакций), демонстрации формата, заглушек в данных.
    Не используй такие номера в продакшене или для реальных платежей.
"""
