import time 
import clr 
import sys 
import numpy as np 
from System import Decimal 
# --- 1. KINESIS DRIVERS --- 
kinesis_path = r"C:\Program Files\Thorlabs\Kinesis" 
sys.path.append(kinesis_path) 
try: 
clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI") 
clr.AddReference("Thorlabs.MotionControl.KCube.PiezoCLI") 
except Exception as e: 
print(f"Error loading DLLs. Check Kinesis path: {e}") 
sys.exit() 
from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI 
from Thorlabs.MotionControl.KCube.PiezoCLI import KCubePiezo 
# --- 2. CONFIGURATION --- 
X_AXIS_SERIAL = "29253329" 
MAX_VOLTAGE = 75.0 
STEPS = 50  # Number of data points in the scan 
DELAY_BETWEEN_STEPS = 0.2  # Seconds to wait for the piezo to physically settle 
def scan_x_axis(serial_number): 
print("=== Optical Tweezers X-Axis Scan ===") 
try: 
DeviceManagerCLI.BuildDeviceList() 
if not DeviceManagerCLI.IsDeviceConnected(serial_number): 
print(f"ERROR: KPZ101 Controller {serial_number} not found.") 
print("Check USB connection and power.") 
return 
# --- 3. CONNECT & INITIALIZE --- 
print(f"Connecting to device {serial_number}...") 
kpz = KCubePiezo.CreateKCubePiezo(serial_number) 
kpz.Connect(serial_number) 
time.sleep(0.5) 
kpz.WaitForSettingsInitialized(5000) 
kpz.StartPolling(250) 
time.sleep(0.5) 
kpz.EnableDevice() 
time.sleep(0.5) 
print("Device connected and enabled successfully.\n") 
# --- 4. EXECUTION --- 
# Generate an array of voltages to step through 
voltage_sweep = np.linspace(0.0, MAX_VOLTAGE, STEPS) 
print(f"Starting scan: 0.0 V to {MAX_VOLTAGE} V in {STEPS} steps...") 
for voltage in voltage_sweep: 
print(f"Moving to: {voltage:.2f} V") 
kpz.SetOutputVoltage(Decimal(float(voltage))) 
# Pause to allow the physical stage to settle before the next movement 
time.sleep(DELAY_BETWEEN_STEPS) 
# --- 5. SHUTDOWN --- 
print("\nScan complete. Returning stage to 0.0 V center position...") 
kpz.SetOutputVoltage(Decimal(0.0)) 
time.sleep(1.0)  
kpz.StopPolling() 
kpz.Disconnect(True) 
print("Device safely disconnected.") 
except Exception as e: 
import traceback 
traceback.print_exc() 
print(f"\nCrash encountered: {e}") 
if __name__ == "__main__": 
scan_x_axis(X_AXIS_SERIAL)
