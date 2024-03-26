import time


def init_temp_sensor():
    """
    This function set the entire path for the temperature sensor.

    return : sensor_file => str -> the path to the speciified sensor
    """
    # Directory where DS18B20 sensor data is stored
    sensor_dir = "/sys/bus/w1/devices/"

    # please change with yours:
    sensor_folders = "28-8000002fbfe8"

    sensor_file = sensor_dir + sensor_folders + "/w1_slave"
    return sensor_file


# Function to read temperature from DS18B20 sensor
def read_temp_raw(sensor):
    """
    This function will try to get the entire data from the sensor
    """
    try:
        with open(sensor, "r") as f:
            lines = f.readlines()
        return lines
    except:
        return None


def read_temp():
    """
    This function will initialise the sensor, get the data from the sensor
    and it will split the data searching for the temperature in the received data.
    The temperature will be manipulared and returned directrly in Celsius degree.

    return : temp => float -> temperature in Celsius degree
    """
    sensor_file = init_temp_sensor()
    lines = read_temp_raw(sensor_file)
    if lines is not None:
        while lines[0].strip()[-3:] != "YES":
            time.sleep(0.2)
            lines = read_temp_raw(sensor)
        equals_pos = lines[1].find("t=")
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2 :]
            temp_c = float(temp_string) / 1000.0
            return round(temp_c, 2)
    return None


def main():
    while True:
        temp_c = read_temp()
        if temp_c is not None:
            print("Temperature: {}C".format(temp_c))
        else:
            print("Failed to read temperature.")
        time.sleep(0.2)


if __name__ == "__main__":
    main()
