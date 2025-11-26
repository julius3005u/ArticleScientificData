"""Batch signal generation script for creating the complete dataset.

This script generates 2500 high-resolution signals and their subsampled versions,
storing all signals of each type in consolidated files:
- High-resolution: 5000 samples in [0, 4π]
- Simple subsampling: 150, 250, 500, 1000 samples (re-evaluation)
- Filtered subsampling: 150, 250, 500, 1000 samples (with anti-aliasing)

Each type is saved as:
- One .npz file containing all 2500 signals as 2D array
- One .txt file containing all 2500 signals (one per row)
- One .json file containing all 2500 signals
- One metadata.json file containing all signal metadata
"""
import json
import numpy as np
from pathlib import Path
from numpy.random import default_rng

from SignalBuilderC.signal_generator import generate_demo_signal
from SignalBuilderC.noise_profiles import NoiseProfileConfig
from SignalBuilderC.subsampling import generate_subsampled_versions
from SignalBuilderC.antialiasing import subsample_with_antialiasing, get_filter_info
from SignalBuilderC.data_export import (
    save_consolidated_signals_npz,
    save_consolidated_signals_txt,
    save_consolidated_signals_json,
    save_consolidated_metadata_json
)


def generate_complete_dataset(num_signals: int = 2500,
                             t_start: float = 0.0,
                             t_end: float = 4 * np.pi,
                             fs_high: float = 5000.0 / (4 * np.pi),
                             subsample_sizes: list = [150, 250, 500, 1000],
                             noise_probability: float = 0.5,
                             base_seed: int = 10000,
                             filter_type: str = 'butter',
                             filter_order: int = 8):
    """Generate complete dataset with all variations in consolidated files.
    
    Args:
        num_signals: Number of high-resolution signals to generate
        t_start: Signal start time
        t_end: Signal end time
        fs_high: High-resolution sampling frequency
        subsample_sizes: List of subsample sizes to generate
        noise_probability: Probability of adding noise (0.5 = 50%)
        base_seed: Base seed for random generation
        filter_type: Anti-aliasing filter type
        filter_order: Anti-aliasing filter order
    """
    # Setup paths
    base_path = Path("SignalBuilderC/data")
    base_path.mkdir(parents=True, exist_ok=True)
    
    # Noise configuration
    noise_config = NoiseProfileConfig(
        p_has_noise=noise_probability,
        p_gaussian=0.5,
        gaussian_std_relative=0.15
    )
    
    print(f"Generating {num_signals} signals with consolidated storage...")
    print(f"High-resolution: {int(fs_high * (t_end - t_start))} samples")
    print(f"Subsample sizes: {subsample_sizes}")
    print(f"Noise probability: {noise_probability * 100}%")
    print(f"Anti-aliasing filter: {filter_type}, order {filter_order}")
    print("-" * 80)
    
    # Initialize storage arrays
    num_samples_high = int(fs_high * (t_end - t_start))
    high_res_signals = np.zeros((num_signals, num_samples_high))
    high_res_clean_signals = np.zeros((num_signals, num_samples_high))
    
    # Initialize subsampled storage
    simple_subsampled = {size: np.zeros((num_signals, size)) for size in subsample_sizes}
    filtered_subsampled = {size: np.zeros((num_signals, size)) for size in subsample_sizes}
    
    # Metadata storage
    all_metadata = []
    
    # Generate all signals
    for i in range(num_signals):
        seed = base_seed + i
        rng = default_rng(seed)
        
        # Generate high-resolution signal
        t_high, clean_signal, noisy_signal, signal_metadata = generate_demo_signal(
            t_start=t_start,
            t_end=t_end,
            fs_high=fs_high,
            noise_config=noise_config,
            rng=rng
        )
        
        signal_metadata['seed'] = seed
        signal_metadata['signal_id'] = f'signal_{i:04d}'
        signal_metadata['index'] = i
        
        # Store high-resolution signals
        high_res_signals[i] = noisy_signal
        high_res_clean_signals[i] = clean_signal
        all_metadata.append(signal_metadata)
        
        # Generate simple subsampled versions
        subsampled = generate_subsampled_versions(
            signal_metadata=signal_metadata,
            t_start=t_start,
            t_end=t_end,
            subsample_sizes=subsample_sizes,
            rng=rng
        )
        
        for size, (t_sub, signal_sub) in subsampled.items():
            simple_subsampled[size][i] = signal_sub
        
        # Generate filtered subsampled versions
        for size in subsample_sizes:
            t_filtered, signal_filtered = subsample_with_antialiasing(
                signal_data=noisy_signal,
                t_original=t_high,
                t_start=t_start,
                t_end=t_end,
                target_size=size,
                filter_type=filter_type,
                order=filter_order
            )
            filtered_subsampled[size][i] = signal_filtered
        
        # Progress report
        if (i + 1) % 100 == 0:
            print(f"Generated {i + 1}/{num_signals} signals")
    
    print("-" * 80)
    print("Saving consolidated files...")
    
    # Save high-resolution signals
    print("  - High-resolution signals (5000 samples)...")
    save_consolidated_signals_npz(
        filepath=str(base_path / "signals_high_resolution_5000.npz"),
        signals=high_res_signals,
        t=t_high,
        clean_signals=high_res_clean_signals
    )
    save_consolidated_signals_txt(
        filepath=str(base_path / "signals_high_resolution_5000.txt"),
        signals=high_res_signals
    )
    save_consolidated_signals_json(
        filepath=str(base_path / "signals_high_resolution_5000.json"),
        signals=high_res_signals,
        t=t_high
    )
    
    # Save simple subsampled signals
    for size in subsample_sizes:
        print(f"  - Simple subsampled signals ({size} samples)...")
        t_sub = np.linspace(t_start, t_end, size)
        
        save_consolidated_signals_npz(
            filepath=str(base_path / f"signals_subsampled_simple_{size}.npz"),
            signals=simple_subsampled[size],
            t=t_sub
        )
        save_consolidated_signals_txt(
            filepath=str(base_path / f"signals_subsampled_simple_{size}.txt"),
            signals=simple_subsampled[size]
        )
        save_consolidated_signals_json(
            filepath=str(base_path / f"signals_subsampled_simple_{size}.json"),
            signals=simple_subsampled[size],
            t=t_sub
        )
    
    # Save filtered subsampled signals
    for size in subsample_sizes:
        print(f"  - Filtered subsampled signals ({size} samples)...")
        t_filtered = np.linspace(t_start, t_end, size)
        
        save_consolidated_signals_npz(
            filepath=str(base_path / f"signals_subsampled_filtered_{size}.npz"),
            signals=filtered_subsampled[size],
            t=t_filtered
        )
        save_consolidated_signals_txt(
            filepath=str(base_path / f"signals_subsampled_filtered_{size}.txt"),
            signals=filtered_subsampled[size]
        )
        save_consolidated_signals_json(
            filepath=str(base_path / f"signals_subsampled_filtered_{size}.json"),
            signals=filtered_subsampled[size],
            t=t_filtered
        )
    
    # Save consolidated metadata
    print("  - Metadata for all signals...")
    save_consolidated_metadata_json(
        filepath=str(base_path / "signals_metadata.json"),
        metadata_list=all_metadata
    )
    
    # Save dataset summary
    print("  - Dataset summary...")
    dataset_summary = {
        'num_signals': num_signals,
        'high_resolution': {
            't_start': float(t_start),
            't_end': float(t_end),
            'num_samples': num_samples_high,
            'fs': float(fs_high)
        },
        'subsample_sizes': subsample_sizes,
        'noise_config': {
            'probability': noise_probability,
            'type': 'mixed (50% Gaussian, 50% structured)',
            'gaussian_std_relative': 0.15
        },
        'base_seed': base_seed,
        'file_structure': {
            'high_resolution': 'signals_high_resolution_5000.[npz|txt|json]',
            'simple_subsampled': 'signals_subsampled_simple_{size}.[npz|txt|json]',
            'filtered_subsampled': 'signals_subsampled_filtered_{size}.[npz|txt|json]',
            'metadata': 'signals_metadata.json'
        },
        'data_format': {
            'npz': 'NumPy compressed array, shape (2500, num_samples)',
            'txt': 'Text file, one signal per row',
            'json': 'JSON array of signals'
        }
    }
    
    with open(base_path / "dataset_summary.json", 'w') as f:
        json.dump(dataset_summary, f, indent=2)
    
    # Save filtering info
    print("  - Anti-aliasing filter info...")
    filter_info = get_filter_info(filter_type, filter_order)
    filter_info['applies_to'] = 'signals_subsampled_filtered_{size}.[npz|txt|json]'
    filter_info['subsample_sizes'] = subsample_sizes
    filter_info['explanation'] = (
        "Anti-aliasing filters are applied to prevent frequency aliasing when "
        "downsampling from high resolution (5000 samples) to lower resolutions. "
        "The filter cutoff is set at 90% of the target Nyquist frequency for each "
        "subsample size. Zero-phase filtering (filtfilt) is used to avoid time shifts."
    )
    
    with open(base_path / "filtering_info.json", 'w') as f:
        json.dump(filter_info, f, indent=2)
    
    print("-" * 80)
    print(f"✅ Completed! Generated {num_signals} signals in consolidated files")
    print("\nDataset structure:")
    print(f"  📁 SignalBuilderC/data/")
    print(f"     📄 signals_high_resolution_5000.[npz|txt|json]")
    for size in subsample_sizes:
        print(f"     📄 signals_subsampled_simple_{size}.[npz|txt|json]")
        print(f"     📄 signals_subsampled_filtered_{size}.[npz|txt|json]")
    print(f"     📄 signals_metadata.json (all {num_signals} signal metadata)")
    print(f"     📄 dataset_summary.json")
    print(f"     📄 filtering_info.json")
    print(f"\n  Total: {3 + 3 * len(subsample_sizes) * 2} data files + 3 metadata files")


if __name__ == "__main__":
    generate_complete_dataset(
        num_signals=2500,
        t_start=0.0,
        t_end=4 * np.pi,
        fs_high=5000.0 / (4 * np.pi),
        subsample_sizes=[150, 250, 500, 1000],
        noise_probability=0.5,
        base_seed=10000,
        filter_type='butter',
        filter_order=8
    )
