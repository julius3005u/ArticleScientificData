"""Main signal generation function."""
import numpy as np

try:
    from .frequency_profiles import generate_non_uniform_high_low_frequency_points
    from .splines import tension_spline_interpolator
    from .amplitude_envelopes import generate_random_amplitude_envelope
    from .noise_profiles import NoiseProfileConfig, apply_noise_profile
except ImportError:
    from frequency_profiles import generate_non_uniform_high_low_frequency_points
    from splines import tension_spline_interpolator
    from amplitude_envelopes import generate_random_amplitude_envelope
    from noise_profiles import NoiseProfileConfig, apply_noise_profile


def generate_demo_signal(
    t_start: float,
    t_end: float,
    fs_high: float,
    noise_config: NoiseProfileConfig,
    rng: np.random.Generator,
    # Frequency parameters
    tau_freq_min: float = 1.0,
    tau_freq_max: float = 2.0,
    high_freq_min: float = 20.0,
    high_freq_max: float = 100.0,
    low_freq_min: float = 1.0,
    low_freq_max: float = 5.0,
    # Amplitude parameters
    p_tension_spline: float = 0.5,
    tau_amp_min: float = 0.5,
    tau_amp_max: float = 2.5,
    amp_min: int = 1,
    amp_max: int = 8,
    # Offset parameters
    offset_mean: float = 0.0,
    offset_std: float = 3.0,
):
    """Generate one synthetic signal with random envelopes and noise.

    Parameters
    ----------
    t_start : float
        Start time.
    t_end : float
        End time.
    fs_high : float
        High-resolution sampling frequency.
    noise_config : NoiseProfileConfig
        Noise configuration.
    rng : np.random.Generator
        Random generator for reproducibility.
    tau_freq_min : float
        Minimum tau for frequency spline.
    tau_freq_max : float
        Maximum tau for frequency spline.
    high_freq_min : float
        Minimum high frequency (Hz).
    high_freq_max : float
        Maximum high frequency (Hz).
    low_freq_min : float
        Minimum low frequency (Hz).
    low_freq_max : float
        Maximum low frequency (Hz).
    p_tension_spline : float
        Probability of using tension spline for amplitude (vs step).
    tau_amp_min : float
        Minimum tau for amplitude tension spline.
    tau_amp_max : float
        Maximum tau for amplitude tension spline.
    amp_min : int
        Minimum amplitude magnitude.
    amp_max : int
        Maximum amplitude magnitude.
    offset_mean : float
        Mean of vertical offset distribution.
    offset_std : float
        Std of vertical offset distribution.
        
    Returns
    -------
    Tuple
        (t_high, clean_signal, noisy_signal, signal_metadata)
    """
    # High-resolution time axis
    t_high = np.arange(t_start, t_end, 1.0 / fs_high)

    # Frequency profile with configurable ranges
    base_points, high_freq_points, variation_type = generate_non_uniform_high_low_frequency_points(
        t_start, t_end,
        high_freq_min=high_freq_min,
        high_freq_max=high_freq_max,
        low_freq_min=low_freq_min,
        low_freq_max=low_freq_max,
        rng=rng,
    )
    base_times = np.array([p[0] for p in base_points])
    base_freqs = np.array([p[1] for p in base_points])

    # Spline-based instantaneous frequency with random tau from discrete values
    # Matches original: np.linspace(1, 2, 21) - 21 discrete values from 1 to 2
    tau_freq_values = np.linspace(tau_freq_min, tau_freq_max, 21)
    tau_freq = float(rng.choice(tau_freq_values))
    base_interp = tension_spline_interpolator(base_times, base_freqs, tau=tau_freq)
    inst_freq = base_interp(t_high)

    # Random amplitude envelope using the same t_high grid
    amp_envelope, amp_knots, amp_values, tau_amp, spline_type = generate_random_amplitude_envelope(
        t_high, 
        rng=rng,
        p_tension_spline=p_tension_spline,
        tau_amp_min=tau_amp_min,
        tau_amp_max=tau_amp_max,
        amp_min=amp_min,
        amp_max=amp_max,
    )

    # Random vertical offset with normal distribution
    offset = rng.normal(loc=offset_mean, scale=offset_std)

    # Phase and clean signal
    phase = 2 * np.pi * np.cumsum(inst_freq) / fs_high
    clean_signal = amp_envelope * np.sin(phase) + offset

    # Apply noise profile
    noisy_signal, noise_metadata = apply_noise_profile(
        rng=rng,
        clean_signal=clean_signal,
        t_high=t_high,
        t_start=t_start,
        t_end=t_end,
        base_points=base_points,
        variation_type=variation_type,
        config=noise_config,
    )

    signal_metadata = {
        "t_start": float(t_start),
        "t_end": float(t_end),
        "fs_high": float(fs_high),
        "tau_frequency": tau_freq,
        "tau_amplitude": float(tau_amp) if tau_amp is not None else None,
        "amplitude_spline_type": spline_type,
        "vertical_offset": float(offset),
        "base_points": base_points,
        "high_freq_points": high_freq_points,
        "variation_type": variation_type,
        "amp_knots": [float(x) for x in amp_knots],
        "amp_values": [float(y) for y in amp_values],
        "noise_profile": noise_metadata,
    }

    return t_high, clean_signal, noisy_signal, signal_metadata
