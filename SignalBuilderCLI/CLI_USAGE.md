# SignalBuilderCLI — CLI Usage

This folder provides two command-line entry points.

## What each command does

### `generate_consolidated_cli.py` — paper dataset reproduction

Generates the consolidated dataset used for the paper workflow.

- High-resolution signals are exported as `.npz`.
- Subsampled versions are exported using **simple subsampling (no anti-aliasing / no filtering)**.
- A consolidated metadata `.json` is also exported.

Use this command when your goal is to reproduce the paper CoSiBD dataset generation settings.

### `generate_signals_cli.py` — custom dataset generation

Generates synthetic signals with user-controlled parameters such as frequency profile, amplitude envelope, noise, and subsampling. Exports consolidated files and can optionally export per-signal files.

Use this command when you need a custom dataset for experiments.

---

## Quick start

### 1) Install

From the project root:

```bash
python -m pip install -r SignalBuilderCLI/requirements.txt
```

Then:

```bash
cd SignalBuilderCLI
```

### 2) Paper dataset — recommended

Run. Defaults reproduce the paper dataset generation settings:

```bash
python generate_consolidated_cli.py
```

That creates a `signals/` folder with `.npz` files and a metadata `.json`.

Important: the subsampled files are **simple subsampling (no anti-aliasing / no filtering)**.

### 3) Custom dataset — advanced

Minimal example, small and consolidated-only:

```bash
python generate_signals_cli.py --num_signals 5 --seed 42 --formats npz --output_dir ./output_example --no_individual
```

---

## Notes

- If you only want the paper dataset, use **only** `generate_consolidated_cli.py`.
- Anti-aliasing exists as an optional capability for alternative experiments, but it is **not used for the paper workflow**.
- For the full list of options at any time: run `--help`.

---

## Command 1: reproduce the consolidated CoSiBD dataset

This is a thin wrapper that invokes the canonical consolidated-dataset generator used to build the paper dataset.

**Reproducibility guarantee (signal content):** same parameters + same seed ⇒ same numerical signals.

### Syntax

```bash
python generate_consolidated_cli.py [--count N] [--seed S] [--output DIR] [--quiet]
```

Running with **no arguments** applies the paper defaults:

```bash
python generate_consolidated_cli.py
```

### Parameters

| Parameter | Type | Required | Default | Allowed values | Description |
|---|---:|:---:|---:|---|---|
| `--count` | int | No | 2500 | integer ≥ 1 | Number of signals to generate. |
| `--seed` | int | No | 42 | any integer | Random seed for reproducibility. Same seed ⇒ same dataset. |
| `--output` | str | No | `signals` | valid path | Output directory (created if needed). Default is `SignalBuilderCLI/signals/`. |
| `--quiet` | flag | No | disabled | (flag) | Suppress console output. |

Tip: see all flags with:

```bash
python generate_consolidated_cli.py --help
```

### Examples

All examples assume:

```bash
cd SignalBuilderCLI
```

- Default paper run (all defaults):
  ```bash
  python generate_consolidated_cli.py
  ```
- `--count`:
  ```bash
  python generate_consolidated_cli.py --count 100
  ```
- `--seed`:
  ```bash
  python generate_consolidated_cli.py --seed 12345
  ```
- `--output`:
  ```bash
  python generate_consolidated_cli.py --output signals_paper_run
  ```
- `--quiet`:
  ```bash
  python generate_consolidated_cli.py --quiet
  ```

### Outputs

In the directory specified by `--output` (default: `SignalBuilderCLI/signals/`):

- `signals_high_resolution_5000.npz`
- `signals_subsampled_simple_150.npz`
- `signals_subsampled_simple_250.npz`
- `signals_subsampled_simple_500.npz`
- `signals_subsampled_simple_1000.npz`
- `signals_metadata_consolidated_2500.json`

Typical NPZ keys:

- `signals`: shape `(count, N)`
- `clean_signals`: shape `(count, N)`
- `t`: shape `(N,)`

---

## Command 2: configurable signal generation

This entry point is meant for controlled experiments where you want to vary parameters and export formats.

**Important:** if your requirement is **exact paper reproduction**, you must use **Command 1**. The configurable generator is a separate workflow.

### Syntax

```bash
python generate_signals_cli.py [options]
```

### Notes

- `--help` prints the full option list.
- If `--fs_high` is omitted, it is computed as: `fs_high = num_samples / (t_end - t_start)`
- Anti-aliasing (`--use_antialiasing`) is optional and not used for the paper workflow.

Show all options:

```bash
python generate_signals_cli.py --help
```

---

## Common options

These are the options most people actually use:

- `--num_signals` / `-n`: how many signals
- `--seed`: reproducibility
- `--output_dir` / `-o`: where files go
- `--formats`: `npz` is usually enough
- `--subsample_sizes`: defaults match the paper-like sizes
- `--no_individual` / `--individual`: usually keep `--no_individual`

Everything else is advanced tuning.

---

## Full option reference

### General

| Parameter | Type | Required | Default | Allowed values | Description |
|---|---:|:---:|---:|---|---|
| `--num_signals`, `-n` | int | No | 100 | integer ≥ 1 | Number of signals to generate. |
| `--t_start` | float | No | 0.0 | real | Start of the time domain. |
| `--t_end` | float | No | 4π | real, must be > `t_start` | End of the time domain. |
| `--num_samples` | int | No | 5000 | integer ≥ 2 | Target high-resolution samples (used if `--fs_high` is omitted). |
| `--fs_high` | float | No | `None` | real > 0 | High-resolution sampling frequency. If `None`, derived from `--num_samples`. |
| `--seed` | int | No | `None` | any integer | Seed. If omitted, a random seed is chosen and stored as `seed_used`. |

### Frequency profile

| Parameter | Type | Required | Default | Allowed values | Description |
|---|---:|:---:|---:|---|---|
| `--tau_freq_min` | float | No | 1.0 | real > 0 | Minimum τ for the frequency tension spline. |
| `--tau_freq_max` | float | No | 2.0 | real > 0 | Maximum τ for the frequency tension spline. |
| `--low_freq_min` | float | No | 1.0 | real ≥ 0 | Minimum low frequency (Hz). |
| `--low_freq_max` | float | No | 5.0 | real ≥ `low_freq_min` | Maximum low frequency (Hz). |
| `--high_freq_min` | float | No | 20.0 | real ≥ 0 | Minimum high frequency (Hz). |
| `--high_freq_max` | float | No | 100.0 | real ≥ `high_freq_min` | Maximum high frequency (Hz). |

### Amplitude envelope

| Parameter | Type | Required | Default | Allowed values | Description |
|---|---:|:---:|---:|---|---|
| `--p_tension_spline` | float | No | 0.5 | [0, 1] | Probability of using a tension spline (vs step / zero-order) for the amplitude envelope. |
| `--tau_amp_min` | float | No | 0.5 | real > 0 | Minimum τ for the amplitude tension spline (only used when spline is selected). |
| `--tau_amp_max` | float | No | 2.5 | real > 0 | Maximum τ for the amplitude tension spline (only used when spline is selected). |
| `--amp_min` | int | No | 1 | integer ≥ 1 | Minimum amplitude magnitude. |
| `--amp_max` | int | No | 8 | integer ≥ `amp_min` | Maximum amplitude magnitude. |

### Vertical offset

| Parameter | Type | Required | Default | Allowed values | Description |
|---|---:|:---:|---:|---|---|
| `--offset_mean` | float | No | 0.0 | real | Mean of the vertical offset. |
| `--offset_std` | float | No | 3.0 | real ≥ 0 | Standard deviation of the vertical offset. |

### Noise

| Parameter | Type | Required | Default | Allowed values | Description |
|---|---:|:---:|---:|---|---|
| `--p_has_noise` | float | No | 0.8 | [0, 1] | Probability that a signal includes noise. |
| `--p_gaussian` | float | No | 0.5 | [0, 1] | Probability of Gaussian noise given that noise exists. |
| `--gaussian_std_relative` | float | No | 0.15 | real ≥ 0 | Gaussian σ relative to signal RMS. |

### Subsampling

| Parameter | Type | Required | Default | Allowed values | Description |
|---|---:|:---:|---:|---|---|
| `--subsample_sizes` | str (csv) | No | `150,250,500,1000` | comma-separated integers | Target subsample sizes. |
| `--use_antialiasing` | flag | No | disabled | (flag) | Apply anti-aliasing filter before subsampling (optional; not part of paper workflow). |
| `--filter_type` | str | No | `butter` | `butter`, `cheby1`, `ellip` | Filter type (only used if `--use_antialiasing`). |
| `--filter_order` | int | No | 8 | integer ≥ 1 | Filter order (only used if `--use_antialiasing`). |

### Output

| Parameter | Type | Required | Default | Allowed values | Description |
|---|---:|:---:|---:|---|---|
| `--output_dir`, `-o` | str | No | `./output` | valid path | Output directory. |
| `--formats` | str (csv) | No | `npz,txt,json` | any combo of `npz`, `txt`, `json` | Output formats (comma-separated). |
| `--consolidated` | flag | No | enabled | (flag) | Enable consolidated outputs. |
| `--no_consolidated` | flag | No | disabled | (flag) | Disable consolidated outputs. |
| `--individual` | flag | No | disabled | (flag) | Enable per-signal files under `output_dir/individual/`. |
| `--no_individual` | flag | No | disabled | (flag) | Disable per-signal files. |
| `--save_metadata` | flag | No | enabled | (flag) | Save `signals_metadata.json`. |
| `--no_metadata` | flag | No | disabled | (flag) | Disable metadata JSON. |
| `--prefix` | str | No | `signal` | string | Prefix for per-signal file names (only if `--individual`). |
| `--verbose`, `-v` | flag | No | disabled | (flag) | Print configuration summary and more logs. |

### Configuration file

| Parameter | Type | Required | Default | Allowed values | Description |
|---|---:|:---:|---:|---|---|
| `--config`, `-c` | str | No | `None` | path to JSON | Load options from a JSON file (overrides CLI args). |
| `--save_config` | str | No | `None` | path to JSON | Save the effective configuration to JSON and exit. |

---

## Appendix: examples

All examples assume:

```bash
cd SignalBuilderCLI
```

Base example used below (small and fast):

```bash
python generate_signals_cli.py --num_signals 5 --seed 42 --formats npz --output_dir ./output_example --no_individual
```

### Help

- `--help`:
  ```bash
  python generate_signals_cli.py --help
  ```

### General

- `--num_signals` / `-n`:
  ```bash
  python generate_signals_cli.py -n 10 --seed 42 --formats npz --output_dir ./output_example --no_individual
  ```
- `--t_start`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --t_start 0.0 --formats npz --output_dir ./output_example --no_individual
  ```
- `--t_end`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --t_end 6.283185307179586 --formats npz --output_dir ./output_example --no_individual
  ```
- `--num_samples`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --num_samples 2000 --formats npz --output_dir ./output_example --no_individual
  ```
- `--fs_high`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --fs_high 400.0 --formats npz --output_dir ./output_example --no_individual
  ```
- `--seed`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 7 --formats npz --output_dir ./output_example --no_individual
  ```

### Frequency profile

- `--tau_freq_min`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --tau_freq_min 1.2 --formats npz --output_dir ./output_example --no_individual
  ```
- `--tau_freq_max`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --tau_freq_max 1.8 --formats npz --output_dir ./output_example --no_individual
  ```
- `--low_freq_min`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --low_freq_min 0.5 --formats npz --output_dir ./output_example --no_individual
  ```
- `--low_freq_max`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --low_freq_max 3.0 --formats npz --output_dir ./output_example --no_individual
  ```
- `--high_freq_min`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --high_freq_min 10.0 --formats npz --output_dir ./output_example --no_individual
  ```
- `--high_freq_max`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --high_freq_max 60.0 --formats npz --output_dir ./output_example --no_individual
  ```

### Amplitude envelope

- `--p_tension_spline`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --p_tension_spline 1.0 --formats npz --output_dir ./output_example --no_individual
  ```
- `--tau_amp_min`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --tau_amp_min 0.6 --formats npz --output_dir ./output_example --no_individual
  ```
- `--tau_amp_max`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --tau_amp_max 2.0 --formats npz --output_dir ./output_example --no_individual
  ```
- `--amp_min`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --amp_min 2 --formats npz --output_dir ./output_example --no_individual
  ```
- `--amp_max`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --amp_max 6 --formats npz --output_dir ./output_example --no_individual
  ```

### Vertical offset

- `--offset_mean`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --offset_mean 1.0 --formats npz --output_dir ./output_example --no_individual
  ```
- `--offset_std`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --offset_std 1.0 --formats npz --output_dir ./output_example --no_individual
  ```

### Noise

- `--p_has_noise`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --p_has_noise 0.0 --formats npz --output_dir ./output_example --no_individual
  ```
- `--p_gaussian`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --p_gaussian 1.0 --formats npz --output_dir ./output_example --no_individual
  ```
- `--gaussian_std_relative`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --gaussian_std_relative 0.05 --formats npz --output_dir ./output_example --no_individual
  ```

### Subsampling

- `--subsample_sizes` (paper-like defaults are `150,250,500,1000`):
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --subsample_sizes 150,250 --formats npz --output_dir ./output_example --no_individual
  ```

#### Optional anti-aliasing mode — not used for the paper workflow

- `--use_antialiasing`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --use_antialiasing --formats npz --output_dir ./output_example --no_individual
  ```
- `--filter_type` (only used with `--use_antialiasing`):
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --use_antialiasing --filter_type ellip --formats npz --output_dir ./output_example --no_individual
  ```
- `--filter_order` (only used with `--use_antialiasing`):
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --use_antialiasing --filter_order 6 --formats npz --output_dir ./output_example --no_individual
  ```

### Output

- `--output_dir` / `-o`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 -o ./output_custom --formats npz --no_individual
  ```
- `--formats`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --formats npz,txt --output_dir ./output_example --no_individual
  ```
- `--consolidated`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --consolidated --formats npz --output_dir ./output_example --no_individual
  ```
- `--no_consolidated`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --no_consolidated --individual --formats npz --output_dir ./output_example
  ```
- `--individual`:
  ```bash
  python generate_signals_cli.py --num_signals 3 --seed 42 --individual --formats npz --output_dir ./output_example
  ```
- `--no_individual`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --no_individual --formats npz --output_dir ./output_example
  ```
- `--save_metadata`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --save_metadata --formats npz --output_dir ./output_example --no_individual
  ```
- `--no_metadata`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --no_metadata --formats npz --output_dir ./output_example --no_individual
  ```
- `--prefix` (only affects `--individual` outputs):
  ```bash
  python generate_signals_cli.py --num_signals 3 --seed 42 --individual --prefix demo --formats npz --output_dir ./output_example
  ```
- `--verbose` / `-v`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --verbose --formats npz --output_dir ./output_example --no_individual
  ```

### Configuration file

- `--config` / `-c`:
  ```bash
  python generate_signals_cli.py --config config.json
  ```
- `--save_config`:
  ```bash
  python generate_signals_cli.py --num_signals 5 --seed 42 --save_config saved_config.json
  ```

---

## Files generated — configurable command

If `--consolidated` is enabled, the generator will create (depending on `--formats`):

- `signals_high_resolution_<N>.npz/.txt/.json`
- `signals_subsampled_simple_<size>.npz/.txt/.json`
  - or `signals_subsampled_filtered_<size>...` **only** if `--use_antialiasing` is enabled (optional)
- `signals_metadata.json` (if metadata is enabled)
- `dataset_summary.json`

---

## Reproducibility notes

- Use `--seed` to obtain reproducible outputs.
- If you omit `--seed`, the program chooses a random seed and writes it as `seed_used` in `dataset_summary.json`.
- For paper reproduction, use `generate_consolidated_cli.py` (Command 1).

---

## Troubleshooting

- Missing dependencies: `pip install -r SignalBuilderCLI/requirements.txt`
- Import errors: run from inside `SignalBuilderCLI`.
- Outputs in unexpected folders: check `--output` (Command 1) vs `--output_dir` (Command 2).
