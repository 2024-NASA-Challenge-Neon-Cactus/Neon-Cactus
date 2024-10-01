import sys
import os
import matplotlib.dates as mdates
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# print(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from scipy import signal
import numpy as np
import obspy
import matplotlib.pyplot as plt
import pandas as pd
from utils import sols_to_earth_date



class SEISData:
    def __init__(self, start_sol, sol_range, channel='BHU', data_path='downloads/seis'):
        self.start_sol = start_sol
        self.sol_range = sol_range
        self.data_path = data_path
        self.channel = channel.lower()
        self.file_names = self._get_file_names()
        self.stream = self._load_data()
        
    def _get_file_names(self):
        file_names = []
        for sol_number in range(self.start_sol, self.start_sol + self.sol_range):
            date = sols_to_earth_date(sol_number)
            year = date.year
            doy = date.timetuple().tm_yday
            found = False
            print('sol , doy, year :', sol_number, doy, year)
            for filename in sorted(os.listdir(self.data_path)):
                if (".mseed" in filename and
                    f"{doy}" in filename and
                    f"{year}" in filename and
                        self.channel in filename.lower()):
                    file_names.append(os.path.join(self.data_path, filename))
                    found = True
                    break
            if not found:
                print(f"SEIS file for sol {sol_number} not found.")
        return file_names

    def _load_data(self):
        if not self.file_names:
            raise FileNotFoundError("No SEIS files found.")
        combined_stream = obspy.read(self.file_names[0])
        for file in self.file_names[1:]:
            combined_stream += obspy.read(file)
        combined_stream.merge(method=1)
        print("[*] SEIS data loaded.")
        print("[*] load data info")
        print(combined_stream[0].stats)
        return combined_stream

    def filter_data(self, minfreq, maxfreq):
        self.filtered_stream = self.stream.copy()
        self.splited_filtered_stream = self.filtered_stream.split()
        for tr in self.splited_filtered_stream:
            tr.filter('bandpass', freqmin=minfreq, freqmax=maxfreq)
        # self.filtered_stream.filter('bandpass', freqmin=minfreq, freqmax=maxfreq)

    def plot_waveform(self, output_path):
        tr = self.stream[0]
        tr_times = tr.times()  # 시간 데이터를 초 단위로 가져옴
        tr_data = tr.data  # 진폭 데이터

        plt.figure(figsize=(10, 5))
        plt.plot(tr_times, tr_data)  # 모든 데이터를 그래프에 표시

        # x축 포맷 설정 (12시간 단위로만 x축 틱 표시)
        ax = plt.gca()
        ax.set_xticks(np.arange(0, max(tr_times), 12 * 3600))  # 12시간 간격으로 x축 틱을 설정 (12 * 3600초)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x // 3600)}h"))  # 초를 시간으로 변환하여 표시

        # Convert tr_times into datetime objects
        times_in_datetime = pd.to_datetime(tr.stats.starttime.datetime + pd.to_timedelta(tr_times, unit='s'))

        # Use DatetimeIndex functions directly
        unique_dates = times_in_datetime.normalize().unique()  # Extract unique days

        # Add vertical red dashed lines at the start of each new day
        for date in unique_dates:
            day_start = (pd.Timestamp(date) - tr.stats.starttime.datetime).total_seconds()  # 초로 변환
            plt.axvline(day_start, color='red', linestyle='--', linewidth=1)

        plt.xlabel('Time (hours)', fontweight='bold')  # x축 레이블을 시간으로 표시
        plt.ylabel('Amplitude', fontweight='bold')
        plt.title('SEIS Waveform')
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

    def plot_spectrogram(self, minfreq, maxfreq, output_path):
        tr = self.filtered_stream[0]
        f, t, sxx = signal.spectrogram(tr.data, tr.stats.sampling_rate)
        sxx = np.sqrt(sxx + 1e-1000)
        sxx = np.log10(sxx + 1e-1000)

        plt.figure(figsize=(10, 5))
        plt.pcolormesh(t, f, sxx, shading='gouraud', cmap='jet')
        plt.ylim([minfreq, maxfreq])
        plt.yscale('log')
        plt.yticks([0.1, 1, 10])

        # Convert time array (t) to datetime using the trace's start time
        times_in_datetime = pd.to_datetime(tr.stats.starttime.datetime + pd.to_timedelta(t, unit='s'))

        # Extract unique days
        unique_dates = pd.Series(times_in_datetime).dt.normalize().unique()  # Use a pandas Series to extract unique dates

        # Add vertical red dashed lines for each day
        for date in unique_dates:
            day_start = (pd.Timestamp(date) - tr.stats.starttime.datetime).total_seconds()  # 초로 변환
            plt.axvline(day_start, color='red', linestyle='--', linewidth=1)

        plt.xlabel('Time (s)', fontweight='bold')
        plt.ylabel('Frequency (Hz)', fontweight='bold')
        plt.title('SEIS Spectrogram')
        cbar = plt.colorbar(orientation='horizontal')
        cbar.set_label('Power ((m/s)/sqrt(Hz))', fontweight='bold')
        plt.tight_layout()
        plt.savefig(output_path)
        print("[*] SEIS Spectrogram plot saved.")
        plt.close()


class TWINSData:
    def __init__(self, start_sol, sol_range, data_path):
        self.start_sol = start_sol
        self.sol_range = sol_range
        self.data_path = data_path
        self.file_names = self._get_file_names()
        self.data_frame = self._load_data()

    def _get_file_names(self):
        file_names = []
        for sol_number in range(self.start_sol, self.start_sol + self.sol_range):
            found = False
            for filename in sorted(os.listdir(self.data_path)):
                if ".csv" in filename and f"{sol_number}" in filename:
                    file_names.append(os.path.join(
                        self.data_path, filename))
                    found = True
                    break
            if not found:
                print(f"TWINS file for sol {sol_number} not found.")
        return file_names

    def _load_data(self):
        if not self.file_names:
            raise FileNotFoundError("No TWINS files found.")
        data_frames = []
        for file_name in self.file_names:
            df = pd.read_csv(file_name)
            df['UTC'] = pd.to_datetime(df['UTC'], format='%Y-%jT%H:%M:%S.%fZ')
            data_frames.append(df)
        combined_df = pd.concat(data_frames, ignore_index=True)
        return combined_df

    def plot_wind_speed(self, output_path, plot_type='line', window_size=200):
        plt.figure(figsize=(15, 8))
        ax = plt.gca()
        ax.set_facecolor('#f0f0f0')  # Light gray background
        
        # Calculate the moving average of wind speed using a rolling window
        self.data_frame['Wind_Speed_MA'] = self.data_frame['HORIZONTAL_WIND_SPEED'].rolling(window=window_size).mean()

        # Plot the original wind speed data with a lighter color
        if plot_type == 'line':
            plt.plot(self.data_frame['UTC'], self.data_frame['HORIZONTAL_WIND_SPEED'], label='Wind Speed', linewidth=1, color='gray', alpha=0.6)
        elif plot_type == 'scatter':
            plt.scatter(self.data_frame['UTC'], self.data_frame['HORIZONTAL_WIND_SPEED'], s=10, label='Wind Speed', color='gray', alpha=0.6)
        else:
            raise ValueError("plot_type must be 'line' or 'scatter'")

        # Plot the moving average with a thicker line
        plt.plot(self.data_frame['UTC'], self.data_frame['Wind_Speed_MA'], label=f'{window_size}-Period Moving Avg', linewidth=3, color='blue')

        # Add vertical red dashed lines at the start of each new day
        unique_dates = pd.to_datetime(self.data_frame['UTC'].dt.date).unique()
        for date in unique_dates:
            plt.axvline(pd.Timestamp(date), color='red', linestyle='--', linewidth=1)

        # Formatting the plot
        plt.title(f'InSight APSS TWINS - Wind Speed with {window_size}-Period Moving Avg ({plot_type.capitalize()} Plot)', fontsize=14, fontweight='bold')
        plt.xlabel('UTC Time', fontsize=12)
        plt.ylabel('Wind Speed (m/s)', fontsize=12)
        plt.legend(fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)  # Save in high resolution
        print(f"[*] TWINS Wind Speed plot with {window_size}-period moving average and daily markers saved.")
        plt.close()



    def plot_temperature(self, output_path, plot_type='line'):
        plt.figure(figsize=(15, 8))
        ax = plt.gca()
        ax.set_facecolor('#f0f0f0')  # Light gray background
        
        # Convert temperature from Kelvin to Celsius
        self.data_frame['BMY_AIR_TEMP_C'] = self.data_frame['BMY_AIR_TEMP'] - 273.15
        self.data_frame['BPY_AIR_TEMP_C'] = self.data_frame['BPY_AIR_TEMP'] - 273.15
        
        if plot_type == 'line':
            plt.plot(self.data_frame['UTC'], self.data_frame['BMY_AIR_TEMP_C'], label='BMY Air Temperature', linewidth=2)
            plt.plot(self.data_frame['UTC'], self.data_frame['BPY_AIR_TEMP_C'], label='BPY Air Temperature', linewidth=2)
        elif plot_type == 'scatter':
            plt.scatter(self.data_frame['UTC'], self.data_frame['BMY_AIR_TEMP_C'], s=10, label='BMY Air Temperature')
            plt.scatter(self.data_frame['UTC'], self.data_frame['BPY_AIR_TEMP_C'], s=10, label='BPY Air Temperature')
        else:
            raise ValueError("plot_type must be 'line' or 'scatter'")

        # Add vertical red dashed lines at the start of each new day
        unique_dates = pd.to_datetime(self.data_frame['UTC'].dt.date).unique()
        for date in unique_dates:
            plt.axvline(pd.Timestamp(date), color='red', linestyle='--', linewidth=1)
        
        # Formatting the plot
        plt.title(f'InSight APSS TWINS - Temperature ({plot_type.capitalize()} Plot)', fontsize=14, fontweight='bold')
        plt.xlabel('UTC Time', fontsize=12)
        plt.ylabel('Temperature (Celsius)', fontsize=12)
        plt.legend(fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)  # Save in high resolution
        print("[*] TWINS Temperature plot with daily markers saved.")
        plt.close()



class PSData:
    def __init__(self, start_sol, sol_range, data_path):
        self.start_sol = start_sol
        self.sol_range = sol_range
        self.data_path = data_path
        self.file_names = self._get_file_names()
        self.data_frame = self._load_data()

    def _get_file_names(self):
        file_names = []
        for sol_number in range(self.start_sol, self.start_sol + self.sol_range):
            found = False
            for filename in sorted(os.listdir(self.data_path)):
                if ".csv" in filename and f"{sol_number}" in filename:
                    file_names.append(os.path.join(self.data_path, filename))
                    found = True
                    break
            if not found:
                print(f"PS file for sol {sol_number} not found.")
        return file_names

    def _load_data(self):
        if not self.file_names:
            raise FileNotFoundError("No PS files found.")
        data_frames = []
        for file_name in self.file_names:
            df = pd.read_csv(file_name)
            # UTC 열을 datetime 형식으로 변환
            df['UTC'] = pd.to_datetime(df['UTC'], format='%Y-%jT%H:%M:%S.%fZ')
            data_frames.append(df)
        combined_df = pd.concat(data_frames, ignore_index=True)
        return combined_df

    def plot_pressure(self, output_path, plot_type='line'):
        plt.figure(figsize=(15, 8))
        ax = plt.gca()
        ax.set_facecolor('#f0f0f0')  # Light gray background
        
        if plot_type == 'line':
            plt.plot(self.data_frame['UTC'], self.data_frame['PRESSURE'], label='Pressure', linewidth=2)
        elif plot_type == 'scatter':
            plt.scatter(self.data_frame['UTC'], self.data_frame['PRESSURE'], s=10, label='Pressure')
        else:
            raise ValueError("plot_type must be 'line' or 'scatter'")

        # Add vertical red dashed lines at the start of each new day
        unique_dates = pd.to_datetime(self.data_frame['UTC'].dt.date).unique()
        for date in unique_dates:
            plt.axvline(pd.Timestamp(date), color='red', linestyle='--', linewidth=1)

        # Formatting the plot
        plt.title(f'InSight APSS PS - Pressure ({plot_type.capitalize()} Plot)', fontsize=14, fontweight='bold')
        plt.xlabel('UTC Time', fontsize=12)
        plt.ylabel('Pressure (Pa)', fontsize=12)
        plt.legend(fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.6)  # Subtle dashed gridlines
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)  # High-resolution output
        print("[*] PS Pressure plot with daily markers saved.")
        plt.close()
