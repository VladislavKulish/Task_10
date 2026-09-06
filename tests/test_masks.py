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
