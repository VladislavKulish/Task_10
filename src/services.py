"""Модуль для считывания финансовых операций из файлов CSV и Excel."""

import csv
from typing import Any

import pandas as pd


def read_csv_transactions(path: str) -> list[dict[str, Any]]:
    """Считывает финансовые операции из CSV-файла и возвращает список словарей.

    Args:
        path: Путь к CSV-файлу.

    Returns:
        Список словарей, каждый из которых описывает одну транзакцию.
        Пустой список, если файл пустой или не содержит данных.

    Raises:
        FileNotFoundError: Если файл не найден.
    """
    transactions: list[dict[str, Any]] = []

    with open(path, encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            transactions.append(dict(row))

    return transactions


def read_excel_transactions(path: str) -> list[dict[str, Any]]:
    """Считывает финансовые операции из Excel-файла и возвращает список словарей.

    Args:
        path: Путь к XLSX-файлу.

    Returns:
        Список словарей, каждый из которых описывает одну транзакцию.
        Пустой список, если файл пустой или не содержит данных.

    Raises:
        FileNotFoundError: Если файл не найден.
    """
    df = pd.read_excel(path)
    transactions: list[dict[str, Any]] = df.to_dict(orient="records")
    return transactions
