import logging
import pytest

from masks import get_mask_account, get_mask_card_number


class TestGetMaskCardNumber:

    @pytest.mark.parametrize("idx", range(6))
    def test_valid_cards(self, card_test_cases, idx):
        inp, expected = card_test_cases[idx]
        assert get_mask_card_number(inp) == expected

    @pytest.mark.parametrize("idx", range(4))
    def test_boundary_lengths(self, card_boundary_cases, idx):
        inp, expected = card_boundary_cases[idx]
        assert get_mask_card_number(inp) == expected

    @pytest.mark.parametrize(
        "s", ["Просто текст", "12345", "1234-5678-9012-3456", "", "   "]
    )
    def test_no_valid_number(self, s):
        assert get_mask_card_number(s) == s

    @pytest.mark.parametrize("val", [None, 12345, 1234567890123456, ["str"], True])
    def test_non_string_input(self, val):
        assert get_mask_card_number(val) == val

    def test_card_inside_text(self):
        s = "Ваш номер: 5500123456789010 OK"
        r = get_mask_card_number(s)
        assert r.startswith("Ваш номер: 5500")
        assert r.endswith("9010 OK")


class TestGetMaskAccount:

    @pytest.mark.parametrize("idx", range(4))
    def test_valid_accounts(self, account_test_cases, idx):
        inp, expected = account_test_cases[idx]
        assert get_mask_account(inp) == expected

    @pytest.mark.parametrize("idx", range(3))
    def test_boundary_lengths(self, account_boundary_cases, idx):
        inp, expected = account_boundary_cases[idx]
        assert get_mask_account(inp) == expected

    @pytest.mark.parametrize(
        "s",
        ["Просто текст", "1234567890123456789", "4081-7810-0000-1234-5678", "", "   "],
    )
    def test_no_valid_number(self, s):
        assert get_mask_account(s) == s

    @pytest.mark.parametrize("val", [None, 123, [], True])
    def test_non_string_input(self, val):
        assert get_mask_account(val) == val


class TestMasksLogging:
    def test_info_logged_on_card_masking(self, caplog):
        """Проверяем, что при маскировании карты пишется INFO-лог."""
        caplog.set_level(logging.INFO, logger="masks")
        card = "1234567890123456"
        get_mask_card_number(card)

        assert any(
            "Маскирование номера карты" in record.message for record in caplog.records
        )

    def test_debug_logged_with_result_card(self, caplog):
        """Проверяем, что результат маскирования карты логируется на уровне DEBUG."""
        caplog.set_level(logging.DEBUG, logger="masks")
        card = "1234567890123456"
        result = get_mask_card_number(card)
        assert result == "1234 56** **** 3456"

        assert any(
            "Результат маскирования" in record.message for record in caplog.records
        )

    def test_warning_logged_for_short_card(self, caplog):
        """Проверяем предупреждение при слишком коротком номере карты."""
        caplog.set_level(logging.WARNING, logger="masks")
        short_card = "1234"
        get_mask_card_number(short_card)

        assert any(
            "Подходящая последовательность цифр не найдена" in record.message
            for record in caplog.records
        )

    def test_info_logged_on_account_masking(self, caplog):
        """Проверяем INFO-лог при маскировании счёта."""
        caplog.set_level(logging.INFO, logger="masks")
        account = "40817810000000000001"
        get_mask_account(account)

        assert any(
            "Маскирование номера счёта" in record.message for record in caplog.records
        )

    def test_debug_logged_with_result_account(self, caplog):
        """Проверяем DEBUG-лог с результатом маскирования счёта."""
        caplog.set_level(logging.DEBUG, logger="masks")
        account = "40817810000000000001"
        result = get_mask_account(account)
        assert result == "**0001"

        assert any(
            "Результат маскирования" in record.message for record in caplog.records
        )
