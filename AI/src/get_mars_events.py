import xml.etree.ElementTree as ET
from obspy import read, UTCDateTime
from scipy.signal import stft
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
from scipy import signal
from downloader import SEISDownloader, TWINSDownloader, PSDownloader
from utils import sols_to_earth_date

landing_date = datetime(2018, 11, 26)

# 퀄리티 순위 정의 (a > b > c > d)
QUALITY_ORDER = {'a': 1, 'b': 2, 'c': 3, 'd': 4}

seis_dir = '../data/downloads/seis'
ps_dir = '../data/downloads/ps'
twins_dir = '../data/downloads/twins'

seis_downloader = SEISDownloader()
twins_downloader = TWINSDownloader()
ps_downloader = PSDownloader()

def parse_quakeml(file_path, selected_quality):
    tree = ET.parse(file_path)
    root = tree.getroot()

    event_parameters = root.find('{http://quakeml.org/xmlns/bed/1.2}eventParameters')
    
    if event_parameters is not None:
        event_data = []
        for idx, event in enumerate(event_parameters.findall('{http://quakeml.org/xmlns/bed/1.2}event')):
            event_id = event.get('publicID')
            print(f"Processing event: {event_id}")
            
            # 시작 시간 (phaseHint == "start")
            start_time = None
            end_time = None
            
            # 관측소 정보
            station_info = []
            event_quality = None
            event_type = None
            magnitude_value = None

            description_element = event.find('{http://quakeml.org/xmlns/bed/1.2}description/{http://quakeml.org/xmlns/bed/1.2}text')
            if description_element is not None:
                event_name = description_element.text
                if event_name and len(event_name) > 0:
                    event_quality = event_name[-1]  # 이름의 마지막 알파벳을 퀄리티로 간주

            required_channels = {'BHN', 'BHE', 'BHZ'}
            found_channels = set()

            for pick in event.findall('{http://quakeml.org/xmlns/bed/1.2}pick'):
                phase_hint = pick.find('{http://quakeml.org/xmlns/bed/1.2}phaseHint').text
                time_value = pick.find('{http://quakeml.org/xmlns/bed/1.2}time/{http://quakeml.org/xmlns/bed/1.2}value').text
                
                waveform = pick.find('{http://quakeml.org/xmlns/bed/1.2}waveformID')
                if waveform is not None:
                    network_code = waveform.get('networkCode', 'N/A')
                    station_code = waveform.get('stationCode', 'N/A')
                    location_code = waveform.get('locationCode', 'N/A')
                    channel_code = waveform.get('channelCode', 'N/A')

                    station_info.append({
                        'network_code': network_code,
                        'station_code': station_code,
                        'location_code': location_code,
                        'channel_code': channel_code
                    })

                    if channel_code in required_channels:
                        found_channels.add(channel_code)
                
                if phase_hint == "start":
                    start_time = time_value
                elif phase_hint == "end":
                    end_time = time_value

            event_type_element = event.find('{http://quakeml.org/xmlns/bed/1.2}type')
            if event_type_element is not None:
                event_type = event_type_element.text

            magnitude_element = event.find('{http://quakeml.org/xmlns/bed/1.2}magnitude/{http://quakeml.org/xmlns/bed/1.2}mag/{http://quakeml.org/xmlns/bed/1.2}value')
            if magnitude_element is not None:
                magnitude_value = magnitude_element.text
            
            if event_quality and QUALITY_ORDER.get(event_quality, 5) <= QUALITY_ORDER[selected_quality] and found_channels == required_channels:
                event_data.append({
                    'event_id': event_id,
                    'start_time': start_time,
                    'end_time': end_time,
                    'station_info': station_info,
                    'event_type': event_type,
                    'magnitude': magnitude_value,
                    'quality': event_quality
                })
                print("start time :", start_time)
                print()

    return event_data

def download_data(date, type='all'):
    all_file_paths = []
    if type == 'all' or type == 'seis':
        file_paths = seis_downloader.crawl_and_download(
            start_date=date,
            end_date=date,
            directory=seis_dir,
            channel_list=['BHU', 'BHV', 'BHW'],  # 채널 목록
            station_list=['elyse']
        )
        all_file_paths.extend(file_paths)

    sol = (date - landing_date).days
    print("sol :", sol)

    if type == 'all' or type == 'twins':
        file_paths = twins_downloader.download_range(
            start_sol=sol,
            end_sol=sol,
            directory=twins_dir
        )
        all_file_paths.extend(file_paths)

    if type == 'all' or type == 'ps':
        ps_downloader.download_range(
            start_sol=sol,
            end_sol=sol,
            directory=ps_dir
        )
        all_file_paths.extend(file_paths)
    
    return all_file_paths

import obspy
from obspy import read, UTCDateTime
from scipy.signal import stft
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
from scipy import signal
from scipy.io.wavfile import write  # WAV 파일 저장을 위한 라이브러리
from downloader import SEISDownloader, TWINSDownloader, PSDownloader
from utils import sols_to_earth_date

def load_and_process_mseed(event, mseed_base_path, min_freq=0.1, max_freq=10):
    """
    MSEED 파일에서 해당 이벤트의 시작과 끝 시간 데이터를 로드하고 STFT 변환.
    오디오 파일과 스펙트로그램 저장.
    """
    start_time = datetime.strptime(event['start_time'], "%Y-%m-%dT%H:%M:%S.%fZ")
    end_time = datetime.strptime(event['end_time'], "%Y-%m-%dT%H:%M:%S.%fZ")
    
    year = start_time.year
    doy = start_time.timetuple().tm_yday
    
    for channel in ['BHU', 'BHV', 'BHW']:  # 채널 목록 순회
        file_found = False

        try:
            for dirpath, dirnames, filenames in os.walk(mseed_base_path):
                for filename in filenames:
                    if str(year) in filename and str(doy) in filename and channel in filename:
                        file_found = True
                        print(f"Found file: {filename}")
                        mseed_file_path = os.path.join(dirpath, filename)
                        
                        # MSEED 파일 읽기
                        stream = read(mseed_file_path)
                        
                        # 이벤트 시간 범위에 해당하는 데이터 슬라이싱
                        stream = stream.slice(starttime=UTCDateTime(start_time), endtime=UTCDateTime(end_time))
                        trace = stream[0]

                        # 스펙트로그램 계산 (SciPy 사용)
                        f, t, sxx = signal.spectrogram(trace.data, trace.stats.sampling_rate)

                        # 로그 변환
                        sxx = np.sqrt(sxx + 1e-1000)
                        sxx = np.log10(sxx + 1e-1000)

                        # 스펙트로그램 결과를 이미지로 저장
                        plt.figure(figsize=(10, 5))
                        plt.pcolormesh(t, f, sxx, shading='gouraud', cmap='jet')

                        # 주파수 범위 설정 및 로그 스케일
                        plt.ylim([min_freq, max_freq])
                        plt.yscale('log')
                        plt.yticks([0.1, 1, 10])

                        plt.title(f'Spectrogram of Event {event["event_id"]} - {trace.stats.channel}')
                        plt.ylabel('Frequency [Hz]')
                        plt.xlabel('Time [sec]')
                        plt.colorbar(label='Log Amplitude')
                        plt.savefig(f'../data/results/see/spectrogram_event_{event["start_time"].split("/")[-1]}_{trace.stats.channel}.png')
                        plt.close()

                        # 학습용 데이터로 저장 (불필요한 시각적 요소 없이)
                        plt.figure(figsize=(10, 5))
                        plt.pcolormesh(t, f, sxx, shading='gouraud', cmap='jet')

                        # 시각적 요소 제거
                        plt.axis('off')  # 축, 눈금, 라벨 제거

                        # 학습용으로 크기를 조정할 필요가 있으면 이미지 리사이즈
                        plt.savefig(f'../data/results/train/spectrogram_event_clean_{event["start_time"].split("/")[-1]}_{trace.stats.channel}.png', 
                                    bbox_inches='tight', pad_inches=0)
                        plt.close()

                        # 오디오 데이터로 저장
                        original_sampling_rate = trace.stats.sampling_rate
                        target_sampling_rate = 44100  # 일반적인 오디오 샘플링 레이트로 변경 (44.1kHz)
                        resample_ratio = target_sampling_rate / original_sampling_rate

                        # 데이터를 numpy 배열로 변환
                        data = trace.data

                        # 리샘플링
                        resampled_data = np.interp(
                            np.linspace(0, len(data), int(len(data) * resample_ratio)),
                            np.arange(len(data)),
                            data
                        )

                        # 데이터 스케일링 (16-bit PCM 형식)
                        max_data = np.max(np.abs(resampled_data))
                        if max_data > 0:
                            normalized_data = np.int16((resampled_data / max_data) * 32767)
                        else:
                            normalized_data = np.int16(resampled_data)

                        # 오디오 파일 저장 (WAV 파일 형식)
                        wav_file_path = f'../data/results/audio/event_{event["start_time"].split("/")[-1]}_{trace.stats.channel}.wav'
                        write(wav_file_path, target_sampling_rate, normalized_data)
                        print(f"Audio file saved as {wav_file_path}")

            # 파일이 없을 경우 다운로드
            if not file_found:
                print(f"No data found for {year}-{doy}. Downloading...")
                file_paths = download_data(start_time, type='seis')
                print("file paths :", file_paths)
                
                if not file_paths:
                    print(f"Failed to download data for {year}-{doy}. Skipping.")
                else:
                    for mseed_file_path in file_paths:
                        print(f"Processing downloaded file: {mseed_file_path}")
                        stream = read(mseed_file_path)
                        
                        # 이벤트 시간 범위에 해당하는 데이터 슬라이싱
                        stream = stream.slice(starttime=UTCDateTime(start_time), endtime=UTCDateTime(end_time))
                        trace = stream[0]

                        f, t, sxx = signal.spectrogram(trace.data, trace.stats.sampling_rate)

                        # 로그 변환
                        sxx = np.sqrt(sxx + 1e-1000)
                        sxx = np.log10(sxx + 1e-1000)

                        # 스펙트로그램 결과를 이미지로 저장
                        plt.figure(figsize=(10, 5))
                        plt.pcolormesh(t, f, sxx, shading='gouraud', cmap='jet')
                        plt.ylim([min_freq, max_freq])
                        plt.yscale('log')
                        plt.yticks([0.1, 1, 10])

                        plt.title(f'Spectrogram of Event {event["event_id"]} - {trace.stats.channel}')
                        plt.ylabel('Frequency [Hz]')
                        plt.xlabel('Time [sec]')
                        plt.colorbar(label='Log Amplitude')
                        plt.savefig(f'../data/results/see/spectrogram_event_{event["start_time"].split("/")[-1]}_{trace.stats.channel}.png')
                        plt.close()

                        # 학습용 데이터로 저장
                        plt.figure(figsize=(10, 5))
                        plt.pcolormesh(t, f, sxx, shading='gouraud', cmap='jet')
                        plt.axis('off')
                        plt.savefig(f'../data/results/train/spectrogram_event_clean_{event["start_time"].split("/")[-1]}_{trace.stats.channel}.png', 
                                    bbox_inches='tight', pad_inches=0)
                        plt.close()

                        # 오디오 데이터로 저장
                        original_sampling_rate = trace.stats.sampling_rate
                        target_sampling_rate = 44100  # 오디오 샘플링 레이트 (44.1kHz)
                        resample_ratio = target_sampling_rate / original_sampling_rate
                        data = trace.data

                        # 리샘플링
                        resampled_data = np.interp(
                            np.linspace(0, len(data), int(len(data) * resample_ratio)),
                            np.arange(len(data)),
                            data
                        )

                        # 스케일링
                        max_data = np.max(np.abs(resampled_data))
                        if max_data > 0:
                            normalized_data = np.int16((resampled_data / max_data) * 32767)
                        else:
                            normalized_data = np.int16(resampled_data)

                        # WAV 파일로 저장
                        wav_file_path = f'../data/results/audio/event_{event["start_time"].split("/")[-1]}_{trace.stats.channel}.wav'
                        write(wav_file_path, target_sampling_rate, normalized_data)
                        print(f"Audio file saved as {wav_file_path}")

        except Exception as e:
            print(f"Error processing {channel} data: {e}")


def main():
    file_path = '../data/events_extended_preferredorigin_2019-10-01.xml'  # 실제 XML 파일 경로
    mseed_path = '../data/downloads/seis'  # 실제 mseed 파일 경로
    selected_quality = 'b'  # 사용자가 선택한 퀄리티 (예: b)
    
    event_list = parse_quakeml(file_path, selected_quality)
    print(f"Found {len(event_list)} events with quality {selected_quality}")
    
    # 이벤트 리스트를 순회하면서 STFT 변환 수행
    for event in event_list:
        print("=======================================================")
        print('event :', event)
        start_date = datetime.strptime(event['start_time'], "%Y-%m-%dT%H:%M:%S.%fZ")
        print(start_date)
        load_and_process_mseed(event, mseed_path)

if __name__ == "__main__":
    main()
