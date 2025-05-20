from mpu6050 import mpu6050
import time

# List of MPU6050 sensors on different buses
mpu_addresses = [0x68] * 6  #All at default address, one per bus
buses = [0x68, 0x68, 0x68, 0x68, 0x68, 0x68]  # I need to replace with actual bus numbersI have configured/ check if it is correct

# Create sensor objects for each bus
sensors = [mpu6050(address, bus) for address, bus in zip(mpu_addresses, buses)]

# Loop forever
while True:
    # Iterate over each MPU sensor and its index
    for i, sensor in enumerate(sensors):
        # Read acceleration data from the current MPU
        accel = sensor.get_accel_data()

        # Read gyroscope (angular velocity) data from the current MPU
        gyro = sensor.get_gyro_data()

        # Print out the sensor number starting from 1
        print(f"MPU {i+1}:")

        # Print formatted acceleration values in x, y, z axes
        print(f"  Accel -> x: {accel['x']:.2f}, y: {accel['y']:.2f}, z: {accel['z']:.2f}")

        # Print formatted gyroscope values in x, y, z axes
        print(f"  Gyro  -> x: {gyro['x']:.2f}, y: {gyro['y']:.2f}, z: {gyro['z']:.2f}")
        
        # Print a blank line for separation between sensors
        print()

    # Wait half a second
    time.sleep(0.5)
