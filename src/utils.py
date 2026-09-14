import json
from pathlib import Path
from typing import Any, Dict, List


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает список транзакций из JSON-файла.

    Возвращает пустой список, если:
      - файл не найден;
      - файл пустой или содержит невалидный JSON;
      - корневой элемент JSON — не список.

    :param file_path: путь к JSON-файлу.
    :return: список словарей с транзакциями.
    """
    path = Path(file_path)

    # Если файла нет — возвращаем пустой список
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError):
        # Невалидный JSON или проблема с кодировкой
        return []

    # Проверяем, что загруженные данные — это список
    if not isinstance(data, list):
        return []

    # Дополнительно: можно проверить, что все элементы — словари,
    # но по ТЗ достаточно вернуть список «как есть», если корень — список.
    return data
