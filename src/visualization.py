"""Data visualization tools for scientific data analysis."""

import os
from typing import Dict, List, Any, Optional, Tuple

try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


def create_scatter_plot(
    data: List[Dict[str, Any]],
    column_x: str,
    column_y: str,
    output_path: str,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 8)
) -> str:
    """
    Create a scatter plot from data.

    Args:
        data: List of dictionaries representing the data.
        column_x: Name of the column for x-axis.
        column_y: Name of the column for y-axis.
        output_path: Path to save the plot.
        title: Plot title (optional).
        xlabel: X-axis label (optional).
        ylabel: Y-axis label (optional).
        figsize: Figure size as (width, height).

    Returns:
        Path to the saved plot.

    Raises:
        ImportError: If matplotlib is not available.
        ValueError: If no valid data points found.
    """
    if not MATPLOTLIB_AVAILABLE:
        raise ImportError("matplotlib is required for visualization")

    pairs = [
        (row.get(column_x), row.get(column_y))
        for row in data
        if isinstance(row.get(column_x), (int, float))
        and isinstance(row.get(column_y), (int, float))
    ]

    if not pairs:
        raise ValueError("No valid data points found for scatter plot")

    x_values = [p[0] for p in pairs]
    y_values = [p[1] for p in pairs]

    fig, ax = plt.subplots(figsize=figsize)
    ax.scatter(x_values, y_values, alpha=0.6, edgecolors='black', linewidth=0.5)

    ax.set_title(title or f"{column_y} vs {column_x}")
    ax.set_xlabel(xlabel or column_x)
    ax.set_ylabel(ylabel or column_y)
    ax.grid(True, alpha=0.3)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close(fig)

    return output_path


def create_histogram(
    data: List[Dict[str, Any]],
    column: str,
    output_path: str,
    bins: int = 20,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: str = "Frequency",
    figsize: Tuple[int, int] = (10, 8)
) -> str:
    """
    Create a histogram from data.

    Args:
        data: List of dictionaries representing the data.
        column: Name of the column to plot.
        output_path: Path to save the plot.
        bins: Number of histogram bins.
        title: Plot title (optional).
        xlabel: X-axis label (optional).
        ylabel: Y-axis label (default: "Frequency").
        figsize: Figure size as (width, height).

    Returns:
        Path to the saved plot.

    Raises:
        ImportError: If matplotlib is not available.
        ValueError: If no valid values found.
    """
    if not MATPLOTLIB_AVAILABLE:
        raise ImportError("matplotlib is required for visualization")

    values = [row.get(column) for row in data if isinstance(row.get(column), (int, float))]

    if not values:
        raise ValueError(f"No valid values found in column '{column}'")

    fig, ax = plt.subplots(figsize=figsize)
    ax.hist(values, bins=bins, edgecolor='black', alpha=0.7)

    ax.set_title(title or f"Distribution of {column}")
    ax.set_xlabel(xlabel or column)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3, axis='y')

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close(fig)

    return output_path


def create_line_plot(
    data: List[Dict[str, Any]],
    column_x: str,
    column_y: str,
    output_path: str,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 8)
) -> str:
    """
    Create a line plot from data.

    Args:
        data: List of dictionaries representing the data.
        column_x: Name of the column for x-axis.
        column_y: Name of the column for y-axis.
        output_path: Path to save the plot.
        title: Plot title (optional).
        xlabel: X-axis label (optional).
        ylabel: Y-axis label (optional).
        figsize: Figure size as (width, height).

    Returns:
        Path to the saved plot.

    Raises:
        ImportError: If matplotlib is not available.
        ValueError: If no valid data points found.
    """
    if not MATPLOTLIB_AVAILABLE:
        raise ImportError("matplotlib is required for visualization")

    pairs = [
        (row.get(column_x), row.get(column_y))
        for row in data
        if isinstance(row.get(column_x), (int, float))
        and isinstance(row.get(column_y), (int, float))
    ]

    if not pairs:
        raise ValueError("No valid data points found for line plot")

    # Sort by x values
    pairs.sort(key=lambda p: p[0])
    x_values = [p[0] for p in pairs]
    y_values = [p[1] for p in pairs]

    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(x_values, y_values, marker='o', linewidth=2, markersize=4)

    ax.set_title(title or f"{column_y} vs {column_x}")
    ax.set_xlabel(xlabel or column_x)
    ax.set_ylabel(ylabel or column_y)
    ax.grid(True, alpha=0.3)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close(fig)

    return output_path


def create_bar_chart(
    categories: List[str],
    values: List[float],
    output_path: str,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 8)
) -> str:
    """
    Create a bar chart from categories and values.

    Args:
        categories: List of category names.
        values: List of values for each category.
        output_path: Path to save the plot.
        title: Plot title (optional).
        xlabel: X-axis label (optional).
        ylabel: Y-axis label (optional).
        figsize: Figure size as (width, height).

    Returns:
        Path to the saved plot.

    Raises:
        ImportError: If matplotlib is not available.
        ValueError: If categories and values have different lengths.
    """
    if not MATPLOTLIB_AVAILABLE:
        raise ImportError("matplotlib is required for visualization")

    if len(categories) != len(values):
        raise ValueError("Categories and values must have the same length")

    fig, ax = plt.subplots(figsize=figsize)
    ax.bar(categories, values, edgecolor='black', alpha=0.7)

    ax.set_title(title or "Bar Chart")
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3, axis='y')

    # Rotate labels if there are many categories
    if len(categories) > 5:
        plt.xticks(rotation=45, ha='right')

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close(fig)

    return output_path


def create_box_plot(
    data: List[Dict[str, Any]],
    columns: List[str],
    output_path: str,
    title: Optional[str] = None,
    ylabel: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 8)
) -> str:
    """
    Create a box plot for one or more columns.

    Args:
        data: List of dictionaries representing the data.
        columns: List of column names to include in the box plot.
        output_path: Path to save the plot.
        title: Plot title (optional).
        ylabel: Y-axis label (optional).
        figsize: Figure size as (width, height).

    Returns:
        Path to the saved plot.

    Raises:
        ImportError: If matplotlib is not available.
        ValueError: If no valid values found.
    """
    if not MATPLOTLIB_AVAILABLE:
        raise ImportError("matplotlib is required for visualization")

    plot_data = []
    valid_columns = []

    for col in columns:
        values = [row.get(col) for row in data if isinstance(row.get(col), (int, float))]
        if values:
            plot_data.append(values)
            valid_columns.append(col)

    if not plot_data:
        raise ValueError("No valid values found for box plot")

    fig, ax = plt.subplots(figsize=figsize)
    ax.boxplot(plot_data, tick_labels=valid_columns)

    ax.set_title(title or "Box Plot")
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3, axis='y')

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close(fig)

    return output_path
