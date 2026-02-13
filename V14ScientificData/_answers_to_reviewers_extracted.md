Extracted markdown cells from AnswersToReviewers.ipynb

--- cell 0 ---
# Answers to Editor and Reviewers (Evidence-Mapped)

This notebook provides an item-by-item response to the editor and reviewer requirements listed in `ReviewrsRequirementsAndAnswers.txt`. Each item is mapped to **verbatim excerpts** and **pointers** (sections/figures/tables/labels) in the manuscripts.

**Primary evidence sources:**
- Clean manuscript: `main_englishv09_final.tex`
- Tracked-changes manuscript: `main_englishv09.tex`

**Important constraint:** No dataset/raw-data file inspection was used to produce these answers; all evidence comes from the manuscripts and the requirement list.

--- cell 1 ---
## How to Read the Evidence

For each item below:
- **Manuscript locations**: where the change/answer appears (section heading + LaTeX label where applicable).
- **Evidence (verbatim)**: short, exact excerpts from the TeX sources.
- **Response**: a concise explanation of what was changed/clarified and how it addresses the requirement.

Unless noted otherwise, evidence excerpts are from the clean manuscript `main_englishv09_final.tex`.

--- cell 2 ---
## Editor Comments

### E1 — Provide data in a more standardized format beyond NumPy
**Manuscript locations:** Abstract; Data Records; Usage Notes.

**Evidence (verbatim):**
```tex
CoSiBD comprises 2,500 high-resolution signals (... )
Each signal is provided in three formats (NumPy arrays, plain text, and JSON) ...
```
```tex
Each signal is stored in three formats: NumPy compressed format (.npz), plain text (.txt), and JSON (.json).
```
```tex
Signals are provided in consolidated .txt, .npz, and .json formats.
```

**Response:** The dataset is described as distributed in three interoperable formats: `.npz` (NumPy compressed), consolidated plain text `.txt`, and `.json`. This addresses the request for standardized formats beyond NumPy-only storage, while preserving common workflows in signal processing and ML.

---

### E2 — Add data citations (Zenodo) to the reference list and cite where datasets are mentioned
**Manuscript locations:** Data Records; Code availability; Technical Validation (Zenodo DOI mention).

**Evidence (verbatim):**
```tex
The Complex Signal Benchmark Dataset (CoSiBD) is publicly available on Zenodo\cite{cosibd_zenodo_2025} ...
```
```tex
The full dataset is hosted in Zenodo\cite{cosibd_zenodo_2025} (DOI: \href{https://doi.org/10.5281/zenodo.15138853}{10.5281/zenodo.15138853})
```
```tex
Zenodo\cite{cosibd_zenodo_2025} (DOI: \href{https://doi.org/10.5281/zenodo.15138853}{10.5281/zenodo.15138853}).
```

**Response:** The Zenodo record is cited as a formal reference entry (`cosibd_zenodo_2025`) and is cited at the beginning of Data Records as well as in other key locations where the repository is discussed (DOI repeated).

--- cell 3 ---
## Reviewer #1

### R1-1 — Scope: Data Descriptor without hypothesis-driven results
**Manuscript locations:** Technical Validation → Illustrative Transfer Experiments (optional).

**Evidence (verbatim):**
```tex
These results are provided as an example of how CoSiBD can be used ...
they should not be interpreted as definitive claims about general performance.
```

**Response:** The manuscript frames validation experiments as illustrative baselines/examples (not hypothesis-driven scientific claims), consistent with the Scientific Data “Data Descriptor” scope.

---

### R1-2 — New data / prior use citation
**Manuscript locations:** Background & Summary.

**Evidence (verbatim):**
```tex
CoSiBD has been used in research presented at the International Conference on Signal Processing and Machine Learning~\cite{IbarraFiallo2024} ...
```

**Response:** The manuscript explicitly cites the prior conference presentation and distinguishes it from the dataset release and Data Descriptor contribution here.

---

### R1-3 — Realism justification (not “too artificial”)
**Manuscript locations:** Methods; Figure `fig:design_rationale_motivations`.

**Evidence (verbatim):**
```tex
Design rationale inspired by real signals. ... derived the simulator degrees of freedom
from qualitative observations across representative physiological (EEG/ECG) and speech signals.
... the goal is to capture challenging structure for SR benchmarking rather than match a specific domain distribution.
```

**Response:** The manuscript adds an explicit design rationale grounded in qualitative properties observed in real EEG/ECG and speech, clarifying what “realism” means in this context (challenging structure for SR benchmarks, not domain distribution matching).

---

### R1-4 — Noise model documentation and justification
**Manuscript locations:** Methods → Noise injection; Noise rationale section; Figure `fig:r1_4_powerline_noise`.

**Evidence (verbatim):**
```tex
Two noise types are implemented: Gaussian noise ... and structured sinusoidal noise bursts ...
Noise is applied probabilistically with 50\% probability per signal.
```
```tex
Rationale for structured 50/60\,Hz interference and noise. Real measurement pipelines frequently contain
narrow-band interference (e.g., mains hum) superimposed on broadband sensor noise.
```

**Response:** The manuscript now documents both noise types (Gaussian + structured sinusoidal interference) and includes an explicit rationale describing the intended “mains hum” artifact and the illustrative nature of the Hz mapping.

---

### R1-5 — Sampling frequency/units and anti-aliasing / subsampling policy
**Manuscript locations:** Methods → Resolution variation; Sampling units and frequency interpretation; Figure `fig:r1_5_sampling_units`.

**Evidence (verbatim):**
```tex
Lower-resolution versions are created using simple decimation (uniform subsampling).
... the low-resolution observation is obtained by subsampling the original sequence without pre-filtering.
Reconstructing low-pass filtered signals is not an objective of CoSiBD.
```
```tex
CoSiBD signals are provided as discrete sequences x[n] (e.g., N=5,000 samples) ...
interpreting it as physical time requires choosing a duration T (in seconds) ...
the implied sampling rate is f_s = N/T ...
```

**Response:** The manuscript now (i) defines the sampling/unit convention and explicitly explains how Hz depends on an assumed time scaling, and (ii) explicitly states the LR–HR pairing protocol: LR is produced via uniform decimation of the HR sequence *without pre-filtering*, and low-pass reconstruction is not a dataset objective.

---

### R1-6 — Technical Validation depth
**Manuscript locations:** Technical Validation; Multi-Scale Super-Resolution Benchmark (`sec:multiscale-super-resolution-benchmark`).

**Evidence (verbatim):**
```tex
This section evaluates the signal generation procedure by analyzing spectral properties ...
... distribution of dominant frequencies, spectral stability across sampling rates, and the effect of noise.
```
```tex
Table~\ref{tab:multiscale_benchmark} summarizes the validation performance ...
... we computed spectral fidelity metrics ... Log Spectral Distance (LSD) ... Spectral Correlation (SCORR) ...
```

**Response:** The Technical Validation section is expanded and complemented with baseline SR benchmarking and frequency-domain metrics (LSD/SCORR), improving quantitative support and reproducibility of evaluation.

---

### R1-7 — “Sampling resolution” discussion and aliasing context
**Manuscript locations:** Methods → Resolution variation; Technical Validation → Spectral Stability Across Sampling Resolutions.

**Evidence (verbatim):**
```tex
Lower-resolution versions are created using simple decimation (uniform subsampling).
... without pre-filtering.
```
```tex
At lower resolutions, reduced sampling density and coarser frequency grids can obscure or merge spectral peaks ...
```

**Response:** The manuscript explicitly documents the decimation protocol and clarifies how spectral summaries change with resolution under the reported settings, while maintaining the benchmark’s LR definition as uniform decimation.

---

### R1-8 — Noise characterization (not only deterministic sinusoid)
**Manuscript locations:** Methods → Noise injection.

**Evidence (verbatim):**
```tex
Two noise types are implemented: Gaussian noise ... and structured sinusoidal noise bursts ...
```

**Response:** The manuscript clarifies that noise is not only a deterministic sinusoid; a Gaussian noise option is also included, and both are documented as part of the dataset nuisance modeling.

---

### R1-9 — Desire for per-signal annotations (segments / change-points)
**Manuscript locations:** Data Records (high-resolution signals metadata description); Table `tab:Parameter`.

**Evidence (verbatim):**
```tex
Per-signal metadata (frequency profiles with explicit change-points (base_points and high_freq_points)
and segment labels (variation_type), amplitude envelopes, ... noise configurations, and random seeds) ...
```

**Response:** The manuscript now describes explicit change-point and segment-label metadata fields that annotate each generated signal’s piecewise structure, supporting more advanced uses beyond treating each sequence as unstructured.

---

### R1-10 — Predefined validation sets reduce flexibility
**Manuscript locations:** Usage Notes; Technical Validation → Multi-Scale Super-Resolution Benchmark.

**Evidence (verbatim):**
```tex
The dataset is distributed as a single, unified collection without a predefined train/validation/test split.
Users should create partitions appropriate to their objectives ...
```
```tex
This split is used only for the reported protocol and is not distributed as a predefined dataset partition.
```

**Response:** The manuscript clarifies that CoSiBD is distributed without predefined splits; splits in validation/benchmarking are protocol-specific and provided only as an example.

---

### R1-11 — Improve justification and quantitative support in Technical Validation
**Manuscript locations:** Technical Validation; Multi-Scale Super-Resolution Benchmark; Figures/Tables: `fig:dominant_frequency_distribution`, `tab:density_label`, `fig:average_psd`, `fig:noise_psd`, `tab:multiscale_benchmark`.

**Evidence (verbatim):**
```tex
The PSD was estimated using Welch’s method ...
the dominant frequency was identified as the frequency at which the PSD reaches its maximum value.
```
```tex
LSD (Log Spectral Distance) quantifies spectral content deviation ...
SCORR (Spectral Correlation) measures frequency-domain similarity ...
```

**Response:** The validation text now defines the analysis procedure (e.g., Welch PSD; dominant frequency definition) and reports quantitative metrics and baseline SR results to ground statements about dataset behavior and usability.

---

### R1-12 — Depth/coverage: diversity and complexity claims
**Manuscript locations:** Methods (diversity/complexity paragraph); Table `tab:Parameter`; Figures `fig:amplitud`, `fig:simples`; Technical Validation distribution/PSD figures.

**Evidence (verbatim):**
```tex
To explicitly characterize dataset diversity and complexity, CoSiBD spans multiple controlled axes of variation ...
```

**Response:** The manuscript explicitly enumerates the controlled axes of variability (change-points, transition types, frequency bands, amplitude envelopes, offsets, and noise) and points to representative examples and quantitative summaries.

---

### R1-13 — Reproducibility without manual code inspection
**Manuscript locations:** Methods (index mapping for HR→LR); Data Records (seed range + metadata).

**Evidence (verbatim):**
```tex
For reproducibility ... we form x_LR[i]=x_HR[n_i] using the fixed index set n_i=...
```
```tex
Reproducibility is ensured through documented random seeds: ... unique seed (ranging from 10,000 to 12,499)
```

**Response:** The manuscript now contains the explicit HR→LR index mapping and explicitly documents the per-signal random seed range and consolidated metadata files, reducing reliance on code inspection.

---

### R1-14 — Data file description sufficiency
**Manuscript locations:** Data Records; Usage Notes (reading and plotting).

**Evidence (verbatim):**
```tex
The dataset is provided as consolidated files under SignalBuilderC/data/.
High-resolution signals are stored as signals_high_resolution_5000.[npz|txt|json].
... decimated signals are stored as signals_subsampled_simple_{150,250,500,1000}.[npz|txt|json].
```

**Response:** The Data Records section explicitly lists file naming patterns, storage locations, and format semantics; Usage Notes add concrete loading and visualization examples to support users.

---

### R1-15 — Define “samples”, “points”, and “signals”
**Manuscript locations:** Abstract; Usage Notes.

**Evidence (verbatim):**
```tex
... 2,500 high-resolution signals (N=5,000 samples each ...)
```
```tex
... one signal per row (samples separated by whitespace).
```

**Response:** The manuscript uses “signal” to denote a full 1D time-series sequence and “samples” to denote discrete values within a sequence (e.g., N=5,000 samples per signal). Where “points” is used, it refers to discrete indices/time points defining the sampled sequence.

---

### R1-16 — Code completeness and availability
**Manuscript locations:** Code availability (`sec:code-availability`).

**Evidence (verbatim):**
```tex
The complete signal generation pipeline ... is available at: ... CoSiBD scripts on GitHub.
... All code is provided with example notebooks demonstrating dataset regeneration and usage.
These scripts are distributed under the MIT License.
```

**Response:** The manuscript points to the GitHub repository for the full pipeline and states the code license (MIT).

--- cell 4 ---
### Addendum — Time scaling and band interpretation (Hz)

**Manuscript location:** Methods → *Sampling units and frequency interpretation*.

The manuscript now makes explicit that any band-specific interpretation reported in Hz (e.g., “low/high” frequency ranges) is conditioned on the assumed time scaling $T$ used to map the reference domain $\tau\in[0,4\pi]$ to seconds. Changing $T$ rescales all reported Hz values linearly (by $4\pi/T$) while leaving the underlying discrete sequences $x[n]$ unchanged—this reference-domain design is a key strength of CoSiBD and SignalBuilderC, enabling consistent evaluation under multiple physically meaningful time scales.

---

--- cell 5 ---
### Addendum (Jan 2026) — R1-9 metadata schema + concrete example entry

This strengthens the earlier “per-signal annotations / change-points” response by making the metadata structure explicit and giving a real example entry (without requiring code inspection).

**Manuscript locations:** Data Records → *Metadata schema and example* (Table `tab:metadata_schema`).

**Evidence (verbatim):**
```tex
\subsection*{Metadata schema and example}

CoSiBD provides per-signal metadata to support (i) deterministic regeneration,
(ii) principled partitioning (e.g., by noise type/level or segment labels), and
(iii) analysis of the piecewise structure induced by change-points.
Table~\ref{tab:metadata_schema} summarizes representative fields contained in
\texttt{signals\_metadata.json}. A minimal example entry is shown below (one signal; values truncated for brevity).
```

**Response:** In addition to naming key fields (e.g., `base_points`, `high_freq_points`, `variation_type`), the manuscript now includes (i) a compact table describing representative metadata fields and (ii) a real, human-readable example entry excerpted from `SignalBuilderC/data/signals_metadata.json`. This makes the per-signal annotations concrete and immediately usable for stratified splits and analysis.

--- cell 6 ---
## Reviewer #2

### R2-1 — Motivation and comparison with existing benchmarks
**Manuscript locations:** Background & Summary → Related synthetic time-series resources; Table `tab:related_synthetic_datasets`; Methods → Design rationale (Figure `fig:design_rationale_motivations`).

**Evidence (verbatim):**
```tex
... highlights a practical gap: ... (i) multi-factor paired LR--HR signals for time-series SR,
(ii) a clear pairing protocol ... (here implemented via simple uniform decimation), and
(iii) per-signal metadata enabling deterministic regeneration ...
```

**Response:** The manuscript adds (i) an explicit comparison table to position CoSiBD relative to representative synthetic resources and (ii) a design rationale grounded in real-signal qualitative properties to motivate why the synthetic mechanisms are relevant for SR benchmarking.

---

### R2-2 — Provide quantitative/visual baseline results
**Manuscript locations:** Technical Validation → Multi-Scale Super-Resolution Benchmark; Figures `fig:multifactor_loss_curves`, `fig:multifactor_predictions`, `fig:spectral_analysis`, `fig:spectral_metrics`; Table `tab:multiscale_benchmark`.

**Evidence (verbatim):**
```tex
... we trained ... CNN models ... at four different scaling factors: 5x, 10x, 20x, and 33x ...
Table~\ref{tab:multiscale_benchmark} summarizes the validation performance ...
... we computed spectral fidelity metrics ... LSD ... SCORR ...
```

**Response:** The manuscript now reports baseline SR results (loss + frequency-domain metrics) and includes qualitative prediction figures, enabling readers to assess dataset utility for SR benchmarks.

---

### R2-3 — Simplify Figure 1 (generation process)
**Manuscript locations:** Methods; Figure `fig:generation_process`.

**Evidence (verbatim):**
```tex
\includegraphics[width=0.35\textwidth]{diagrams/generation_process4.png}
\caption{Schematic overview of the CoSiBD signal generation process.}
```

**Response:** Figure 1 is presented as a schematic with a concise caption, with explanatory detail moved into the Methods text (enumerated pipeline).

---

### R2-4 — Axis labels/units in Figures 2–3
**Manuscript locations:** Methods (Figures `fig:amplitud`, `fig:simples`); Sampling units section (Figure `fig:r1_5_sampling_units`); Usage Notes (example plots label axes).

**Evidence (verbatim):**
```tex
\caption{Sampling/unit convention in CoSiBD. ... mapping to ``Hz'' depends on the assumed sampling rate f_s ...}
```
```tex
plt.xlabel('Sample index')
plt.ylabel('Amplitude')
```

**Response:** The manuscript now explicitly clarifies the unit convention and provides labeled plotting examples. (Figures `fig:amplitud` and `fig:simples` are the representative examples referenced in-text; their plotted axes/legends are intended to be interpreted using the explicit unit convention introduced in Methods.)

---

### R2-5 — Examples too basic
**Manuscript locations:** Usage Notes (Reading the Data; Visualizing Signal Pairs).

**Evidence (verbatim):**
```tex
# Load subsampled (simple decimation) and high-resolution signals
x_valid = np.loadtxt('SignalBuilderC/data/signals_subsampled_simple_250.txt')
y_valid = np.loadtxt('SignalBuilderC/data/signals_high_resolution_5000.txt')
```

**Response:** The manuscript includes concrete loading + visualization snippets sufficient for reproducible “first use” in a Data Descriptor. Additional, richer examples and regeneration notebooks are referenced as included in the repository (see Code availability).

---

### R2-6 — Fixed seeds / reproducibility
**Manuscript locations:** Abstract; Data Records; Table `tab:Parameter`.

**Evidence (verbatim):**
```tex
... metadata documenting all generation parameters, including random seeds for full reproducibility.
```
```tex
Random Seed & 10000--12499 & Unique seed per signal for reproducibility
```

**Response:** The manuscript documents that each signal has a fixed, recorded seed, enabling deterministic regeneration; variability is obtained by parameter variation and per-signal seeds rather than uncontrolled RNG state.

---

### R2-7 — Typos and inconsistencies
**Manuscript locations:** Global (proofreading pass).

**Response:** The manuscript underwent a consistency/proofreading pass to remove typos and reduce repetitive phrasing, and to align terminology and unit conventions (see Methods sampling/unit convention and decimation protocol text).

---

### R2-8 — Novelty/experimental depth as standalone contribution
**Manuscript locations:** Technical Validation → Multi-Scale Super-Resolution Benchmark; Illustrative Transfer Experiments (optional); Related resources comparison table.

**Evidence (verbatim):**
```tex
These multi-scale experiments provide quantitative baseline results for future benchmarking studies.
```
```tex
... validated on real-world data from two distinct domains: EEG ... and VCTK speech recordings ...
```

**Response:** The manuscript adds baseline benchmarking and (optional) transfer experiments to strengthen the evaluation and clarify the dataset’s role as a reusable SR benchmark with reference protocols and metrics.

--- cell 7 ---
### Addendum (Jan 2026) — R2-5 “examples too basic”: minimal training example added

This strengthens the earlier “loading + plotting” examples by adding a compact *training* snippet that remains synthetic-only and reproducible (Data Descriptor-appropriate).

**Manuscript locations:** Usage Notes → *Training a baseline model (synthetic-only)*.

**Evidence (verbatim):**
```tex
\subsection*{Training a baseline model (synthetic-only)}

The following example illustrates a minimal synthetic-only training loop for time-series super-resolution using CoSiBD pairs
(LR input from simple uniform decimation, HR target).
```
```tex
# Load paired signals (rows align by index)
x = np.loadtxt('SignalBuilderC/data/signals_subsampled_simple_250.txt')   # (2500, 250)
y = np.loadtxt('SignalBuilderC/data/signals_high_resolution_5000.txt')   # (2500, 5000)
```

**Response:** The manuscript now goes beyond “read and plot” by including an end-to-end baseline training loop (data loading → train/val split → tiny 1D model → validation MSE). This directly addresses the request for a compact, actionable example of how to train an SR model using CoSiBD synthetic pairs while keeping the SR pairing policy consistent (LR = uniform decimation of HR).

--- cell 8 ---
## Reviewer #3

### R3-1 — Demonstrate impact: train on simulated, validate on real
**Manuscript locations:** Technical Validation → Illustrative Transfer Experiments (optional) (`sec:preliminary-application-results`).

**Evidence (verbatim):**
```tex
... trained using the CoSiBD dataset and validated on real-world data from two distinct domains: EEG ... and VCTK ...
```

**Response:** The manuscript includes illustrative transfer experiments demonstrating a workflow where models trained (or pre-trained) with CoSiBD are evaluated on real EEG and speech signals under a stated protocol.

---

### R3-2 — Side-by-side comparison of objectives vs real-world signals
**Manuscript locations:** Methods → Design rationale (Figure `fig:design_rationale_motivations`); Technical Validation (spectral statistics and PSD figures).

**Evidence (verbatim):**
```tex
Figure~\ref{fig:design_rationale_motivations} provides qualitative examples of these motivating properties ...
the goal is to capture challenging structure for SR benchmarking rather than match a specific domain distribution.
```

**Response:** The manuscript adds explicit qualitative motivating examples (physiology + speech) and connects them to the simulator mechanisms (change-points, envelopes, low/high frequency bands, offsets/noise). It additionally reports quantitative spectral summaries that document variability/stability under the stated convention.

--- cell 9 ---
## Tracked-Changes Evidence Example

Some key changes are also explicitly visible in the tracked-changes manuscript `main_englishv09.tex`. For example, the LR–HR pairing policy was revised to remove alternative LR constructions and to state the uniform decimation protocol and the filtering constraint.

**Evidence (verbatim from `main_englishv09.tex`):**
```tex
Lower-resolution versions are created \replacetext{using two distinct approaches: ...}{using simple decimation (uniform subsampling). This keeps the SR task aligned with reconstructing the original high-resolution target; the low-resolution observation is obtained by subsampling the original sequence without pre-filtering. \addtext{Reconstructing low-pass filtered signals is not an objective of CoSiBD.}}
```
