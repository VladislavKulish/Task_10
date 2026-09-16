import logging
import re
from pathlib import Path
from typing import Any

# Настройка логгера
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

log_dir = Path(__file__).resolve().parent.parent / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "masks.log"

file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
file_handler.setFormatter(
    logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: Any) -> Any:
    """
    Маскирует номер банковской карты в формате XXXX XX** **** XXXX.

    Находит в строке последовательность из 13–19 цифр и маскирует её.
    Текст до и после номера сохраняется. Если входное значение — не строка
    или подходящая последовательность не найдена, возвращает его без изменений.

    :param card_number: строка с номером карты или произвольное значение.
    :return: замаскированная строка или исходное значение.
    """
    if not isinstance(card_number, str):
        return card_number

    logger.info(f"Маскирование номера карты: {card_number[:4]}...")

    match = re.search(r"(?<!\d)\d{13,19}(?!\d)", card_number)
    if not match:
        logger.warning("Подходящая последовательность цифр не найдена")
        return card_number

    number = match.group()
    masked = f"{number[:4]} {number[4:6]}** **** {number[-4:]}"
    result = card_number[: match.start()] + masked + card_number[match.end():]
    logger.debug(f"Результат маскирования: {result}")
    return result


def get_mask_account(account_number: Any) -> Any:
    """
    Маскирует номер счёта в формате **XXXX.

    Находит в строке последовательность ровно из 20 цифр и маскирует её.
    Текст до и после номера сохраняется. Если входное значение — не строка
    или подходящая последовательность не найдена, возвращает его без изменений.

    :param account_number: строка с номером счёта или произвольное значение.
    :return: замаскированная строка или исходное значение.
    """
    if not isinstance(account_number, str):
        return account_number

    logger.info(f"Маскирование номера счёта: {account_number[:2]}...")

    match = re.search(r"(?<!\d)\d{20}(?!\d)", account_number)
    if not match:
        logger.warning("Подходящая последовательность цифр не найдена")
        return account_number

    number = match.group()
    masked = f"**{number[-4:]}"
    result = account_number[: match.start()] + masked + account_number[match.end():]
    logger.debug(f"Результат маскирования: {result}")
    return result
