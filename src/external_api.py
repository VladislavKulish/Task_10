import os
from typing import Any
from typing import Union

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY", "")
API_URL = "https://api.apilayer.com/exchangerates_data/convert"


def convert_to_rub(transaction: dict[str, Any]) -> float:
    """
    Принимает транзакцию и возвращает сумму в рублях.

    Если валюта транзакции — USD или EUR, обращается к внешнему API
    для получения текущего курса и конвертации. Для RUB возвращает
    сумму без изменений.

    :param transaction: словарь с данными о транзакции.
    :return: сумма транзакции в рублях (float).
    """
    operation = transaction.get("operationAmount", {})
    amount = operation.get("amount", 0)
    currency = operation.get("currency", {}).get("name", "RUB")

    if currency == "RUB":
        return float(amount)

    if currency in ("USD", "EUR"):
        rate = _fetch_exchange_rate(currency, "RUB")
        if rate is not None:
            return float(amount) * rate

    # Если API недоступен или валюта не поддерживается — возвращаем 0.0
    return 0.0


def _fetch_exchange_rate(from_currency: str, to_currency: str) -> float | None:
    """
    Запрашивает курс валют через Exchange Rates Data API.

    :param from_currency: исходная валюта (например, 'USD').
    :param to_currency: целевая валюта (например, 'RUB').
    :return: курс как float или None при ошибке.
    """
    if not API_KEY:
        return None

    params: dict[str, Union[str, int]] = {
        "from": from_currency,
        "to": to_currency,
        "amount": 1,
    }
    try:
        response = requests.get(
            API_URL,
            headers={"apikey": API_KEY},
            params=params,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        if data.get("success"):
            return float(data["result"])
    except Exception:  # <-- ловим всё подряд, включая обычный Exception
        return None

    return None
