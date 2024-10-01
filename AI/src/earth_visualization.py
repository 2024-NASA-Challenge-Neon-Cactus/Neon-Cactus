import matplotlib.pyplot as plt
import pandas as pd
from meteostat import Point, Hourly
from datetime import datetime


class EarthDataPlotter:
    def __init__(self, location, start, end):
        self.location = location
        self.start = start
        self.end = end
        self.data = self._fetch_data()

    def _fetch_data(self):
        data = Hourly(self.location, self.start, self.end)
        return data.fetch()

    def plot_wind_speed(self, output_path, show_dashed_lines=True):
        # Fetch wind speed data
        wind_speed = self.data[['wspd']]

        # Set up the figure and axes
        plt.figure(figsize=(15, 8))
        ax = plt.gca()
        ax.set_facecolor('#f0f0f0')  # Light gray background

        # Plot wind speed
        plt.plot(wind_speed.index, wind_speed['wspd'], label='Wind Speed', color='blue', linewidth=2)

        # Optionally add red dashed lines for each day
        if show_dashed_lines:
            unique_dates = pd.to_datetime(wind_speed.index.normalize()).unique()
            for date in unique_dates:
                plt.axvline(pd.Timestamp(date), color='red', linestyle='--', linewidth=1)

        # Formatting the plot
        plt.title(f'Earth Data: Wind Speed', fontsize=14, fontweight='bold')
        plt.xlabel('Time', fontsize=12)
        plt.ylabel('Wind Speed (m/s)', fontsize=12)
        plt.legend(fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()

        # Save the plot
        plt.savefig(output_path, dpi=300)
        print(f"[*] Wind speed plot saved at {output_path}")
        plt.close()

    def plot_pressure(self, output_path, show_dashed_lines=True):
        # Fetch pressure data
        pressure = self.data[['pres']]

        # Set up the figure and axes
        plt.figure(figsize=(15, 8))
        ax = plt.gca()
        ax.set_facecolor('#f0f0f0')  # Light gray background

        # Plot pressure
        plt.plot(pressure.index, pressure['pres'], label='Pressure', color='green', linewidth=2)

        # Optionally add red dashed lines for each day
        if show_dashed_lines:
            unique_dates = pd.to_datetime(pressure.index.normalize()).unique()
            for date in unique_dates:
                plt.axvline(pd.Timestamp(date), color='red', linestyle='--', linewidth=1)

        # Formatting the plot
        plt.title(f'Earth Data: Pressure', fontsize=14, fontweight='bold')
        plt.xlabel('Time', fontsize=12)
        plt.ylabel('Pressure (hPa)', fontsize=12)
        plt.legend(fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()

        # Save the plot
        plt.savefig(output_path, dpi=300)
        print(f"[*] Pressure plot saved at {output_path}")
        plt.close()


# Example usage:
# Coordinates for Seoul, South Korea
location = Point(37.5665, 126.9780, 38)  # 서울, 대한민국

# Time range: October 10, 2023, 00:00 to October 13, 2023, 00:00
start = datetime(2023, 10, 10, 0, 0)
end = datetime(2023, 10, 13, 0, 0)

# Initialize plotter
plotter = EarthDataPlotter(location, start, end)

# Plot wind speed and save the plot
plotter.plot_wind_speed('wind_speed_plot.png', show_dashed_lines=True)

# Plot pressure and save the plot
plotter.plot_pressure('pressure_plot.png', show_dashed_lines=True)
