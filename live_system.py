import serial
import time
import json
import numpy as np
from smbus2 import SMBus

# --- MPU6050 Setup ---
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43
MPU_ADDRESS = 0x68
bus = SMBus(1)
bus.write_byte_data(MPU_ADDRESS, PWR_MGMT_1, 0)

# --- Serial Setup ---
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# --- Kalman Filter ---
class KalmanFilter:
    def __init__(self, process_variance=0.01, measurement_variance=0.1):
        self.process_variance = process_variance
        self.measurement_variance = measurement_variance
        self.estimate = 0
        self.error_estimate = 1

    def update(self, measurement):
        kalman_gain = self.error_estimate / (self.error_estimate + self.measurement_variance)
        self.estimate += kalman_gain * (measurement - self.estimate)
        self.error_estimate = (1 - kalman_gain) * self.error_estimate + self.process_variance
        return self.estimate

gyroX_filter = KalmanFilter()
gyroY_filter = KalmanFilter()

def read_word(bus, addr, reg):
    high = bus.read_byte_data(addr, reg)
    low = bus.read_byte_data(addr, reg + 1)
    value = (high << 8) + low
    if value >= 0x8000:
        value = -((65535 - value) + 1)
    return value

def read_mpu6050():
    acc_x = read_word(bus, MPU_ADDRESS, ACCEL_XOUT_H)
    acc_y = read_word(bus, MPU_ADDRESS, ACCEL_XOUT_H + 2)
    acc_z = read_word(bus, MPU_ADDRESS, ACCEL_XOUT_H + 4)
    gyro_x = read_word(bus, MPU_ADDRESS, GYRO_XOUT_H)
    gyro_y = read_word(bus, MPU_ADDRESS, GYRO_XOUT_H + 2)
    gyro_z = read_word(bus, MPU_ADDRESS, GYRO_XOUT_H + 4)

    return {
        "GyroX": gyro_x,
        "GyroY": gyro_y,
        "AccelX": acc_x,
        "AccelY": acc_y,
        "AccelZ": acc_z
    }

# --- Movement Detection ---
def detect_movement(sensor_data):
    fsr_values = sensor_data.get("FSR", [])
    imu_values = sensor_data.get("IMU", {})

    weight_shift = sum(fsr_values) / len(fsr_values) if fsr_values else 0
    if weight_shift > 500:
        return "Step Detected"

    if abs(imu_values.get("GyroX", 0)) > 1000 or abs(imu_values.get("GyroY", 0)) > 1000:
        return "Balance Shift Detected"

    return "No Movement"

# --- Adaptive Control Logic ---
def adaptive_control(movement):
    if movement == "Step Detected":
        return {"motor": "Increase Support", "torque": 20}
    elif movement == "Balance Shift Detected":
        return {"motor": "Stabilize Posture", "torque": 10}
    return {"motor": "Maintain Position", "torque": 0}

# --- Main Loop ---
print("Running real-time FSR + IMU integration...")

while True:
    try:
        line = ser.readline().decode('utf-8').strip()
        if not line:
            continue
        arduino_data = json.loads(line)

        # Read MPU6050 from Pi
        imu_data = read_mpu6050()
        imu_data["GyroX"] = gyroX_filter.update(imu_data["GyroX"])
        imu_data["GyroY"] = gyroY_filter.update(imu_data["GyroY"])

        # Combine FSR + IMU
        full_data = {
            "timestamp": arduino_data["timestamp"],
            "FSR": arduino_data["FSR"],
            "IMU": imu_data
        }

        print(f"Raw Data: {full_data}")

        movement = detect_movement(full_data)
        print(f"Detected: {movement}")

        control = adaptive_control(movement)
        print(f"Control Signal: {control}")

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(0.1)
