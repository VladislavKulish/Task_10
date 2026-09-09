import pytest

from processing import filter_by_state, sort_by_date


def _is_valid(date_str):
    from datetime import datetime

    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False


class TestFilterByState:

    @pytest.mark.parametrize("state", ["EXECUTED", "PENDING", "CANCELED", "NEW"])
    def test_all_states(self, operations_all_states, state):
        result = filter_by_state(operations_all_states, state)
        expected = [op for op in operations_all_states if op.get("state") == state]
        assert result == expected
        assert all(op["state"] == state for op in result)

    @pytest.mark.parametrize("val", [None, "not a list", 123])
    def test_non_list_input(self, val):
        assert filter_by_state(val, "EXECUTED") == []

    def test_empty_list(self, operations_empty):
        assert filter_by_state(operations_empty, "EXECUTED") == []

    def test_no_matching_state(self, sample_operations):
        assert filter_by_state(sample_operations, "NONEXISTENT") == []

    def test_all_match(self, operations_all_executed):
        result = filter_by_state(operations_all_executed, "EXECUTED")
        assert len(result) == 3
        assert all(op["state"] == "EXECUTED" for op in result)

    def test_missing_state_key(self, operations_missing_state):
        result = filter_by_state(operations_missing_state, "EXECUTED")
        assert result == [{"id": 1, "state": "EXECUTED", "date": "2024-01-01"}]

    def test_non_dict_skipped(self, operations_mixed_types):
        result = filter_by_state(operations_mixed_types, "EXECUTED")
        assert result == [{"id": 1, "state": "EXECUTED", "date": "2024-01-01"}]

    def test_state_none_filter(self, operations_state_none):
        result = filter_by_state(operations_state_none, None)
        assert len(result) == 2
        assert all(op["state"] is None for op in result)

    def test_case_sensitive(self, sample_operations):
        assert filter_by_state(sample_operations, "executed") == []


class TestSortByDate:

    @pytest.mark.parametrize("reverse", [False, True])
    def test_sort_basic(self, sample_operations, reverse):
        result = sort_by_date(sample_operations, reverse=reverse)
        assert len(result) == len(sample_operations)
        valid = [
            op["date"]
            for op in result
            if isinstance(op.get("date"), str) and _is_valid(op["date"])
        ]
        assert valid == sorted(valid, reverse=reverse)

    @pytest.mark.parametrize("reverse", [False, True])
    def test_same_dates_stable(self, operations_same_dates, reverse):
        result = sort_by_date(operations_same_dates, reverse=reverse)
        assert [op["id"] for op in result] == [1, 2, 3]

    @pytest.mark.parametrize("reverse", [False, True])
    def test_all_valid(self, operations_all_valid, reverse):
        result = sort_by_date(operations_all_valid, reverse=reverse)
        dates = [op["date"] for op in result]
        assert dates == sorted(dates, reverse=reverse)

    @pytest.mark.parametrize("reverse", [False, True])
    def test_all_invalid(self, operations_all_invalid, reverse):
        result = sort_by_date(operations_all_invalid, reverse=reverse)
        assert [op["id"] for op in result] == [1, 2, 3]

    @pytest.mark.parametrize("reverse", [False, True])
    def test_empty_list(self, operations_empty, reverse):
        assert sort_by_date(operations_empty, reverse=reverse) == []

    @pytest.mark.parametrize("val", [None, "not a list", 123])
    def test_non_list_input(self, val):
        assert sort_by_date(val, False) == []

    def test_invalid_dates_ascending(self, operations_invalid_dates):
        result = sort_by_date(operations_invalid_dates, reverse=False)
        valid = [
            op
            for op in result
            if isinstance(op.get("date"), str) and _is_valid(op["date"])
        ]
        invalid = [op for op in result if op not in valid]
        assert all(op in result[-len(valid) :] for op in valid)
        assert all(op in result[: len(invalid)] for op in invalid)

    def test_invalid_dates_descending(self, operations_invalid_dates):
        result = sort_by_date(operations_invalid_dates, reverse=True)
        valid = [
            op
            for op in result
            if isinstance(op.get("date"), str) and _is_valid(op["date"])
        ]
        invalid = [op for op in result if op not in valid]
        assert all(op in result[: len(valid)] for op in valid)
        assert all(op in result[-len(invalid) :] for op in invalid)

    def test_mixed_types(self, operations_mixed_types):
        result = sort_by_date(operations_mixed_types, reverse=False)
        assert len(result) == len(operations_mixed_types)

    @pytest.mark.parametrize("date_val,valid_id", [(None, 2), (20240101, 2), ("", 1)])
    def test_date_non_string_types(self, date_val, valid_id):
        ops = [
            {"id": 1, "state": "X", "date": date_val},
            {"id": 2, "state": "Y", "date": "2024-01-01"},
        ]
        result = sort_by_date(ops, reverse=True)
        assert result[0]["id"] == valid_id

    def test_date_wrong_format(self):
        ops = [
            {"id": 1, "state": "X", "date": "01.05.2024"},
            {"id": 2, "state": "Y", "date": "2024-01-01"},
        ]
        result = sort_by_date(ops, reverse=False)
        assert result[0]["id"] == 1
        assert result[1]["id"] == 2

    @pytest.mark.parametrize("reverse", [False, True])
    def test_single_valid(self, reverse):
        ops = [{"id": 1, "state": "X", "date": "2024-06-15"}]
        assert sort_by_date(ops, reverse) == ops

    @pytest.mark.parametrize("reverse", [False, True])
    def test_single_invalid(self, reverse):
        ops = [{"id": 1, "state": "X", "date": "bad"}]
        assert sort_by_date(ops, reverse) == ops
