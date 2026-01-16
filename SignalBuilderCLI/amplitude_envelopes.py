"""Random amplitude envelope generation."""
import numpy as np

try:
    from .splines import tension_spline_interpolator, zero_order_spline_interpolator
except ImportError:
    from splines import tension_spline_interpolator, zero_order_spline_interpolator


def generate_random_amplitude_envelope(
    t: np.ndarray, 
    rng: np.random.Generator = None,
    p_tension_spline: float = 0.5,
    tau_amp_min: float = 0.5,
    tau_amp_max: float = 2.5,
    amp_min: int = 1,
    amp_max: int = 8,
):
    """Generate a random amplitude envelope over `t` using a tension spline.

    This mirrors the original SignalBuilder amplitude constructor:
    - Random amplitude and frequency (with random sign, integer magnitude).
    - Random phase in [0, pi].
    - 1 to 4 interior control points.
    - Amplitude floor around 0.5.
    - Configurable probability of tension spline vs step function.
    - NEW: Continuous tau range instead of discrete aggressive values.
    
    Parameters
    ----------
    t : np.ndarray
        Time array for envelope evaluation.
    rng : np.random.Generator, optional
        Random generator for reproducibility.
    p_tension_spline : float
        Probability of using tension spline (vs step function).
        Default 0.5 means 50% step function, 50% tension spline (IMPROVED).
    tau_amp_min : float
        Minimum tau for tension spline (was: 1, now: 0.5 for smoother transitions).
    tau_amp_max : float
        Maximum tau for tension spline (was: 20, now: 2.5 for less aggressive).
    amp_min : int
        Minimum amplitude magnitude (was: 3, now: 1 for more natural variation).
    amp_max : int
        Maximum amplitude magnitude (was: 15, now: 8 for controlled peaks).
        
    Returns
    -------
    Tuple
        (amp_envelope, amp_knots, amp_values, tau, spline_type)
    """
    if rng is None:
        rng = np.random.default_rng()

    t = np.asarray(t, dtype=float)
    x0 = float(t[0])
    x1 = float(t[-1])

    # Random amplitude with configurable range
    amplitude = (2 * rng.random() - 1.0) * rng.integers(amp_min, amp_max + 1)
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

    # Configurable probability: tension spline vs step function
    use_tension = rng.random() < p_tension_spline
    
    if use_tension:
        # Use continuous uniform distribution instead of aggressive discrete choices
        tau = float(rng.uniform(tau_amp_min, tau_amp_max))
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
