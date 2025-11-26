"""Main signal generation function."""
import numpy as np
from .frequency_profiles import generate_non_uniform_high_low_frequency_points
from .splines import tension_spline_interpolator
from .amplitude_envelopes import generate_random_amplitude_envelope
from .noise_profiles import NoiseProfileConfig, apply_noise_profile


def generate_demo_signal(t_start: float,
                         t_end: float,
                         fs_high: float,
                         noise_config: NoiseProfileConfig,
                         rng: np.random.Generator):
    """Generate one demo signal with random envelopes and noise.

    Frequency profile uses tau aleatorio en [1, 2] (paso 0.05).
    Amplitude envelope uses tau aleatorio en {1,3,5,8,10,12,15,20} con 50% probabilidad
    o step function (50%).
    """
    # High-resolution time axis
    t_high = np.arange(t_start, t_end, 1.0 / fs_high)

    # Frequency profile (API without rng)
    base_points, high_freq_points, variation_type = generate_non_uniform_high_low_frequency_points(
        t_start, t_end
    )
    base_times = np.array([p[0] for p in base_points])
    base_freqs = np.array([p[1] for p in base_points])

    # Spline-based instantaneous frequency with random tau in [1, 2]
    tau_freq = float(rng.choice(np.linspace(1, 2, 21)))
    base_interp = tension_spline_interpolator(base_times, base_freqs, tau=tau_freq)
    inst_freq = base_interp(t_high)

    # Random amplitude envelope using the same t_high grid
    amp_envelope, amp_knots, amp_values, tau_amp, spline_type = generate_random_amplitude_envelope(
        t_high, rng=rng
    )

    # Random vertical offset with normal distribution (concentrated around 0)
    # ~68% within [-3, 3], ~95% within [-6, 6], ~99.7% within [-9, 9]
    offset = rng.normal(loc=0.0, scale=3.0)

    # Phase and clean signal
    phase = 2 * np.pi * np.cumsum(inst_freq) / fs_high
    clean_signal = amp_envelope * np.sin(phase) + offset

    # Apply noise profile with the correct signature
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
        "tau_amplitude": tau_amp if tau_amp is not None else "N/A",
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
