"""Data loading utilities for scientific data analysis."""

import csv
from typing import Dict, List, Any, Optional


def load_csv_data(filepath: str, delimiter: str = ',') -> List[Dict[str, Any]]:
    """
    Load data from a CSV file.

    Args:
        filepath: Path to the CSV file.
        delimiter: CSV delimiter character (default: ',').

    Returns:
        List of dictionaries where each dictionary represents a row.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty or has no valid data.
    """
    data = []
    try:
        with open(filepath, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=delimiter)
            for row in reader:
                # Convert numeric strings to appropriate types
                converted_row = {}
                for key, value in row.items():
                    converted_row[key] = _convert_value(value)
                data.append(converted_row)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")

    if not data:
        raise ValueError(f"No valid data found in file: {filepath}")

    return data


def _convert_value(value: str) -> Any:
    """
    Convert a string value to the appropriate type.

    Args:
        value: String value to convert.

    Returns:
        Converted value (int, float, or original string).
    """
    if value is None or value == '':
        return None

    # Try integer conversion
    try:
        return int(value)
    except ValueError:
        pass

    # Try float conversion
    try:
        return float(value)
    except ValueError:
        pass

    # Return as string
    return value


def extract_column(data: List[Dict[str, Any]], column: str) -> List[Any]:
    """
    Extract a single column from the data.

    Args:
        data: List of dictionaries representing the data.
        column: Name of the column to extract.

    Returns:
        List of values from the specified column.

    Raises:
        KeyError: If the column does not exist in the data.
    """
    if not data:
        return []

    if column not in data[0]:
        raise KeyError(f"Column '{column}' not found in data")

    return [row.get(column) for row in data]


def filter_data(
    data: List[Dict[str, Any]],
    column: str,
    condition: callable
) -> List[Dict[str, Any]]:
    """
    Filter data based on a condition.

    Args:
        data: List of dictionaries representing the data.
        column: Name of the column to filter on.
        condition: A callable that takes a value and returns True/False.

    Returns:
        Filtered list of dictionaries.
    """
    return [row for row in data if condition(row.get(column))]


def get_column_names(data: List[Dict[str, Any]]) -> List[str]:
    """
    Get the column names from the data.

    Args:
        data: List of dictionaries representing the data.

    Returns:
        List of column names.
    """
    if not data:
        return []
    return list(data[0].keys())
