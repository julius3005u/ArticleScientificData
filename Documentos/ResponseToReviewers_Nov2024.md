# Response to Reviewers - November 2024
## Complex Signal Benchmark Dataset (CoSiBD)

Dear Editor and Reviewers,

We sincerely thank the reviewers for their constructive feedback. We have carefully addressed all concerns and substantially strengthened the manuscript. Below we provide point-by-point responses with specific locations of changes in the revised manuscript (main_englishv09.tex).

**Note:** All additions and modifications are highlighted in yellow in the revised PDF (using LaTeX `\addtext{}` commands in draft mode).

---

## Response to Reviewer #1

### Concern: Evidence that synthetic signals resemble real-world signals

**Response:**
We have added a new subsection "Preliminary Application Results" (Section: Technical Validation, before Usage Notes) that provides quantitative validation of the dataset's utility. We trained convolutional neural networks (CNNs) on CoSiBD synthetic signals and validated them on two real-world datasets:

1. **EEG clinical signals** (500 training, 690 validation samples)
2. **VCTK speech recordings** (44 hours from 109 speakers)

**Key findings:**
- Mixed training (synthetic + real) improved EEG performance by **9.64%** (MAE: 9.73×10⁻² vs 10.77×10⁻² for real-only)
- Pre-training on synthetic data + fine-tuning improved VCTK speech by **25.51%** (MAE: 4.41×10⁻³ vs 5.92×10⁻³)
- Models trained exclusively on synthetic data showed higher errors, confirming synthetic signals **complement** rather than replace real data

These quantitative results demonstrate that CoSiBD synthetic signals successfully transfer knowledge to real-world super-resolution tasks across distinct domains (physiological and acoustic signals).

**Location in manuscript:** New subsection "Preliminary Application Results" with Table 2 and Figure 9.

**Key references cited:**
- Kuleshov et al. (2017): Audio super-resolution using neural networks
- Kaniraja et al. (2024): Deep learning framework for ECG super-resolution
- Forestier et al. (2017): Generating synthetic time series to augment sparse datasets
- Luciw et al. (2014): Multi-channel EEG recordings dataset
- Yamagishi et al. (2019): VCTK speech corpus

---

## Response to Reviewer #1 - Additional Item

### Concern: Conference paper mentioned without explicit citation

**Comment from Reviewer #1 (Scope, Question 2):**
> "The manuscript mentions that 'CoSiBD has been used in research presented at the International Conference on Signal Processing and Machine Learning' but does not provide an explicit reference."

**Response:**
We have added the explicit citation to our conference paper where CoSiBD was first presented:

- **Ibarra-Fiallo & Lara (2024)**: "Contextual deep learning approaches for time series reconstruction" presented at IEEE COINS 2024, London, UK.

This citation has been added at the first mention of the conference in the Background section (Introduction).

**Location in manuscript:** Line 68 (Background section) - now includes `~\cite{IbarraFiallo2024}`

---

## Response to Reviewer #2

### Concern: Need for numerical results and baseline comparisons

**Response:**
We have added comprehensive quantitative evaluation comparing four training strategies:

1. **Real-only** (baseline trained exclusively on domain-specific real data)
2. **Synth-only** (trained exclusively on CoSiBD synthetic signals)
3. **Mixed** (combined synthetic + real training data)
4. **Tunned** (pre-trained on synthetic, fine-tuned on real)

**Quantitative metrics:**
- Mean Absolute Error (MAE) for signal reconstruction
- Evaluated on two independent real-world test sets (EEG and VCTK)
- Statistical comparison showing 9.64% to 25.51% improvements

**Visual comparisons:**
- Figure 9 shows side-by-side reconstruction comparisons for all four strategies
- Demonstrates visual quality improvements from synthetic data augmentation

**Location in manuscript:** Table 2 (MAE comparison) and Figure 9 (visual comparisons) in "Preliminary Application Results" subsection.

---

## Response to Reviewer #3

### Concern: Validation using CNNs/RNNs/LSTMs trained with simulated data and validated on real-world data

**Response:**
We have directly addressed this requirement by implementing and evaluating a CNN-based super-resolution model (TimeSeriesSRNet) with encoder-decoder architecture:

**Architecture:**
- Encoder: Conv1d layers (1→64→128→256 channels)
- Upsampler: Interpolation + Conv1d decoder (256→128→64→1)
- PyTorch implementation with full training/evaluation pipeline

**Training and validation:**
- Trained on CoSiBD synthetic signals (1,000 training, 300 validation)
- Validated on **independent real-world datasets**:
  - EEG clinical data (690 validation samples)
  - VCTK speech dataset (44 hours, 109 speakers)

**Cross-domain validation:**
- EEG represents physiological time-series (in-domain validation)
- VCTK speech represents acoustic signals (out-of-domain validation)
- Both datasets show significant improvements with synthetic data augmentation

**Key result:** The Tunned strategy (pre-train on synthetic, fine-tune on real) achieved **25.51% improvement** on out-of-domain VCTK data, demonstrating robust transfer learning from synthetic to real signals.

**Location in manuscript:** "Preliminary Application Results" subsection with detailed methodology, Table 2, and Figure 9.

---

## Response to Reviewer #4 (if applicable)

### Concern: Anti-aliasing filter documentation

**Response:**
We have added a dedicated subsection "Anti-Aliasing Filter Validation" (Section: Technical Validation) documenting:

- **Filter design:** 8th-order Butterworth low-pass filter
- **Cutoff frequency:** 90% of target Nyquist frequency
- **Implementation:** Zero-phase filtering (scipy.signal.filtfilt)
- **Validation:** Mathematical formulation and practical examples
- **Dataset provision:** Both filtered and unfiltered versions available

**Location in manuscript:** New subsection "Anti-Aliasing Filter Validation" in Technical Validation section.

---

## Summary of Major Changes

1. **New subsection:** "Preliminary Application Results" with CNN validation (14 paragraphs + table + figure)
2. **New subsection:** "Anti-Aliasing Filter Validation" with detailed documentation
3. **New Table 2:** Quantitative MAE comparison across 4 training strategies and 2 datasets
4. **New Figure 9:** Visual reconstruction comparisons for EEG and VCTK signals
5. **Quantitative evidence:** 9.64% and 25.51% improvements demonstrating dataset utility
6. **Cross-domain validation:** Both physiological (EEG) and acoustic (VCTK) domains tested

---

## Additional Notes

The preliminary application results presented in this revised manuscript are part of a more comprehensive study currently under preparation as a separate research article. The full study includes:

- Extended experimental methodology
- Additional baseline comparisons (interpolation methods, traditional SR algorithms)
- Ablation studies on model architecture
- Detailed hyperparameter analysis
- Broader discussion of synthetic data augmentation strategies

We believe these manuscript revisions substantially strengthen the contribution by providing:
1. **Quantitative validation** of dataset utility
2. **Real-world application** demonstration across multiple domains
3. **Deep learning model** evaluation (CNN-based super-resolution)
4. **Evidence** that synthetic signals successfully transfer to real tasks

We hope these revisions adequately address all reviewer concerns and demonstrate the scientific value of the CoSiBD dataset.

Sincerely,
[Authors]

---

## Document Version Control

- **Date:** November 21, 2024 (updated)
- **Manuscript version:** main_englishv09.tex
- **PDF pages:** 14 (increased from 13 pages in previous version)
- **Track changes:** All new content highlighted in yellow in draft mode
- **Key additions:**
  - Lines 387-430: New "Preliminary Application Results" subsection
  - Table 2: CNN performance comparison
  - Figure 9: Visual reconstruction comparisons
  - Lines 376-386: "Anti-Aliasing Filter Validation" subsection
  - **Line 77 (Nov 21):** Updated Figure 1 to simplified version (generation_process4.png replacing generation_process3.png) - improved clarity and reduced visual complexity in signal generation process diagram
