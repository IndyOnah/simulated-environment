import numpy as np
import time

def generate_imu_data():
    """Simulates the output of the IMU sensor. Data from the gyroscope,
    accelerometer, and magnetometer are generated and returned as simulated IMU data to be
    used in the simulated environment."""
    #The accelerometer data
    accel_x = np.random.uniform(-2, 2)
    accel_y = np.random.uniform(-2, 2)

    #To simulate the gravity on the z-axis
    accel_z = np.random.uniform(9.5, 10.5)

    #Simulating the gyroscope data in degrees per second
    gyro_x = np.random.uniform(-250, 250)
    gyro_y = np.random.uniform(-250, 250)
    gyro_z = np.random.uniform(-250, 250)

    #Simulating the magnetometer data
    mag_x = np.random.uniform(-50, 50)
    mag_y = np.random.uniform(-50, 50)
    mag_z = np.random.uniform(-50, 50)

#Returning the simulated sensor data for the gyroscope, magnetometer, and accelerometer data
    return {
        "accelerometer": (accel_x, accel_y, accel_z),
        "gyroscope": (gyro_x, gyro_y, gyro_z),
        "magnetometer": (mag_x, mag_y, mag_z)
    }

#Generating the simulated IMU data
#The main execution block
if __name__ == "__main__":
    print("Simulating IMU data. Press Ctrl+C to stop.")
    try:
        while True:
            imu_data = generate_imu_data()
            print(f"IMU Data: {imu_data}")
            #Stop for 0. seconds to simulate a data rate of 10 Hz
            time.sleep(0.1)
    except KeyboardInterrupt:
        #Displaying that the simulation has now stopped
        print("Simulation stopped.")
