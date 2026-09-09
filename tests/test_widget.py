import pytest

from widget import (
    get_date,
    mask_account_card,
    mask_account_number,
    mask_card_number,
    process_data,
)

# ── mask_card_number (обёртка над get_mask_card_number) ──


class TestMaskCardNumber:

    @pytest.mark.parametrize("idx", range(6))
    def test_valid_cards(self, card_test_cases, idx):
        inp, expected = card_test_cases[idx]
        assert mask_card_number(inp) == expected

    @pytest.mark.parametrize("idx", range(4))
    def test_boundary_lengths(self, card_boundary_cases, idx):
        inp, expected = card_boundary_cases[idx]
        assert mask_card_number(inp) == expected

    @pytest.mark.parametrize("val", [None, 12345, True])
    def test_non_string_input(self, val):
        assert mask_card_number(val) == val


# ── mask_account_number (обёртка над get_mask_account) ──


class TestMaskAccountNumber:

    @pytest.mark.parametrize("idx", range(4))
    def test_valid_accounts(self, account_test_cases, idx):
        inp, expected = account_test_cases[idx]
        assert mask_account_number(inp) == expected

    @pytest.mark.parametrize("idx", range(3))
    def test_boundary_lengths(self, account_boundary_cases, idx):
        inp, expected = account_boundary_cases[idx]
        assert mask_account_number(inp) == expected

    @pytest.mark.parametrize("val", [None, 123, True])
    def test_non_string_input(self, val):
        assert mask_account_number(val) == val


# ── mask_account_card ──────────────────────────


class TestMaskAccountCard:

    @pytest.mark.parametrize("idx", range(6))
    def test_mixed_cards_and_accounts(self, mixed_mask_cases, idx):
        inp, expected = mixed_mask_cases[idx]
        assert mask_account_card(inp) == expected

    @pytest.mark.parametrize("idx", range(5))
    def test_boundary_lengths(self, mask_boundary_cases, idx):
        inp, expected = mask_boundary_cases[idx]
        assert mask_account_card(inp) == expected

    @pytest.mark.parametrize("s", ["Нет номера", "12345", "1234-5678-9012-3456", "   "])
    def test_no_valid_sequence(self, s):
        assert mask_account_card(s) == s

    @pytest.mark.parametrize("val", [None, 1234567890123456, ["test"], True])
    def test_non_string_input(self, val):
        assert mask_account_card(val) == val

    def test_empty_string(self):
        assert mask_account_card("") == ""

    def test_card_first_then_account(self):
        s = "Card 7000123456789012 Acc 40817810000012345678"
        r = mask_account_card(s)
        assert r.startswith("Card 7000 12** **** 9012")


# ── get_date ────────────────────────────────────


class TestGetDate:

    @pytest.mark.parametrize("idx", range(9))
    def test_standard_formats(self, date_standard_cases, idx):
        inp, expected = date_standard_cases[idx]
        assert get_date(inp) == expected

    @pytest.mark.parametrize("idx", range(6))
    def test_microsecond_variants(self, date_microsecond_cases, idx):
        inp, expected = date_microsecond_cases[idx]
        assert get_date(inp) == expected

    @pytest.mark.parametrize("idx", range(6))
    def test_edge_cases(self, date_edge_cases, idx):
        inp, expected = date_edge_cases[idx]
        assert get_date(inp) == expected

    @pytest.mark.parametrize(
        "s", ["abc123", "2024-09", "32.01.2024", "2024-02-30", "", "   "]
    )
    def test_no_valid_date(self, s):
        assert get_date(s) == s

    @pytest.mark.parametrize("val", [None, 12345, ["2024-09-10"], True])
    def test_non_string_input(self, val):
        assert get_date(val) == val

    def test_multiple_dates_first_only(self):
        s = "2023-01-01 и 2024-12-31"
        r = get_date(s)
        assert r.startswith("01.01.2023")
        assert "2024-12-31" in r

    def test_date_inside_long_text(self):
        s = "Создано: 2024-06-15, изменено: 2024-06-20"
        r = get_date(s)
        assert r.startswith("Создано: 15.06.2024")
        assert "2024-06-20" in r

    def test_iso_microseconds_value_error_fallback(self):
        assert get_date("2024-09-10T12:34:56.") == "10.09.2024"

    def test_iso_t_invalid_time_fallback(self):
        assert get_date("2024-09-10T99:99:99") == "10.09.2024"


# ── process_data ───────────────────────────────


class TestProcessData:

    @pytest.mark.parametrize("idx", range(2))
    def test_full_operations(self, full_operations, idx):
        op = full_operations[idx]
        result = process_data(op)
        # Должна быть отформатированная дата
        assert "2024" in result or result
        # Должен быть description
        assert op["description"] in result
        # Должны быть замаскированные номера
        assert "**" in result

    def test_minimal_operation(self, minimal_operation):
        result = process_data(minimal_operation)
        assert result == "Открытие счёта"

    def test_empty_operation(self, empty_operation):
        result = process_data(empty_operation)
        assert result == ""

    def test_non_dict_input(self):
        assert process_data(None) == ""
        assert process_data("string") == ""
        assert process_data([]) == ""

    def test_operation_no_amount(self, operation_no_amount):
        result = process_data(operation_no_amount)
        assert "01.05.2024" in result
        assert "Тест" in result
        # from и to замаскированы
        assert "7000" in result
        assert "**5678" in result
        # Нет суммы
        assert "руб." not in result

    def test_operation_amount_not_dict(self, operation_amount_not_dict):
        result = process_data(operation_amount_not_dict)
        assert "Тест" in result
        assert "50000" not in result

    def test_operation_currency_not_dict(self, operation_currency_not_dict):
        result = process_data(operation_currency_not_dict)
        assert "Тест" in result
        assert "100" in result
        # currency не dict → name пустой
        assert "руб." not in result

    def test_operation_from_only(self, operation_from_only):
        result = process_data(operation_from_only)
        assert "7000" in result
        assert "100" in result
        assert "руб." in result

    def test_operation_no_date(self):
        op = {
            "description": "Перевод",
            "from": "Visa 7000123456789012",
            "to": "Счёт 40817810000012345678",
            "operationAmount": {"amount": "500", "currency": {"name": "руб."}},
        }
        result = process_data(op)
        # Нет даты — просто description
        assert result.startswith("Перевод")
        assert "7000" in result
        assert "**5678" in result
