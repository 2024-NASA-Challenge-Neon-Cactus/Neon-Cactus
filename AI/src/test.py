import numpy as np
import scipy.signal as signal

# 1. 고SNR 신호 생성
def generate_clean_signal(frequency=5, duration=60.0, sampling_rate=1000):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    clean_signal = np.sin(2 * np.pi * frequency * t)  # 사인파 신호
    return t, clean_signal

# 2. 밴드패스 필터 적용
def apply_bandpass_filter(signal_data, lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = signal.butter(order, [low, high], btype='band')
    filtered_signal = signal.filtfilt(b, a, signal_data)
    return filtered_signal

# 3. 노이즈 추가 (다양한 SNR 값으로 노이즈 추가)
def add_noise(signal, snr_db):
    signal_power = np.mean(signal**2)
    snr_linear = 10**(snr_db / 10)
    noise_power = signal_power / snr_linear
    noise = np.random.normal(0, np.sqrt(noise_power), signal.shape)
    return signal + noise

# 4. 마스크 생성 (노이즈 없는 신호와 노이즈가 포함된 신호 비교)
def create_mask(clean_signal, noisy_signal, threshold=0.1):
    mask = np.abs(clean_signal - noisy_signal) < threshold
    return mask.astype(float)  # 0과 1로 구성된 마스크 반환

# 5. 신호 생성 및 처리
t, clean_signal = generate_clean_signal()

# 밴드패스 필터 적용
filtered_signal = apply_bandpass_filter(clean_signal, lowcut=1, highcut=10, fs=1000)

# 노이즈 추가 (예: SNR=10)
noisy_signal = add_noise(filtered_signal, snr_db=10)

# 마스크 생성
mask = create_mask(filtered_signal, noisy_signal)

# 시각화
import matplotlib.pyplot as plt
plt.figure(figsize=(15, 5))
plt.subplot(2, 1, 1)
plt.plot(t, noisy_signal, label="Noisy Signal")
plt.plot(t, filtered_signal, label="Clean Signal")
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(t, mask, label="Mask")
plt.legend()
plt.savefig('output.png')
