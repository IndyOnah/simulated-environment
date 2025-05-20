import pandas as pd
import numpy as np

# Load the simulated and normalised data
imu_data = pd.read_csv("simulated_imu_data.csv")
fsr_data = pd.read_csv("simulated_fsr_data.csv")
imu_normalised = pd.read_csv("normalised_imu_data.csv")
fsr_normalised = pd.read_csv("normalised_fsr_data.csv")

# Open report file to write
with open("data_integrity_report.txt", "w") as report:
    report.write("Data Integrity Report\n")
    report.write("=====================\n\n")

    # IMU Data Checks
    report.write("--- IMU Data Verification ---\n")
    report.write(f"IMU Data Summary:\n{imu_data.describe()}\n\n")

    timestamp_diff = np.diff(imu_data['Timestamp'])
    if not np.allclose(timestamp_diff, timestamp_diff[0]):
        report.write("Error: Timestamps in IMU data are not evenly spaced.\n")
    else:
        report.write("Timestamps are evenly spaced in IMU data.\n")

    if not (-2 <= imu_data['Acc_X'].min() <= 2):
        report.write("Error: Acc_X values out of range (-2 to 2).\n")
    if not (9.5 <= imu_data['Acc_Z'].max() <= 10.5):
        report.write("Error: Acc_Z values do not reflect gravity (9.5 to 10.5).\n")

    if not (-0.1 <= imu_data['AngVel_Yaw'].min() <= 0.1):
        report.write("Warning: AngVel_Yaw values exceed expected range (-0.1 to 0.1).\n")

    # FSR Data Checks
    report.write("\n--- FSR Data Verification ---\n")
    report.write(f"FSR Data Summary:\n{fsr_data.describe()}\n\n")

    if not np.allclose(imu_data['Timestamp'], fsr_data['Timestamp']):
        report.write("Error: Timestamps in FSR data do not align with IMU data.\n")
    else:
        report.write("Timestamps are consistent between IMU and FSR data.\n")

    if fsr_data[['Heel_Pressure', 'Toe_Pressure']].min().min() < 0:
        report.write("Error: Negative pressure values in FSR data.\n")
    if fsr_data[['Heel_Pressure', 'Toe_Pressure']].max().max() > 50:
        report.write("Error: Pressure values exceed maximum simulated value (50 N).\n")

    # Normalised Data Checks
    def check_normalised_data(normalised_data, original_data, label):
        report.write(f"\n--- {label} Normalised Data Verification ---\n")
        report.write(f"{label} Normalised Data Summary:\n{normalised_data.describe()}\n\n")

        if not ((0 <= normalised_data.iloc[:, :-1].min().min()) and (normalised_data.iloc[:, :-1].max().max() <= 1)):
            report.write(f"Error: {label} normalised data contains values outside [0, 1].\n")

        if not np.allclose(normalised_data['Timestamp'], original_data['Timestamp']):
            report.write(f"Error: Timestamps in {label} normalised data do not match original data.\n")

    check_normalised_data(imu_normalised, imu_data, "IMU")
    check_normalised_data(fsr_normalised, fsr_data, "FSR")

    report.write("\nVerification completed successfully.\n")

print("Data integrity report generated: data_integrity_report.txt")
