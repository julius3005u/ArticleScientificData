"""SignalBuilderCLI - Command Line Interface for Synthetic Signal Generation.

This package provides a complete CLI for generating synthetic temporal
signals with spline-based envelopes, non-uniform frequency profiles,
and configurable noise profiles.

Usage:
    python generate_signals_cli.py --help
"""

from .splines import tension_spline_interpolator, zero_order_spline_interpolator, n_degree_spline_interpolator
from .frequency_profiles import generate_non_uniform_high_low_frequency_points
from .amplitude_envelopes import generate_random_amplitude_envelope
from .noise_profiles import NoiseProfileConfig, apply_noise_profile
from .signal_generator import generate_demo_signal
from .subsampling import resample_signal_from_params, generate_subsampled_versions
from .antialiasing import subsample_with_antialiasing, apply_antialiasing_filter
from .data_export import (
    save_signal_npz, save_signal_txt, save_signal_json,
    save_consolidated_signals_npz, save_consolidated_signals_txt, save_consolidated_signals_json,
    save_consolidated_metadata_json
)

__version__ = "1.0.0"
__all__ = [
    "tension_spline_interpolator",
    "zero_order_spline_interpolator", 
    "n_degree_spline_interpolator",
    "generate_non_uniform_high_low_frequency_points",
    "generate_random_amplitude_envelope",
    "NoiseProfileConfig",
    "apply_noise_profile",
    "generate_demo_signal",
    "resample_signal_from_params",
    "generate_subsampled_versions",
    "subsample_with_antialiasing",
    "apply_antialiasing_filter",
]
