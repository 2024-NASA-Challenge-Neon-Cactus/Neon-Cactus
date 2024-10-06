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
import pandas as pd

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
        file_paths = ps_downloader.download_range(
            start_sol=sol,
            end_sol=sol,
            directory=ps_dir
        )
        print('file_paths :', file_paths)
        all_file_paths.extend(file_paths)
    
    return all_file_paths



def load_and_process_mseed(event, mseed_base_path, min_freq=0.1, max_freq=10):
    """
    MSEED 파일에서 해당 이벤트의 시작과 끝 시간 데이터를 로드하고 STFT 변환.
    오디오 파일과 스펙트로그램 저장.
    """
    start_time = datetime.strptime(event['start_time'], "%Y-%m-%dT%H:%M:%S.%fZ")
    end_time = datetime.strptime(event['end_time'], "%Y-%m-%dT%H:%M:%S.%fZ")
    
    year = start_time.year
    doy = start_time.timetuple().tm_yday
    
    file_paths = download_data(start_time, type='seis')
    print("file paths :", file_paths)
    
    # 다운로드 후 파일이 있는지 확인
    if not file_paths:
        print(f"Failed to download data for {year}-{doy}. Skipping.")
    else:
        # 다운로드한 파일 처리
        for mseed_file_path in file_paths:
            print(f"Processing downloaded file: {mseed_file_path}")
            stream = read(mseed_file_path)
            print('stream :', stream)
            print('stream stat :', stream[0].stats)
            
            # 이벤트 시간 범위에 해당하는 데이터 슬라이싱
            print("start time :", start_time)
            print("end time :", end_time)
            # stream = stream.slice(starttime=UTCDateTime(start_time), endtime=UTCDateTime(end_time))
            print('stream len :', len(stream))
            trace = stream[0]

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
            plt.savefig(f'../data/results/seis/see/spectrogram_event_{event["start_time"].split("/")[-1]}_{trace.stats.channel}.png')
            plt.close()

            # 학습용 데이터로 저장 (불필요한 시각적 요소 없이)
            plt.figure(figsize=(10, 5))
            plt.pcolormesh(t, f, sxx, shading='gouraud', cmap='jet')

            # 시각적 요소 제거
            plt.axis('off')  # 축, 눈금, 라벨 제거

            # 학습용으로 크기를 조정할 필요가 있으면 이미지 리사이즈
            plt.savefig(f'../data/results/seis/train/spectrogram_event_clean_{event["start_time"].split("/")[-1]}_{trace.stats.channel}.png', 
                        bbox_inches='tight', pad_inches=0)
            plt.close()

            # npy로 저장
            np.save(f'../data/results/seis/raw/spectrogram_event_{event["start_time"].split("/")[-1]}_{trace.stats.channel}.npy', trace)



def load_and_process_twins(event, twins_base_path):

    start_time = datetime.strptime(event['start_time'], "%Y-%m-%dT%H:%M:%S.%fZ")
    end_time = datetime.strptime(event['end_time'], "%Y-%m-%dT%H:%M:%S.%fZ")

    year = start_time.year
    doy = start_time.timetuple().tm_yday

    file_paths = download_data(start_time, type='twins')[0]
    print("file paths :", file_paths)
    # read twins data

    df = pd.read_csv(file_paths)
    df['UTC'] = pd.to_datetime(df['UTC'], format='%Y-%jT%H:%M:%S.%fZ')
    print('twins bef :', df.head())

    twins_data = df # df[(df['UTC'] >= start_time) & (df['UTC'] <= end_time)]
    print('twins aft :', twins_data.head())

    # save as npy
    print(twins_data['HORIZONTAL_WIND_SPEED'])
    np.save(f'../data/results/twins/raw/twins_data_{event["start_time"].split("/")[-1]}.npy', twins_data['HORIZONTAL_WIND_SPEED'])

    # save as plot
    plt.figure(figsize=(10, 5))
    plt.plot(twins_data['UTC'], twins_data['HORIZONTAL_WIND_SPEED'], label='Horizontal Wind Speed', linewidth=2)
    plt.title(f'TWINS Data of Event {event["event_id"]}')

    plt.savefig(f'../data/results/twins/see/twins_data_{event["start_time"].split("/")[-1]}.png')
    plt.close()
    

def load_and_process_ps(event, ps_base_path):
    start_time = datetime.strptime(event['start_time'], "%Y-%m-%dT%H:%M:%S.%fZ")
    end_time = datetime.strptime(event['end_time'], "%Y-%m-%dT%H:%M:%S.%fZ")

    year = start_time.year
    doy = start_time.timetuple().tm_yday

    file_paths = download_data(start_time, type='ps')[0]
    print("file paths :", file_paths)

    # read ps data
    df = pd.read_csv(file_paths)
    df['UTC'] = pd.to_datetime(df['UTC'], format='%Y-%jT%H:%M:%S.%fZ')

    ps_data = df # df[(df['UTC'] >= start_time) & (df['UTC'] <= end_time)]

    # save as npy
    np.save(f'../data/results/ps/raw/ps_data_{event["start_time"].split("/")[-1]}.npy', ps_data['PRESSURE'])

    # save as plot 
    plt.figure(figsize=(10, 5))
    plt.plot(ps_data['UTC'], ps_data['PRESSURE'],  label='Pressure', linewidth=2)
    plt.title(f'PS Data of Event {event["event_id"]}')

    plt.savefig(f'../data/results/ps/see/ps_data_{event["start_time"].split("/")[-1]}.png')
    plt.close()

    

def main():
    file_path = '../data/events_extended_preferredorigin_2019-10-01.xml'  # 실제 XML 파일 경로
    mseed_path = '../data/downloads/seis'  # 실제 mseed 파일 경로
    twins_path = '../data/downloads/twins'  # TWINS 데이터 경로

    selected_quality = 'a'  # 사용자가 선택한 퀄리티 (예: b)
    
    event_list = parse_quakeml(file_path, selected_quality)
    print(f"Found {len(event_list)} events with quality {selected_quality}")
    
    # 이벤트 리스트를 순회하면서 STFT 변환 수행
    for event in event_list:
        print("=======================================================")
        print('event :', event)
        start_date = datetime.strptime(event['start_time'], "%Y-%m-%dT%H:%M:%S.%fZ")
        print(start_date)
        load_and_process_mseed(event, mseed_path)
        load_and_process_twins(event, twins_path)
        load_and_process_ps(event, twins_path)

if __name__ == "__main__":
    main()
