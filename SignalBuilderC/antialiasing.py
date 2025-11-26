"""Anti-aliasing filtering module for subsampling with proper frequency control."""
import numpy as np
from scipy import signal


def design_antialiasing_filter(fs_original: float, fs_target: float, 
                               filter_type: str = 'butter', 
                               order: int = 8) -> tuple:
    """Design an anti-aliasing low-pass filter for subsampling.
    
    The filter cutoff frequency is set to ensure no aliasing occurs when
    downsampling from fs_original to fs_target.
    
    Args:
        fs_original: Original sampling frequency (Hz)
        fs_target: Target sampling frequency after subsampling (Hz)
        filter_type: Type of filter ('butter' for Butterworth, 'cheby1', 'ellip')
        order: Filter order (higher = sharper cutoff, default=8)
        
    Returns:
        (b, a): Filter coefficients for scipy.signal.filtfilt
        
    Notes:
        - Nyquist frequency for target is fs_target / 2
        - We set cutoff slightly below Nyquist to ensure no aliasing
        - Uses filtfilt for zero-phase filtering (no time shift)
    """
    # Target Nyquist frequency
    nyquist_target = fs_target / 2.0
    
    # Set cutoff at 90% of target Nyquist to have safety margin
    cutoff_freq = 0.9 * nyquist_target
    
    # Normalize by original Nyquist
    nyquist_original = fs_original / 2.0
    normalized_cutoff = cutoff_freq / nyquist_original
    
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


def apply_antialiasing_filter(signal_data: np.ndarray, 
                              fs_original: float, 
                              fs_target: float,
                              filter_type: str = 'butter',
                              order: int = 8) -> np.ndarray:
    """Apply anti-aliasing filter to signal before subsampling.
    
    Args:
        signal_data: Signal array to filter
        fs_original: Original sampling frequency
        fs_target: Target sampling frequency after subsampling
        filter_type: Type of filter to use
        order: Filter order
        
    Returns:
        Filtered signal array (same length as input)
    """
    # Design filter
    b, a = design_antialiasing_filter(fs_original, fs_target, filter_type, order)
    
    # Apply zero-phase filtering (no time shift)
    filtered_signal = signal.filtfilt(b, a, signal_data)
    
    return filtered_signal


def subsample_with_antialiasing(signal_data: np.ndarray,
                                t_original: np.ndarray,
                                t_start: float,
                                t_end: float,
                                target_size: int,
                                filter_type: str = 'butter',
                                order: int = 8) -> tuple:
    """Subsample signal with anti-aliasing filtering.
    
    This is the proper way to subsample according to reviewers' requirements:
    1. Apply low-pass anti-aliasing filter
    2. Resample to target resolution
    
    Args:
        signal_data: High-resolution signal array
        t_original: High-resolution time array
        t_start: Signal start time
        t_end: Signal end time
        target_size: Target number of samples
        filter_type: Type of anti-aliasing filter
        order: Filter order
        
    Returns:
        (t_new, signal_new): New time array and subsampled signal
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
    
    Args:
        filter_type: Type of filter
        order: Filter order
        
    Returns:
        Dictionary with filter information
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
