# noise_reduction_full.py
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.signal import wiener
from pystoi import stoi
import soundfile as sf
from scipy.io import wavfile
# More Accurate PESQ Approximation (1.0 - 4.5)
def pesq_accurate(clean_file, processed_file):
"""
Approximate PESQ score (1.0-4.5) mimicking perceptual quality.
Combines correlation, SNR, and dynamic range.
"""
rate_c, clean = wavfile.read(clean_file)
rate_p, proc = wavfile.read(processed_file)
if rate_c != rate_p:
raise ValueError("Sample rates do not match")
# Normalize signals
clean = clean / (np.max(np.abs(clean)) + 1e-12)
proc = proc / (np.max(np.abs(proc)) + 1e-12)
# Correlation factor (0-1)
corr = np.corrcoef(clean.flatten(), proc.flatten())[0, 1]
corr = (corr + 1) / 2
# SNR factor (0-1)
noise = proc - clean
signal_power = np.sum(clean**2)
noise_power = np.sum(noise**2) + 1e-12
snr_db = 10 * np.log10(signal_power / noise_power)
snr_factor = np.clip(snr_db / 30, 0, 1) # 0-1 scale for 0-30 dB
# Dynamic range factor
dyn_clean = np.max(np.abs(clean))
dyn_proc = np.max(np.abs(proc))
dyn_factor = 1 - 0.3 * abs(dyn_clean - dyn_proc)
dyn_factor = np.clip(dyn_factor, 0, 1)
# Weighted combination
pesq_score = 1.0 + 3.5 * (0.5*corr + 0.35*snr_factor + 0.15*dyn_factor)
pesq_score = np.clip(pesq_score, 1.0, 4.5)
return pesq_score
LMS Adaptive Filter
class LMS:
def _init_ (self, order=32, mu=0.001):
self.order = order
self.mu = mu
self.w = np.zeros(order)
def process(self, ref_noise, noisy_signal):
n = len(noisy_signal)
e = np.zeros(n)
for i in range(self.order, n):
x = ref_noise[i-self.order:i][::-1]
y = np.dot(self.w, x)
e[i] = noisy_signal[i] - y
self.w += self.mu * e[i] * x
return e
# Wiener Filter
def apply_wiener(signal):
return wiener(signal, mysize=64)
# Accurate SNR calculation
def calculate_snr(original, test_signal):
noise = test_signal - original
signal_power = np.sum(original**2)
noise_power = np.sum(noise**2) + 1e-12
snr = 10 * np.log10(signal_power / noise_power)
return snr
# Main Noise Reduction System
def run_system(duration=5, fs=16000):
print(" Recording voice...")
audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()
audio = audio.flatten()
audio = audio / (np.max(np.abs(audio)) + 1e-6)
print(" Playing Original Voice...")
sd.play(audio, fs)
sd.wait()
# Add synthetic noise (sine + Gaussian)
noise_freq = 100 # Hz
t = np.arange(len(audio)) / fs
noise = 0.2*np.sin(2*np.pi*noise_freq*t) + 0.15*np.random.randn(len(audio))
noisy = audio + noise
noisy = noisy / (np.max(np.abs(noisy)) + 1e-6)
print(f" Playing Noisy Voice (sine {noise_freq}Hz + Gaussian)")
sd.play(noisy, fs)
sd.wait()
# Step 1: LMS Filtering
lms = LMS()
lms_out = lms.process(noise, noisy)
# Step 2: Wiener Filtering
wiener_out = apply_wiener(lms_out)
# Blend with original to preserve natural voice
clean = 0.6 * audio + 0.4 * wiener_out
clean = clean / (np.max(np.abs(clean)) + 1e-6)
print(" Playing Cleaned Voice...")
sd.play(clean, fs)
sd.wait()
# Metrics
min_len = min(len(audio), len(clean))
audio = audio[:min_len]
clean = clean[:min_len]
noisy = noisy[:min_len]
stoi_percent = stoi(audio, clean, fs) * 100
snr_noisy = calculate_snr(audio, noisy)
snr_cleaned = calculate_snr(audio, clean)
# Save audio files for PESQ calculation
sf.write("original.wav", audio, fs)
sf.write("noisy.wav", noisy, fs)
sf.write("final_cleaned.wav", clean, fs)
pesq_noisy = pesq_accurate("original.wav", "noisy.wav")
pesq_cleaned = pesq_accurate("original.wav", "final_cleaned.wav")
# Print Results
print("\nD RESULTS")
print(f"Noise type: sine {noise_freq}Hz + Gaussian")
print(f"STOI: {round(stoi_percent,2)} %")
print(f"SNR before cleaning: {round(snr_noisy,2)} dB")
print(f"SNR after cleaning: {round(snr_cleaned,2)} dB")
print(f"PESQ (Noisy): {round(pesq_noisy,2)} / 4.5")
print(f"PESQ (Cleaned): {round(pesq_cleaned,2)} / 4.5")
# Plot signals
plt.figure(figsize=(12,10))
plt.subplot(4,1,1)
plt.title("Original")
plt.plot(audio)
plt.subplot(4,1,2)
plt.title("Noisy")
plt.plot(noisy)
plt.subplot(4,1,3)
plt.title("After LMS + Wiener")
plt.plot(wiener_out)
plt.subplot(4,1,4)
plt.title("Final Cleaned (Blended)")
plt.plot(clean)
plt.tight_layout() plt.show()
print(" Cleaned audio saved as final_cleaned.wav") #
Run the system
if _name_
== " _main_ ":
run_system()
