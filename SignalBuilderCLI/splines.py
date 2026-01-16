"""Spline-based utilities for temporal signal generation.

This module contains core spline interpolators used to build amplitude
and frequency envelopes for synthetic temporal signals.
"""

from typing import Callable, Iterable, Sequence, Tuple

import numpy as np
from numpy.random import Generator
from scipy.interpolate import interp1d, make_interp_spline


def tension_spline_interpolator(x: Sequence[float],
                                y: Sequence[float],
                                tau: float) -> Callable[[np.ndarray], np.ndarray]:
    """Create a tension spline interpolator.

    This is equivalent in spirit to the original implementation in
    `temana.py` and is kept as the core envelope builder.
    
    Parameters
    ----------
    x : Sequence[float]
        Knot x-coordinates (must be strictly increasing).
    y : Sequence[float]
        Knot y-values.
    tau : float
        Tension parameter. Higher values produce more linear interpolation.
        
    Returns
    -------
    Callable
        Function that evaluates the spline at given x values.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(x) - 1

    h = np.diff(x)
    alpha = 1.0 / h - tau / np.sinh(tau * h)
    beta = tau * np.cosh(tau * h) / np.sinh(tau * h) - 1.0 / h
    gamma = tau**2 * np.diff(y) / h

    A = np.zeros((n + 1, n + 1), dtype=float)
    rhs = np.zeros(n + 1, dtype=float)

    A[0, 0] = 1.0
    A[n, n] = 1.0
    for i in range(1, n):
        A[i, i - 1] = alpha[i - 1]
        A[i, i] = beta[i - 1] + beta[i]
        A[i, i + 1] = alpha[i]
        rhs[i] = gamma[i] - gamma[i - 1]

    z = np.linalg.solve(A, rhs)

    def evaluate(x_eval: np.ndarray) -> np.ndarray:
        x_eval = np.asarray(x_eval, dtype=float)
        result = np.zeros_like(x_eval)
        for i in range(n):
            mask = (x_eval >= x[i]) & (x_eval <= x[i + 1])
            if not np.any(mask):
                continue
            xi = x_eval[mask]
            t1 = z[i] * np.sinh(tau * (x[i + 1] - xi)) + z[i + 1] * np.sinh(
                tau * (xi - x[i])
            )
            t1 /= tau**2 * np.sinh(tau * h[i])
            t2 = (y[i] - z[i] / tau**2) * (x[i + 1] - xi) / h[i]
            t3 = (y[i + 1] - z[i + 1] / tau**2) * (xi - x[i]) / h[i]
            result[mask] = t1 + t2 + t3
        return result

    return evaluate


def zero_order_spline_interpolator(points: Iterable[Tuple[float, float]]) -> Callable[[np.ndarray], np.ndarray]:
    """Create a zero-order (stepwise) interpolator from (x, y) points.
    
    Parameters
    ----------
    points : Iterable[Tuple[float, float]]
        List of (x, y) control points.
        
    Returns
    -------
    Callable
        Function that evaluates the step function at given x values.
    """
    x_coords, y_coords = zip(*points)
    interpolator = interp1d(x_coords, y_coords, kind="zero", fill_value="extrapolate")
    return lambda x: interpolator(np.asarray(x, dtype=float))


def n_degree_spline_interpolator(points: Iterable[Tuple[float, float]],
                                 degree: int) -> Callable[[np.ndarray], np.ndarray]:
    """Create an n-degree spline interpolator from (x, y) points.
    
    Parameters
    ----------
    points : Iterable[Tuple[float, float]]
        List of (x, y) control points.
    degree : int
        Spline degree (1=linear, 2=quadratic, 3=cubic, etc.).
        
    Returns
    -------
    Callable
        Function that evaluates the spline at given x values.
    """
    x_coords, y_coords = zip(*points)
    spline = make_interp_spline(x_coords, y_coords, k=degree)
    return lambda x: spline(np.asarray(x, dtype=float))


def generate_random_amplitude_points(x0: float,
                                     x1: float,
                                     rng: Generator | None = None,
                                     amp_min: int = 1,
                                     amp_max: int = 10) -> Tuple[np.ndarray, np.ndarray]:
    """Generate random amplitude change points.

    This follows the same strategy as the original SignalBuilder constructor:
    - Random amplitude and frequency (with random sign and integer magnitude).
    - Random phase in [0, pi].
    - Random number of interior points between 1 and 4.
    - Partition [x0, x1] uniformly and evaluate a sinusoid, enforcing a
      minimum amplitude floor around 0.5.
      
    Parameters
    ----------
    x0 : float
        Start of interval.
    x1 : float
        End of interval.
    rng : Generator, optional
        NumPy random generator for reproducibility.
    amp_min : int
        Minimum amplitude magnitude.
    amp_max : int
        Maximum amplitude magnitude.
        
    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        (x_coords, y_coords) of the amplitude control points.
    """
    if rng is None:
        rng = np.random.default_rng()

    amplitude = (2 * rng.random() - 1.0) * rng.integers(amp_min, amp_max + 1)
    frequency = (2 * rng.random() - 1.0) * rng.integers(1, 10)
    phase = rng.random() * np.pi

    num_points = int(rng.integers(1, 5))
    partition = np.linspace(x0, x1, num_points + 2)

    x_coords = []
    y_coords = []

    for x in partition:
        y = amplitude * np.sin(frequency * (x - phase))
        y = abs(y)
        if y < 0.5:
            y = abs(amplitude * rng.uniform(0.5, 1.0))
        x_coords.append(float(x))
        y_coords.append(float(y))

    return np.asarray(x_coords, dtype=float), np.asarray(y_coords, dtype=float)


def generate_random_amplitude_envelope(t: np.ndarray,
                                       tau: float,
                                       rng: Generator | None = None
                                       ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generate a random amplitude envelope over ``t`` using a tension spline.

    Parameters
    ----------
    t : np.ndarray
        Time axis where the envelope will be evaluated.
    tau : float
        Tension parameter for the spline.
    rng : Generator, optional
        NumPy Generator for reproducibility.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray, np.ndarray]
        (amp_envelope, amp_knots, amp_values) - The evaluated envelope 
        and the underlying spline control points.
    """
    t = np.asarray(t, dtype=float)
    x0 = float(t[0])
    x1 = float(t[-1])

    amp_knots, amp_values = generate_random_amplitude_points(x0, x1, rng=rng)
    interpolator = tension_spline_interpolator(amp_knots, amp_values, tau=tau)
    amp_envelope = interpolator(t)

    return amp_envelope, amp_knots, amp_values
