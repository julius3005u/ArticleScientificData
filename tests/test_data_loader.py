"""Tests for data_loader module."""

import os
import tempfile
import pytest
from src.data_loader import (
    load_csv_data,
    _convert_value,
    extract_column,
    filter_data,
    get_column_names
)


class TestConvertValue:
    """Tests for _convert_value function."""

    def test_convert_integer(self):
        assert _convert_value("42") == 42

    def test_convert_float(self):
        assert _convert_value("3.14") == 3.14

    def test_convert_string(self):
        assert _convert_value("hello") == "hello"

    def test_convert_empty_string(self):
        assert _convert_value("") is None

    def test_convert_none(self):
        assert _convert_value(None) is None


class TestLoadCsvData:
    """Tests for load_csv_data function."""

    def test_load_valid_csv(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("id,value,name\n")
            f.write("1,10.5,test1\n")
            f.write("2,20.5,test2\n")
            temp_path = f.name

        try:
            data = load_csv_data(temp_path)
            assert len(data) == 2
            assert data[0]['id'] == 1
            assert data[0]['value'] == 10.5
            assert data[0]['name'] == "test1"
        finally:
            os.unlink(temp_path)

    def test_load_nonexistent_file(self):
        with pytest.raises(FileNotFoundError):
            load_csv_data("nonexistent_file.csv")

    def test_load_empty_csv(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("id,value,name\n")
            temp_path = f.name

        try:
            with pytest.raises(ValueError, match="No valid data found"):
                load_csv_data(temp_path)
        finally:
            os.unlink(temp_path)


class TestExtractColumn:
    """Tests for extract_column function."""

    def test_extract_existing_column(self):
        data = [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}]
        result = extract_column(data, 'a')
        assert result == [1, 3]

    def test_extract_nonexistent_column(self):
        data = [{'a': 1, 'b': 2}]
        with pytest.raises(KeyError, match="Column 'c' not found"):
            extract_column(data, 'c')

    def test_extract_from_empty_data(self):
        assert extract_column([], 'a') == []


class TestFilterData:
    """Tests for filter_data function."""

    def test_filter_numeric_condition(self):
        data = [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}, {'a': 5, 'b': 6}]
        result = filter_data(data, 'a', lambda x: x > 2)
        assert len(result) == 2
        assert result[0]['a'] == 3
        assert result[1]['a'] == 5

    def test_filter_string_condition(self):
        data = [{'name': 'A', 'val': 1}, {'name': 'B', 'val': 2}]
        result = filter_data(data, 'name', lambda x: x == 'A')
        assert len(result) == 1
        assert result[0]['name'] == 'A'


class TestGetColumnNames:
    """Tests for get_column_names function."""

    def test_get_column_names(self):
        data = [{'a': 1, 'b': 2, 'c': 3}]
        result = get_column_names(data)
        assert 'a' in result
        assert 'b' in result
        assert 'c' in result

    def test_get_column_names_empty(self):
        assert get_column_names([]) == []
