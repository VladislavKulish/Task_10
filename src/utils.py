import json
import logging
from pathlib import Path
from typing import Any, Dict, List

# Настройка логгера для модуля utils
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

# Путь к файлу логов
log_dir = Path(__file__).resolve().parent.parent / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "utils.log"

# FileHandler с режимом 'w' — перезапись при каждом запуске
file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
file_handler.setFormatter(
    logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
)
logger.addHandler(file_handler)


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает список транзакций из JSON-файла.

    Возвращает пустой список, если файл не найден, пустой,
    содержит невалидный JSON или корневой элемент — не список.

    :param file_path: путь к JSON-файлу.
    :return: список словарей с транзакциями.
    """
    logger.info(f"Запрос на загрузку транзакций из файла: {file_path}")
    path = Path(file_path)

    if not path.exists():
        logger.warning(f"Файл не найден: {file_path}")
        return []

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"Файл {file_path} успешно загружен")
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        logger.error(f"Ошибка чтения файла {file_path}: {exc}")
        return []

    if not isinstance(data, list):
        logger.warning(f"Корневой элемент в {file_path} — не список")
        return []

    logger.info(f"Загружено транзакций: {len(data)}")
    return data
