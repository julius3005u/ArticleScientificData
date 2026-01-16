#!/usr/bin/env python3
"""Generate 2500 consolidated signals with proper structure."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from SignalBuilderC.signal_generator import generate_demo_signal
from SignalBuilderC.noise_profiles import NoiseProfileConfig
import json
from datetime import datetime

def generate_consolidated_dataset(
    num_signals: int = 2500,
    output_dir: str = "signals",
    seed: int = 42,
    verbose: bool = True
) -> dict:
    """Generate 2500 consolidated signals with subsampling.
    
    Parameters
    ----------
    num_signals : int
        Number of signals to generate.
    output_dir : str
        Directory where signals will be saved.
    seed : int
        Random seed for reproducibility.
    verbose : bool
        Print progress information.
    """
    
    output_path = Path(output_dir)
    # If output_dir is relative, resolve it relative to the script location
    if not output_path.is_absolute():
        output_path = Path(__file__).parent / output_dir
    output_path.mkdir(parents=True, exist_ok=True)
    
    # CRITICAL: Reset NumPy and Python's global RNG state
    # This ensures reproducibility regardless of prior RNG calls
    np.random.seed(seed)
    import random
    random.seed(seed)
    
    rng = np.random.default_rng(seed)
    
    # Noise configuration
    noise_config = NoiseProfileConfig(
        p_has_noise=0.8,
        p_gaussian=0.7,
        gaussian_std_relative=0.15,
    )
    
    # Signal generation parameters
    t_start = 0.0
    t_end = 4 * np.pi  # 0 to 4π (12.566...)
    num_samples_high = 5000  # High-resolution: 5000 samples
    fs_high = num_samples_high / (t_end - t_start)  # Calculate sampling rate from desired samples
    
    if verbose:
        print(f"\n{'='*70}")
        print(f"Generating {num_signals} consolidated signals")
        print(f"{'='*70}")
        print(f"Output directory: {output_path}")
        print(f"Time range: 0 to 4π ({t_end:.6f})")
        print(f"Sampling rate: {fs_high} Hz")
        print(f"Samples per signal: {num_samples_high}")
        print(f"{'='*70}\n")
    
    # Initialize arrays
    signals_high = np.zeros((num_signals, num_samples_high))
    signals_clean_high = np.zeros((num_signals, num_samples_high))
    t_high = np.arange(t_start, t_end, 1.0 / fs_high)[:num_samples_high]
    
    metadata_list = []
    
    # Generate signals
    for i in range(num_signals):
        try:
            t, clean_signal, noisy_signal, signal_metadata = generate_demo_signal(
                t_start=t_start,
                t_end=t_end,
                fs_high=fs_high,
                noise_config=noise_config,
                rng=rng,
            )
            
            # Ensure correct size
            n = min(len(noisy_signal), num_samples_high)
            signals_high[i, :n] = noisy_signal[:n]
            signals_clean_high[i, :n] = clean_signal[:n]
            
            metadata_list.append(signal_metadata)
            
            if verbose and (i + 1) % 500 == 0:
                amp_tau = signal_metadata.get('tau_amplitude', 'N/A')
                amp_type = signal_metadata.get('amplitude_spline_type', 'N/A')
                print(f"  Generated {i+1:4d}/{num_signals} signals "
                      f"(tau_amp={str(amp_tau)[:5]:>5s}, type={amp_type})")
        
        except Exception as e:
            print(f"ERROR generating signal {i+1}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    # Save high-resolution consolidated NPZ
    npz_high = output_path / "signals_high_resolution_5000.npz"
    np.savez_compressed(
        npz_high,
        signals=signals_high,
        clean_signals=signals_clean_high,
        t=t_high
    )
    if verbose:
        print(f"\n✓ Saved high-resolution: {npz_high}")
        print(f"  Shape: {signals_high.shape}")
    
    # Generate subsampled versions
    subsampling_rates = {
        150: 5000 // 150,   # decimate by ~33
        250: 5000 // 250,   # decimate by 20
        500: 5000 // 500,   # decimate by 10
        1000: 5000 // 1000, # decimate by 5
    }
    
    for target_samples, decimation_factor in subsampling_rates.items():
        # Simple subsampling (decimation without filter)
        indices = np.arange(0, num_samples_high, decimation_factor)[:target_samples]
        
        signals_sub = signals_high[:, indices]
        signals_clean_sub = signals_clean_high[:, indices]
        t_sub = t_high[indices]
        
        npz_sub = output_path / f"signals_subsampled_simple_{target_samples}.npz"
        np.savez_compressed(
            npz_sub,
            signals=signals_sub,
            clean_signals=signals_clean_sub,
            t=t_sub
        )
        if verbose:
            print(f"✓ Saved subsampled-{target_samples}: {npz_sub}")
            print(f"  Shape: {signals_sub.shape}")
    
    # Save consolidated metadata
    metadata_file = output_path / "signals_metadata_consolidated_2500.json"
    with open(metadata_file, 'w') as f:
        json.dump({
            "dataset_info": {
                "num_signals": len(metadata_list),
                "temporal_range": {
                    "start": float(t_start),
                    "end": float(t_end),
                    "description": "0 to 4π"
                },
                "sampling_rate": fs_high,
                "amplitude_optimization": {
                    "tau_range": [0.5, 2.5],
                    "amplitude_range": [1, 8],
                    "spline_balance": "50/50 (tension/step)",
                    "date": "2026-01-13",
                    "improvement": "52.6% reduction in peak amplitudes"
                },
                "subsampling_method": "simple (decimation without filters)",
                "subsampled_sizes": [150, 250, 500, 1000],
                "generation_time": datetime.now().isoformat()
            },
            "signals": metadata_list
        }, f, indent=2, default=str)
    
    if verbose:
        print(f"\n✓ Saved consolidated metadata: {metadata_file}")
        print(f"\n{'='*70}")
        print(f"✅ Dataset Generation Complete")
        print(f"{'='*70}")
        print(f"Generated: {len(metadata_list)} signals")
        print(f"Output directory: {output_path}")
        
        # Statistics
        all_tau_amps = [m.get('tau_amplitude') for m in metadata_list 
                       if isinstance(m.get('tau_amplitude'), (int, float))]
        if all_tau_amps:
            print(f"\nAmplitude Statistics (tau values):")
            print(f"  Mean: {np.mean(all_tau_amps):.3f}")
            print(f"  Min:  {np.min(all_tau_amps):.3f}")
            print(f"  Max:  {np.max(all_tau_amps):.3f}")
        
        spline_types = [m.get('amplitude_spline_type') for m in metadata_list]
        tension_count = sum(1 for t in spline_types if t == 'tension')
        step_count = sum(1 for t in spline_types if t == 'zero_order')
        print(f"\nSpline Distribution:")
        print(f"  Tension: {tension_count} ({100*tension_count/len(metadata_list):.1f}%)")
        print(f"  Step:    {step_count} ({100*step_count/len(metadata_list):.1f}%)")
        print(f"{'='*70}\n")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate 2500 consolidated signals with subsampling"
    )
    parser.add_argument("--count", type=int, default=2500,
                       help="Number of signals (default: 2500)")
    parser.add_argument("--seed", type=int, default=42,
                       help="Random seed (default: 42)")
    parser.add_argument("--output", type=str, default="signals",
                       help="Output directory (default: signals)")
    parser.add_argument("--quiet", action="store_true",
                       help="Suppress output")
    
    args = parser.parse_args()
    
    generate_consolidated_dataset(
        num_signals=args.count,
        output_dir=args.output,
        seed=args.seed,
        verbose=not args.quiet,
    )
