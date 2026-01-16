"""Anti-aliasing filtering module for subsampling with proper frequency control.

This module is OPTIONAL and only used when --use_antialiasing flag is set.
By default, signals are subsampled WITHOUT filtering to preserve high-frequency
content for reconstruction/super-resolution tasks.
"""
import numpy as np
from scipy import signal


def design_antialiasing_filter(
    fs_original: float, 
    fs_target: float, 
    filter_type: str = 'butter', 
    order: int = 8
) -> tuple:
    """Design an anti-aliasing low-pass filter for subsampling.
    
    The filter cutoff frequency is set to ensure no aliasing occurs when
    downsampling from fs_original to fs_target.
    
    Parameters
    ----------
    fs_original : float
        Original sampling frequency (Hz).
    fs_target : float
        Target sampling frequency after subsampling (Hz).
    filter_type : str
        Type of filter ('butter', 'cheby1', 'ellip').
    order : int
        Filter order (higher = sharper cutoff).
        
    Returns
    -------
    Tuple
        (b, a) filter coefficients for scipy.signal.filtfilt.
    """
    # Target Nyquist frequency
    nyquist_target = fs_target / 2.0
    
    # Set cutoff at 90% of target Nyquist to have safety margin
    cutoff_freq = 0.9 * nyquist_target
    
    # Normalize by original Nyquist
    nyquist_original = fs_original / 2.0
    normalized_cutoff = cutoff_freq / nyquist_original
    
    # Ensure normalized cutoff is valid
    normalized_cutoff = min(normalized_cutoff, 0.99)
    
    # Design filter
    if filter_type == 'butter':
        b, a = signal.butter(order, normalized_cutoff, btype='low', analog=False)
    elif filter_type == 'cheby1':
        b, a = signal.cheby1(order, 0.1, normalized_cutoff, btype='low', analog=False)
    elif filter_type == 'ellip':
        b, a = signal.ellip(order, 0.1, 40, normalized_cutoff, btype='low', analog=False)
    else:
        raise ValueError(f"Unknown filter type: {filter_type}")
    
    return b, a


def apply_antialiasing_filter(
    signal_data: np.ndarray, 
    fs_original: float, 
    fs_target: float,
    filter_type: str = 'butter',
    order: int = 8
) -> np.ndarray:
    """Apply anti-aliasing filter to signal before subsampling.
    
    Parameters
    ----------
    signal_data : np.ndarray
        Signal array to filter.
    fs_original : float
        Original sampling frequency.
    fs_target : float
        Target sampling frequency after subsampling.
    filter_type : str
        Type of filter to use.
    order : int
        Filter order.
        
    Returns
    -------
    np.ndarray
        Filtered signal array (same length as input).
    """
    # Design filter
    b, a = design_antialiasing_filter(fs_original, fs_target, filter_type, order)
    
    # Apply zero-phase filtering (no time shift)
    filtered_signal = signal.filtfilt(b, a, signal_data)
    
    return filtered_signal


def subsample_with_antialiasing(
    signal_data: np.ndarray,
    t_original: np.ndarray,
    t_start: float,
    t_end: float,
    target_size: int,
    filter_type: str = 'butter',
    order: int = 8
) -> tuple:
    """Subsample signal with anti-aliasing filtering.
    
    This applies:
    1. Low-pass anti-aliasing filter
    2. Resample to target resolution
    
    Parameters
    ----------
    signal_data : np.ndarray
        High-resolution signal array.
    t_original : np.ndarray
        High-resolution time array.
    t_start : float
        Signal start time.
    t_end : float
        Signal end time.
    target_size : int
        Target number of samples.
    filter_type : str
        Type of anti-aliasing filter.
    order : int
        Filter order.
        
    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        (t_new, signal_new)
    """
    # Calculate sampling frequencies
    fs_original = len(t_original) / (t_end - t_start)
    fs_target = target_size / (t_end - t_start)
    
    # Apply anti-aliasing filter to original signal
    filtered_signal = apply_antialiasing_filter(
        signal_data, fs_original, fs_target, filter_type, order
    )
    
    # Create new time array
    t_new = np.linspace(t_start, t_end, target_size)
    
    # Interpolate filtered signal to new time points
    signal_new = np.interp(t_new, t_original, filtered_signal)
    
    return t_new, signal_new


def get_filter_info(filter_type: str = 'butter', order: int = 8) -> dict:
    """Get filter information for documentation.
    
    Parameters
    ----------
    filter_type : str
        Type of filter.
    order : int
        Filter order.
        
    Returns
    -------
    dict
        Dictionary with filter information.
    """
    info = {
        'filter_type': filter_type,
        'order': order,
        'description': '',
        'cutoff_frequency': 'Set at 90% of target Nyquist frequency',
        'phase_response': 'Zero-phase (using filtfilt)',
        'purpose': 'Prevent aliasing when downsampling to lower resolutions'
    }
    
    if filter_type == 'butter':
        info['description'] = 'Butterworth low-pass filter - maximally flat passband'
    elif filter_type == 'cheby1':
        info['description'] = 'Chebyshev Type I filter - sharper cutoff with passband ripple'
    elif filter_type == 'ellip':
        info['description'] = 'Elliptic filter - sharpest cutoff with ripple in both bands'
    
    return info
