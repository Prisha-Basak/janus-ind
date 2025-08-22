"""Name: Prisha Basak
Student ID: 2025A8PS1075H"""

import sys, os
import numpy as np
import pandas as pd

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QLabel, QSpinBox, QCheckBox, QGroupBox, QFormLayout
)
from PyQt5.QtCore import QTimer

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

try:
    from scipy.signal import savgol_filter
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False


# --- Utility functions ---
def read_excel_autodetect(path):
    """Read Excel, pick 'Pressure (Pa)', clean to numeric, handle junk like '*****'."""
    df = pd.read_excel(path, sheet_name=0)

    # Normalize expected pressure column name to 'pressure_pa'
    df = df.rename(columns={"Pressure (Pa)": "pressure_pa"})

    # Clean to numeric: remove commas/whitespace, coerce errors (e.g., '*****') to NaN
    s = (
        df["pressure_pa"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df["pressure_pa"] = pd.to_numeric(s, errors="coerce")

    # Fill gaps only on the pressure series
    df["pressure_pa"] = df["pressure_pa"].interpolate().ffill().bfill()

    # Keep rows that have a valid number after cleaning
    df = df[df["pressure_pa"].notna()].reset_index(drop=True)
    return df


def pressure_to_altitude(df):
    """pressure_pa -> altitude using ISA barometric relation."""
    T, L, R, G, P = 288.15, 0.0065, 287.05, 9.80665, 101325.0  # K, K/m, J/kgK, m/s^2, Pa
    expo = (R * L) / G

    df = df.copy()
    # Be defensive: ensure numeric and filled (in case of future data sources)
    df["pressure_pa"] = pd.to_numeric(df["pressure_pa"], errors="coerce").interpolate().ffill().bfill()

    # Barometric formula (troposphere approximation)
    df["alt_raw_m"] = (T / L) * ((P / df["pressure_pa"]) ** expo - 1)
    return df


def smooth_altitude(df, med_w=5, mean_w=5, use_savgol=True):
    """Median -> mean -> optional Savitzky–Golay; result in alt_clean."""
    df = df.copy()

    med_w = max(1, int(med_w))
    mean_w = max(1, int(mean_w))

    df["alt_med"] = df["alt_raw_m"].rolling(med_w, center=True, min_periods=1).median()
    df["alt_smooth"] = df["alt_med"].rolling(mean_w, center=True, min_periods=1).mean()

    if use_savgol and SCIPY_AVAILABLE:
        # choose an odd window up to len(df); require >=3
        w = 7 if len(df) >= 7 else (len(df) if len(df) % 2 == 1 else len(df) - 1)
        if w >= 3:
            df["alt_sg"] = savgol_filter(df["alt_smooth"], window_length=w, polyorder=2, mode="interp")
        else:
            df["alt_sg"] = df["alt_smooth"]
    else:
        df["alt_sg"] = df["alt_smooth"]

    df["alt_clean"] = df["alt_sg"]
    return df


def compute_velocity(df):
    """Simple finite-difference velocity using uniform 1 s steps."""
    df = df.copy()
    df["time_s"] = np.arange(len(df))
    df["vel_raw_mps"] = np.gradient(df["alt_raw_m"], df["time_s"])
    df["vel_clean_mps"] = np.gradient(df["alt_clean"], df["time_s"])
    return df


# --- Matplotlib canvas ---
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=9, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        self.axes = fig.subplots(2, 1)
        super().__init__(fig)
        self.setParent(parent)


# --- GUI ---
class FlightVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flight Visualizer [Excel only]")
        self.setGeometry(120, 120, 1000, 800)

        self.raw_df, self.proc_df = None, None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._playback_step)

        self.canvas = MplCanvas(self, width=9, height=7, dpi=100)
        self.ax_alt, self.ax_vel = self.canvas.axes

        self.line_alt_raw = self.line_alt_clean = self.line_vel = None

        self._build_controls()
        self._layout()
        self.statusBar().showMessage("Ready. Load an Excel file.")

    def _build_controls(self):
        self.btn_load = QPushButton("Load Excel")
        self.btn_load.clicked.connect(self.on_load)

        self.btn_start = QPushButton("Start")
        self.btn_start.clicked.connect(self.on_start)

        self.btn_stop = QPushButton("Stop")
        self.btn_stop.clicked.connect(self.on_stop)
        self.btn_stop.setEnabled(False)

        self.spin_med = QSpinBox(); self.spin_med.setRange(1, 51); self.spin_med.setValue(5)
        self.spin_mean = QSpinBox(); self.spin_mean.setRange(1, 51); self.spin_mean.setValue(5)
        self.chk_savgol = QCheckBox("Use Savitzky–Golay (scipy)")
        self.chk_savgol.setChecked(SCIPY_AVAILABLE)
        if not SCIPY_AVAILABLE:
            self.chk_savgol.setEnabled(False)

        self.lbl_info = QLabel("No file loaded.")

    def _layout(self):
        controls = QWidget()
        vbox = QVBoxLayout()

        row1 = QHBoxLayout()
        row1.addWidget(self.btn_load)
        row1.addWidget(self.btn_start)
        row1.addWidget(self.btn_stop)
        vbox.addLayout(row1)

        grp = QGroupBox("Smoothing")
        form = QFormLayout()
        form.addRow("Median window:", self.spin_med)
        form.addRow("Mean window:", self.spin_mean)
        form.addRow(self.chk_savgol)
        grp.setLayout(form)
        vbox.addWidget(grp)

        vbox.addWidget(self.lbl_info)
        controls.setLayout(vbox)

        central = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.canvas, stretch=8)
        main_layout.addWidget(controls, stretch=2)
        central.setLayout(main_layout)
        self.setCentralWidget(central)

    def on_load(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Excel", "", "Excel files (*.xlsx *.xls)")
        if not path:
            return

        self.raw_df = read_excel_autodetect(path)

        # full pipeline
        self.proc_df = compute_velocity(
            smooth_altitude(
                pressure_to_altitude(self.raw_df),
                med_w=self.spin_med.value(),
                mean_w=self.spin_mean.value(),
                use_savgol=self.chk_savgol.isChecked()
            )
        )
        self.lbl_info.setText(f"Loaded {os.path.basename(path)} ({len(self.proc_df)} rows)")
        self._init_plot()
        self._draw_frame(0)

    def on_start(self):
        if self.proc_df is None:
            return
        self._play_index = 0
        self.timer.start(100)  # ms step
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)

    def on_stop(self):
        self.timer.stop()
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)

    def _init_plot(self):
        self.ax_alt.clear(); self.ax_vel.clear()
        self.ax_alt.set_xlabel("Time (s)"); self.ax_alt.set_ylabel("Altitude (m)")
        self.ax_vel.set_xlabel("Time (s)"); self.ax_vel.set_ylabel("Velocity (m/s)")
        self.line_alt_raw, = self.ax_alt.plot([], [], lw=1, label="Raw Altitude")
        self.line_alt_clean, = self.ax_alt.plot([], [], lw=2, label="Smoothed Altitude")
        self.line_vel, = self.ax_vel.plot([], [], lw=2, label="Velocity")
        self.ax_alt.legend(); self.ax_vel.legend()

    def _draw_frame(self, idx):
        idx = max(0, min(idx, len(self.proc_df) - 1))
        t = self.proc_df["time_s"][:idx + 1]
        self.line_alt_raw.set_data(t, self.proc_df["alt_raw_m"][:idx + 1])
        self.line_alt_clean.set_data(t, self.proc_df["alt_clean"][:idx + 1])
        self.line_vel.set_data(t, self.proc_df["vel_clean_mps"][:idx + 1])
        self.ax_alt.relim(); self.ax_alt.autoscale_view()
        self.ax_vel.relim(); self.ax_vel.autoscale_view()
        self.canvas.draw_idle()

    def _playback_step(self):
        if self._play_index < len(self.proc_df):
            self._draw_frame(self._play_index)
            self._play_index += 1
        else:
            self.on_stop()


def main():
    app = QApplication(sys.argv)
    w = FlightVisualizer(); w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
