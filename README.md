Overview

This project was built to solve the “Get Data – Display Data – Make it Fantastic” challenge.
The goal was to:

Extract raw pressure data from test-flight logs (Excel).

Convert pressure → altitude using the barometric formula.

Visualize altitude-time and velocity-time data clearly.

Handle noisy sensor data with smoothing filters.

Make the visualization fantastic by animating the graph, adding a new data point every second.

Features ✨

📂 Excel file import (auto-detects pressure column).

📉 Altitude & velocity calculation using physics formulas.

🪄 Noise reduction with median filter, moving average, and optional Savitzky–Golay smoothing (if scipy is installed).

📊 Dual plots:

Altitude vs Time

Velocity vs Time

⏱️ Real-time animation: data points added sequentially to simulate playback.

🖥️ Interactive GUI built with PyQt5.

Tech Stack ⚙️

Python 3.8+

PyQt5 – GUI framework

pandas – Data handling

numpy – Math operations

matplotlib – Graph plotting

scipy (optional) – Savitzky–Golay smoothing

Installation 🚀

Clone this repo:

git clone https://github.com/your-username/flight-visualizer.git
cd flight-visualizer


Create & activate a virtual environment:

python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt


Dependencies (requirements.txt):

PyQt5
numpy
pandas
matplotlib
scipy
openpyxl

Usage ▶️

Run the program:

python main.py


In the GUI:

Click Load Excel and select a test-flight data file (with a Pressure (Pa) column).

Click Start to play the animated graph.

Adjust smoothing options:

Median filter window

Mean filter window

Toggle Savitzky–Golay filter (if available).

Click Stop to pause animation.

How Each Question Was Tackled ✅

1. Get Data!

Used pandas.read_excel() to extract the Pressure (Pa) column.

Cleaned data (removed commas, converted to numeric, interpolated missing values).

2. Calculate Altitude!

Applied the barometric formula with constants (T, L, R, G, P).

Created a derived column alt_raw_m for raw altitude.

3. Velocity Computation!

Used numpy.gradient() over altitude-time to compute velocity (vel_raw_mps, vel_clean_mps).

4. Deal with Noisy Data!

Applied median filter + moving average.

Added optional Savitzky–Golay filter (for smooth curves without lag).

5. Display Data!

Plotted Altitude vs Time and Velocity vs Time with Matplotlib.

Clearly labeled axes, legends, and units.

6. Make it Fantastic!

Added real-time animation: each second, a new data point is drawn.

Built a PyQt5 GUI with controls for loading, starting, stopping, and adjusting smoothing parameters.
