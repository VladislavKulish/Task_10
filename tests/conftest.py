import pytest

# ═══════════════════════════════════════════════
# Фикстуры: списки операций (processing)
# ═══════════════════════════════════════════════


@pytest.fixture
def sample_operations():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-15", "amount": 10000},
        {"id": 2, "state": "PENDING", "date": "2024-03-10", "amount": 5000},
        {"id": 3, "state": "EXECUTED", "date": "2023-12-01", "amount": 25000},
        {"id": 4, "state": "CANCELED", "date": "2024-02-20", "amount": 1500},
        {"id": 5, "state": "EXECUTED", "date": "2024-03-10", "amount": 8000},
    ]


@pytest.fixture
def operations_same_dates():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-05-01", "amount": 100},
        {"id": 2, "state": "PENDING", "date": "2024-05-01", "amount": 200},
        {"id": 3, "state": "EXECUTED", "date": "2024-05-01", "amount": 300},
    ]


@pytest.fixture
def operations_invalid_dates():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-01", "amount": 100},
        {"id": 2, "state": "PENDING", "date": None, "amount": 200},
        {"id": 3, "state": "EXECUTED", "date": "bad-format", "amount": 300},
        {"id": 4, "state": "CANCELED", "date": "01.05.2024", "amount": 400},
        {"id": 5, "state": "EXECUTED", "date": "2024-13-01", "amount": 500},
    ]


@pytest.fixture
def operations_missing_state():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-01"},
        {"id": 2, "date": "2024-02-01"},
        {"id": 3, "state": None, "date": "2024-03-01"},
        {"id": 4, "state": "PENDING", "date": "2024-04-01"},
    ]


@pytest.fixture
def operations_mixed_types():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-01"},
        "not a dict",
        None,
        {"id": 2, "state": "PENDING", "date": "2024-02-01"},
        12345,
    ]


@pytest.fixture
def operations_all_executed():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-10"},
        {"id": 2, "state": "EXECUTED", "date": "2024-02-20"},
        {"id": 3, "state": "EXECUTED", "date": "2024-03-30"},
    ]


@pytest.fixture
def operations_all_invalid():
    return [
        {"id": 1, "state": "EXECUTED", "date": None},
        {"id": 2, "state": "PENDING", "date": "bad"},
        {"id": 3, "state": "CANCELED", "date": 12345},
    ]


@pytest.fixture
def operations_all_valid():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-01"},
        {"id": 2, "state": "PENDING", "date": "2024-01-01"},
        {"id": 3, "state": "CANCELED", "date": "2024-02-01"},
    ]


@pytest.fixture
def operations_empty_date_string():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-01"},
        {"id": 2, "state": "PENDING", "date": ""},
        {"id": 3, "state": "CANCELED", "date": "2024-03-01"},
    ]


@pytest.fixture
def operations_state_none():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-01"},
        {"id": 2, "state": None, "date": "2024-02-01"},
        {"id": 3, "state": None, "date": "2024-03-01"},
    ]


@pytest.fixture
def operations_empty():
    return []


@pytest.fixture
def operations_all_states():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-01", "amount": 100},
        {"id": 2, "state": "PENDING", "date": "2024-02-01", "amount": 200},
        {"id": 3, "state": "CANCELED", "date": "2024-03-01", "amount": 300},
        {"id": 4, "state": "NEW", "date": "2024-04-01", "amount": 400},
    ]


# ═══════════════════════════════════════════════
# Фикстуры: строки для масок (widget + masks)
# ═══════════════════════════════════════════════


@pytest.fixture
def card_test_cases():
    return [
        ("Visa 7000123456789012", "Visa 7000 12** **** 9012"),
        ("Mastercard 5536912345678901", "Mastercard 5536 91** **** 8901"),
        ("Amex 341234567890123", "Amex 3412 34** **** 0123"),
        ("Maestro 6759123456789", "Maestro 6759 12** **** 6789"),
        ("Card 9999888877776665555", "Card 9999 88** **** 5555"),
        ("1234567890123456", "1234 56** **** 3456"),
    ]


@pytest.fixture
def card_boundary_cases():
    return [
        ("123456789012", "123456789012"),
        ("1111222233333", "1111 22** **** 3333"),
        ("9999888877776665555", "9999 88** **** 5555"),
        ("12345678901234567890", "12345678901234567890"),
    ]


@pytest.fixture
def account_test_cases():
    return [
        ("Счёт 40817810000012345678", "Счёт **5678"),
        ("Ваш счёт: 30101810200000000003 конец.", "Ваш счёт: **0003 конец."),
        ("Account 40702810500000000444", "Account **0444"),
        ("40817810000001234567", "**4567"),
    ]


@pytest.fixture
def account_boundary_cases():
    return [
        ("1234567890123456789", "1234567890123456789"),
        ("40817810000012345678", "**5678"),
        ("123456789012345678901", "123456789012345678901"),
    ]


@pytest.fixture
def mixed_mask_cases():
    return [
        ("Visa 7000123456789012", "Visa 7000 12** **** 9012"),
        ("Счёт 40817810000012345678", "Счёт **5678"),
        ("Account 40702810500000000444", "Account **0444"),
        ("Amex 341234567890123", "Amex 3412 34** **** 0123"),
        ("Текст без номера", "Текст без номера"),
        ("", ""),
    ]


@pytest.fixture
def mask_boundary_cases():
    return [
        ("123456789012", "123456789012"),
        ("1111222233333", "1111 22** **** 3333"),
        ("9999888877776665555", "9999 88** **** 5555"),
        ("40817810000012345678", "**5678"),
        ("123456789012345678901", "123456789012345678901"),
    ]


# ═══════════════════════════════════════════════
# Фикстуры: строки с датами (widget)
# ═══════════════════════════════════════════════


@pytest.fixture
def date_standard_cases():
    return [
        ("2024-09-10", "10.09.2024"),
        ("2024/09/10", "10.09.2024"),
        ("10.09.2024", "10.09.2024"),
        ("2024-09-10T12:34:56", "10.09.2024"),
        ("2024-09-10 12:34:56", "10.09.2024"),
        ("2024-09-10T12:34:56.123456", "10.09.2024"),
        ("Заказ от 2024-09-10 готов", "Заказ от 10.09.2024 готов"),
        ("Нет даты здесь", "Нет даты здесь"),
        ("2024-13-01", "2024-13-01"),
    ]


@pytest.fixture
def date_microsecond_cases():
    return [
        ("2024-09-10T12:34:56.1", "10.09.2024"),
        ("2024-09-10T12:34:56.12", "10.09.2024"),
        ("2024-09-10T12:34:56.123", "10.09.2024"),
        ("2024-09-10T12:34:56.1234", "10.09.2024"),
        ("2024-09-10T12:34:56.12345", "10.09.2024"),
        ("2024-09-10T12:34:56.123456", "10.09.2024"),
    ]


@pytest.fixture
def date_edge_cases():
    return [
        ("2024-09-10T99:99:99", "10.09.2024"),
        ("2024-09-10T12:34:56.", "10.09.2024"),
        ("2024-09-10T12:34:56.1234567", "10.09.2024"),
        ("0001-01-01", "01.01.0001"),
        ("9999-12-31", "31.12.9999"),
        ("xxx2024-09-10xxx", "xxx10.09.2024xxx"),
    ]


# ═══════════════════════════════════════════════
# Фикстуры: операции для process_data (widget)
# ═══════════════════════════════════════════════


@pytest.fixture
def full_operations():
    """Полные операции со всеми полями для process_data."""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2024-01-15T08:30:00",
            "description": "Перевод организации",
            "from": "Visa 7000123456789012",
            "to": "Счёт 40817810000012345678",
            "operationAmount": {
                "amount": "50000",
                "currency": {"name": "руб."},
            },
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2024-03-10",
            "description": "Перевод с карты на карту",
            "from": "Maestro 6759123456789",
            "to": "Mastercard 5536912345678901",
            "operationAmount": {
                "amount": "12000",
                "currency": {"name": "USD"},
            },
        },
    ]


@pytest.fixture
def minimal_operation():
    """Операция только с description."""
    return {"description": "Открытие счёта"}


@pytest.fixture
def empty_operation():
    """Пустой словарь."""
    return {}


@pytest.fixture
def operation_no_amount():
    """Операция без operationAmount."""
    return {
        "date": "2024-05-01",
        "description": "Тест",
        "from": "Visa 7000123456789012",
        "to": "Счёт 40817810000012345678",
    }


@pytest.fixture
def operation_amount_not_dict():
    """operationAmount — не словарь."""
    return {
        "date": "2024-05-01",
        "description": "Тест",
        "operationAmount": "50000",
    }


@pytest.fixture
def operation_currency_not_dict():
    """currency внутри operationAmount — не словарь."""
    return {
        "date": "2024-05-01",
        "description": "Тест",
        "operationAmount": {"amount": "100", "currency": "руб."},
    }


@pytest.fixture
def operation_from_only():
    """Есть 'from', но нет 'to'."""
    return {
        "date": "2024-05-01",
        "description": "Тест",
        "from": "Visa 7000123456789012",
        "operationAmount": {"amount": "100", "currency": {"name": "руб."}},
    }
