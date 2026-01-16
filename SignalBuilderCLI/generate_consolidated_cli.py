#!/usr/bin/env python3
"""Generate a consolidated dataset (CLI wrapper).

This script is a thin wrapper that imports and calls the canonical consolidated
dataset generator used by the repository. It does not re-implement generation.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from SignalBuilderC.generate_consolidated_dataset import generate_consolidated_dataset

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate 2500 consolidated signals with subsampling (CLI wrapper)"
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
    
    # Construct absolute output path as SignalBuilderCLI/signals
    cli_signals_path = (Path(__file__).parent / args.output).absolute()
    
    # Call the function directly (not via subprocess)
    # Pass absolute path to ensure correct output location
    generate_consolidated_dataset(
        num_signals=args.count,
        output_dir=str(cli_signals_path),
        seed=args.seed,
        verbose=not args.quiet,
    )
