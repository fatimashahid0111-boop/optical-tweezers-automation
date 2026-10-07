import time 
import clr 
import sys 
import numpy as np 
import matplotlib.pyplot as plt 
from System import Decimal 
# KINESIS DRIVERS --- 
kinesis_path = r"C:\Program Files\Thorlabs\Kinesis" 
sys.path.append(kinesis_path) 
try: 
clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI") 
clr.AddReference("Thorlabs.MotionControl.KCube.PiezoCLI") 
clr.AddReference("Thorlabs.MotionControl.KCube.PositionAlignerCLI") 
except Exception as e: 
print(f"Error loading DLLs. Check Kinesis path: {e}") 
sys.exit() 
from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI 
from Thorlabs.MotionControl.KCube.PiezoCLI import KCubePiezo 
from Thorlabs.MotionControl.KCube.PositionAlignerCLI import KCubePositionAligner 
# --- 2. HARDWARE SETUP --- 
KPZ_SERIAL = "29xxxxxx" # X-Axis Piezo 
KPA_SERIAL = "69xxxxxx" # KPA101 Quad Detector 
# Constants for Force Calc 
k_B = 0.013806 # Boltzmann constant in pN*nm/K 
T = 298 # Room Temp in Kelvin 
PIEZO_TRAVEL_UM = 20.0 # 75V maps to 20 um travel 
def run_full_force_calibration(): 
print("=== Optical Tweezers Calibration & Force Measurement ===") 
DeviceManagerCLI.BuildDeviceList() 
# Connect Piezo (KPZ101) 
kpz = KCubePiezo.CreateKCubePiezo(KPZ_SERIAL) 
kpz.Connect(KPZ_SERIAL) 
time.sleep(0.5) 
kpz.EnableDevice() 
kpz.StartPolling(250) 
# Connect QPD (KPA101) 
kpa = KCubePositionAligner.CreateKCubePositionAligner(KPA_SERIAL) 
kpa.Connect(KPA_SERIAL) 
time.sleep(0.5) 
kpa.EnableDevice() 
kpa.StartPolling(250) 
time.sleep(1)  
# --- PHASE 1: THE SCAN (Extracting Gamma) --- 
print("\n--- Phase 1: Scanning to extract Gamma ---") 
scan_volts = np.linspace(25.0, 50.0, 40)  
piezo_positions_um = [] 
qpd_signals = [] 
for v in scan_volts: 
kpz.SetOutputVoltage(Decimal(float(v))) 
time.sleep(0.2) # Wait for piezo to physically settle 
# Calculate theoretical position in microns 
pos_um = (v / 75.0) * PIEZO_TRAVEL_UM 
# Read QPD X-Difference Signal 
qpd_val = float(str(kpa.Status.PositionDifference.X)) 
piezo_positions_um.append(pos_um) 
qpd_signals.append(qpd_val) 
print(f"Voltage: {v:.1f}V | Pos: {pos_um:.2f} um | QPD: {qpd_val:.4f} V") 
# Calculate Gamma (Slope of the central region) 
slope, intercept = np.polyfit(piezo_positions_um, qpd_signals, 1) 
gamma = abs(slope) 
print(f"\n=> Extracted Position Sensitivity (Gamma): {gamma:.4f} V/um") 
# --- PHASE 2: STATIONARY TRAP (Calculating k) --- 
print("\n--- Phase 2: Stationary Fluctuation Measurement ---") 
center_voltage = 37.5 
kpz.SetOutputVoltage(Decimal(float(center_voltage))) 
print(f"Moving stage back to trap center ({center_voltage} V)...") 
time.sleep(2.0) # Wait for the particle to perfectly stabilize 
print("Recording high-frequency QPD thermal fluctuations...") 
stationary_qpd = [] 
for _ in range(300): # Collect 300 quick data points 
qpd_val = float(str(kpa.Status.PositionDifference.X)) 
stationary_qpd.append(qpd_val) 
time.sleep(0.01) # ~10ms sampling interval 
sigma_v = np.std(stationary_qpd) 
print(f"Voltage Standard Deviation (Sigma_V): {sigma_v:.5f} V") 
# Equipartition Math 
gamma_nm = gamma / 1000.0 # Convert V/um to V/nm 
variance_nm2 = (sigma_v / gamma_nm)**2 
trap_stiffness_k = (k_B * T) / variance_nm2 
print(f"\n=> Final Trap Stiffness (k): {trap_stiffness_k:.5f} pN/nm") 
# --- SAFE SHUTDOWN --- 
kpz.StopPolling() 
kpz.Disconnect(True) 
kpa.StopPolling() 
kpa.Disconnect(True) 
print("Hardware safely disconnected.") 
# --- PHASE 3: GRAPHING RESULTS --- 
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5)) 
# Graph 1: The Gamma Calibration Scan 
ax1.plot(piezo_positions_um, qpd_signals, 'o-', color='dodgerblue', alpha=0.7, label='Raw Scan Data') 
fit_line = slope * np.array(piezo_positions_um) + intercept 
ax1.plot(piezo_positions_um, fit_line, 'r--', linewidth=2.5, label=f'Fit: $\gamma$ = {gamma:.3f} 
V/$\mu$m') 
ax1.set_xlabel(r'Piezo Displacement ($\mu$m)') 
ax1.set_ylabel('QPD Signal (V)') 
ax1.set_title('Phase 1: Gamma Factor Calibration') 
ax1.legend() 
ax1.grid(True, alpha=0.3) 
# Graph 2: The Stationary Fluctuations 
time_axis = np.linspace(0, 300*0.01, 300) 
ax2.plot(time_axis, stationary_qpd, color='teal', linewidth=1.2) 
mean_v = np.mean(stationary_qpd) 
ax2.axhline(mean_v, color='black', linestyle='--', alpha=0.5) 
ax2.axhline(mean_v + sigma_v, color='red', linestyle=':', linewidth=2, label=r'$+\sigma_V$') 
ax2.axhline(mean_v - sigma_v, color='red', linestyle=':', linewidth=2, label=r'$-\sigma_V$') 
ax2.set_xlabel('Time (seconds)') 
ax2.set_ylabel('QPD Signal (V)') 
ax2.set_title(f'Phase 2: Equipartition\nTrap Stiffness ($k$) = {trap_stiffness_k:.4f} pN/nm') 
ax2.legend() 
ax2.grid(True, alpha=0.3) 
plt.tight_layout() 
plt.show() 
if __name__ == "__main__": 
run_full_force_calibration()
