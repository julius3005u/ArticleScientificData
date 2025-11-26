"""Data export utilities for saving signals in multiple formats."""
import json
import numpy as np
from pathlib import Path


def save_signal_npz(filepath: str, signal: np.ndarray, t: np.ndarray, 
                    clean_signal: np.ndarray = None, metadata: dict = None):
    """Save signal data in NPZ format.
    
    Args:
        filepath: Path to save NPZ file
        signal: Noisy signal array
        t: Time array
        clean_signal: Clean signal array (optional)
        metadata: Additional metadata to store (optional)
    """
    data_dict = {
        'signal': signal,
        't': t
    }
    if clean_signal is not None:
        data_dict['clean_signal'] = clean_signal
    if metadata is not None:
        # Store metadata as JSON string in npz
        data_dict['metadata_json'] = json.dumps(metadata)
    
    np.savez(filepath, **data_dict)


def save_signal_txt(filepath: str, signal: np.ndarray):
    """Save signal data in TXT format (single column).
    
    Args:
        filepath: Path to save TXT file
        signal: Signal array to save
    """
    np.savetxt(filepath, signal, fmt='%.18e')


def save_signal_json(filepath: str, signal: np.ndarray, t: np.ndarray):
    """Save signal data in JSON format.
    
    Args:
        filepath: Path to save JSON file
        signal: Signal array
        t: Time array
    """
    data = {
        't': t.tolist(),
        'signal': signal.tolist()
    }
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def save_metadata_json(filepath: str, metadata: dict):
    """Save metadata in JSON format.
    
    Args:
        filepath: Path to save metadata JSON file
        metadata: Metadata dictionary
    """
    with open(filepath, 'w') as f:
        json.dump(metadata, f, indent=2)


def save_signal_all_formats(base_path: str, signal: np.ndarray, t: np.ndarray,
                            clean_signal: np.ndarray = None, metadata: dict = None,
                            save_metadata_separate: bool = False):
    """Save signal in all formats (npz, txt, json) and optionally metadata.
    
    Args:
        base_path: Base path without extension (e.g., 'data/signal_000')
        signal: Signal array
        t: Time array
        clean_signal: Clean signal array (optional)
        metadata: Metadata dictionary (optional)
        save_metadata_separate: If True, save metadata in separate file
    """
    base_path = Path(base_path)
    
    # Save NPZ
    save_signal_npz(f"{base_path}.npz", signal, t, clean_signal, metadata)
    
    # Save TXT (only signal values)
    save_signal_txt(f"{base_path}.txt", signal)
    
    # Save JSON (signal data)
    save_signal_json(f"{base_path}.json", signal, t)
    
    # Save metadata separately if requested
    if save_metadata_separate and metadata is not None:
        save_metadata_json(f"{base_path}_metadata.json", metadata)


# ==================== CONSOLIDATED EXPORT FUNCTIONS ====================

def save_consolidated_signals_npz(filepath: str, signals: np.ndarray, t: np.ndarray,
                                  clean_signals: np.ndarray = None):
    """Save multiple signals in a single NPZ file.
    
    Args:
        filepath: Path to save NPZ file
        signals: 2D array of shape (num_signals, num_samples)
        t: Time array (1D, shared by all signals)
        clean_signals: 2D array of clean signals (optional)
    """
    data_dict = {
        'signals': signals,
        't': t
    }
    if clean_signals is not None:
        data_dict['clean_signals'] = clean_signals
    
    np.savez_compressed(filepath, **data_dict)


def save_consolidated_signals_txt(filepath: str, signals: np.ndarray):
    """Save multiple signals in a single TXT file.
    
    Each row represents one complete signal.
    
    Args:
        filepath: Path to save TXT file
        signals: 2D array of shape (num_signals, num_samples)
    """
    np.savetxt(filepath, signals, fmt='%.18e')


def save_consolidated_signals_json(filepath: str, signals: np.ndarray, t: np.ndarray):
    """Save multiple signals in a single JSON file.
    
    Args:
        filepath: Path to save JSON file
        signals: 2D array of shape (num_signals, num_samples)
        t: Time array (1D, shared by all signals)
    """
    data = {
        't': t.tolist(),
        'signals': signals.tolist()
    }
    with open(filepath, 'w') as f:
        json.dump(data, f)


def save_consolidated_metadata_json(filepath: str, metadata_list: list):
    """Save metadata for all signals in a single JSON file.
    
    Args:
        filepath: Path to save metadata JSON file
        metadata_list: List of metadata dictionaries, one per signal
    """
    with open(filepath, 'w') as f:
        json.dump(metadata_list, f, indent=2)
