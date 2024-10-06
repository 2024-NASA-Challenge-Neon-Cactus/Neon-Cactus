import matplotlib.pyplot as plt
import obspy
import pandas as pd
import numpy as np

class SeismicDataPlotter:
    def __init__(self, seismic_file):
        self.seismic_file = seismic_file
        self.seismic_data = self._fetch_seismic_data()

    def _fetch_seismic_data(self):
        try:
            # Read the seismic data from MiniSEED file
            stream = obspy.read(self.seismic_file)
            return stream
        except Exception as e:
            print(f"Error reading seismic data: {e}")
            return None

    def plot_seismic_waveform(self, output_path, show_dashed_lines=True):
        # Check if seismic data is available
        if self.seismic_data is None:
            print("No seismic data available.")
            return

        # Set up the figure
        plt.figure(figsize=(15, 8))
        ax = plt.gca()
        ax.set_facecolor('#f0f0f0')  # Light gray background

        # Plot each trace with calculated time in datetime
        for i, trace in enumerate(self.seismic_data):
            npts = trace.stats.npts
            sampling_rate = trace.stats.sampling_rate
            starttime = trace.stats.starttime

            # Generate time axis as datetime
            times = pd.date_range(start=starttime.datetime, periods=npts, freq=pd.to_timedelta(1 / sampling_rate, unit='s'))
            amplitudes = trace.data  # Amplitude data

            plt.plot(times, amplitudes, label=f'Trace {i}', linewidth=1)

        # Optionally add red dashed lines to indicate specific days
        if show_dashed_lines:
            unique_dates = pd.to_datetime(times.date).unique()
            for date in unique_dates:
                plt.axvline(x=date, color='red', linestyle='--', linewidth=1)

        # Formatting the plot
        plt.title('SEIS Waveform', fontsize=14, fontweight='bold')
        plt.xlabel('Time', fontsize=12)
        plt.ylabel('Amplitude', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()

        # Save the plot
        plt.savefig(output_path, dpi=300)
        print(f"[*] Seismic waveform plot saved at {output_path}")
        plt.close()

# Example usage:
# MiniSEED 파일 경로
seismic_file = 'earth_original_seismic.mseed'

# Initialize seismic plotter
seismic_plotter = SeismicDataPlotter(seismic_file)

# Plot seismic waveform and save the plot
seismic_plotter.plot_seismic_waveform('seismic_waveform_plot.png', show_dashed_lines=True)
