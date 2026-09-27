"""Тесты для модуля считывания финансовых операций из CSV и Excel."""

from typing import Any
from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.services import read_csv_transactions, read_excel_transactions


# ---------- read_csv_transactions ----------


@pytest.fixture
def sample_csv_rows() -> list[dict[str, Any]]:
    """Возвращает тестовые строки CSV в виде списка словарей."""
    return [
        {
            "id": "650702",
            "state": "EXECUTED",
            "date": "2023-09-10T14:30:00.000",
            "amount": "1000",
            "currency_name": "RUB",
            "currency_code": "RUB",
            "from": "Счет 123456",
            "to": "Счет 789012",
            "description": "Перевод",
        },
        {
            "id": "650703",
            "state": "PENDING",
            "date": "2023-09-11T10:00:00.000",
            "amount": "500",
            "currency_name": "USD",
            "currency_code": "USD",
            "from": "Счет 111111",
            "to": "Счет 222222",
            "description": "Оплата",
        },
    ]


def test_read_csv_transactions_returns_list_of_dicts(
    sample_csv_rows: list[dict[str, Any]],
) -> None:
    """Проверяет, что функция возвращает список словарей с транзакциями."""
    with patch("builtins.open", mock_open(read_data="")) as mock_file:
        with patch("csv.DictReader") as mock_dict_reader:
            mock_dict_reader.return_value = sample_csv_rows
            result = read_csv_transactions("data/transactions.csv")

    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(item, dict) for item in result)
    assert result[0]["id"] == "650702"
    assert result[1]["description"] == "Оплата"
    mock_file.assert_called_once_with("data/transactions.csv", encoding="utf-8")


def test_read_csv_transactions_empty_file() -> None:
    """Проверяет, что пустой CSV-файл возвращает пустой список."""
    with patch("builtins.open", mock_open(read_data="")):
        with patch("csv.DictReader") as mock_dict_reader:
            mock_dict_reader.return_value = []
            result = read_csv_transactions("data/empty.csv")

    assert result == []


def test_read_csv_transactions_file_not_found() -> None:
    """Проверяет, что при отсутствии файла поднимается FileNotFoundError."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            read_csv_transactions("data/nonexistent.csv")


# ---------- read_excel_transactions ----------


@pytest.fixture
def sample_excel_df() -> pd.DataFrame:
    """Возвращает тестовый DataFrame для эмуляции Excel-файла."""
    return pd.DataFrame(
        [
            {
                "id": "650702",
                "state": "EXECUTED",
                "date": "2023-09-10T14:30:00",
                "amount": 1000,
                "currency_name": "RUB",
                "currency_code": "RUB",
                "from": "Счет 123456",
                "to": "Счет 789012",
                "description": "Перевод",
            },
            {
                "id": "650703",
                "state": "PENDING",
                "date": "2023-09-11T10:00:00",
                "amount": 500,
                "currency_name": "USD",
                "currency_code": "USD",
                "from": "Счет 111111",
                "to": "Счет 222222",
                "description": "Оплата",
            },
        ]
    )


def test_read_excel_transactions_returns_list_of_dicts(
    sample_excel_df: pd.DataFrame,
) -> None:
    """Проверяет, что функция возвращает список словарей с транзакциями."""
    with patch("pandas.read_excel", return_value=sample_excel_df):
        result = read_excel_transactions("data/transactions_excel.xlsx")

    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(item, dict) for item in result)
    assert result[0]["id"] == "650702"
    assert result[1]["description"] == "Оплата"


def test_read_excel_transactions_empty_file() -> None:
    """Проверяет, что пустой Excel-файл возвращает пустой список."""
    empty_df = pd.DataFrame()
    with patch("pandas.read_excel", return_value=empty_df):
        result = read_excel_transactions("data/empty.xlsx")

    assert result == []


def test_read_excel_transactions_file_not_found() -> None:
    """Проверяет, что при отсутствии файла поднимается FileNotFoundError."""
    with patch("pandas.read_excel", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            read_excel_transactions("data/nonexistent.xlsx")
