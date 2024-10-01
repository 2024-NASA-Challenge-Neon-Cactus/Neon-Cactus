import obspy
from obspy import read
import numpy as np
from scipy.io.wavfile import write

# mseed 파일 경로 설정 (사용자 데이터셋으로 변경)
mseed_file_path = 'data/CI.PASC.10.HHZ_2023-08-20T21_40_17.577_2023-08-20T21_51_17.577.mseed'

# mseed 파일 읽기
st = read(mseed_file_path)

# 첫 번째 트레이스를 선택
trace = st[0]

# 지진 데이터의 원래 샘플링 레이트를 확인
original_sampling_rate = trace.stats.sampling_rate

# 일반적인 오디오 샘플링 레이트로 변경 (44.1kHz)
target_sampling_rate = 44100

# 샘플링 비율 변경을 위한 비율 계산
resample_ratio = target_sampling_rate / original_sampling_rate

# 데이터를 numpy 배열로 변환
data = trace.data

# 데이터를 일반적인 오디오 샘플링 레이트로 리샘플링
resampled_data = np.interp(
    np.linspace(0, len(data), int(len(data) * resample_ratio)),
    np.arange(len(data)),
    data
)

# 데이터가 너무 크거나 작으면 적절한 범위로 스케일링 (16-bit PCM 형식)
max_data = np.max(np.abs(resampled_data))
if max_data > 0:
    normalized_data = np.int16((resampled_data / max_data) * 32767)
else:
    normalized_data = np.int16(resampled_data)

# WAV 파일로 저장 (44.1kHz로 저장)
wav_file_path = "output_resampled_sound.wav"
write(wav_file_path, target_sampling_rate, normalized_data)

print(f"Resampled sound file saved as {wav_file_path}")
