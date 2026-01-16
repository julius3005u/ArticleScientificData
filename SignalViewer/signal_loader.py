"""Module for loading signals and metadata from SignalBuilderC and SignalBuilderCLI."""
import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class SignalLoader:
    """Load signals from .npz files and their metadata from .json files."""
    
    def __init__(self, signalbuilderc_path: str, signalbuildercli_path: str):
        """Initialize loader with paths to both data sources.
        
        Args:
            signalbuilderc_path: Path to SignalBuilderC/data (can be None)
            signalbuildercli_path: Path to SignalBuilderCLI/output (can be None)
        """
        self.sbc_path = Path(signalbuilderc_path) if signalbuilderc_path else None
        self.sbcli_path = Path(signalbuildercli_path) if signalbuildercli_path else None
        self.metadata = {}
        self.signal_files = {}
        self._load_metadata()
        
    def _load_metadata(self):
        """Load all metadata from both sources."""
        # Load from SignalBuilderC
        if self.sbc_path:
            sbc_meta_file = self.sbc_path / "signals_metadata.json"
            if sbc_meta_file.exists():
                with open(sbc_meta_file, 'r') as f:
                    sbc_metadata = json.load(f)
                for idx, meta in enumerate(sbc_metadata):
                    signal_id = meta.get("signal_id", f"SBC_{idx}")
                    self.metadata[signal_id] = {
                        "source": "SignalBuilderC",
                        "metadata": meta,
                        "index": idx
                    }
        
        # Load from SignalBuilderCLI
        if self.sbcli_path:
            sbcli_meta_file = self.sbcli_path / "signals_metadata.json"
            if sbcli_meta_file.exists():
                with open(sbcli_meta_file, 'r') as f:
                    sbcli_metadata = json.load(f)
                for idx, meta in enumerate(sbcli_metadata):
                    signal_id = f"SBCLI_{idx}"
                    self.metadata[signal_id] = {
                        "source": "SignalBuilderCLI",
                        "metadata": meta,
                        "index": idx
                    }
    
    def get_signal_ids(self) -> List[str]:
        """Get list of all available signal IDs."""
        return sorted(self.metadata.keys())
    
    def get_signal(self, signal_id: str) -> Optional[Tuple[np.ndarray, Dict]]:
        """Load a signal and its metadata by ID.
        
        Args:
            signal_id: Signal identifier
            
        Returns:
            Tuple of (signal_array, metadata_dict) or None if not found
        """
        if signal_id not in self.metadata:
            return None
        
        meta_info = self.metadata[signal_id]
        source = meta_info["source"]
        metadata = meta_info["metadata"]
        idx = meta_info["index"]
        
        try:
            if source == "SignalBuilderC":
                signal_dir = self.sbc_path / "signals" / "Prueba01"
                signal_file = signal_dir / f"signal_{idx:03d}.npz"
                
                if signal_file.exists():
                    npz_data = np.load(signal_file)
                    # Extract the signal
                    if 'signal' in npz_data:
                        signal = npz_data['signal']
                    elif 'signals' in npz_data:
                        signals = npz_data['signals']
                        if signals.ndim > 1 and signals.shape[0] > 0:
                            signal = signals[0]
                        else:
                            signal = signals
                    else:
                        signal = npz_data[list(npz_data.files)[0]]
                    return signal, metadata
            
            else:  # SignalBuilderCLI
                # Load from consolidated signals_high_resolution_5000.npz
                signal_file = self.sbcli_path / "signals_high_resolution_5000.npz"
                
                if signal_file.exists():
                    npz_data = np.load(signal_file)
                    # Try to get signals array
                    if 'signals' in npz_data:
                        signals = npz_data['signals']
                        if signals.ndim > 1 and signals.shape[0] > idx:
                            signal = signals[idx]
                            return signal, metadata
                    elif 'signal' in npz_data:
                        signal = npz_data['signal']
                        return signal, metadata
                    else:
                        # Get first array
                        signal = npz_data[list(npz_data.files)[0]]
                        if signal.ndim > 1 and signal.shape[0] > idx:
                            return signal[idx], metadata
                        return signal, metadata
        
        except Exception as e:
            print(f"Error loading signal {signal_id}: {e}")
        
        return None, metadata
    
    def get_metadata(self, signal_id: str) -> Optional[Dict]:
        """Get metadata for a signal without loading the signal data."""
        if signal_id not in self.metadata:
            return None
        return self.metadata[signal_id]["metadata"]
    
    def get_source(self, signal_id: str) -> Optional[str]:
        """Get source of a signal (SignalBuilderC or SignalBuilderCLI)."""
        if signal_id not in self.metadata:
            return None
        return self.metadata[signal_id]["source"]
