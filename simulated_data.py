import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

#50 samples per second
sampling_rate = 50

#The parameters for the simulation
#100 gait cycles to simulate
num_steps = 100

#1 second for each gait cycle
time_per_step = 1
total_time = num_steps * time_per_step
timestamps = np.linspace(0, total_time, num_steps * sampling_rate)

#Simulating acceleration in 3 axes (x, y, z)
acc_x = np.sin(2 * np.pi * timestamps / time_per_step) * 0.5  # Forward acceleration
acc_y = np.zeros_like(timestamps)  # Lateral movement (minimal for walking)
acc_z = np.abs(np.sin(2 * np.pi * timestamps / time_per_step)) * 9.8  # Vertical acceleration (gravity)

#Simulating angular velocity (yaw, pitch, roll)
ang_vel_yaw = np.sin(2 * np.pi * timestamps / (time_per_step * 2)) * 0.1
ang_vel_pitch = np.zeros_like(timestamps)
ang_vel_roll = np.cos(2 * np.pi * timestamps / (time_per_step * 2)) * 0.1

#Combine data into a DataFrame
imu_data = pd.DataFrame({
    'Timestamp': timestamps,
    'Acc_X': acc_x,
    'Acc_Y': acc_y,
    'Acc_Z': acc_z,
    'AngVel_Yaw': ang_vel_yaw,
    'AngVel_Pitch': ang_vel_pitch,
    'AngVel_Roll': ang_vel_roll,
})

#Save to CSV
imu_data.to_csv("simulated_imu_data.csv", index=False)

#Simulating FSR data for heel and toe pressure
heel_pressure = np.maximum(0, np.sin(2 * np.pi * timestamps / time_per_step)) * 50  # Max 50 N
toe_pressure = np.maximum(0, np.cos(2 * np.pi * timestamps / time_per_step)) * 50  # Max 50 N

#Combine data into a DataFrame
fsr_data = pd.DataFrame({
    'Timestamp': timestamps,
    'Heel_Pressure': heel_pressure,
    'Toe_Pressure': toe_pressure,
})

#Save to CSV
fsr_data.to_csv("simulated_fsr_data.csv", index=False)

#Normalise IMU data
scaler = MinMaxScaler()
imu_data_normalized = scaler.fit_transform(imu_data.iloc[:, 1:])
imu_data_normalized = pd.DataFrame(imu_data_normalized, columns=imu_data.columns[1:])
imu_data_normalized['Timestamp'] = imu_data['Timestamp']

#Normalise FSR data
fsr_data_normalized = scaler.fit_transform(fsr_data.iloc[:, 1:])
fsr_data_normalized = pd.DataFrame(fsr_data_normalized, columns=fsr_data.columns[1:])
fsr_data_normalized['Timestamp'] = fsr_data['Timestamp']

#Save normalised data
imu_data_normalized.to_csv("normalized_imu_data.csv", index=False)
fsr_data_normalized.to_csv("normalized_fsr_data.csv", index=False)

#Parameters for zoom (set to None for full data, or specify start/end times)
zoom_start_time = 0  #Start time (seconds) for zoomed-in plot (set to None for full data)
zoom_end_time = 5    #End time (seconds) for zoomed-in plot (set to None for full data)

#Apply zoom filter if zoom parameters are specified
if zoom_start_time is not None and zoom_end_time is not None:
    imu_zoomed = imu_data[(imu_data['Timestamp'] >= zoom_start_time) & (imu_data['Timestamp'] <= zoom_end_time)]
    fsr_zoomed = fsr_data[(fsr_data['Timestamp'] >= zoom_start_time) & (fsr_data['Timestamp'] <= zoom_end_time)]
else:
    imu_zoomed = imu_data
    fsr_zoomed = fsr_data

#Plotting acceleration
plt.figure(figsize=(10, 6))
plt.plot(imu_zoomed['Timestamp'], imu_zoomed['Acc_X'], label='Acc_X')
plt.plot(imu_zoomed['Timestamp'], imu_zoomed['Acc_Z'], label='Acc_Z')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (m/s²)')
plt.title('Simulated IMU Acceleration Data')
plt.legend()
plt.show()

#Plotting FSR data
plt.figure(figsize=(10, 6))
plt.plot(fsr_zoomed['Timestamp'], fsr_zoomed['Heel_Pressure'], label='Heel Pressure')
plt.plot(fsr_zoomed['Timestamp'], fsr_zoomed['Toe_Pressure'], label='Toe Pressure')
plt.xlabel('Time (s)')
plt.ylabel('Pressure (N)')
plt.title('Simulated FSR Data')
plt.legend()
plt.show()
