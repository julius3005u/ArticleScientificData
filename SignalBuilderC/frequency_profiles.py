"""Frequency profile generators for non-uniform temporal signals.

This module keeps the core idea of mixing low and high frequency
bands across non-uniform temporal segments, as in the original
`generate_non_uniform_high_low_frequency_points` function.
"""

from typing import List, Literal, Tuple

import numpy as np
import random

VariationType = Literal["low", "high", "no_change"]


def generate_non_uniform_high_low_frequency_points(
    x0: float,
    x1: float,
) -> Tuple[List[Tuple[float, float]], List[Tuple[float, float]], List[VariationType]]:
    """Generate non-uniform low/high frequency reference points.

    The design mirrors the original generator, keeping the idea of
    long low-frequency segments with occasional high-frequency bursts.
    """
    high_frequency = np.sort(np.random.uniform(20.0, 100.0, 10))
    low_frequency = np.sort(np.random.uniform(1.0, 5.0, 10))

    num_points = random.randint(2, 11)
    tdom = np.zeros(num_points + 2)
    tdom[-1] = 1.0
    tdom[1:-1] = np.sort(np.random.rand(num_points))
    partition = x0 + (x1 - x0) * tdom

    points: List[Tuple[float, float]] = []
    variation_type: List[VariationType] = []
    high_freq_tdom: List[float] = [tdom[0]]
    high_freq_y: List[float] = []

    current_variation: VariationType = np.random.choice(["low", "high"], p=[0.96, 0.04])  # type: ignore
    y = 1.0

    for i in range(num_points + 2):
        x = partition[i]

        if i == 0:
            if current_variation == "low":
                y = float(np.random.choice(low_frequency))
                variation_type.append("low")
                high_freq_y.append(0.0)
            else:
                y = float(np.random.choice(low_frequency))
                variation_type.append("high")
                high_freq_tdom.append(float(np.random.uniform(partition[i], partition[i + 1], 1)[0]))
                temp_high_freq = float(np.random.choice(high_frequency))
                high_freq_y.append(temp_high_freq)
                high_freq_y.append(temp_high_freq)
        else:
            if variation_type[-1] == "high":
                current_variation = np.random.choice(["low", "no_change"], p=[0.95, 0.05])  # type: ignore
            else:
                current_variation = np.random.choice(
                    ["low", "high", "no_change"],
                    p=[0.20, 0.07, 0.73],
                )  # type: ignore

            if current_variation == "low":
                y = float(np.random.choice(low_frequency))
                high_freq_y.append(0.0)
                high_freq_tdom.append(x)
                variation_type.append("low")
            elif current_variation == "high":
                y = float(np.random.choice(low_frequency))
                variation_type.append("high")
                high_freq_tdom.append(x)
                if i != num_points + 1:
                    temp_high_freq = float(np.random.choice(high_frequency))
                    high_freq_tdom.append(float(np.random.uniform(partition[i], partition[i + 1], 1)[0]))
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
