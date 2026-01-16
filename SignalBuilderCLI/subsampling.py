"""Subsampling module for re-evaluating signals at different resolutions.

This module provides two methods for subsampling:
1. Simple re-evaluation (default): Re-evaluates the signal at new time points
   using the original generation parameters. NO filtering is applied.
2. Anti-aliasing subsampling (optional): Applies low-pass filter before subsampling.

For signal reconstruction/super-resolution tasks, the simple method is preferred
as it preserves high-frequency information in the target signal.
"""
import numpy as np

try:
    from .splines import tension_spline_interpolator, zero_order_spline_interpolator
except ImportError:
    from splines import tension_spline_interpolator, zero_order_spline_interpolator


def resample_signal_from_params(
    t_new: np.ndarray, 
    t_start: float,
    t_end: float,
    fs_high: float,
    base_points: list,
    tau_frequency: float,
    amp_knots: list,
    amp_values: list,
    tau_amplitude: float,
    amplitude_spline_type: str,
    vertical_offset: float,
    noise_profile: dict,
    rng: np.random.Generator
) -> np.ndarray:
    """Re-evaluate a signal at new time points using the original generation parameters.
    
    This function reconstructs the signal generation process at different time points,
    allowing for true re-evaluation rather than simple interpolation of existing samples.
    
    NO FILTERING IS APPLIED - this preserves all frequency content for reconstruction tasks.
    
    Parameters
    ----------
    t_new : np.ndarray
        New time array for evaluation.
    t_start : float
        Original signal start time.
    t_end : float
        Original signal end time.
    fs_high : float
        Original high sampling frequency.
    base_points : list
        Frequency profile base points [(t, f), ...].
    tau_frequency : float
        Tension parameter for frequency spline.
    amp_knots : list
        Amplitude envelope knot times.
    amp_values : list
        Amplitude envelope knot values.
    tau_amplitude : float
        Tension parameter for amplitude spline (None for zero-order).
    amplitude_spline_type : str
        'tension' or 'zero_order'.
    vertical_offset : float
        Vertical offset to add.
    noise_profile : dict
        Noise profile metadata dict.
    rng : np.random.Generator
        Random number generator.
        
    Returns
    -------
    np.ndarray
        Signal evaluated at t_new time points (clean, without noise).
    """
    # Reconstruct frequency profile
    base_times = np.array([p[0] for p in base_points])
    base_freqs = np.array([p[1] for p in base_points])
    freq_interp = tension_spline_interpolator(base_times, base_freqs, tau=tau_frequency)
    inst_freq = freq_interp(t_new)
    
    # Reconstruct amplitude envelope
    if amplitude_spline_type == 'zero_order':
        amp_points = list(zip(amp_knots, amp_values))
        amp_interp = zero_order_spline_interpolator(amp_points)
        amp_envelope = amp_interp(t_new)
    else:  # tension spline
        amp_interp = tension_spline_interpolator(
            np.array(amp_knots), 
            np.array(amp_values), 
            tau=tau_amplitude
        )
        amp_envelope = amp_interp(t_new)
    
    # Compute phase (integrate frequency)
    dt = np.mean(np.diff(t_new))  # Average time step
    phase = 2 * np.pi * np.cumsum(inst_freq) * dt
    
    # Generate clean signal
    clean_signal = amp_envelope * np.sin(phase) + vertical_offset
    
    # Note: Noise is NOT re-applied for subsampled versions
    # We return the clean signal at the new time points
    return clean_signal


def subsample_simple(
    t_original: np.ndarray,
    signal_original: np.ndarray,
    t_start: float,
    t_end: float,
    target_size: int,
) -> tuple:
    """Simple subsampling by linear interpolation (NO filtering).
    
    This is the default method - no anti-aliasing filter is applied.
    The signal is simply interpolated to the new time points.
    
    Parameters
    ----------
    t_original : np.ndarray
        Original time array.
    signal_original : np.ndarray
        Original signal array.
    t_start : float
        Signal start time.
    t_end : float
        Signal end time.
    target_size : int
        Target number of samples.
        
    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        (t_new, signal_new)
    """
    t_new = np.linspace(t_start, t_end, target_size)
    signal_new = np.interp(t_new, t_original, signal_original)
    return t_new, signal_new


def generate_subsampled_versions(
    signal_metadata: dict, 
    t_start: float,
    t_end: float,
    subsample_sizes: list,
    rng: np.random.Generator,
    use_antialiasing: bool = False,
    t_original: np.ndarray = None,
    signal_original: np.ndarray = None,
    filter_type: str = 'butter',
    filter_order: int = 8,
) -> dict:
    """Generate multiple subsampled versions of a signal.
    
    Parameters
    ----------
    signal_metadata : dict
        Metadata dictionary from high-resolution signal.
    t_start : float
        Signal start time.
    t_end : float
        Signal end time.
    subsample_sizes : list
        List of subsample sizes (e.g., [150, 250, 500, 1000]).
    rng : np.random.Generator
        Random number generator.
    use_antialiasing : bool
        If True, apply anti-aliasing filter before subsampling.
        Default is False (simple re-evaluation).
    t_original : np.ndarray, optional
        Original time array (required if use_antialiasing=True).
    signal_original : np.ndarray, optional
        Original signal array (required if use_antialiasing=True).
    filter_type : str
        Type of anti-aliasing filter ('butter', 'cheby1', 'ellip').
    filter_order : int
        Filter order.
        
    Returns
    -------
    dict
        Dictionary mapping subsample size to (t_new, signal_new) tuples.
    """
    subsampled_signals = {}
    
    for size in subsample_sizes:
        if use_antialiasing:
            # Import here to avoid circular dependency
            try:
                from .antialiasing import subsample_with_antialiasing
            except ImportError:
                from antialiasing import subsample_with_antialiasing
            
            if t_original is None or signal_original is None:
                raise ValueError(
                    "t_original and signal_original are required when use_antialiasing=True"
                )
            
            t_new, signal_new = subsample_with_antialiasing(
                signal_data=signal_original,
                t_original=t_original,
                t_start=t_start,
                t_end=t_end,
                target_size=size,
                filter_type=filter_type,
                order=filter_order,
            )
        else:
            # Simple re-evaluation (default, no filtering)
            t_new = np.linspace(t_start, t_end, size)
            signal_new = resample_signal_from_params(
                t_new=t_new,
                t_start=t_start,
                t_end=t_end,
                fs_high=signal_metadata['fs_high'],
                base_points=signal_metadata['base_points'],
                tau_frequency=signal_metadata['tau_frequency'],
                amp_knots=signal_metadata['amp_knots'],
                amp_values=signal_metadata['amp_values'],
                tau_amplitude=signal_metadata['tau_amplitude'],
                amplitude_spline_type=signal_metadata['amplitude_spline_type'],
                vertical_offset=signal_metadata['vertical_offset'],
                noise_profile=signal_metadata['noise_profile'],
                rng=rng
            )
        
        subsampled_signals[size] = (t_new, signal_new)
    
    return subsampled_signals
