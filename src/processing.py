from datetime import datetime


def filter_by_state(operations: list, state: str) -> list:
    """
    Фильтрует список словарей по значению ключа 'state'.
    """
    if not isinstance(operations, list):
        return []

    return [
        op for op in operations if isinstance(op, dict) and op.get("state") == state
    ]


def _parse_date(op) -> datetime | None:
    if not isinstance(op, dict):
        return None
    raw = op.get("date")
    if not isinstance(raw, str):
        return None
    if not raw:
        return datetime.max
    try:
        return datetime.strptime(raw, "%Y-%m-%d")
    except ValueError:
        return None


def sort_by_date(operations: list, reverse: bool = True) -> list:
    """
    Сортирует список словарей по полю 'date' (формат YYYY-MM-DD).
    reverse=True — по убыванию (новые сначала), False — по возрастанию.
    Невалидные даты помещаются в конец при reverse=True и в начало при reverse=False.
    """
    if not isinstance(operations, list):
        return []

    valid = []
    invalid = []

    for op in operations:
        dt = _parse_date(op)
        if dt is not None:
            valid.append((dt, op))
        else:
            invalid.append(op)

    valid.sort(key=lambda x: x[0], reverse=reverse)

    if reverse:
        return [op for _, op in valid] + invalid
    else:
        return invalid + [op for _, op in valid]
