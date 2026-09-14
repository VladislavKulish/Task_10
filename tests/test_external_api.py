from unittest.mock import patch, Mock

import pytest

from src.external_api import convert_to_rub, _fetch_exchange_rate


class TestConvertToRub:
    @pytest.fixture
    def rub_transaction(self):
        return {
            "operationAmount": {
                "amount": 5000,
                "currency": {"name": "RUB"},
            }
        }

    @pytest.fixture
    def usd_transaction(self):
        return {
            "operationAmount": {
                "amount": 100,
                "currency": {"name": "USD"},
            }
        }

    @pytest.fixture
    def eur_transaction(self):
        return {
            "operationAmount": {
                "amount": 50,
                "currency": {"name": "EUR"},
            }
        }

    def test_rub_returns_amount_directly(self, rub_transaction):
        assert convert_to_rub(rub_transaction) == 5000.0

    @patch("src.external_api._fetch_exchange_rate")
    def test_usd_converted(self, mock_fetch, usd_transaction):
        mock_fetch.return_value = 90.0
        result = convert_to_rub(usd_transaction)
        assert result == 9000.0

    @patch("src.external_api._fetch_exchange_rate")
    def test_eur_converted(self, mock_fetch, eur_transaction):
        mock_fetch.return_value = 100.0
        result = convert_to_rub(eur_transaction)
        assert result == 5000.0

    @patch("src.external_api._fetch_exchange_rate")
    def test_api_returns_none(self, mock_fetch, usd_transaction):
        mock_fetch.return_value = None
        assert convert_to_rub(usd_transaction) == 0.0

    def test_missing_operation_amount(self):
        assert convert_to_rub({}) == 0.0

    def test_missing_currency(self):
        tx = {"operationAmount": {"amount": 100}}
        assert convert_to_rub(tx) == 100.0

    def test_empty_transaction(self):
        assert convert_to_rub({}) == 0.0


class TestFetchExchangeRate:
    @patch("src.external_api.requests.get")
    def test_successful_fetch(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"success": True, "result": 92.5}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        rate = _fetch_exchange_rate("USD", "RUB")
        assert rate == 92.5

    @patch("src.external_api.requests.get")
    def test_api_error(self, mock_get):
        mock_get.side_effect = Exception("Network error")
        assert _fetch_exchange_rate("USD", "RUB") is None

    @patch("src.external_api.requests.get")
    def test_no_success_flag(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"success": False}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        assert _fetch_exchange_rate("USD", "RUB") is None

    @patch("src.external_api.API_KEY", "")
    def test_no_api_key(self):
        assert _fetch_exchange_rate("USD", "RUB") is None