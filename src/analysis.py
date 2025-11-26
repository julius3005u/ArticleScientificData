"""Statistical analysis functions for scientific data."""

import math
from typing import Dict, List, Any, Optional, Tuple


def calculate_statistics(
    data: List[Dict[str, Any]],
    column: str
) -> Dict[str, float]:
    """
    Calculate descriptive statistics for a column.

    Args:
        data: List of dictionaries representing the data.
        column: Name of the column to analyze.

    Returns:
        Dictionary containing mean, median, std_dev, min, max, and count.

    Raises:
        ValueError: If no numeric values found in the column.
    """
    values = [row.get(column) for row in data if isinstance(row.get(column), (int, float))]

    if not values:
        raise ValueError(f"No numeric values found in column '{column}'")

    n = len(values)
    mean = sum(values) / n

    sorted_values = sorted(values)
    if n % 2 == 0:
        median = (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2
    else:
        median = sorted_values[n // 2]

    variance = sum((x - mean) ** 2 for x in values) / (n - 1) if n > 1 else 0
    std_dev = math.sqrt(variance)

    return {
        'mean': mean,
        'median': median,
        'std_dev': std_dev,
        'min': min(values),
        'max': max(values),
        'count': n
    }


def perform_correlation_analysis(
    data: List[Dict[str, Any]],
    column_x: str,
    column_y: str
) -> Dict[str, float]:
    """
    Calculate Pearson correlation coefficient between two columns.

    Args:
        data: List of dictionaries representing the data.
        column_x: Name of the first column.
        column_y: Name of the second column.

    Returns:
        Dictionary containing correlation coefficient and related statistics.

    Raises:
        ValueError: If insufficient data for correlation analysis.
    """
    pairs = [
        (row.get(column_x), row.get(column_y))
        for row in data
        if isinstance(row.get(column_x), (int, float))
        and isinstance(row.get(column_y), (int, float))
    ]

    if len(pairs) < 2:
        raise ValueError("Insufficient data for correlation analysis")

    x_values = [p[0] for p in pairs]
    y_values = [p[1] for p in pairs]

    n = len(pairs)
    mean_x = sum(x_values) / n
    mean_y = sum(y_values) / n

    # Calculate covariance and standard deviations (sample formulas with n-1)
    n_minus_1 = n - 1 if n > 1 else 1
    covariance = sum((x - mean_x) * (y - mean_y) for x, y in pairs) / n_minus_1
    std_x = math.sqrt(sum((x - mean_x) ** 2 for x in x_values) / n_minus_1)
    std_y = math.sqrt(sum((y - mean_y) ** 2 for y in y_values) / n_minus_1)

    if std_x == 0 or std_y == 0:
        correlation = 0.0
    else:
        correlation = covariance / (std_x * std_y)

    return {
        'correlation': correlation,
        'covariance': covariance,
        'n_pairs': n,
        'mean_x': mean_x,
        'mean_y': mean_y
    }


def perform_linear_regression(
    data: List[Dict[str, Any]],
    column_x: str,
    column_y: str
) -> Dict[str, float]:
    """
    Perform simple linear regression.

    Args:
        data: List of dictionaries representing the data.
        column_x: Name of the independent variable column.
        column_y: Name of the dependent variable column.

    Returns:
        Dictionary containing slope, intercept, and r_squared.

    Raises:
        ValueError: If insufficient data for regression analysis.
    """
    pairs = [
        (row.get(column_x), row.get(column_y))
        for row in data
        if isinstance(row.get(column_x), (int, float))
        and isinstance(row.get(column_y), (int, float))
    ]

    if len(pairs) < 2:
        raise ValueError("Insufficient data for regression analysis")

    x_values = [p[0] for p in pairs]
    y_values = [p[1] for p in pairs]

    n = len(pairs)
    mean_x = sum(x_values) / n
    mean_y = sum(y_values) / n

    # Calculate slope
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in pairs)
    denominator = sum((x - mean_x) ** 2 for x in x_values)

    if denominator == 0:
        slope = 0.0
        intercept = mean_y
    else:
        slope = numerator / denominator
        intercept = mean_y - slope * mean_x

    # Calculate R-squared
    y_pred = [slope * x + intercept for x in x_values]
    ss_res = sum((y - yp) ** 2 for y, yp in zip(y_values, y_pred))
    ss_tot = sum((y - mean_y) ** 2 for y in y_values)

    if ss_tot == 0:
        r_squared = 1.0
    else:
        r_squared = 1 - (ss_res / ss_tot)

    return {
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_squared,
        'n_observations': n
    }


def calculate_percentile(
    data: List[Dict[str, Any]],
    column: str,
    percentile: float
) -> float:
    """
    Calculate a specific percentile of a column.

    Args:
        data: List of dictionaries representing the data.
        column: Name of the column to analyze.
        percentile: Percentile to calculate (0-100).

    Returns:
        The percentile value.

    Raises:
        ValueError: If percentile is out of range or no numeric values found.
    """
    if not 0 <= percentile <= 100:
        raise ValueError("Percentile must be between 0 and 100")

    values = [row.get(column) for row in data if isinstance(row.get(column), (int, float))]

    if not values:
        raise ValueError(f"No numeric values found in column '{column}'")

    sorted_values = sorted(values)
    n = len(sorted_values)

    k = (n - 1) * (percentile / 100)
    f = math.floor(k)
    c = math.ceil(k)

    if f == c:
        return sorted_values[int(k)]

    return sorted_values[int(f)] * (c - k) + sorted_values[int(c)] * (k - f)


def calculate_z_scores(
    data: List[Dict[str, Any]],
    column: str
) -> List[Optional[float]]:
    """
    Calculate z-scores for all values in a column.

    Args:
        data: List of dictionaries representing the data.
        column: Name of the column to analyze.

    Returns:
        List of z-scores (None for non-numeric values).

    Raises:
        ValueError: If standard deviation is zero.
    """
    stats = calculate_statistics(data, column)
    mean = stats['mean']
    std_dev = stats['std_dev']

    if std_dev == 0:
        raise ValueError("Cannot calculate z-scores when standard deviation is zero")

    z_scores = []
    for row in data:
        value = row.get(column)
        if isinstance(value, (int, float)):
            z_scores.append((value - mean) / std_dev)
        else:
            z_scores.append(None)

    return z_scores
