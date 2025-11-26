#!/usr/bin/env python3
"""Test script to verify SignalBuilderC library functionality.

Run this from the parent directory of SignalBuilderC.
"""

import sys
from pathlib import Path

# Add current directory to path (parent of SignalBuilderC)
sys.path.insert(0, str(Path(__file__).parent.parent))

print("Testing SignalBuilderC library...\n")

# Test imports
print("1. Testing imports...")
try:
    from SignalBuilderC import (
        SignalConfig,
        BatchConfig,
        PathConfig,
        generate_signal,
        generate_signal_batch,
        analyze_batch_statistics,
        __version__,
    )
    print(f"   ✓ All imports successful (v{__version__})")
except ImportError as e:
    print(f"   ✗ Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test single signal generation
print("\n2. Testing single signal generation...")
try:
    signal_config = SignalConfig()
    t, signal, metadata = generate_signal(
        signal_id="TestSignal",
        config=signal_config,
        seed=42,
    )
    print(f"   ✓ Generated signal: {len(signal)} samples")
    print(f"   ✓ Metadata: {metadata.noise_type} noise, {metadata.amplitude_spline_type} amplitude")
except Exception as e:
    print(f"   ✗ Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test batch generation (small batch)
print("\n3. Testing batch generation...")
try:
    batch_config = BatchConfig(
        num_signals=3,
        seed_start=0,
        signal_config=SignalConfig(),
        save_figures=False,  # Skip figures for speed
    )
    path_config = PathConfig(base_dir="./SignalBuilderC/test_output")
    
    metadata_list = generate_signal_batch(
        batch_config=batch_config,
        path_config=path_config,
        verbose=False,
    )
    print(f"   ✓ Generated {len(metadata_list)} signals")
except Exception as e:
    print(f"   ✗ Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test batch statistics
print("\n4. Testing batch statistics...")
try:
    stats = analyze_batch_statistics(metadata_list, verbose=False)
    print(f"   ✓ Statistics computed for {stats['num_signals']} signals")
    print(f"   ✓ Noise distribution: {stats['noise_types']}")
except Exception as e:
    print(f"   ✗ Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*50)
print("All tests passed! ✓")
print("="*50)
print("\nSignalBuilderC library is ready for use!")
