import pandas as pd
import numpy as np

#Load the simulated and normalized data
#The IMU data with the raw simulated values
imu_data = pd.read_csv("simulated_imu_data.csv")
#The FSR data for the heel and toe pressure
fsr_data = pd.read_csv("simulated_fsr_data.csv")
#The normalised IMU data scaled between 0 and 1
imu_normalised = pd.read_csv("normalised_imu_data.csv")
#The FSR data is also scaled between 0 and 1
fsr_normalised = pd.read_csv("normalised_fsr_data.csv")

#Checking IMU Data
def check_imu_data(imu_data):
    print("\n--- IMU Data Verification ---")
    print("IMU Data Summary:\n", imu_data.describe())

#Checkimg timestamps are evenly spread out
    timestamp_diff = np.diff(imu_data['Timestamp'])
    if not np.allclose(timestamp_diff, timestamp_diff[0]):
        print("Error: Timestamps in IMU data are not evenly spaced.")
    else:
        print("Timestamps are evenly spaced in IMU data.")

#Validating the acceleration ranges
    if not (-2 <= imu_data['Acc_X'].min() <= 2):
        print("Error: Acc_X values out of range (-2 to 2).")
    if not (9.5 <= imu_data['Acc_Z'].max() <= 10.5):
        print("Error: Acc_Z values do not reflect gravity (9.5 to 10.5).")

#Validating the ranges of angular velocity
    if not (-0.1 <= imu_data['AngVel_Yaw'].min() <= 0.1):
        print("Warning: AngVel_Yaw values exceed expected periodic range (-0.1 to 0.1).")

check_imu_data(imu_data)

#Checking the FSR Data
def check_fsr_data(fsr_data):
    print("\n--- FSR Data Verification ---")
    print("FSR Data Summary:\n", fsr_data.describe())

#Checking that the timestamps match IMU data
    if not np.allclose(imu_data['Timestamp'], fsr_data['Timestamp']):
        print("Error: Timestamps in FSR data do not align with IMU data.")
    else:
        print("Timestamps are consistent between IMU and FSR data.")

#Validating the FSR pressure ranges
    if fsr_data[['Heel_Pressure', 'Toe_Pressure']].min().min() < 0:
        print("Error: Negative pressure values in FSR data.")
    if fsr_data[['Heel_Pressure', 'Toe_Pressure']].max().max() > 50:
        print("Error: Pressure values exceed maximum simulated value (50 N).")

check_fsr_data(fsr_data)

#Checking Normalized Data
def check_normalised_data(normalised_data, original_data, label):
    print(f"\n--- {label} Normalised Data Verification ---")
    print(f"{label} Normalised Data Summary:\n", normalised_data.describe())

#Checking if normalized values are in range
    if not ((0 <= normalised_data.iloc[:, :-1].min().min()) and (normalised_data.iloc[:, :-1].max().max() <= 1)):
        print(f"Error: {label} normalised data contains values outside [0, 1].")

#Making sure the timestamp column matches the original data
    if not np.allclose(normalised_data['Timestamp'], original_data['Timestamp']):
        print(f"Error: Timestamps in {label} normalised data do not match original data.")

check_normalised_data(imu_normalised, imu_data, "IMU")
check_normalised_data(fsr_normalised, fsr_data, "FSR")

print("\nVerification done")