"""Frequency profile generators for non-uniform temporal signals.

This module keeps the core idea of mixing low and high frequency
bands across non-uniform temporal segments.
"""

from typing import List, Literal, Tuple

import numpy as np

VariationType = Literal["low", "high", "no_change"]


def generate_non_uniform_high_low_frequency_points(
    x0: float,
    x1: float,
    high_freq_min: float = 20.0,
    high_freq_max: float = 100.0,
    low_freq_min: float = 1.0,
    low_freq_max: float = 5.0,
    p_start_high: float = 0.04,
    p_transition_to_high: float = 0.07,
    rng: np.random.Generator = None,
) -> Tuple[List[Tuple[float, float]], List[Tuple[float, float]], List[VariationType]]:
    """Generate non-uniform low/high frequency reference points.

    The design mirrors the original generator, keeping the idea of
    long low-frequency segments with occasional high-frequency bursts.
    
    Parameters
    ----------
    x0 : float
        Start time of the signal.
    x1 : float
        End time of the signal.
    high_freq_min : float
        Minimum high frequency value (Hz).
    high_freq_max : float
        Maximum high frequency value (Hz).
    low_freq_min : float
        Minimum low frequency value (Hz).
    low_freq_max : float
        Maximum low frequency value (Hz).
    p_start_high : float
        Probability of starting in high-frequency mode.
    p_transition_to_high : float
        Probability of transitioning to high-frequency mode.
    rng : np.random.Generator, optional
        Random generator for reproducibility.
        
    Returns
    -------
    Tuple
        (base_points, high_freq_points, variation_type)
    """
    if rng is None:
        rng = np.random.default_rng()
    
    high_frequency = np.sort(rng.uniform(high_freq_min, high_freq_max, 10))
    low_frequency = np.sort(rng.uniform(low_freq_min, low_freq_max, 10))

    num_points = rng.integers(2, 12)
    tdom = np.zeros(num_points + 2)
    tdom[-1] = 1.0
    tdom[1:-1] = np.sort(rng.random(num_points))
    partition = x0 + (x1 - x0) * tdom

    points: List[Tuple[float, float]] = []
    variation_type: List[VariationType] = []
    high_freq_tdom: List[float] = [tdom[0]]
    high_freq_y: List[float] = []

    current_variation: VariationType = rng.choice(
        ["low", "high"], p=[1 - p_start_high, p_start_high]
    )
    y = 1.0

    for i in range(num_points + 2):
        x = partition[i]

        if i == 0:
            if current_variation == "low":
                y = float(rng.choice(low_frequency))
                variation_type.append("low")
                high_freq_y.append(0.0)
            else:
                y = float(rng.choice(low_frequency))
                variation_type.append("high")
                high_freq_tdom.append(float(rng.uniform(partition[i], partition[i + 1])))
                temp_high_freq = float(rng.choice(high_frequency))
                high_freq_y.append(temp_high_freq)
                high_freq_y.append(temp_high_freq)
        else:
            if variation_type[-1] == "high":
                current_variation = rng.choice(["low", "no_change"], p=[0.95, 0.05])
            else:
                current_variation = rng.choice(
                    ["low", "high", "no_change"],
                    p=[0.20, p_transition_to_high, 1 - 0.20 - p_transition_to_high],
                )

            if current_variation == "low":
                y = float(rng.choice(low_frequency))
                high_freq_y.append(0.0)
                high_freq_tdom.append(x)
                variation_type.append("low")
            elif current_variation == "high":
                y = float(rng.choice(low_frequency))
                variation_type.append("high")
                high_freq_tdom.append(x)
                if i != num_points + 1:
                    temp_high_freq = float(rng.choice(high_frequency))
                    high_freq_tdom.append(float(rng.uniform(partition[i], partition[i + 1])))
                    high_freq_y.append(temp_high_freq)
                    high_freq_y.append(temp_high_freq)
                else:
                    high_freq_y.append(0.0)
            else:
                variation_type.append(variation_type[-1])
                high_freq_y.append(0.0)
                high_freq_tdom.append(x)

        points.append((x, y))

    high_freq_points = list(zip(high_freq_tdom, high_freq_y))
    return points, high_freq_points, variation_type
