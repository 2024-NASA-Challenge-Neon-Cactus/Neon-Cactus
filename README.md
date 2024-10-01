# 🚀 Mars Data Explorer

Mars Data Explorer is a Python-based tool that allows easy download and processing of SEIS (Seismic Experiment for Interior Structure) and TWINS (Temperature and Wind for InSight) data provided by NASA's InSight mission. With this tool, you can collect, analyze, and visualize seismic and weather data from Mars.

## 🌟 Key Features
- **Automated Data Download:** Automatically download data for the desired period using command-line arguments.
- **Flexible Start Point Specification:** Specify the data's start point using Sol number, Earth date, or DOY (Day of Year).
- **Data Processing and Visualization:** Filter the downloaded data and generate waveforms and spectrograms.
- **Frequency Range Setting:** Set minimum and maximum frequencies to process data in the desired frequency band.

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/mars-data-explorer.git
cd mars-data-explorer
2. Create and Activate a Virtual Environment
```


### 2. Create virtual environment (Python 3.7 or higher required)
```bash
python -m venv venv
```

# Activate virtual environment (Windows)
```bash
venv\Scripts\activate
```

# Activate virtual environment (macOS/Linux)
```bash
source venv/bin/activate
```


### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

## 🚴 Usage


```bash
Command-line Arguments

python main.py [OPTIONS]
Argument	Description	Example
--start_sol	Start Sol number	--start_sol 237
--start_date	Start Earth date (format: YYYY-MM-DD)	--start_date 2020-01-31
--start_doy	Start DOY (Day of Year)	--start_doy 31
--year	Specify the year when using --start_doy	--year 2020
--range	Number of Sols or days to process (default: 3)	--range 3
--channel	SEIS channel (default: BHU)	--channel BHU
--minfreq	Minimum frequency (default: 0.1 Hz)	--minfreq 0.5
--maxfreq	Maximum frequency (default: 10 Hz)	--maxfreq 5.0
```

### Usage Examples

```bash
Process Data by Sol Number
python main.py --start_sol 237 --range 3 --channel BHU

Process Data by Earth Date
python main.py --start_date 2020-01-31 --range 3 --channel BHU

Process Data by DOY and Year
python main.py --start_doy 31 --year 2020 --range 3 --channel BHU

Process Data with Frequency Range
python main.py --start_sol 237 --range 3 --minfreq 0.5 --maxfreq 5.0 --channel BHU
```


## 📁 Directory Structure

```bash
mars-data-explorer/
├── data/
│   ├── downloads/
│   │   ├── seis/
│   │   └── twins/
│   └── results/
├── src/
│   ├── main.py
│   ├── data_model.py
│   ├── utils.py
│   ├── seis_downloader.py
│   └── twins_downloader.py
├── requirements.txt
├── README.md
└── .gitignore
```

data/: Directory for data files.
downloads/: Contains the raw downloaded data.
seis/: SEIS data.
twins/: TWINS data.
results/: Processed data and visualization outputs.
src/: Directory for source code.
main.py: Entry point for the program.
data_model.py: Classes for data processing.
utils.py: Utility functions.
seis_downloader.py: Module for downloading SEIS data.
twins_downloader.py: Module for downloading TWINS data.
requirements.txt: List of required Python packages.
README.md: Project documentation.
.gitignore: Files and directories to exclude from version control.


## 🔍 Key Modules
main.py
Entry point of the program, handles command-line arguments and manages the data download and processing workflow.

data_model.py

SEISData class: Provides functionalities for processing SEIS data.
TWINSData class: Provides functionalities for processing TWINS data.
utils.py
Contains utility functions used across different modules, such as date conversion.

seis_downloader.py & twins_downloader.py
These modules handle the downloading of SEIS and TWINS data, respectively.

## 🎨 Example Results
Waveform Plot

Spectrogram

Wind Speed Graph

## 🤝 Contributing
Fork this repository.
Create a new branch. (git checkout -b feature/your-feature-name)
Commit your changes. (git commit -m 'Add some feature')
Push to the branch. (git push origin feature/your-feature-name)
Open a Pull Request.

## 📝 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 📞 Contact
If you have any questions or suggestions about the project, feel free to reach out via email.

Email:
Made with ❤️ by Cactus