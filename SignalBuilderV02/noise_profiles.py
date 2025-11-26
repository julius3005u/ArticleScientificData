"""Noise profile utilities for SignalBuilderV02.

This module provides helper functions to decide if a signal has noise,
which type of noise is used (Gaussian vs structured), and how it is
applied in time.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Dict, Any

import numpy as np

NoiseType = Literal["none", "gaussian", "structured"]


@dataclass
class NoiseProfileConfig:
    """Configuration for noise generation.

    Parameters
    ----------
    p_has_noise : float
        Probability that a given signal will contain any noise at all.
    p_gaussian : float
        Conditional probability that, given there is noise, it is Gaussian.
        The complementary probability (1 - p_gaussian) is used for
        structured noise.
    gaussian_std_relative : float
        Standard deviation of Gaussian noise relative to signal RMS.
    """

    p_has_noise: float = 0.1
    p_gaussian: float = 0.5
    gaussian_std_relative: float = 0.15


def apply_noise_profile(
    rng: np.random.Generator,
    clean_signal: np.ndarray,
    t_high: np.ndarray,
    t_start: float,
    t_end: float,
    base_points,
    variation_type,
    config: NoiseProfileConfig,
) -> tuple[np.ndarray, Dict[str, Any]]:
    """Apply a noise profile to a clean signal.

    This function decides (1) whether the signal has noise at all,
    (2) which noise type is used, and (3) how it is applied. The
    Gaussian case uses the same localized strategies discussed in the
    demo notebook (central time window vs. high-variation segments).

    Returns
    -------
    noisy_signal : np.ndarray
        Signal with noise (or unchanged if no noise is applied).
    noise_metadata : dict
        Dictionary describing the noise type and parameters.
    """

    has_noise_draw = rng.random()
    if has_noise_draw >= config.p_has_noise:
        noise_metadata = {
            "has_noise": False,
            "noise_type": "none",
            "p_has_noise": float(config.p_has_noise),
            "p_gaussian": float(config.p_gaussian),
            "gaussian_std_relative": float(config.gaussian_std_relative),
        }
        return clean_signal, noise_metadata

    noise_type_draw = rng.random()
    if noise_type_draw < config.p_gaussian:
        noise_type: NoiseType = "gaussian"
    else:
        noise_type = "structured"

    if noise_type == "gaussian":
        noisy_signal, detail = _apply_gaussian_localized_noise(
            rng,
            clean_signal,
            t_high,
            t_start,
            t_end,
            base_points,
            variation_type,
            config.gaussian_std_relative,
        )
    else:
        noisy_signal, detail = _apply_structured_noise(
            rng,
            clean_signal,
            t_high,
            t_start,
            t_end,
            base_points,
            variation_type,
        )

    noise_metadata = {
        "has_noise": True,
        "noise_type": noise_type,
        "p_has_noise": float(config.p_has_noise),
        "p_gaussian": float(config.p_gaussian),
        "gaussian_std_relative": float(config.gaussian_std_relative),
        **detail,
    }
    return noisy_signal, noise_metadata


def _apply_gaussian_localized_noise(
    rng: np.random.Generator,
    clean_signal: np.ndarray,
    t_high: np.ndarray,
    t_start: float,
    t_end: float,
    base_points,
    variation_type,
    noise_std_relative: float,
):
    """Apply localized Gaussian noise with two internal strategies.

    Strategy 1 (30%): central time window [0.3 * T, 0.7 * T].
    Strategy 2 (70%): only in segments labeled as "high".
    """

    base_times = np.array([p[0] for p in base_points])
    segment_labels = np.array(variation_type)
    segment_times = base_times

    sample_labels = np.empty_like(t_high, dtype=object)
    seg_idx = 0
    for i, t in enumerate(t_high):
        while seg_idx + 1 < len(segment_times) and t >= segment_times[seg_idx + 1]:
            seg_idx += 1
        sample_labels[i] = segment_labels[seg_idx]

    internal_draw = rng.random()
    if internal_draw < 0.3:
        noise_mask = (t_high >= 0.3 * t_end) & (t_high <= 0.7 * t_end)
        internal_strategy = "central_window"
    else:
        noise_mask = sample_labels == "high"
        internal_strategy = "high_segments"

    # Compute noise std relative to signal RMS to avoid overpowering
    signal_rms = np.sqrt(np.mean(clean_signal**2))
    noise_std = noise_std_relative * signal_rms
    
    noise = rng.normal(loc=0.0, scale=noise_std, size=clean_signal.shape)
    noisy_signal = clean_signal + noise * noise_mask

    detail = {
        "noise_std": float(noise_std),
        "gaussian_internal_strategy": internal_strategy,
    }
    return noisy_signal, detail


def _apply_structured_noise(
    rng: np.random.Generator,
    clean_signal: np.ndarray,
    t_high: np.ndarray,
    t_start: float,
    t_end: float,
    base_points,
    variation_type,
):
    """Apply structured noise in random segments.

    Uses high-frequency sine/cosine oscillations applied to 1-3 random
    segments of the signal. Parameters inspired by the original constructor:
    A = ± [0.1, 0.5] * signal_scale
    B = ± [100, 200]
    """

    # Estimate signal scale for relative noise amplitude
    signal_rms = np.sqrt(np.mean(clean_signal**2))
    
    structured = np.zeros_like(clean_signal)
    
    # Apply noise to 1-3 random segments
    n_segments = rng.integers(1, 4)
    segment_info = []
    
    for _ in range(n_segments):
        # Random segment boundaries
        seg_start = rng.uniform(t_start, t_end * 0.8)
        seg_duration = rng.uniform(0.02 * (t_end - t_start), 0.3 * (t_end - t_start))
        seg_end = min(t_end, seg_start + seg_duration)
        mask = (t_high >= seg_start) & (t_high <= seg_end)
        
        # Choose sine or cosine
        choose = rng.integers(0, 2)
        # Amplitude: [0.1, 0.5] * signal_rms
        A = (2 * rng.random() - 1.0) * rng.uniform(0.1, 0.5) * signal_rms
        # High frequency: [100, 200]
        B = (2 * rng.random() - 1.0) * rng.uniform(100, 200)
        
        if choose == 0:
            structured[mask] += A * np.sin(B * t_high[mask])
        else:
            structured[mask] += A * np.cos(B * t_high[mask])
        
        segment_info.append({
            "start": float(seg_start),
            "end": float(seg_end),
            "amplitude": float(A),
            "frequency": float(B),
            "type": "sin" if choose == 0 else "cos",
        })

    noisy_signal = clean_signal + structured

    detail = {
        "structured_segments": int(n_segments),
        "segment_details": segment_info,
    }
    return noisy_signal, detail
