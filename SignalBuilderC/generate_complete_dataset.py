#!/usr/bin/env python3
"""Generate complete optimized signal dataset with subsampling and metadata."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from SignalBuilderC.signal_generator import generate_demo_signal
from SignalBuilderC.noise_profiles import NoiseProfileConfig
import json
from datetime import datetime
import pickle


def subsample_arrays(t: np.ndarray, clean: np.ndarray, noisy: np.ndarray, 
                     rate: int) -> tuple:
    """Simple downsampling by taking every rate-th sample.
    
    Parameters
    ----------
    t : np.ndarray
        Time array
    clean : np.ndarray
        Clean signal
    noisy : np.ndarray
        Noisy signal
    rate : int
        Downsampling rate (keep every rate-th sample)
    
    Returns
    -------
    tuple
        (t_downsampled, clean_downsampled, noisy_downsampled)
    """
    if rate == 1:
        return t, clean, noisy
    
    indices = np.arange(0, len(t), rate)
    return t[indices], clean[indices], noisy[indices]

def generate_complete_dataset(
    num_signals: int = 2500,
    output_dir: str = "signals/Dataset_Optimized_2500",
    subsample_rates: list = None,
    seed: int = 42,
    verbose: bool = True
) -> dict:
    """Generate complete signal dataset with subsampling and metadata.
    
    Parameters
    ----------
    num_signals : int
        Number of signals to generate.
    output_dir : str
        Base directory where signals will be saved.
    subsample_rates : list
        Subsampling rates (as factors). Default: [1, 2, 5, 10] 
        (i.e., original, 1/2, 1/5, 1/10 of original sampling rate)
    seed : int
        Random seed for reproducibility.
    verbose : bool
        Print progress information.
    
    Returns
    -------
    dict
        Generation metadata and statistics.
    """
    
    if subsample_rates is None:
        subsample_rates = [1, 2, 5, 10]  # Original + 3 downsampled versions
    
    base_path = Path(__file__).parent / output_dir
    base_path.mkdir(parents=True, exist_ok=True)
    
    # Create subdirectories for each sampling rate
    signal_dirs = {}
    for rate in subsample_rates:
        if rate == 1:
            subdir = base_path / "high_resolution"
        else:
            subdir = base_path / f"downsampled_{rate}x"
        subdir.mkdir(parents=True, exist_ok=True)
        signal_dirs[rate] = subdir
    
    rng = np.random.default_rng(seed)
    
    # Noise configuration - match actual NoiseProfileConfig parameters
    noise_config = NoiseProfileConfig(
        p_has_noise=0.7,                    # 70% of signals have noise
        p_gaussian=0.5,                     # 50% Gaussian, 50% structured
        gaussian_std_relative=0.15,         # 15% of signal RMS
    )
    
    # Signal generation parameters
    t_start = 0.0
    t_end = 10.0
    fs_high = 5000  # 5 kHz original sampling
    
    all_metadata = []
    signal_stats = {
        "count": 0,
        "amp_tau_values": [],
        "amp_spline_types": {"tension": 0, "zero_order": 0},
        "offsets": [],
        "errors": 0,
    }
    
    generation_stats = {
        "total_signals_requested": num_signals,
        "generated_signals": 0,
        "t_start": t_start,
        "t_end": t_end,
        "fs_high": fs_high,
        "num_samples_high": int((t_end - t_start) * fs_high),
        "subsample_rates": subsample_rates,
        "output_directory": str(base_path),
        "seed": seed,
        "noise_config": {
            "p_has_noise": noise_config.p_has_noise,
            "p_gaussian": noise_config.p_gaussian,
            "gaussian_std_relative": noise_config.gaussian_std_relative,
        },
        "amplitude_parameters": {
            "range": "[1, 8]",
            "tau_range": "[0.5, 2.5]",
            "tension_spline_probability": 0.5,
            "note": "Optimized on 2026-01-13 for natural amplitude transitions"
        },
        "start_time": datetime.now().isoformat(),
    }
    
    if verbose:
        print(f"\n{'='*80}")
        print(f"🚀 Generating {num_signals} signals with subsampling and metadata")
        print(f"{'='*80}")
        print(f"Output directory: {base_path}")
        print(f"Time range: {t_start:.1f}s - {t_end:.1f}s")
        print(f"Original sampling rate: {fs_high} Hz")
        print(f"Samples (original): {generation_stats['num_samples_high']}")
        print(f"Subsample rates: {subsample_rates}")
        print(f"Seed: {seed} (reproducible)")
        print(f"{'='*80}\n")
    
    # Generate signals
    for signal_num in range(1, num_signals + 1):
        try:
            # Generate base signal
            t_high, clean_signal, noisy_signal, signal_metadata = generate_demo_signal(
                t_start=t_start,
                t_end=t_end,
                fs_high=fs_high,
                noise_config=noise_config,
                rng=rng,
            )
            
            # Store signal metadata
            signal_metadata_enhanced = {
                "signal_id": signal_num,
                "generation_time": datetime.now().isoformat(),
                **signal_metadata,
                "subsampled_versions": {}
            }
            
            # Save high-resolution version and create subsampled versions
            for rate in subsample_rates:
                if rate == 1:
                    # Save original resolution
                    t_save = t_high
                    clean_save = clean_signal
                    noisy_save = noisy_signal
                    fs_save = fs_high
                else:
                    # Create subsampled version
                    t_save, clean_save, noisy_save = subsample_arrays(
                        t_high, clean_signal, noisy_signal, rate
                    )
                    fs_save = fs_high // rate
                
                # Save as .npz file
                filename = signal_dirs[rate] / f"signal_{signal_num:06d}.npz"
                np.savez(
                    filename,
                    t=t_save,
                    clean_signal=clean_save,
                    noisy_signal=noisy_save,
                    metadata=signal_metadata,
                )
                
                # Record subsampling info in metadata
                signal_metadata_enhanced["subsampled_versions"][f"{rate}x"] = {
                    "filename": str(filename.name),
                    "fs": float(fs_save),
                    "num_samples": len(noisy_save),
                    "path": str(signal_dirs[rate]),
                }
            
            all_metadata.append(signal_metadata_enhanced)
            
            # Collect statistics
            signal_stats["count"] += 1
            tau_amp = signal_metadata.get('tau_amplitude')
            if tau_amp != 'N/A':
                signal_stats["amp_tau_values"].append(float(tau_amp))
            
            spline_type = signal_metadata.get('amplitude_spline_type')
            if spline_type in signal_stats["amp_spline_types"]:
                signal_stats["amp_spline_types"][spline_type] += 1
            
            offset = signal_metadata.get('vertical_offset')
            if offset is not None:
                signal_stats["offsets"].append(float(offset))
            
            # Progress output
            if verbose and signal_num % 100 == 0:
                amp_tau = signal_metadata.get('tau_amplitude', 'N/A')
                amp_type = signal_metadata.get('amplitude_spline_type', 'N/A')
                elapsed = (datetime.fromisoformat(signal_metadata_enhanced["generation_time"]) - 
                          datetime.fromisoformat(generation_stats["start_time"])).total_seconds()
                rate_s = signal_num / elapsed if elapsed > 0 else 0
                remaining = (num_signals - signal_num) / rate_s if rate_s > 0 else 0
                print(f"  ✓ {signal_num:5d}/{num_signals} | "
                      f"tau_amp={str(amp_tau)[:5]:>5s} | type={amp_type:11s} | "
                      f"Rate: {rate_s:.1f} sig/s | ETA: {remaining/60:.1f}m")
        
        except Exception as e:
            signal_stats["errors"] += 1
            if verbose:
                print(f"  ✗ ERROR signal {signal_num}: {e}")
            continue
    
    # Save complete metadata
    metadata_file = base_path / "complete_metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump({
            "signals": all_metadata,
            "signal_statistics": signal_stats,
            "generation_statistics": generation_stats,
        }, f, indent=2, default=str)
    
    # Also save as pickle for faster loading
    pickle_file = base_path / "complete_metadata.pkl"
    with open(pickle_file, 'wb') as f:
        pickle.dump({
            "signals": all_metadata,
            "signal_statistics": signal_stats,
            "generation_statistics": generation_stats,
        }, f)
    
    generation_stats["end_time"] = datetime.now().isoformat()
    generation_stats["generated_signals"] = signal_stats["count"]
    generation_stats["failed_signals"] = signal_stats["errors"]
    generation_stats["metadata_file"] = str(metadata_file)
    generation_stats["pickle_file"] = str(pickle_file)
    
    # Print summary
    if verbose:
        print(f"\n{'='*80}")
        print(f"✅ Dataset Generation Complete")
        print(f"{'='*80}")
        print(f"Generated: {signal_stats['count']}/{num_signals} signals successfully")
        print(f"Failed: {signal_stats['errors']}")
        print(f"Output directory: {base_path}")
        print(f"\nFiles created:")
        for rate in subsample_rates:
            subdir = signal_dirs[rate]
            print(f"  • {subdir.name}/: {signal_stats['count']} .npz files")
        print(f"  • complete_metadata.json ({metadata_file.stat().st_size / (1024*1024):.1f} MB)")
        print(f"  • complete_metadata.pkl ({pickle_file.stat().st_size / (1024*1024):.1f} MB)")
        
        # Amplitude statistics
        if signal_stats["amp_tau_values"]:
            taus = np.array(signal_stats["amp_tau_values"])
            print(f"\nAmplitude Envelope Statistics:")
            print(f"  Tau values (tension splines):")
            print(f"    Mean: {np.mean(taus):.3f}")
            print(f"    Min:  {np.min(taus):.3f}")
            print(f"    Max:  {np.max(taus):.3f}")
            print(f"    Std:  {np.std(taus):.3f}")
        
        print(f"\nSpline Type Distribution:")
        total = signal_stats["amp_spline_types"]["tension"] + signal_stats["amp_spline_types"]["zero_order"]
        tension_pct = 100 * signal_stats["amp_spline_types"]["tension"] / total if total > 0 else 0
        step_pct = 100 * signal_stats["amp_spline_types"]["zero_order"] / total if total > 0 else 0
        print(f"  Tension splines: {signal_stats['amp_spline_types']['tension']:5d} ({tension_pct:5.1f}%)")
        print(f"  Step functions:  {signal_stats['amp_spline_types']['zero_order']:5d} ({step_pct:5.1f}%)")
        
        # Offset statistics
        if signal_stats["offsets"]:
            offsets = np.array(signal_stats["offsets"])
            print(f"\nVertical Offset Statistics:")
            print(f"  Mean: {np.mean(offsets):+.3f}")
            print(f"  Min:  {np.min(offsets):+.3f}")
            print(f"  Max:  {np.max(offsets):+.3f}")
            print(f"  Std:  {np.std(offsets):.3f}")
        
        # Sampling rate info
        print(f"\nSampling Rate Information:")
        for rate in subsample_rates:
            fs = fs_high // rate
            num_samples = int((t_end - t_start) * fs)
            print(f"  {rate}x downsampling: {fs:5d} Hz, {num_samples:5d} samples")
        
        print(f"{'='*80}\n")
    
    return generation_stats


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate complete optimized signal dataset with subsampling"
    )
    parser.add_argument("--count", type=int, default=2500,
                       help="Number of signals to generate (default: 2500)")
    parser.add_argument("--output", type=str, default="signals/Dataset_Optimized_2500",
                       help="Output directory base")
    parser.add_argument("--rates", type=int, nargs="+", default=[1, 2, 5, 10],
                       help="Subsample rates (default: 1 2 5 10)")
    parser.add_argument("--seed", type=int, default=42,
                       help="Random seed (default: 42)")
    parser.add_argument("--quiet", action="store_true",
                       help="Suppress progress output")
    
    args = parser.parse_args()
    
    stats = generate_complete_dataset(
        num_signals=args.count,
        output_dir=args.output,
        subsample_rates=args.rates,
        seed=args.seed,
        verbose=not args.quiet,
    )
    
    sys.exit(0 if stats["generated_signals"] == args.count else 1)
