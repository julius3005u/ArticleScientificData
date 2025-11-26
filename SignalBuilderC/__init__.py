"""SignalBuilderV02 core package.

This package provides building blocks for generating synthetic temporal
signals with spline-based envelopes and non-uniform frequency profiles.
All comments and documentation are written in English.
"""

from .splines import tension_spline_interpolator, zero_order_spline_interpolator, n_degree_spline_interpolator
from .frequency_profiles import generate_non_uniform_high_low_frequency_points

__all__ = [
    "tension_spline_interpolator",
    "zero_order_spline_interpolator",
    "n_degree_spline_interpolator",
    "generate_non_uniform_high_low_frequency_points",
]
