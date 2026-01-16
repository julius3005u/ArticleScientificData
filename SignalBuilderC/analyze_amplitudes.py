"""Analyze amplitude envelope generation to verify improvements."""
import sys
from pathlib import Path

# Add parent directory to path to enable imports
sys.path.insert(0, str(Path(__file__).parent))

import numpy as np
import matplotlib.pyplot as plt
from amplitude_envelopes import generate_random_amplitude_envelope

# Generate multiple amplitude envelopes to analyze
n_samples = 10  # Generate 10 envelopes to check
fs_high = 5000
t = np.arange(0, 10, 1.0 / fs_high)  # 10 seconds at high resolution

rng = np.random.default_rng(42)  # Fixed seed for reproducibility

envelopes = []
max_values = []
min_values = []
spline_types = []
tau_values = []

print("Generating and analyzing amplitude envelopes...")
print("-" * 70)

for i in range(n_samples):
    amp_envelope, amp_knots, amp_values, tau, spline_type = generate_random_amplitude_envelope(t, rng)
    envelopes.append(amp_envelope)
    max_values.append(np.max(amp_envelope))
    min_values.append(np.min(amp_envelope))
    spline_types.append(spline_type)
    tau_values.append(tau if tau is not None else 0)
    
    print(f"Envelope {i+1:2d}: Type={spline_type:10s} | tau={str(tau)[:5]:>5s} | "
          f"min={np.min(amp_envelope):6.2f} | max={np.max(amp_envelope):6.2f} | "
          f"range={np.max(amp_envelope) - np.min(amp_envelope):6.2f}")

print("-" * 70)
print(f"Mean max value:        {np.mean(max_values):.2f} (should be moderate)")
print(f"Mean min value:        {np.mean(min_values):.2f}")
print(f"Mean range:            {np.mean(np.array(max_values) - np.array(min_values)):.2f}")
print(f"Tension splines:       {sum(1 for t in spline_types if t == 'tension')}/{n_samples}")
print(f"Step functions:        {sum(1 for t in spline_types if t == 'zero_order')}/{n_samples}")
print(f"Mean tau (tension):    {np.mean([t for t in tau_values if t > 0]):.2f} (should be 0.5-2.5)")
print()
print("✓ If max values are mostly < 10 and tau < 3, the fix is working correctly")
print("✓ Should see 50% tension splines and 50% step functions")

# Visualization
fig, axes = plt.subplots(2, 1, figsize=(12, 6))

# Plot 1: All envelopes
for i, env in enumerate(envelopes[:5]):  # Show first 5 for clarity
    axes[0].plot(t, env, label=f"Env {i+1} ({spline_types[i]})", alpha=0.7)
axes[0].set_xlabel("Time (s)")
axes[0].set_ylabel("Amplitude")
axes[0].set_title("Sample Amplitude Envelopes (first 5)")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Plot 2: Distribution of max values
axes[1].hist(max_values, bins=8, edgecolor='black', alpha=0.7)
axes[1].set_xlabel("Max Amplitude Value")
axes[1].set_ylabel("Frequency")
axes[1].set_title("Distribution of Maximum Amplitude Values (should be < 10)")
axes[1].axvline(np.mean(max_values), color='red', linestyle='--', label=f"Mean: {np.mean(max_values):.2f}")
axes[1].legend()
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig("amplitude_analysis.png", dpi=150)
print(f"\n✓ Visualization saved to: amplitude_analysis.png")
plt.close()
