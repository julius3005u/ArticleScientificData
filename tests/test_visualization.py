"""Tests for visualization module."""

import os
import tempfile
import pytest

# Check if matplotlib is available for testing
try:
    import matplotlib
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

from src.visualization import (
    create_scatter_plot,
    create_histogram,
    create_line_plot,
    create_bar_chart,
    create_box_plot
)


@pytest.fixture
def sample_data():
    """Provide sample data for visualization tests."""
    return [
        {'x': 1, 'y': 2, 'value': 10},
        {'x': 2, 'y': 4, 'value': 20},
        {'x': 3, 'y': 6, 'value': 30},
        {'x': 4, 'y': 8, 'value': 40},
        {'x': 5, 'y': 10, 'value': 50}
    ]


@pytest.fixture
def temp_output_path():
    """Provide a temporary output path for plots."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield os.path.join(tmpdir, 'test_plot.png')


@pytest.mark.skipif(not MATPLOTLIB_AVAILABLE, reason="matplotlib not available")
class TestCreateScatterPlot:
    """Tests for create_scatter_plot function."""

    def test_create_scatter_plot(self, sample_data, temp_output_path):
        result = create_scatter_plot(sample_data, 'x', 'y', temp_output_path)
        assert os.path.exists(result)

    def test_scatter_plot_with_custom_labels(self, sample_data, temp_output_path):
        result = create_scatter_plot(
            sample_data, 'x', 'y', temp_output_path,
            title="Test Title",
            xlabel="X Label",
            ylabel="Y Label"
        )
        assert os.path.exists(result)

    def test_scatter_plot_no_valid_data(self, temp_output_path):
        data = [{'x': 'a', 'y': 'b'}]
        with pytest.raises(ValueError, match="No valid data points"):
            create_scatter_plot(data, 'x', 'y', temp_output_path)


@pytest.mark.skipif(not MATPLOTLIB_AVAILABLE, reason="matplotlib not available")
class TestCreateHistogram:
    """Tests for create_histogram function."""

    def test_create_histogram(self, sample_data, temp_output_path):
        result = create_histogram(sample_data, 'value', temp_output_path)
        assert os.path.exists(result)

    def test_histogram_custom_bins(self, sample_data, temp_output_path):
        result = create_histogram(sample_data, 'value', temp_output_path, bins=5)
        assert os.path.exists(result)

    def test_histogram_no_valid_values(self, temp_output_path):
        data = [{'value': 'text'}]
        with pytest.raises(ValueError, match="No valid values"):
            create_histogram(data, 'value', temp_output_path)


@pytest.mark.skipif(not MATPLOTLIB_AVAILABLE, reason="matplotlib not available")
class TestCreateLinePlot:
    """Tests for create_line_plot function."""

    def test_create_line_plot(self, sample_data, temp_output_path):
        result = create_line_plot(sample_data, 'x', 'y', temp_output_path)
        assert os.path.exists(result)


@pytest.mark.skipif(not MATPLOTLIB_AVAILABLE, reason="matplotlib not available")
class TestCreateBarChart:
    """Tests for create_bar_chart function."""

    def test_create_bar_chart(self, temp_output_path):
        categories = ['A', 'B', 'C']
        values = [10, 20, 30]
        result = create_bar_chart(categories, values, temp_output_path)
        assert os.path.exists(result)

    def test_bar_chart_mismatched_lengths(self, temp_output_path):
        categories = ['A', 'B']
        values = [10]
        with pytest.raises(ValueError, match="same length"):
            create_bar_chart(categories, values, temp_output_path)


@pytest.mark.skipif(not MATPLOTLIB_AVAILABLE, reason="matplotlib not available")
class TestCreateBoxPlot:
    """Tests for create_box_plot function."""

    def test_create_box_plot(self, sample_data, temp_output_path):
        result = create_box_plot(sample_data, ['x', 'y', 'value'], temp_output_path)
        assert os.path.exists(result)

    def test_box_plot_no_valid_data(self, temp_output_path):
        data = [{'x': 'text', 'y': 'text'}]
        with pytest.raises(ValueError, match="No valid values"):
            create_box_plot(data, ['x', 'y'], temp_output_path)
