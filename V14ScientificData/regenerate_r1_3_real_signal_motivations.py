from __future__ import annotations

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from PIL import Image, ImageDraw, ImageFont
from scipy import signal as sig
from scipy.io import wavfile
from scipy.ndimage import gaussian_filter1d


def _read_txt_1d(path: Path) -> np.ndarray:
    vals = [float(x) for x in path.read_text(encoding="utf-8", errors="replace").split()]
    return np.asarray(vals, dtype=float)


def estimate_pitch_autocorr(
    x: np.ndarray,
    sr: int,
    frame_length_s: float = 0.03,
    hop_length_s: float = 0.01,
) -> tuple[np.ndarray, np.ndarray]:
    frame_len = max(64, int(sr * frame_length_s))
    hop = max(16, int(sr * hop_length_s))

    pitches: list[float] = []
    times: list[float] = []

    x = x.astype(np.float64)
    for start in range(0, max(1, len(x) - frame_len), hop):
        frame = x[start : start + frame_len]
        frame = frame - np.mean(frame)
        if np.allclose(frame, 0):
            pitches.append(float("nan"))
            times.append(start / sr)
            continue

        ac = np.correlate(frame, frame, mode="full")[frame_len - 1 :]
        ac[0] = 0.0

        min_lag = int(sr / 300.0)
        max_lag = int(sr / 80.0)
        if max_lag <= min_lag + 1 or max_lag >= len(ac):
            pitches.append(float("nan"))
            times.append(start / sr)
            continue

        lag = min_lag + int(np.argmax(ac[min_lag:max_lag]))
        pitch_hz = (sr / lag) if lag > 0 else float("nan")
        pitches.append(float(pitch_hz))
        times.append(start / sr)

    return np.asarray(times), np.asarray(pitches)


def _find_title_bbox_top_left_panel(arr_rgba: np.ndarray) -> tuple[int, int, int, int] | None:
    """Detect the title text bounding box in the top-left panel.

    We restrict to a small band near the top of the top-left quadrant to avoid
    axes/ticks. Returns (left, top, right, bottom) in image coordinates.
    """

    h, w, _ = arr_rgba.shape
    x0, x1 = 0, w // 2
    # The original composite figure places the panel title slightly lower than
    # a typical Matplotlib title; use a taller band to catch it reliably.
    y0, y1 = 0, min(200, h)

    roi = arr_rgba[y0:y1, x0:x1, :]
    if roi.size == 0:
        return None

    lum = 0.2126 * roi[..., 0] + 0.7152 * roi[..., 1] + 0.0722 * roi[..., 2]
    mask = (lum < 80) & (roi[..., 3] > 0)
    if not bool(mask.any()):
        return None

    ys, xs = np.where(mask)
    left = int(xs.min()) + x0
    right = int(xs.max()) + x0
    top = int(ys.min()) + y0
    bottom = int(ys.max()) + y0
    return left, top, right, bottom


def _choose_font(size_px: int) -> ImageFont.ImageFont:
    try:
        font_path = fm.findfont("DejaVu Sans")
        return ImageFont.truetype(font_path, size=size_px)
    except Exception:
        return ImageFont.load_default()


def patch_existing_png_title(png_path: Path) -> Path:
    """Patch the embedded title in the existing PNG (no raw data needed)."""

    if not png_path.exists():
        raise FileNotFoundError(f"Missing existing figure to patch: {png_path}")

    im = Image.open(png_path).convert("RGBA")
    arr = np.array(im)

    bbox = _find_title_bbox_top_left_panel(arr)
    w, h = im.size
    if bbox is None:
        # Conservative fallback region inside top-left quadrant.
        left, top, right, bottom = int(w * 0.05), int(h * 0.01), int(w * 0.49), int(h * 0.14)
    else:
        left, top, right, bottom = bbox

    pad_x, pad_y = 40, 18
    left = max(0, left - pad_x)
    right = min((w // 2) - 1, right + pad_x)
    top = max(0, top - pad_y)
    bottom = min(max(top + 1, min(200, h - 1)), bottom + pad_y)

    draw = ImageDraw.Draw(im)
    background = (255, 255, 255, 255)
    draw.rectangle([left, top, right, bottom], fill=background)

    new_title = "Physiological example: ECG/EEG-like waveform"

    # Fit font to available rectangle
    rect_w = max(1, right - left)
    rect_h = max(1, bottom - top)
    font_size = 22
    while font_size >= 10:
        font = _choose_font(font_size)
        tb = draw.textbbox((0, 0), new_title, font=font)
        tw, th = tb[2] - tb[0], tb[3] - tb[1]
        if tw <= rect_w and th <= rect_h:
            break
        font_size -= 1

    font = _choose_font(max(font_size, 10))
    cx = left + rect_w // 2
    cy = top + rect_h // 2
    draw.text((cx, cy), new_title, fill=(0, 0, 0, 255), font=font, anchor="mm")

    im.save(png_path)
    return png_path


def generate(out_dir: Path) -> Path:
    root = Path(__file__).resolve().parents[1]

    eeg_data_path = root / "time-series-srnet" / "data" / "eeg"
    vctk_path = root / "VCTK-Corpus" / "VCTK" / "Dataset_2Seg"

    out_dir.mkdir(parents=True, exist_ok=True)

    # If raw data isn't present (common in manuscript-only checkouts), patch the
    # existing PNG title in-place to keep manuscript/figure wording coherent.
    out_fig = out_dir / "r1_3_real_signal_motivations.png"
    if not eeg_data_path.exists() or not vctk_path.exists():
        return patch_existing_png_title(out_fig)

    # EEG example
    eeg_files = sorted(list(eeg_data_path.rglob("*.txt")))
    if not eeg_files:
        raise FileNotFoundError(f"No .txt files found under {eeg_data_path}")

    eeg = _read_txt_1d(eeg_files[0])
    eeg = eeg[: min(len(eeg), 5000)]

    fs_eeg_assumed = 250.0  # qualitative axis only
    f_eeg, pxx = sig.welch(eeg - np.mean(eeg), fs=fs_eeg_assumed, nperseg=min(1024, len(eeg)))

    # VCTK speech example
    wav_files = sorted(list(vctk_path.glob("*.wav")))
    if not wav_files:
        raise FileNotFoundError(f"No .wav files found under {vctk_path}")

    sr, audio = wavfile.read(str(wav_files[0]))
    audio = audio.astype(np.float32)
    if audio.ndim == 2:
        audio = audio.mean(axis=1)

    audio = audio / (np.max(np.abs(audio)) + 1e-9)

    seg_len = min(len(audio), int(sr * 0.20))
    audio_seg = audio[:seg_len]
    t_audio_ms = (np.arange(seg_len) / float(sr)) * 1000.0

    env = gaussian_filter1d(np.abs(audio_seg), sigma=max(1, int(0.002 * sr)))

    times_s, pitches = estimate_pitch_autocorr(audio_seg, sr)
    valid = ~np.isnan(pitches)
    if valid.any():
        pitch_smooth = gaussian_filter1d(
            np.interp(times_s, times_s[valid], pitches[valid]),
            sigma=2,
        )
    else:
        pitch_smooth = pitches

    fig = plt.figure(figsize=(12, 8))
    gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.25)

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(eeg, linewidth=0.9)
    ax1.set_title("Physiological example: ECG/EEG-like waveform")
    ax1.set_xlabel("Sample")
    ax1.set_ylabel("Amplitude")
    ax1.grid(True, alpha=0.25)

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.semilogy(f_eeg, pxx + 1e-12, linewidth=1.0)
    ax2.set_title("Physiological PSD (Welch, qualitative)")
    ax2.set_xlabel("Frequency (Hz) [assumed]")
    ax2.set_ylabel("PSD")
    ax2.set_xlim(0, min(60, float(np.max(f_eeg))))
    ax2.grid(True, alpha=0.25)

    ax3 = fig.add_subplot(gs[1, 0])
    ax3.plot(t_audio_ms, audio_seg, linewidth=0.8, label="waveform")
    ax3.plot(t_audio_ms, env, linewidth=1.2, label="envelope (smoothed |x|)")
    ax3.set_title("Speech example: waveform + amplitude envelope")
    ax3.set_xlabel("Time (ms)")
    ax3.set_ylabel("Amplitude (norm.)")
    ax3.legend(loc="upper right")
    ax3.grid(True, alpha=0.25)

    ax4 = fig.add_subplot(gs[1, 1])
    if valid.any():
        ax4.scatter(times_s[valid] * 1000.0, pitches[valid], s=10, alpha=0.6, label="F0 (raw)")
        ax4.plot(times_s * 1000.0, pitch_smooth, linewidth=1.5, label="F0 (smoothed)")
    ax4.set_title("Speech example: pitch trend (F0)")
    ax4.set_xlabel("Time (ms)")
    ax4.set_ylabel("Pitch (Hz)")
    ax4.grid(True, alpha=0.25)
    if valid.any():
        ax4.legend(loc="upper right")

    fig.suptitle("Real-signal properties motivating CoSiBD design (qualitative examples)", y=0.98)

    fig.savefig(out_fig, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return out_fig


def main() -> None:
    root = Path(__file__).resolve().parents[1]

    out1 = generate(root / "graphs" / "r1_3_design_rationale")
    out2 = generate(root / "V14ScientificData" / "graphs" / "r1_3_design_rationale")

    print("Saved:")
    print("-", out1)
    print("-", out2)


if __name__ == "__main__":
    main()
