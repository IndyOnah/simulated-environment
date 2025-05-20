import pandas as pd
import numpy as np

#Load the simulated data
imu_data = pd.read_csv("normalised_imu_data.csv")
fsr_data = pd.read_csv("normalised_fsr_data.csv")

#Feature Extraction Function
def extract_features(imu_data, fsr_data):
    features = {}

    #IMU Features
    features['acc_x_mean'] = imu_data['Acc_X'].mean()
    features['acc_x_std'] = imu_data['Acc_X'].std()
    features['acc_z_peak'] = imu_data['Acc_Z'].max()

    features['gyro_yaw_mean'] = imu_data['AngVel_Yaw'].mean()
    features['gyro_yaw_std'] = imu_data['AngVel_Yaw'].std()

    #FSR Features
    features['heel_pressure_mean'] = fsr_data['Heel_Pressure'].mean()
    features['toe_pressure_mean'] = fsr_data['Toe_Pressure'].mean()
    features['heel_toe_pressure_ratio'] = features['heel_pressure_mean'] / (features['toe_pressure_mean'] + 1e-5)  # Avoid division by zero

    #Additional Features
    features['step_variability'] = fsr_data['Heel_Pressure'].std() + fsr_data['Toe_Pressure'].std()

    return features

#Extract Features
features = extract_features(imu_data, fsr_data)

#Convert features to DataFrame and save
features_df = pd.DataFrame([features])
features_df.to_csv("extracted_features.csv", index=False)

print("Feature extraction complete. Features saved to extracted_features.csv.")
