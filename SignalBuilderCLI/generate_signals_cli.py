#!/usr/bin/env python3
"""
SignalBuilderCLI - Command Line Interface for Synthetic Signal Generation

This script generates synthetic temporal signals with configurable parameters
for use in signal reconstruction and super-resolution tasks.

Usage:
    python generate_signals_cli.py --help
    python generate_signals_cli.py --num_signals 100 --output_dir ./output
    python generate_signals_cli.py --config config.json

Author: SignalBuilderCLI
Version: 1.0.0
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

import numpy as np

# Local imports
from signal_generator import generate_demo_signal
from noise_profiles import NoiseProfileConfig
from subsampling import generate_subsampled_versions
from data_export import (
    save_signal_npz,
    save_signal_txt,
    save_signal_json,
    save_consolidated_signals_npz,
    save_consolidated_signals_txt,
    save_consolidated_signals_json,
    save_consolidated_metadata_json,
    save_dataset_summary,
)

# Try to import tqdm for progress bar
try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    def tqdm(iterable, **kwargs):
        return iterable


def parse_list(value: str, dtype=int):
    """Parse a comma-separated string into a list."""
    return [dtype(x.strip()) for x in value.split(',')]


def normalize_csv_or_list(value, *, item_cast, field_name: str):
    """Normalize a config value that may be a CSV string or a JSON list.

    This is used to make `--save_config` round-trip friendly with `--config`.
    """
    if value is None:
        return None
    if isinstance(value, list):
        return [item_cast(v) for v in value]
    if isinstance(value, str):
        return [item_cast(x.strip()) for x in value.split(',') if x.strip()]
    raise TypeError(f"Invalid type for {field_name}: expected list or str, got {type(value).__name__}")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Generate synthetic temporal signals for signal reconstruction tasks.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage - generate 100 signals
  python generate_signals_cli.py --num_signals 100

  # Custom output directory and seed for reproducibility
  python generate_signals_cli.py --num_signals 500 --output_dir ./my_dataset --seed 42

  # Generate with specific subsample sizes
  python generate_signals_cli.py --num_signals 100 --subsample_sizes 150,250,500,1000

  # Enable anti-aliasing filtering (NOT recommended for reconstruction)
  python generate_signals_cli.py --num_signals 100 --use_antialiasing

  # Load configuration from JSON file
  python generate_signals_cli.py --config my_config.json

  # Save only consolidated files (not individual)
  python generate_signals_cli.py --num_signals 100 --no_individual --consolidated
        """
    )
    
    # ==================== GENERAL PARAMETERS ====================
    general = parser.add_argument_group('General Parameters')
    general.add_argument(
        '--num_signals', '-n',
        type=int,
        default=100,
        help='Number of signals to generate (default: 100)'
    )
    general.add_argument(
        '--t_start',
        type=float,
        default=0.0,
        help='Start time of signals (default: 0.0)'
    )
    general.add_argument(
        '--t_end',
        type=float,
        default=4 * np.pi,
        help='End time of signals (default: 4π ≈ 12.566)'
    )
    general.add_argument(
        '--num_samples',
        type=int,
        default=5000,
        help='Target number of high-resolution samples (default: 5000)'
    )
    general.add_argument(
        '--fs_high',
        type=float,
        default=None,
        help='High-resolution sampling frequency. If None, calculated from num_samples (default: None)'
    )
    general.add_argument(
        '--seed',
        type=int,
        default=None,
        help='Random seed for reproducibility (default: None = random)'
    )
    
    # ==================== FREQUENCY PARAMETERS ====================
    freq = parser.add_argument_group('Frequency Profile Parameters')
    freq.add_argument(
        '--tau_freq_min',
        type=float,
        default=1.0,
        help='Minimum tension parameter for frequency spline (default: 1.0)'
    )
    freq.add_argument(
        '--tau_freq_max',
        type=float,
        default=2.0,
        help='Maximum tension parameter for frequency spline (default: 2.0)'
    )
    freq.add_argument(
        '--high_freq_min',
        type=float,
        default=20.0,
        help='Minimum high frequency in Hz (default: 20.0)'
    )
    freq.add_argument(
        '--high_freq_max',
        type=float,
        default=100.0,
        help='Maximum high frequency in Hz (default: 100.0)'
    )
    freq.add_argument(
        '--low_freq_min',
        type=float,
        default=1.0,
        help='Minimum low frequency in Hz (default: 1.0)'
    )
    freq.add_argument(
        '--low_freq_max',
        type=float,
        default=5.0,
        help='Maximum low frequency in Hz (default: 5.0)'
    )
    
    # ==================== AMPLITUDE PARAMETERS ====================
    amp = parser.add_argument_group('Amplitude Envelope Parameters')
    amp.add_argument(
        '--p_tension_spline',
        type=float,
        default=0.5,
        help='Probability of using tension spline for amplitude (default: 0.5, balanced)'
    )
    amp.add_argument(
        '--tau_amp_min',
        type=float,
        default=0.5,
        help='Minimum tau for amplitude spline (default: 0.5)'
    )
    amp.add_argument(
        '--tau_amp_max',
        type=float,
        default=2.5,
        help='Maximum tau for amplitude spline (default: 2.5)'
    )
    amp.add_argument(
        '--amp_min',
        type=int,
        default=1,
        help='Minimum amplitude magnitude (default: 1)'
    )
    amp.add_argument(
        '--amp_max',
        type=int,
        default=8,
        help='Maximum amplitude magnitude (default: 8)'
    )
    
    # ==================== OFFSET PARAMETERS ====================
    offset = parser.add_argument_group('Vertical Offset Parameters')
    offset.add_argument(
        '--offset_mean',
        type=float,
        default=0.0,
        help='Mean of vertical offset normal distribution (default: 0.0)'
    )
    offset.add_argument(
        '--offset_std',
        type=float,
        default=3.0,
        help='Standard deviation of vertical offset (default: 3.0)'
    )
    
    # ==================== NOISE PARAMETERS ====================
    noise = parser.add_argument_group('Noise Profile Parameters')
    noise.add_argument(
        '--p_has_noise',
        type=float,
        default=0.8,
        help='Probability that a signal has noise (default: 0.8)'
    )
    noise.add_argument(
        '--p_gaussian',
        type=float,
        default=0.5,
        help='Probability of Gaussian noise given noise exists (default: 0.5)'
    )
    noise.add_argument(
        '--gaussian_std_relative',
        type=float,
        default=0.15,
        help='Gaussian noise std relative to signal RMS (default: 0.15)'
    )
    
    # ==================== SUBSAMPLING PARAMETERS ====================
    sub = parser.add_argument_group('Subsampling Parameters')
    sub.add_argument(
        '--subsample_sizes',
        type=str,
        default='150,250,500,1000',
        help='Comma-separated subsample sizes (default: 150,250,500,1000)'
    )
    sub.add_argument(
        '--use_antialiasing',
        action='store_true',
        default=False,
        help='Apply anti-aliasing filter before subsampling (default: False, simple re-evaluation)'
    )
    sub.add_argument(
        '--filter_type',
        type=str,
        choices=['butter', 'cheby1', 'ellip'],
        default='butter',
        help='Anti-aliasing filter type (default: butter). Only used if --use_antialiasing is set'
    )
    sub.add_argument(
        '--filter_order',
        type=int,
        default=8,
        help='Anti-aliasing filter order (default: 8). Only used if --use_antialiasing is set'
    )
    
    # ==================== OUTPUT PARAMETERS ====================
    out = parser.add_argument_group('Output Parameters')
    out.add_argument(
        '--output_dir', '-o',
        type=str,
        default='./output',
        help='Output directory (default: ./output)'
    )
    out.add_argument(
        '--formats',
        type=str,
        default='npz,txt,json',
        help='Comma-separated output formats: npz,txt,json (default: npz,txt,json)'
    )
    parser.set_defaults(consolidated=True)
    out.add_argument(
        '--consolidated',
        dest='consolidated',
        action='store_true',
        help='Save consolidated files with all signals (default: enabled)'
    )
    out.add_argument(
        '--no_consolidated',
        dest='consolidated',
        action='store_false',
        help='Disable consolidated files'
    )

    parser.set_defaults(individual=False)
    out.add_argument(
        '--individual',
        dest='individual',
        action='store_true',
        help='Save individual per-signal files (default: disabled)'
    )
    out.add_argument(
        '--no_individual',
        dest='individual',
        action='store_false',
        help='Disable individual per-signal files'
    )

    parser.set_defaults(save_metadata=True)
    out.add_argument(
        '--save_metadata',
        dest='save_metadata',
        action='store_true',
        help='Save signal metadata JSON (default: enabled)'
    )
    out.add_argument(
        '--no_metadata',
        dest='save_metadata',
        action='store_false',
        help='Disable metadata JSON'
    )
    out.add_argument(
        '--prefix',
        type=str,
        default='signal',
        help='Prefix for output files (default: signal)'
    )
    
    # ==================== CONFIGURATION FILE ====================
    config = parser.add_argument_group('Configuration')
    config.add_argument(
        '--config', '-c',
        type=str,
        default=None,
        help='Path to JSON configuration file (overrides command line arguments)'
    )
    config.add_argument(
        '--save_config',
        type=str,
        default=None,
        help='Save current configuration to JSON file'
    )
    config.add_argument(
        '--verbose', '-v',
        action='store_true',
        default=False,
        help='Verbose output'
    )
    
    return parser.parse_args()


def load_config(config_path: str) -> dict:
    """Load configuration from JSON file."""
    with open(config_path, 'r') as f:
        return json.load(f)


def save_config(config: dict, config_path: str):
    """Save configuration to JSON file."""
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)


def args_to_config(args) -> dict:
    """Convert argparse namespace to configuration dictionary."""
    t_start = float(args.t_start)
    t_end = float(args.t_end)
    num_samples = int(args.num_samples)
    fs_high = args.fs_high
    if fs_high is None:
        duration = t_end - t_start
        if duration <= 0:
            raise ValueError(f"Invalid time range: t_end ({t_end}) must be > t_start ({t_start})")
        fs_high = num_samples / duration

    subsample_sizes = normalize_csv_or_list(
        args.subsample_sizes,
        item_cast=int,
        field_name='subsample_sizes',
    )
    if subsample_sizes is None:
        subsample_sizes = parse_list('150,250,500,1000', int)

    formats = normalize_csv_or_list(
        args.formats,
        item_cast=lambda s: str(s).strip(),
        field_name='formats',
    )
    if formats is None:
        formats = [f.strip() for f in 'npz,txt,json'.split(',')]
    formats = [f for f in formats if f]

    return {
        'num_signals': args.num_signals,
        't_start': t_start,
        't_end': t_end,
        'num_samples': num_samples,
        'fs_high': float(fs_high),
        'seed': args.seed,
        'tau_freq_min': args.tau_freq_min,
        'tau_freq_max': args.tau_freq_max,
        'high_freq_min': args.high_freq_min,
        'high_freq_max': args.high_freq_max,
        'low_freq_min': args.low_freq_min,
        'low_freq_max': args.low_freq_max,
        'p_tension_spline': args.p_tension_spline,
        'tau_amp_min': args.tau_amp_min,
        'tau_amp_max': args.tau_amp_max,
        'amp_min': args.amp_min,
        'amp_max': args.amp_max,
        'offset_mean': args.offset_mean,
        'offset_std': args.offset_std,
        'p_has_noise': args.p_has_noise,
        'p_gaussian': args.p_gaussian,
        'gaussian_std_relative': args.gaussian_std_relative,
        'subsample_sizes': subsample_sizes,
        'use_antialiasing': args.use_antialiasing,
        'filter_type': args.filter_type,
        'filter_order': args.filter_order,
        'output_dir': args.output_dir,
        'formats': formats,
        'consolidated': bool(args.consolidated),
        'individual': bool(args.individual),
        'save_metadata': bool(args.save_metadata),
        'prefix': args.prefix,
        'verbose': args.verbose,
    }


def merge_config(args, file_config: dict):
    """Merge file configuration into args (file config takes precedence)."""
    for key, value in file_config.items():
        if hasattr(args, key):
            setattr(args, key, value)
    return args


def print_config(config: dict):
    """Print configuration summary."""
    print("\n" + "="*60)
    print("SIGNAL GENERATION CONFIGURATION")
    print("="*60)
    print(f"  Signals to generate: {config['num_signals']}")
    print(f"  Time range: [{config['t_start']}, {config['t_end']}]")
    print(f"  Samples per signal (high-res): {config.get('num_samples', 'N/A')}")
    print(f"  High-res sampling: {config['fs_high']} Hz")
    print(f"  Random seed: {config['seed']}")
    print(f"\n  Frequency range (low): [{config['low_freq_min']}, {config['low_freq_max']}] Hz")
    print(f"  Frequency range (high): [{config['high_freq_min']}, {config['high_freq_max']}] Hz")
    print(f"  Frequency tau range: [{config['tau_freq_min']}, {config['tau_freq_max']}]")
    print(f"\n  Amplitude range: [{config['amp_min']}, {config['amp_max']}]")
    print(f"  P(tension spline): {config['p_tension_spline']} (step function: {1-config['p_tension_spline']})")
    print(f"  Amplitude tau range: [{config['tau_amp_min']}, {config['tau_amp_max']}]")
    print(f"\n  Offset distribution: N({config['offset_mean']}, {config['offset_std']})")
    print(f"\n  P(has noise): {config['p_has_noise']}")
    print(f"  P(gaussian | noise): {config['p_gaussian']}")
    print(f"  Gaussian std (relative): {config['gaussian_std_relative']}")
    print(f"\n  Subsample sizes: {config['subsample_sizes']}")
    print(f"  Anti-aliasing: {'ENABLED' if config['use_antialiasing'] else 'DISABLED (simple re-evaluation)'}")
    if config['use_antialiasing']:
        print(f"  Filter: {config['filter_type']}, order={config['filter_order']}")
    print(f"\n  Output directory: {config['output_dir']}")
    print(f"  Output formats: {config['formats']}")
    print(f"  Save consolidated: {config['consolidated']}")
    print(f"  Save individual: {config['individual']}")
    print("="*60 + "\n")


def generate_signals(config: dict):
    """Main signal generation function."""
    # Setup
    output_dir = Path(config['output_dir'])
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create subdirectories
    if config['individual']:
        (output_dir / 'individual').mkdir(exist_ok=True)
    
    # Initialize RNG
    seed = config['seed']
    if seed is None:
        seed = np.random.default_rng().integers(0, 2**31)
    rng = np.random.default_rng(seed)
    config['seed_used'] = seed
    
    # Noise configuration
    noise_config = NoiseProfileConfig(
        p_has_noise=config['p_has_noise'],
        p_gaussian=config['p_gaussian'],
        gaussian_std_relative=config['gaussian_std_relative'],
    )
    
    # Storage for consolidated data
    num_signals = config['num_signals']
    t_start = config['t_start']
    t_end = config['t_end']
    fs_high = config['fs_high']
    subsample_sizes = config['subsample_sizes']
    
    # Calculate sizes
    n_samples_high = int((t_end - t_start) * fs_high)
    
    all_signals_high = []
    all_clean_signals_high = []
    all_metadata = []
    all_subsampled = {size: [] for size in subsample_sizes}
    
    print(f"\nGenerating {num_signals} signals...")
    
    # Generate signals
    iterator = range(num_signals)
    if HAS_TQDM:
        iterator = tqdm(iterator, desc="Generating signals", unit="signal")
    
    for i in iterator:
        # Generate high-resolution signal
        t_high, clean_signal, noisy_signal, metadata = generate_demo_signal(
            t_start=t_start,
            t_end=t_end,
            fs_high=fs_high,
            noise_config=noise_config,
            rng=rng,
            tau_freq_min=config['tau_freq_min'],
            tau_freq_max=config['tau_freq_max'],
            high_freq_min=config['high_freq_min'],
            high_freq_max=config['high_freq_max'],
            low_freq_min=config['low_freq_min'],
            low_freq_max=config['low_freq_max'],
            p_tension_spline=config['p_tension_spline'],
            tau_amp_min=config['tau_amp_min'],
            tau_amp_max=config['tau_amp_max'],
            amp_min=config['amp_min'],
            amp_max=config['amp_max'],
            offset_mean=config['offset_mean'],
            offset_std=config['offset_std'],
        )
        
        metadata['signal_index'] = i
        
        # Generate subsampled versions
        subsampled = generate_subsampled_versions(
            signal_metadata=metadata,
            t_start=t_start,
            t_end=t_end,
            subsample_sizes=subsample_sizes,
            rng=rng,
            use_antialiasing=config['use_antialiasing'],
            t_original=t_high,
            signal_original=noisy_signal,
            filter_type=config['filter_type'],
            filter_order=config['filter_order'],
        )
        
        # Store data
        all_signals_high.append(noisy_signal)
        all_clean_signals_high.append(clean_signal)
        all_metadata.append(metadata)
        
        for size in subsample_sizes:
            t_sub, signal_sub = subsampled[size]
            all_subsampled[size].append(signal_sub)
        
        # Save individual files if requested
        if config['individual']:
            base_path = output_dir / 'individual' / f"{config['prefix']}_{i:06d}"
            
            if 'npz' in config['formats']:
                save_signal_npz(
                    f"{base_path}.npz", 
                    noisy_signal, 
                    t_high, 
                    clean_signal, 
                    metadata
                )
            if 'txt' in config['formats']:
                save_signal_txt(f"{base_path}.txt", noisy_signal)
            if 'json' in config['formats']:
                save_signal_json(f"{base_path}.json", noisy_signal, t_high)
    
    # Convert to arrays
    all_signals_high = np.array(all_signals_high)
    all_clean_signals_high = np.array(all_clean_signals_high)
    for size in subsample_sizes:
        all_subsampled[size] = np.array(all_subsampled[size])
    
    # Save consolidated files
    if config['consolidated']:
        print("\nSaving consolidated files...")
        
        # High-resolution signals
        base_name = f"signals_high_resolution_{n_samples_high}"
        if 'npz' in config['formats']:
            save_consolidated_signals_npz(
                str(output_dir / f"{base_name}.npz"),
                all_signals_high,
                t_high,
                all_clean_signals_high,
            )
        if 'txt' in config['formats']:
            save_consolidated_signals_txt(
                str(output_dir / f"{base_name}.txt"),
                all_signals_high,
            )
        if 'json' in config['formats']:
            save_consolidated_signals_json(
                str(output_dir / f"{base_name}.json"),
                all_signals_high,
                t_high,
            )
        
        # Subsampled signals
        subsample_method = "filtered" if config['use_antialiasing'] else "simple"
        for size in subsample_sizes:
            t_sub = np.linspace(t_start, t_end, size)
            base_name = f"signals_subsampled_{subsample_method}_{size}"
            
            if 'npz' in config['formats']:
                save_consolidated_signals_npz(
                    str(output_dir / f"{base_name}.npz"),
                    all_subsampled[size],
                    t_sub,
                )
            if 'txt' in config['formats']:
                save_consolidated_signals_txt(
                    str(output_dir / f"{base_name}.txt"),
                    all_subsampled[size],
                )
            if 'json' in config['formats']:
                save_consolidated_signals_json(
                    str(output_dir / f"{base_name}.json"),
                    all_subsampled[size],
                    t_sub,
                )
        
        # Metadata
        if config['save_metadata']:
            save_consolidated_metadata_json(
                str(output_dir / "signals_metadata.json"),
                all_metadata,
            )
    
    # Create dataset summary
    summary = {
        'generation_date': datetime.now().isoformat(),
        'num_signals': num_signals,
        'seed_used': config['seed_used'],
        't_start': t_start,
        't_end': t_end,
        'fs_high': fs_high,
        'n_samples_high': n_samples_high,
        'subsample_sizes': subsample_sizes,
        'subsample_method': 'filtered' if config['use_antialiasing'] else 'simple',
        'noise_config': {
            'p_has_noise': config['p_has_noise'],
            'p_gaussian': config['p_gaussian'],
            'gaussian_std_relative': config['gaussian_std_relative'],
        },
        'frequency_config': {
            'tau_range': [config['tau_freq_min'], config['tau_freq_max']],
            'low_freq_range': [config['low_freq_min'], config['low_freq_max']],
            'high_freq_range': [config['high_freq_min'], config['high_freq_max']],
        },
        'amplitude_config': {
            'p_tension_spline': config['p_tension_spline'],
            'tau_range': [config['tau_amp_min'], config['tau_amp_max']],
            'amp_range': [config['amp_min'], config['amp_max']],
        },
        'offset_config': {
            'mean': config['offset_mean'],
            'std': config['offset_std'],
        },
        'files_generated': {
            'high_resolution': f"signals_high_resolution_{n_samples_high}",
            'subsampled': [f"signals_subsampled_{subsample_method}_{s}" for s in subsample_sizes],
            'metadata': 'signals_metadata.json' if config['save_metadata'] else None,
        },
    }
    
    if config['use_antialiasing']:
        summary['filter_info'] = {
            'type': config['filter_type'],
            'order': config['filter_order'],
        }
    
    save_dataset_summary(str(output_dir / "dataset_summary.json"), summary)
    
    print(f"\n✓ Generation complete!")
    print(f"  Output directory: {output_dir}")
    print(f"  Signals generated: {num_signals}")
    print(f"  Seed used: {config['seed_used']}")
    
    return summary


def main():
    """Main entry point."""
    args = parse_arguments()
    
    # Load config file if provided
    if args.config:
        file_config = load_config(args.config)
        args = merge_config(args, file_config)
    
    # Convert to config dict
    config = args_to_config(args)
    
    # Save config if requested
    if args.save_config:
        save_config(config, args.save_config)
        print(f"Configuration saved to: {args.save_config}")
        return
    
    # Print configuration
    if config['verbose']:
        print_config(config)
    
    # Generate signals
    try:
        summary = generate_signals(config)
    except KeyboardInterrupt:
        print("\n\nGeneration interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError during generation: {e}")
        raise


if __name__ == '__main__':
    main()
