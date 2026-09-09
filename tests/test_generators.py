import pytest

from src.generators import (
    filter_by_currency,
    transaction_descriptions,
    card_number_generator,
)

# ───────────────────────── Фикстуры ─────────────────────────


@pytest.fixture
def sample_transactions():
    """Транзакции с разными валютами и полями."""
    return [
        {
            "id": 1,
            "date": "2024-05-01T12:34:56.000000",
            "description": "Перевод другу",
            "from": "Счёт 40817810000012345678",
            "to": "Карта 2200123412341234",
            "operationAmount": {
                "amount": 5000,
                "currency": {"name": "USD"},
            },
        },
        {
            "id": 2,
            "date": "2024-05-02T09:15:00.000000",
            "description": "Оплата услуг",
            "to": "Счёт 40702810123456789012",
            "operationAmount": {
                "amount": 1200,
                "currency": {"name": "RUB"},
            },
        },
        {
            "id": 3,
            "date": "2024-05-03T18:00:00.000000",
            "description": "Покупка в магазине",
            "from": "Карта 5555666677778888",
            "to": "Счёт 12345678901234567890",
            "operationAmount": {
                "amount": 300,
                "currency": {"name": "USD"},
            },
        },
        {
            "id": 4,
            "date": "2024-05-04T10:20:30.000000",
            "description": "Возврат средств",
            "operationAmount": {
                "amount": 150,
                "currency": {"name": "EUR"},
            },
        },
        {
            "id": 5,
            "description": "Транзакция без суммы и валюты",
            "from": "Счёт 11112222333344445555",
            "to": "Карта 9999888877776666",
        },
    ]


@pytest.fixture
def empty_transactions():
    return []


@pytest.fixture
def transactions_without_currency():
    """Транзакции, у которых нет поля currency или оно неполное."""
    return [
        {"id": 1, "operationAmount": {"amount": 100}},
        {"id": 2, "operationAmount": {"amount": 200, "currency": {}}},
        {"id": 3, "operationAmount": {}},
        {"id": 4},
    ]


# ───────────────────── filter_by_currency ─────────────────────


class TestFilterByCurrency:
    """Тесты функции filter_by_currency."""

    @pytest.mark.parametrize(
        "currency, expected_ids",
        [
            ("USD", [1, 3]),
            ("RUB", [2]),
            ("EUR", [4]),
            ("GBP", []),
        ],
    )
    def test_filter_by_currency(self, sample_transactions, currency, expected_ids):
        """Фильтрация по разным валютам."""
        result = list(filter_by_currency(sample_transactions, currency))
        actual_ids = [t["id"] for t in result]
        assert actual_ids == expected_ids

    @pytest.mark.parametrize("currency", ["usd", "UsD", "USD", "uSd"])
    def test_case_insensitive(self, sample_transactions, currency):
        """Поиск без учёта регистра: usd, UsD и т. д. находят USD."""
        result = list(filter_by_currency(sample_transactions, currency))
        actual_ids = sorted(t["id"] for t in result)
        assert actual_ids == [1, 3]

    def test_no_matching_currency(self, sample_transactions):
        """Нет транзакций с заданной валютой — пустой результат."""
        result = list(filter_by_currency(sample_transactions, "JPY"))
        assert result == []

    def test_empty_list(self, empty_transactions):
        """Пустой список на входе — пустой результат, без ошибок."""
        result = list(filter_by_currency(empty_transactions, "USD"))
        assert result == []

    def test_missing_currency_keys(self, transactions_without_currency):
        """Транзакции без поля currency — не падает, возвращает пусто."""
        result = list(filter_by_currency(transactions_without_currency, "USD"))
        assert result == []

    def test_returns_generator(self, sample_transactions):
        """Функция возвращает генератор, а не список."""
        gen = filter_by_currency(sample_transactions, "USD")
        assert hasattr(gen, "__next__")
        first = next(gen)
        assert first["id"] == 1


# ─────────────────── transaction_descriptions ───────────────────


class TestTransactionDescriptions:
    """Тесты генератора transaction_descriptions."""

    def test_single_transaction(self, sample_transactions):
        """Корректное описание для одной транзакции."""
        result = list(transaction_descriptions([sample_transactions[0]]))
        assert len(result) == 1
        desc = result[0]
        assert "2024-05-01" in desc
        assert "Перевод другу" in desc
        assert "5000 USD" in desc

    def test_multiple_transactions(self, sample_transactions):
        """Все транзакции обработаны, количество совпадает."""
        result = list(transaction_descriptions(sample_transactions))
        assert len(result) == 5

    @pytest.mark.parametrize(
        "index, expected_fragments",
        [
            (0, ["2024-05-01", "Перевод другу", "5000 USD"]),
            (1, ["2024-05-02", "Оплата услуг", "1200 RUB"]),
            (2, ["2024-05-03", "Покупка в магазине", "300 USD"]),
            (3, ["2024-05-04", "Возврат средств", "150 EUR"]),
            (4, ["Транзакция без суммы и валюты"]),
        ],
    )
    def test_description_content(self, sample_transactions, index, expected_fragments):
        """Проверка содержимого описания для каждой транзакции."""
        result = list(transaction_descriptions([sample_transactions[index]]))
        desc = result[0]
        for fragment in expected_fragments:
            assert fragment in desc

    def test_empty_list(self, empty_transactions):
        """Пустой список — пустой результат."""
        result = list(transaction_descriptions(empty_transactions))
        assert result == []

    def test_transaction_without_amount(self, sample_transactions):
        """Транзакция без operationAmount — описание без суммы."""
        tx = sample_transactions[4]
        result = list(transaction_descriptions([tx]))
        desc = result[0]
        assert "Транзакция без суммы и валюты" in desc
        assert "USD" not in desc
        assert "RUB" not in desc

    def test_transaction_without_sender(self, sample_transactions):
        """Транзакция без поля 'from' — описание без стрелки."""
        tx = sample_transactions[1]
        result = list(transaction_descriptions([tx]))
        desc = result[0]
        assert "->" not in desc

    def test_returns_generator(self, sample_transactions):
        """Функция возвращает генератор."""
        gen = transaction_descriptions(sample_transactions)
        assert hasattr(gen, "__next__")
        first = next(gen)
        assert isinstance(first, str)


# ─────────────────── card_number_generator ───────────────────


class TestCardNumberGenerator:
    """Тесты генератора card_number_generator."""

    def test_range_from_one(self):
        """Генерация с 1 — первые три номера."""
        result = list(card_number_generator(1, 3))
        assert result == [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
        ]

    def test_arbitrary_range(self):
        """Произвольный диапазон."""
        result = list(card_number_generator(1234567890123450, 1234567890123452))
        assert result == [
            "1234 5678 9012 3450",
            "1234 5678 9012 3451",
            "1234 5678 9012 3452",
        ]

    @pytest.mark.parametrize("value", [1, 5, 9999999999999999])
    def test_single_value_range(self, value):
        """Диапазон из одного числа — ровно один результат."""
        result = list(card_number_generator(value, value))
        assert len(result) == 1
        s = result[0].replace(" ", "")
        assert int(s) == value

    def test_max_boundary(self):
        """Крайнее верхнее значение диапазона."""
        result = list(card_number_generator(9999999999999998, 9999999999999999))
        assert result == [
            "9999 9999 9999 9998",
            "9999 9999 9999 9999",
        ]

    def test_min_boundary(self):
        """Крайнее нижнее значение диапазона."""
        result = list(card_number_generator(1, 2))
        assert result == [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
        ]

    @pytest.mark.parametrize(
        "start, end",
        [
            (1, 10),
            (1000, 1005),
            (9999999999999990, 9999999999999999),
        ],
    )
    def test_format(self, start, end):
        """Каждый номер: 19 символов, 4 группы по 4 цифры, разделённых пробелом."""
        for num_str in card_number_generator(start, end):
            assert len(num_str) == 19
            parts = num_str.split(" ")
            assert len(parts) == 4
            for p in parts:
                assert len(p) == 4
                assert p.isdigit()

    def test_invalid_start_zero(self):
        """start = 0 — ValueError."""
        with pytest.raises(ValueError):
            list(card_number_generator(0, 5))

    def test_invalid_start_negative(self):
        """Отрицательный start — ValueError."""
        with pytest.raises(ValueError):
            list(card_number_generator(-1, 5))

    def test_invalid_end_too_large(self):
        """end > 9999999999999999 — ValueError."""
        with pytest.raises(ValueError):
            list(card_number_generator(1, 10_000_000_000_000_000))

    def test_start_greater_than_end(self):
        with pytest.raises(ValueError, match="start must not be greater than end"):
            list(card_number_generator(10, 5))

    def test_returns_generator(self):
        """Функция возвращает генератор."""
        gen = card_number_generator(1, 3)
        assert hasattr(gen, "__next__")
        first = next(gen)
        assert first == "0000 0000 0000 0001"

    def test_sequential(self):
        """Числа идут строго по порядку."""
        result = list(card_number_generator(5, 8))
        nums = [int(r.replace(" ", "")) for r in result]
        assert nums == [5, 6, 7, 8]
