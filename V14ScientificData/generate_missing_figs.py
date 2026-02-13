from __future__ import annotations

import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def generate_metadata_vis(out_path: Path) -> None:
    t = np.linspace(0, 12.56, 1000)

    freq_profile = np.piecewise(t, [t < 6.28, t >= 6.28], [1.0, 3.0])
    phase = np.cumsum(freq_profile) * (t[1] - t[0]) * 2 * np.pi
    carrier = np.sin(phase)

    env_knots_t = [0.0, 6.28, 12.56]
    env_knots_v = [0.72, 1.22, 0.96]
    envelope = np.interp(t, env_knots_t, env_knots_v)

    signal = carrier * envelope

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    ax1.plot(t, signal, "k-", alpha=0.6, label="Synthetic Signal")
    ax1.plot(t, envelope, "r--", linewidth=2, label="Amplitude Envelope (from amp_values)")
    ax1.scatter(env_knots_t, env_knots_v, color="red", s=100, zorder=5, label="amp_knots")

    ax1.axvspan(0, 6.28, alpha=0.1, color="blue", label='Interval 1: "low"')
    ax1.axvspan(6.28, 12.56, alpha=0.1, color="green", label='Interval 2: "high"')
    ax1.set_ylabel("Amplitude")
    ax1.legend(loc="upper right")
    ax1.set_title("Signal Reconstruction from Metadata (ID: signal_0000)")

    ax2.step(t, freq_profile, where="post", color="blue", linewidth=2, label="Frequency Profile")
    ax2.scatter([0, 6.28], [1.0, 3.0], color="blue", s=100, label="base_points (t, f)")
    ax2.set_xlabel("Time (tau)")
    ax2.set_ylabel("Frequency (Hz equiv)")
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    plt.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


def generate_cli_demo(out_path: Path) -> None:
    fig = plt.figure(figsize=(10, 5), facecolor="#1e1e1e")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor("#1e1e1e")
    ax.axis("off")

    text_content = """
$ python generate_dataset.py --n_signals 2500 --resolution 5000 --noise_prob 0.5

[INFO] Initializing Signal Generator...
[INFO] Configuration:
       - Signals: 2500
       - Resolution: 5000 samples
       - Domain: [0, 4pi]
       - Noise Probability: 0.5
[INFO] Output Directory: ./dataset_output/

Processing: 100%|██████████████████████| 2500/2500 [00:45<00:00, 55.20it/s]

[SUCCESS] Dataset generation complete.
[INFO] Generated 2500 .npz files.
[INFO] Metadata saved to ./dataset_output/signals_metadata.json

$ ls -lh ./dataset_output/ | head -n 5
total 420M
-rw-r--r-- 1 user staff 120K Jan 10 10:00 signal_0000.npz
-rw-r--r-- 1 user staff 120K Jan 10 10:00 signal_0001.npz
-rw-r--r-- 1 user staff 120K Jan 10 10:00 signal_0002.npz
""".strip("\n")

    plt.text(
        0.02,
        0.95,
        text_content,
        color="#00ff00",
        fontfamily="monospace",
        fontsize=12,
        verticalalignment="top",
    )

    fig.savefig(out_path, dpi=300, facecolor="#1e1e1e")
    plt.close(fig)


def main() -> None:
    out_dir = Path(__file__).resolve().parent / "graphs"
    os.makedirs(out_dir, exist_ok=True)

    metadata_path = out_dir / "metadata_vis.png"
    cli_path = out_dir / "cli_tool_demo.png"

    generate_metadata_vis(metadata_path)
    generate_cli_demo(cli_path)

    print(f"Generated {metadata_path}")
    print(f"Generated {cli_path}")


if __name__ == "__main__":
    main()
