#!/usr/bin/env python3
"""Generate optimized signal dataset using improved amplitude parameters."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from SignalBuilderC.signal_generator import generate_demo_signal
from SignalBuilderC.noise_profiles import NoiseProfileConfig
import json
from datetime import datetime

def generate_signal_dataset(
    num_signals: int = 100,
    output_dir: str = "signals/Prueba01_Optimized",
    seed: int = None,
    verbose: bool = True
) -> dict:
    """Generate a complete dataset of signals with optimized parameters.
    
    Parameters
    ----------
    num_signals : int
        Number of signals to generate.
    output_dir : str
        Directory where signals will be saved.
    seed : int, optional
        Random seed for reproducibility.
    verbose : bool
        Print progress information.
    
    Returns
    -------
    dict
        Generation metadata and statistics.
    """
    
    output_path = Path(__file__).parent / output_dir
    output_path.mkdir(parents=True, exist_ok=True)
    
    if seed is not None:
        rng = np.random.default_rng(seed)
    else:
        rng = np.random.default_rng()
    
    # Noise configuration
    noise_config = NoiseProfileConfig(
        additive_gaussian_stddev=0.5,
        multiplicative_gaussian_stddev=0.05,
        sparsity_rate=0.01,
        temporal_correlation_tau=0.5,
        frequency_dependent=True,
    )
    
    # Signal generation parameters
    t_start = 0.0
    t_end = 10.0
    fs_high = 5000  # 5 kHz sampling
    
    metadata_list = []
    stats = {
        "total_signals": num_signals,
        "t_start": t_start,
        "t_end": t_end,
        "fs_high": fs_high,
        "num_samples": int((t_end - t_start) * fs_high),
        "noise_config": {
            "additive_gaussian_stddev": noise_config.additive_gaussian_stddev,
            "multiplicative_gaussian_stddev": noise_config.multiplicative_gaussian_stddev,
            "sparsity_rate": noise_config.sparsity_rate,
            "temporal_correlation_tau": noise_config.temporal_correlation_tau,
            "frequency_dependent": noise_config.frequency_dependent,
        },
        "amplitude_parameters": {
            "range": "[1, 8]",  # Optimized from [3, 15]
            "tau_range": "[0.5, 2.5]",  # Optimized from {1,3,5,8,10,12,15,20}
            "tension_spline_probability": 0.5,  # Optimized from 0.3
            "note": "Optimized on 2026-01-13 for natural amplitude transitions"
        },
        "start_time": datetime.now().isoformat(),
    }
    
    if verbose:
        print(f"\n{'='*70}")
        print(f"Generating {num_signals} signals with optimized parameters")
        print(f"{'='*70}")
        print(f"Output directory: {output_path}")
        print(f"Time range: {t_start:.1f}s - {t_end:.1f}s")
        print(f"Sampling rate: {fs_high} Hz")
        print(f"Samples per signal: {stats['num_samples']}")
        print(f"{'='*70}\n")
    
    # Generate signals
    for i in range(num_signals):
        try:
            # Generate signal
            t_high, clean_signal, noisy_signal, signal_metadata = generate_demo_signal(
                t_start=t_start,
                t_end=t_end,
                fs_high=fs_high,
                noise_config=noise_config,
                rng=rng,
            )
            
            # Save signal as .npz file
            signal_num = i + 1
            filename = output_path / f"signal_{signal_num:06d}.npz"
            
            np.savez(
                filename,
                t=t_high,
                clean_signal=clean_signal,
                noisy_signal=noisy_signal,
                metadata=signal_metadata,
            )
            
            metadata_list.append(signal_metadata)
            
            # Progress output
            if verbose and (i + 1) % 10 == 0:
                amp_tau = signal_metadata.get('tau_amplitude', 'N/A')
                amp_type = signal_metadata.get('amplitude_spline_type', 'N/A')
                print(f"  Generated {i+1:3d}/{num_signals} signals "
                      f"(tau_amp={str(amp_tau)[:5]:>5s}, type={amp_type})")
        
        except Exception as e:
            print(f"ERROR generating signal {i+1}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    # Save metadata
    metadata_file = output_path / "metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump({
            "signals": metadata_list,
            "generation_stats": stats,
        }, f, indent=2, default=str)
    
    stats["end_time"] = datetime.now().isoformat()
    stats["generated_signals"] = len(metadata_list)
    stats["metadata_file"] = str(metadata_file)
    
    # Print summary
    if verbose:
        print(f"\n{'='*70}")
        print(f"✅ Generation Complete")
        print(f"{'='*70}")
        print(f"Generated: {len(metadata_list)}/{num_signals} signals")
        print(f"Output directory: {output_path}")
        print(f"Metadata file: {metadata_file}")
        
        # Calculate amplitude statistics
        all_tau_amps = [m.get('tau_amplitude') for m in metadata_list if m.get('tau_amplitude') != 'N/A']
        if all_tau_amps:
            print(f"\nAmplitude Statistics (tau values):")
            print(f"  Mean: {np.mean(all_tau_amps):.3f}")
            print(f"  Min:  {np.min(all_tau_amps):.3f}")
            print(f"  Max:  {np.max(all_tau_amps):.3f}")
        
        # Count spline types
        spline_types = [m.get('amplitude_spline_type') for m in metadata_list]
        tension_count = sum(1 for t in spline_types if t == 'tension')
        step_count = sum(1 for t in spline_types if t == 'zero_order')
        print(f"\nSpline Type Distribution:")
        print(f"  Tension splines: {tension_count} ({100*tension_count/len(metadata_list):.1f}%)")
        print(f"  Step functions:  {step_count} ({100*step_count/len(metadata_list):.1f}%)")
        
        print(f"{'='*70}\n")
    
    return stats


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate optimized signal dataset with improved amplitude parameters"
    )
    parser.add_argument("--count", type=int, default=100,
                       help="Number of signals to generate (default: 100)")
    parser.add_argument("--output", type=str, default="signals/Prueba01_Optimized",
                       help="Output directory for signals")
    parser.add_argument("--seed", type=int, default=None,
                       help="Random seed for reproducibility")
    parser.add_argument("--quiet", action="store_true",
                       help="Suppress progress output")
    
    args = parser.parse_args()
    
    stats = generate_signal_dataset(
        num_signals=args.count,
        output_dir=args.output,
        seed=args.seed,
        verbose=not args.quiet,
    )
    
    sys.exit(0 if stats["generated_signals"] == args.count else 1)
