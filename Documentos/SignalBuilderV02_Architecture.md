## SignalBuilderV02: Architecture and Engineering Overview

This document describes the architecture, design decisions, and implementation
details of the `SignalBuilderV02` package. The goal of this package is to
provide a transparent, reproducible, and extensible framework for generating
synthetic temporal signals with spline-based envelopes and non-uniform
frequency content. It is designed to accompany the CoSiBD dataset and to
address reviewer concerns about realism, reproducibility, and documentation.

### 1. High-level goals

- **Realistic yet controllable signals**: combine smooth amplitude and
	frequency envelopes with localized high-frequency bursts.
- **Explicit sampling and anti-aliasing**: make sampling rates and
	resampling steps explicit so that aliasing can be discussed and controlled.
- **Reproducibility**: use explicit random seeds and record them in metadata.
- **Rich metadata**: annotate each signal with parameters, envelopes, and
	segment types (low / high / no-change frequency regions).
- **Extensibility**: allow new envelope types, noise models, and validation
	routines to be added without breaking the public API.

The implementation is split into small, testable modules. Below we describe
each part in detail.

### 2. Package layout

At the top level of the project we have the following structure:

- `SignalBuilderV02/src/`
	- `splines.py`: spline-based envelope utilities.
	- `frequency_profiles.py`: non-uniform frequency profile generators.
	- `__init__.py`: public API surface for the core utilities.
- `data/`
	- `signals/`: binary or text files containing generated signals.
	- `metadata/`: JSON or CSV files describing each generated signal.
- `figures/`: plots used for the paper or for exploratory analysis.
- `notebooks/`: Jupyter notebooks demonstrating the generation pipeline.

This layout separates the reusable library code (`SignalBuilderV02/src`) from
experiment artifacts (signals, metadata, and figures).

### 3. Core module: `splines.py`

The `splines.py` module collects spline-based interpolators that are used to
construct amplitude and frequency envelopes. The functions are:

#### 3.1 `tension_spline_interpolator`

```python
def tension_spline_interpolator(
		x: Sequence[float],
		y: Sequence[float],
		tau: float,
) -> Callable[[np.ndarray], np.ndarray]:
		"""Create a tension spline interpolator.

		This is equivalent in spirit to the original implementation in
		`temana.py` and is kept as the core envelope builder.
		"""
```

- **Inputs**:
	- `x`: strictly increasing knot positions.
	- `y`: envelope values at the knots.
	- `tau`: tension parameter controlling how stiff the spline is.
- **Output**: a callable `evaluate(x_eval)` that returns interpolated values
	at arbitrary positions `x_eval`.

Internally, the function:

1. Converts `x` and `y` to NumPy arrays and computes interval lengths `h`.
2. Builds a tridiagonal-like system `A z = rhs`, where `z` are auxiliary
	 values controlling the curvature under tension.
3. Solves for `z` using `np.linalg.solve`.
4. Returns an `evaluate` closure that, for each evaluation point, identifies
	 the interval `[x[i], x[i+1]]` and applies the closed-form expression for
	 the tension spline segment.

This implementation preserves the essence of the original tension spline used
in CoSiBD while making the code self-contained and easier to test.

#### 3.2 `zero_order_spline_interpolator`

```python
def zero_order_spline_interpolator(
		points: Iterable[Tuple[float, float]],
) -> Callable[[np.ndarray], np.ndarray]:
		"""Create a zero-order (stepwise) interpolator from (x, y) points."""
```

- Wraps `scipy.interpolate.interp1d` with `kind="zero"`.
- Useful for piecewise-constant envelopes (e.g., step changes in amplitude
	or frequency).

#### 3.3 `n_degree_spline_interpolator`

```python
def n_degree_spline_interpolator(
		points: Iterable[Tuple[float, float]],
		degree: int,
) -> Callable[[np.ndarray], np.ndarray]:
		"""Create an n-degree spline interpolator from (x, y) points."""
```

- Uses `scipy.interpolate.make_interp_spline` with degree `k=degree`.
- Provides a flexible way to create smooth envelopes of arbitrary order
	(e.g., cubic splines for smooth trends).

Together, these interpolators are the main tools for constructing the
amplitude and frequency envelopes that define each synthetic signal.

### 4. Core module: `frequency_profiles.py`

The `frequency_profiles.py` module generates non-uniform frequency profiles
that alternate between low-frequency and high-frequency regimes. The key
function is:

#### 4.1 `generate_non_uniform_high_low_frequency_points`

```python
def generate_non_uniform_high_low_frequency_points(
		x0: float,
		x1: float,
) -> Tuple[List[Tuple[float, float]],
					 List[Tuple[float, float]],
					 List[VariationType]]:
		"""Generate non-uniform low/high frequency reference points.

		The design mirrors the original generator, keeping the idea of
		long low-frequency segments with occasional high-frequency bursts.
		"""
```

- **Inputs**:
	- `x0`, `x1`: start and end of the temporal interval.
- **Outputs**:
	- `points`: list of `(time, base_frequency)` pairs describing the base
		low-frequency envelope.
	- `high_freq_points`: list of `(time, high_frequency)` pairs describing
		additional high-frequency bursts (often zero outside bursts).
	- `variation_type`: list of `"low"`, `"high"`, or `"no_change"` labels for
		each segment.

The algorithm:

1. Samples candidate low-frequency values in `[1, 5]` Hz and high-frequency
	 values in `[20, 100]` Hz.
2. Draws a non-uniform partition of the interval `[x0, x1]` using random
	 points scaled to the interval.
3. Iterates over segments, deciding whether each segment is `low`, `high`, or
	 `no_change` using a categorical distribution with specified probabilities.
4. When a segment is labeled `high`, it inserts high-frequency points within
	 the segment (using an additional random time inside the interval).
5. Records both the base low-frequency value (`points`) and the high-frequency
	 bursts (`high_freq_points`), along with the segment labels.

This function preserves the logic of the original `temana.py` generator while
making the outputs explicit and easy to feed into envelope and metadata
generation.

### 5. Public API module: `__init__.py`

The `SignalBuilderV02/src/__init__.py` file exposes the core utilities:

```python
from .splines import (
		tension_spline_interpolator,
		zero_order_spline_interpolator,
		n_degree_spline_interpolator,
)
from .frequency_profiles import generate_non_uniform_high_low_frequency_points

__all__ = [
		"tension_spline_interpolator",
		"zero_order_spline_interpolator",
		"n_degree_spline_interpolator",
		"generate_non_uniform_high_low_frequency_points",
]
```

This keeps the public surface small and focused. External code should import
from `SignalBuilderV02` rather than reaching into the individual modules.

### 6. Planned module: `signals.py`

The next step in the design is a `signals.py` module that will:

- Compose spline-based envelopes and frequency profiles into full-resolution
	time series.
- Apply explicit sampling (and, if needed, pre-filtering) for low-resolution
	and high-resolution versions of each signal.
- Add configurable noise models (e.g., Gaussian white noise, band-limited
	noise, and optional sinusoidal components for comparison with the original
	generator).
- Return both raw arrays and structured metadata for each generated signal.

A typical high-level function might look like:

```python
def generate_signal(
		duration: float,
		fs_high: float,
		fs_low: float,
		seed: int,
		noise_config: NoiseConfig,
) -> Tuple[np.ndarray, np.ndarray, dict]:
		"""Generate a pair of (low-res, high-res) signals and metadata."""
```

Internally, it would:

1. Set random seeds for NumPy and Python's `random`.
2. Call `generate_non_uniform_high_low_frequency_points` to obtain segment
	 structure.
3. Build amplitude and frequency envelopes using the spline interpolators.
4. Synthesize the underlying clean signal from the envelopes.
5. Generate noise according to `noise_config` and add it to the clean signal.
6. Apply appropriate filtering before downsampling from `fs_high` to `fs_low`
	 to control aliasing.
7. Assemble metadata describing all of the above choices.

### 7. Metadata design

Metadata is critical for reproducibility and for enabling downstream analyses.
We envision two levels of metadata:

1. **Per-signal metadata** (stored as one JSON object per signal or as rows in
	 a CSV file):
	 - `signal_id`: unique identifier.
	 - `seed`: integer random seed used for this signal.
	 - `duration`: total duration in seconds.
	 - `fs_high`, `fs_low`: sampling rates for high- and low-resolution
		 versions.
	 - `low_freq_points`: list of `(time, frequency)` pairs.
	 - `high_freq_points`: list of `(time, frequency)` pairs for bursts.
	 - `variation_type`: list of segment labels (`low`, `high`, `no_change`).
	 - `amplitude_envelope_params`: description of knots and spline type.
	 - `noise_config`: parameters of the noise model (e.g., standard deviation,
		 bandwidth, optional sinusoidal components).
	 - `generation_version`: version string for the generator code.

2. **Dataset-level metadata** (a summary JSON/CSV file):
	 - Number of signals.
	 - Global ranges for duration, sampling rates, and noise levels.
	 - Date of generation.
	 - Git commit hash or code version tag.

The metadata files are stored under `data/metadata/`, while the corresponding
signals are stored under `data/signals/` with a filename convention that ties
signals to their metadata (e.g., `signal_000123.npy` with
`signal_000123.json`).

### 8. Reproducibility and random seeds

To ensure reproducibility:

- All top-level generation functions accept a `seed` argument.
- The seed is used to initialize both `numpy.random` and Python's `random`
	module.
- The seed is recorded in the per-signal metadata.
- For batch generation (datasets), we also record the master seed and the
	sequence of per-signal seeds.

This design guarantees that a dataset can be exactly regenerated by another
researcher using the same code version and configuration.

### 9. Extending the library

The modular design makes it straightforward to extend `SignalBuilderV02`:

- **New envelope types**: implement additional interpolators or envelope
	shapes in `splines.py` or a new module, and plug them into `signals.py`.
- **New frequency profiles**: add alternative profile generators in
	`frequency_profiles.py` (e.g., more structured bursts, rhythmic patterns).
- **New noise models**: define new `NoiseConfig` variants that generate
	different types of noise (e.g., colored noise) and integrate them into the
	signal synthesis functions.
- **Validation utilities**: add modules for computing power spectral density,
	SNR, and other diagnostics directly from generated signals.

Because the public API is small and explicit, these extensions can be made
without breaking existing code that depends on `SignalBuilderV02`.

### 10. Example usage

Below is a high-level example of how the library is intended to be used once
the `signals.py` module is implemented:

```python
from SignalBuilderV02 import (
		tension_spline_interpolator,
		generate_non_uniform_high_low_frequency_points,
)

duration = 10.0  # seconds
fs_high = 512.0  # Hz
fs_low = 128.0   # Hz
seed = 42

# 1. Generate non-uniform frequency profile
points, high_freq_points, variation_type = (
		generate_non_uniform_high_low_frequency_points(0.0, duration)
)

# 2. Build an amplitude envelope (example with a simple spline)
amp_knots = [0.0, duration * 0.5, duration]
amp_values = [1.0, 2.0, 1.0]
amp_spline = tension_spline_interpolator(amp_knots, amp_values, tau=1.0)

# 3. (Future) Generate full signals and metadata using signals.py
# low_res, high_res, meta = generate_signal(
#     duration=duration,
#     fs_high=fs_high,
#     fs_low=fs_low,
#     seed=seed,
#     noise_config=NoiseConfig(...),
# )
```

This example shows how the existing building blocks fit together and how the
planned `signals.py` module will provide a higher-level interface for
generating complete datasets.
