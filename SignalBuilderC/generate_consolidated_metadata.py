#!/usr/bin/env python3
"""Generate consolidated metadata for 2500 signals with subsampling.

Uses SIMPLE (non-filtered) subsampling to preserve signal reconstruction fidelity.
Temporal range: 0 to 4π (12.566370614359172)
Subsampling sizes: 150, 250, 500, 1000
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import json
from datetime import datetime


def generate_consolidated_metadata(
    output_dir: str = "data",
    subsample_sizes: list = None,
    verbose: bool = True
) -> dict:
    """Generate consolidated metadata for existing signal datasets.
    
    Uses existing .npz files:
    - signals_high_resolution_5000.npz (original, 5000 samples)
    - signals_subsampled_simple_*.npz (decimated versions)
    
    Parameters
    ----------
    output_dir : str
        Directory containing signal .npz files
    subsample_sizes : list
        List of subsampling sizes (samples). Default: [150, 250, 500, 1000]
    verbose : bool
        Print progress information
    
    Returns
    -------
    dict
        Complete metadata structure
    """
    
    if subsample_sizes is None:
        subsample_sizes = [150, 250, 500, 1000]
    
    data_path = Path(__file__).parent / output_dir
    
    if verbose:
        print(f"\n{'='*80}")
        print(f"📊 Generating Consolidated Metadata for 2500 Signals")
        print(f"{'='*80}")
        print(f"Data directory: {data_path}")
        print(f"Subsample sizes: {subsample_sizes}")
        print(f"{'='*80}\n")
    
    # Load high-resolution signals
    high_res_file = data_path / "signals_high_resolution_5000.npz"
    if not high_res_file.exists():
        raise FileNotFoundError(f"High-resolution file not found: {high_res_file}")
    
    high_res_data = np.load(high_res_file)
    signals_high = high_res_data['signals']  # Shape: (2500, 5000)
    t_high = high_res_data['t']  # Time axis for high resolution
    num_signals = signals_high.shape[0]
    
    if verbose:
        print(f"✓ Loaded high-resolution signals: {signals_high.shape}")
        print(f"✓ Time axis: {t_high[0]:.4f} to {t_high[-1]:.4f} (4π ≈ 12.5664)")
    
    # Load subsampled versions
    subsampled_data = {}
    for size in subsample_sizes:
        subsampled_file = data_path / f"signals_subsampled_simple_{size}.npz"
        if not subsampled_file.exists():
            if verbose:
                print(f"⚠ Warning: File not found: {subsampled_file}")
            continue
        
        data = np.load(subsampled_file)
        subsampled_data[size] = {
            'signals': data['signals'],  # Shape: (2500, size)
            't': data['t'],
        }
        if verbose:
            print(f"✓ Loaded subsampled {size}: {data['signals'].shape}")
    
    # Load existing metadata if available (for amplitude parameters)
    existing_metadata = None
    metadata_file = data_path / "signals_metadata.json"
    if metadata_file.exists():
        with open(metadata_file, 'r') as f:
            existing_metadata = json.load(f)
        if verbose:
            print(f"✓ Loaded existing metadata with {len(existing_metadata)} entries")
    
    # Build consolidated metadata
    consolidated_metadata = {
        "dataset_info": {
            "name": "SignalBuilderC Optimized Dataset",
            "num_signals": num_signals,
            "creation_date": datetime.now().isoformat(),
            "temporal_range": {
                "start": float(t_high[0]),
                "end": float(t_high[-1]),
                "description": "0 to 4π (12.566370614359172)"
            },
            "amplitude_optimization": {
                "date": "2026-01-13",
                "tau_amplitude_range": "[0.5, 2.5]",
                "amplitude_range": "±[1, 8]",
                "spline_balance": "50% tension / 50% step",
                "note": "Optimized for natural, non-artificial amplitude transitions"
            },
            "subsampling": {
                "method": "simple",
                "description": "Decimation only - NO filtering to preserve reconstruction fidelity",
                "sizes": subsample_sizes,
            }
        },
        "signals": []
    }
    
    # Process each signal
    for i in range(num_signals):
        signal_meta = {
            "signal_id": i + 1,
            "high_resolution": {
                "filename": "signals_high_resolution_5000.npz",
                "shape": (num_signals, signals_high.shape[1]),
                "samples": signals_high.shape[1],
                "temporal_range": [float(t_high[0]), float(t_high[-1])],
            },
            "subsampled_versions": {}
        }
        
        # Add information about each subsampled version
        for size in subsample_sizes:
            if size in subsampled_data:
                signal_meta["subsampled_versions"][f"{size}_samples"] = {
                    "filename": f"signals_subsampled_simple_{size}.npz",
                    "samples": size,
                    "array_index": i,
                    "shape_in_file": (num_signals, size),
                }
        
        # Add existing amplitude metadata if available
        if existing_metadata and i < len(existing_metadata):
            orig_meta = existing_metadata[i]
            signal_meta["amplitude_parameters"] = {
                "tau_amplitude": orig_meta.get('tau_amplitude'),
                "tau_frequency": orig_meta.get('tau_frequency'),
                "amplitude_spline_type": orig_meta.get('amplitude_spline_type'),
                "vertical_offset": orig_meta.get('vertical_offset'),
                "amp_knots": orig_meta.get('amp_knots'),
                "amp_values": orig_meta.get('amp_values'),
                "base_points": orig_meta.get('base_points'),
                "high_freq_points": orig_meta.get('high_freq_points'),
                "variation_type": orig_meta.get('variation_type'),
            }
            
            if orig_meta.get('noise_profile'):
                signal_meta["noise_profile"] = orig_meta.get('noise_profile')
        
        consolidated_metadata["signals"].append(signal_meta)
        
        # Progress output
        if verbose and (i + 1) % 500 == 0:
            print(f"  Processed {i+1}/{num_signals} signals")
    
    # Save consolidated metadata
    output_file = data_path / "signals_metadata_consolidated_2500.json"
    with open(output_file, 'w') as f:
        json.dump(consolidated_metadata, f, indent=2)
    
    if verbose:
        print(f"\n{'='*80}")
        print(f"✅ Consolidated Metadata Generated")
        print(f"{'='*80}")
        print(f"Output file: {output_file}")
        print(f"File size: {output_file.stat().st_size / (1024*1024):.1f} MB")
        print(f"Signals: {len(consolidated_metadata['signals'])}")
        print(f"Subsampled versions per signal: {len(subsample_sizes)}")
        print(f"\nUsage Example:")
        print(f"  import json")
        print(f"  with open('{output_file.name}', 'r') as f:")
        print(f"      metadata = json.load(f)")
        print(f"  signal_info = metadata['signals'][0]")
        print(f"  print(signal_info['subsampled_versions'])")
        print(f"{'='*80}\n")
    
    return consolidated_metadata


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate consolidated metadata for signal dataset"
    )
    parser.add_argument("--output", type=str, default="data",
                       help="Output directory (default: data)")
    parser.add_argument("--sizes", type=int, nargs="+", default=[150, 250, 500, 1000],
                       help="Subsampling sizes (default: 150 250 500 1000)")
    parser.add_argument("--quiet", action="store_true",
                       help="Suppress progress output")
    
    args = parser.parse_args()
    
    metadata = generate_consolidated_metadata(
        output_dir=args.output,
        subsample_sizes=args.sizes,
        verbose=not args.quiet,
    )
    
    sys.exit(0)
