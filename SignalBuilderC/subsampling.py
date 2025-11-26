"""Subsampling module for re-evaluating signals at different resolutions."""
import numpy as np
from .splines import tension_spline_interpolator, zero_order_spline_interpolator
from .amplitude_envelopes import generate_random_amplitude_envelope


def resample_signal_from_params(t_new: np.ndarray, 
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
                                 rng: np.random.Generator) -> np.ndarray:
    """Re-evaluate a signal at new time points using the original generation parameters.
    
    This function reconstructs the signal generation process at different time points,
    allowing for true re-evaluation rather than simple interpolation of existing samples.
    
    Args:
        t_new: New time array for evaluation
        t_start: Original signal start time
        t_end: Original signal end time
        fs_high: Original high sampling frequency
        base_points: Frequency profile base points [(t, f), ...]
        tau_frequency: Tension parameter for frequency spline
        amp_knots: Amplitude envelope knot times
        amp_values: Amplitude envelope knot values
        tau_amplitude: Tension parameter for amplitude spline (None for zero-order)
        amplitude_spline_type: 'tension' or 'zero_order'
        vertical_offset: Vertical offset to add
        noise_profile: Noise profile metadata dict
        rng: Random number generator
        
    Returns:
        Signal evaluated at t_new time points
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


def generate_subsampled_versions(signal_metadata: dict, 
                                 t_start: float,
                                 t_end: float,
                                 subsample_sizes: list,
                                 rng: np.random.Generator) -> dict:
    """Generate multiple subsampled versions of a signal by re-evaluation.
    
    Args:
        signal_metadata: Metadata dictionary from high-resolution signal
        t_start: Signal start time
        t_end: Signal end time
        subsample_sizes: List of subsample sizes (e.g., [150, 250, 500, 1000])
        rng: Random number generator
        
    Returns:
        Dictionary mapping subsample size to (t_new, signal_new) tuples
    """
    subsampled_signals = {}
    
    for size in subsample_sizes:
        # Create new time array
        t_new = np.linspace(t_start, t_end, size)
        
        # Re-evaluate signal at new time points
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
