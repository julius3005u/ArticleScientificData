"""Tests for analysis module."""

import pytest
import math
from src.analysis import (
    calculate_statistics,
    perform_correlation_analysis,
    perform_linear_regression,
    calculate_percentile,
    calculate_z_scores
)


class TestCalculateStatistics:
    """Tests for calculate_statistics function."""

    def test_basic_statistics(self):
        data = [
            {'value': 10},
            {'value': 20},
            {'value': 30},
            {'value': 40},
            {'value': 50}
        ]
        stats = calculate_statistics(data, 'value')

        assert stats['mean'] == 30.0
        assert stats['median'] == 30.0
        assert stats['count'] == 5
        assert stats['min'] == 10
        assert stats['max'] == 50
        assert stats['std_dev'] == pytest.approx(14.142, rel=0.01)

    def test_even_count_median(self):
        data = [
            {'value': 10},
            {'value': 20},
            {'value': 30},
            {'value': 40}
        ]
        stats = calculate_statistics(data, 'value')
        assert stats['median'] == 25.0

    def test_no_numeric_values(self):
        data = [{'value': 'text'}, {'value': 'more text'}]
        with pytest.raises(ValueError, match="No numeric values"):
            calculate_statistics(data, 'value')

    def test_mixed_values(self):
        data = [
            {'value': 10},
            {'value': 'text'},
            {'value': 30}
        ]
        stats = calculate_statistics(data, 'value')
        assert stats['count'] == 2
        assert stats['mean'] == 20.0


class TestPerformCorrelationAnalysis:
    """Tests for perform_correlation_analysis function."""

    def test_perfect_positive_correlation(self):
        data = [
            {'x': 1, 'y': 2},
            {'x': 2, 'y': 4},
            {'x': 3, 'y': 6},
            {'x': 4, 'y': 8}
        ]
        result = perform_correlation_analysis(data, 'x', 'y')
        assert result['correlation'] == pytest.approx(1.0, rel=0.001)

    def test_perfect_negative_correlation(self):
        data = [
            {'x': 1, 'y': 8},
            {'x': 2, 'y': 6},
            {'x': 3, 'y': 4},
            {'x': 4, 'y': 2}
        ]
        result = perform_correlation_analysis(data, 'x', 'y')
        assert result['correlation'] == pytest.approx(-1.0, rel=0.001)

    def test_insufficient_data(self):
        data = [{'x': 1, 'y': 2}]
        with pytest.raises(ValueError, match="Insufficient data"):
            perform_correlation_analysis(data, 'x', 'y')


class TestPerformLinearRegression:
    """Tests for perform_linear_regression function."""

    def test_perfect_linear_relationship(self):
        data = [
            {'x': 1, 'y': 3},
            {'x': 2, 'y': 5},
            {'x': 3, 'y': 7},
            {'x': 4, 'y': 9}
        ]
        result = perform_linear_regression(data, 'x', 'y')
        assert result['slope'] == pytest.approx(2.0, rel=0.001)
        assert result['intercept'] == pytest.approx(1.0, rel=0.001)
        assert result['r_squared'] == pytest.approx(1.0, rel=0.001)

    def test_insufficient_data(self):
        data = [{'x': 1, 'y': 2}]
        with pytest.raises(ValueError, match="Insufficient data"):
            perform_linear_regression(data, 'x', 'y')


class TestCalculatePercentile:
    """Tests for calculate_percentile function."""

    def test_median_percentile(self):
        data = [
            {'value': 10},
            {'value': 20},
            {'value': 30},
            {'value': 40},
            {'value': 50}
        ]
        result = calculate_percentile(data, 'value', 50)
        assert result == 30.0

    def test_invalid_percentile_high(self):
        data = [{'value': 10}]
        with pytest.raises(ValueError, match="Percentile must be between"):
            calculate_percentile(data, 'value', 110)

    def test_invalid_percentile_low(self):
        data = [{'value': 10}]
        with pytest.raises(ValueError, match="Percentile must be between"):
            calculate_percentile(data, 'value', -5)


class TestCalculateZScores:
    """Tests for calculate_z_scores function."""

    def test_z_scores_calculation(self):
        data = [
            {'value': 10},
            {'value': 20},
            {'value': 30}
        ]
        z_scores = calculate_z_scores(data, 'value')

        assert len(z_scores) == 3
        # Mean = 20, std_dev ≈ 8.16
        assert z_scores[0] == pytest.approx(-1.224, rel=0.01)
        assert z_scores[1] == pytest.approx(0.0, rel=0.01)
        assert z_scores[2] == pytest.approx(1.224, rel=0.01)

    def test_z_scores_with_zero_std_dev(self):
        data = [
            {'value': 10},
            {'value': 10},
            {'value': 10}
        ]
        with pytest.raises(ValueError, match="standard deviation is zero"):
            calculate_z_scores(data, 'value')
