"""Random amplitude envelope generation."""
import numpy as np
from .splines import tension_spline_interpolator, zero_order_spline_interpolator


def generate_random_amplitude_envelope(t: np.ndarray, rng=None):
    """Generate a random amplitude envelope over `t` using a tension spline.

    This mirrors the original SignalBuilder amplitude constructor:
    - random amplitude and frequency (with random sign, integer magnitude 1..9),
    - random phase in [0, pi],
    - 1 to 4 interior control points,
    - amplitude floor around 0.5,
    - tau aleatorio en {1,3,5,8,10,12,15,20} con 50% probabilidad,
    - 70% step function (zero-order spline).
    """
    if rng is None:
        rng = np.random.default_rng()

    t = np.asarray(t, dtype=float)
    x0 = float(t[0])
    x1 = float(t[-1])

    # Amplitud más alta (3-15) para mayor contraste visual
    amplitude = (2 * rng.random() - 1.0) * rng.integers(3, 16)
    frequency = (2 * rng.random() - 1.0) * rng.integers(1, 10)
    phase = rng.random() * np.pi

    num_points = int(rng.integers(1, 5))
    partition = np.linspace(x0, x1, num_points + 2)

    amp_knots = []
    amp_values = []
    for x in partition:
        y = amplitude * np.sin(frequency * (x - phase))
        y = abs(y)
        if y < 0.5:
            y = abs(amplitude * rng.uniform(0.5, 1.0))
        amp_knots.append(float(x))
        amp_values.append(float(y))

    amp_knots = np.asarray(amp_knots, dtype=float)
    amp_values = np.asarray(amp_values, dtype=float)

    # 70% step function (variaciones bruscas) vs 30% tension spline
    use_tension = rng.choice([True, False], p=[0.3, 0.7])
    if use_tension:
        tau = float(rng.choice([1, 3, 5, 8, 10, 12, 15, 20]))
        amp_spline = tension_spline_interpolator(amp_knots, amp_values, tau=tau)
        amp_envelope = amp_spline(t)
        spline_type = 'tension'
    else:
        points = list(zip(amp_knots, amp_values))
        amp_spline = zero_order_spline_interpolator(points)
        amp_envelope = amp_spline(t)
        tau = None
        spline_type = 'zero_order'

    return amp_envelope, amp_knots, amp_values, tau, spline_type
