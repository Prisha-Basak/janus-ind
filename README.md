## **Overview:** 
This project was built to solve the “Fantastic Four: First Launch” challenge.
1) Extract raw pressure data from test-flight logs from Excel.
2) Convert pressure to altitude using the barometric formula.
3) Visualize altitude-time and velocity-time data clearly.
4) Handle noisy sensor data with smoothing filters.
5) Make the visualization fantastic by animating the graph, adding a new data point every second.
-----------------------------------------------------------------------------------------------------------------------
### **Features:**
1) Excel file import (auto-detects pressure column).
2) Altitude & velocity calculation using physics formulas.
3) Noise reduction with median filter, moving average, and optional Savitzky–Golay smoothing (if scipy is installed).
4) Real-time animation: data points added sequentially to simulate playback.
5) Interactive GUI built with PyQt5.
-----------------------------------------------------------------------------------------------------------------------
### **Dual plots:**
1) Altitude vs Time
2) Velocity vs Time
-----------------------------------------------------------------------------------------------------------------------
### **Tech Stack:**
> Python 3.8+ | PyQt5 – GUI framework | pandas – Data handling | numpy – Math operations | matplotlib – Graph plotting | scipy – Savitzky–Golay smoothing
-----------------------------------------------------------------------------------------------------------------------
### **Installation:**
1) Clone this repo:
`git clone https://github.com/Prisha-Basak/janus-ind.git
cd janus`
2) Create & activate a virtual environment:
`python3 -m venv venv
source venv/bin/activate`
3) Install dependencies:
`pip install -r requirements.txt`
-----------------------------------------------------------------------------------------------------------------------
### **Dependencies:**
> PyQt5 | numpy | pandas | matplotlib | scipy | openpyxl
-----------------------------------------------------------------------------------------------------------------------
### **Usage:**
1) Run the program:
`python main.py`
2) In the GUI:
Click Load Excel and select a test-flight data file (with a Pressure (Pa) column).
Click Start to play the animated graph.
Adjust smoothing options:
Median filter window
Mean filter window
Toggle Savitzky–Golay filter
Click Stop to pause animation.
-----------------------------------------------------------------------------------------------------------------------
### **How Each Question Was Tackled:**
1. Get Data:
*Used pandas.read_excel() to extract the Pressure (Pa) column.
Cleaned data (removed commas, converted to numeric, interpolated missing values).*

3. Calculate Altitude:
*Applied the barometric formula with constants (T, L, R, G, P).
Created a derived column alt_raw_m for raw altitude.*

3. Velocity Computation:
*Used numpy.gradient() over altitude-time to compute velocity (vel_raw_mps, vel_clean_mps).*

4. Deal with Noisy Data:
*Applied median filter + moving average.
Added optional Savitzky–Golay filter (for smooth curves without lag).*

5. Display Data:
*Plotted Altitude vs Time and Velocity vs Time with Matplotlib.
Clearly labeled axes, legends, and units.*

6. Make it Fantastic:
*Added real-time animation: each second, a new data point is drawn.
Built a PyQt5 GUI with controls for loading, starting, stopping, and adjusting smoothing parameters.*
