from datetime import datetime

from masks import get_mask_account, get_mask_card_number


def mask_card_number(card_str: str) -> str:
    """Публичная обёртка над get_mask_card_number."""
    return get_mask_card_number(card_str)


def mask_account_number(account_str: str) -> str:
    """Публичная обёртка над get_mask_account."""
    return get_mask_account(account_str)


def mask_account_card(input_str: str) -> str:
    """Распознаёт тип номера (карта или счёт) и применяет нужную маску."""
    if not isinstance(input_str, str) or not input_str:
        return input_str

    i = 0
    n = len(input_str)
    while i < n:
        if not input_str[i].isdigit():
            i += 1
            continue
        start = i
        while i < n and input_str[i].isdigit():
            i += 1
        end = i
        digits = input_str[start:end]
        length = len(digits)

        if length == 20:
            return input_str[:start] + f"**{digits[-4:]}" + input_str[end:]
        if 13 <= length <= 19:
            masked = get_mask_card_number(digits)
            return input_str[:start] + masked + input_str[end:]

    return input_str


def get_date(input_str: str) -> str:
    """Извлекает дату из строки и возвращает её в формате ДД.ММ.ГГГГ."""
    if not isinstance(input_str, str):
        return input_str

    s = input_str
    n = len(s)

    # Поиск шаблона YYYY-MM-DD
    for i in range(max(0, n - 9)):
        if (
            i + 10 <= n and s[i + 4] == "-" and s[i + 7] == "-" and s[i: i + 4].isdigit() and s[i + 5: i + 7].isdigit() and s[i + 8: i + 10].isdigit()
        ):
            try:
                date_str = s[i: i + 10]
                dt = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                continue

            end = i + 10
            # Если после даты есть T или пробел — поглощаем временную часть
            if end < n and s[end] in ("T", " "):
                j = end + 1
                # Поглощаем только если следующий символ — цифра
                if j < n and s[j].isdigit():
                    while j < n and (s[j].isdigit() or s[j] in (":", ".")):
                        j += 1
                    end = j

            return s[:i] + dt.strftime("%d.%m.%Y") + s[end:]

    # Пробуем другие форматы фиксированной длины
    for start in range(n):
        for p in ["%Y/%m/%d", "%d.%m.%Y"]:
            if start + 10 > n:
                break
            candidate = s[start: start + 10]
            try:
                dt = datetime.strptime(candidate, p)
                return s[:start] + dt.strftime("%d.%m.%Y") + s[start + 10:]
            except ValueError:
                continue

    return input_str


def process_data(operation: dict) -> str:
    """Формирует человекочитаемое описание банковской операции."""
    if not isinstance(operation, dict):
        return ""

    date_raw = operation.get("date", "")
    date_formatted = get_date(date_raw) if date_raw else ""

    description = operation.get("description", "")

    from_field = operation.get("from", "")
    to_field = operation.get("to", "")

    from_masked = mask_account_card(from_field) if from_field else ""
    to_masked = mask_account_card(to_field) if to_field else ""

    amount_str = ""
    currency_name = ""

    operation_amount = operation.get("operationAmount")
    if isinstance(operation_amount, dict):
        amount_str = str(operation_amount.get("amount", ""))
        currency = operation_amount.get("currency")
        # Берём name только если currency — словарь
        if isinstance(currency, dict):
            currency_name = currency.get("name", "")
        else:
            currency_name = ""

    parts = []
    if date_formatted:
        parts.append(f"{date_formatted} {description}")
    else:
        parts.append(description)

    if from_masked and to_masked:
        parts.append(f"{from_masked} -> {to_masked}")
    elif from_masked:
        parts.append(from_masked)
    elif to_masked:
        parts.append(to_masked)

    if amount_str:
        if currency_name:
            parts.append(f"{amount_str} {currency_name}")
        else:
            parts.append(amount_str)

    return "\n".join(parts)
